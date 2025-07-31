from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import uuid
from .models import Payment
import hashlib
import hmac
import logging
from django.views.decorators.http import require_POST

def initiate_payment(request):
    if request.method == 'POST':
        # Get amount and email from your form (e.g., product details)
        amount = 1000 # Example amount in pesewas (10 GHS). Paystack expects amount in Kobo/Pesewas
        email = request.user.email if request.user.is_authenticated else "guest@example.com"
        
        # Create a new Payment object in your database
        payment = Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            amount=amount / 100, # Store actual GHS amount
            currency='GHS',
        )

        # Prepare data for Paystack API
        paystack_data = {
            'email': email,
            'amount': amount, # in pesewas
            'reference': str(uuid.uuid4()), # Unique reference for this transaction
            'callback_url': request.build_absolute_uri('/payments/verify/'), # URL for verification
        }

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                data=json.dumps(paystack_data)
            )
            response.raise_for_status() # Raise an exception for HTTP errors
            
            response_data = response.json()
            if response_data['status']:
                # Redirect user to Paystack's authorization URL
                return redirect(response_data['data']['authorization_url'])
            else:
                return HttpResponseBadRequest(f"Paystack Error: {response_data['message']}")
        except requests.exceptions.RequestException as e:
            return HttpResponseBadRequest(f"Payment initiation failed: {e}")

    return render(request, 'main.html', {'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})


@csrf_exempt # Use this carefully, better to verify signature for webhooks
def verify_payment(request):
    if request.method == 'GET':
        # This is where Paystack redirects the user after payment.
        # It sends 'reference' as a query parameter.
        reference = request.GET.get('reference')
        
        if not reference:
            return HttpResponseBadRequest("Payment reference missing.")

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return HttpResponseBadRequest("Invalid payment reference.")

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(
                f'https://api.paystack.co/transaction/verify/{reference}',
                headers=headers
            )
            response.raise_for_status()
            
            response_data = response.json()
            if response_data['status'] and response_data['data']['status'] == 'success':
                payment.status = 'success'
                payment.paystack_payment_id = response_data['data']['id']
                payment.save()
                # Process your order, update user's account, etc.
                return render(request, 'success.html', {'payment': payment})
            else:
                payment.status = 'failed'
                payment.save()
                return render(request, 'fail.html', {'payment': payment, 'message': response_data['data']['gateway_response']})
        except requests.exceptions.RequestException as e:
            return HttpResponseBadRequest(f"Payment verification failed: {e}")

    return HttpResponseBadRequest("Invalid request method.")

# For webhook (more robust for production)
@csrf_exempt # You MUST implement signature verification for webhooks!
@require_POST
def paystack_webhook(request):
    logger = logging.getLogger(__name__)
    # Get signature from header
    paystack_signature = request.headers.get('x-paystack-signature')
    if not paystack_signature:
        logger.warning("Missing Paystack signature header.")
        return HttpResponseBadRequest("Missing signature.")

    # Compute expected signature
    secret = settings.PAYSTACK_SECRET_KEY.encode()
    computed_signature = hmac.new(secret, request.body, hashlib.sha512).hexdigest()

    if not hmac.compare_digest(computed_signature, paystack_signature):
        logger.warning("Invalid Paystack signature.")
        return HttpResponseBadRequest("Invalid signature.")

    payload = json.loads(request.body)
    event = payload.get('event')
    data = payload.get('data', {})

    if event == 'charge.success':
        reference = data.get('reference')
        try:
            payment = Payment.objects.get(reference=reference)
            if payment.status != 'success':
                payment.status = 'success'
                payment.paystack_payment_id = data.get('id')
                payment.save()
                # Further processing: fulfill order, send email etc.
                logger.info(f"Payment {reference} successfully processed via webhook.")
        except Payment.DoesNotExist:
            logger.error(f"Payment {reference} not found for webhook.")
        return JsonResponse({'status': 'success'})
    elif event == 'charge.failed':
        reference = data.get('reference')
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = 'failed'
            payment.save()
            logger.info(f"Payment {reference} failed via webhook.")
        except Payment.DoesNotExist:
            logger.error(f"Payment {reference} not found for webhook.")
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'ignored'}, status=200)

def mupage(request):
    return render(request, 'home.html')