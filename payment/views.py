import json
import hmac
import hashlib
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import requests, json, uuid
from .models import Transaction
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from products.serializers import CartSerializer 

class Checkout(APIView):
    serializer_class = CartSerializer
    def post(self, request, *args, **kwargs):
        #get the amount from the request data
        serializer = CartSerializer(data=request.data)

        # 2. Validate the data. This is the key step.
        if serializer.is_valid():
            # Get the validated data. 
            validated_data = serializer.validated_data
            amount = validated_data.get('total_price')

        try:
            amount_in_pesewas = int(amount * 100)
        except (ValueError, TypeError) as e:
            return Response(
                {"error": f"Invalid amount format: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paystack headers
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        # Paystack payload
        payload = {
            'email': 'example@gma.com',  # Assuming the user is authenticated and has an email
            'amount': amount_in_pesewas,  # it is multipled by hundred cause it is in peswas
            'currency': 'GHS',
            'channels': ('card', 'mobile_money', 'bank_transfer'),
            'reference': str(uuid.uuid4()), # Generate a unique reference for the transaction
            'callback_url': f'{request.scheme}://{request.get_host()}/payment/success/', # callback to this url after paystack completes the transaction
        }

        # Send request to Paystack
        try:
            response = requests.post(
                'https://api.paystack.co/transaction/initialize', # the site where the request is verified
                headers=headers,
                data=json.dumps(payload)
            )
            response_data = response.json()

            if response_data.get('status') is True: 
                return Response(
                    {
                        "message": "Payment initialization successful",
                        "authorization_url": response_data['data']['authorization_url'] # this is the main url to the payment page
                    },
                    status=status.HTTP_200_OK 
                )
            else:
                return Response(
                    {"error": "Payment Initialization Failed"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "An error occurred while connecting to Paystack."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Payment success and failure views
def payment_success(request):
    return HttpResponse('Payment Successful')


def payment_failed(request):
    return HttpResponse('Payment Failed')


#this is the webhook handler that will handle the webhooks from paystack
@method_decorator(csrf_exempt, name='dispatch') # we make sure the csrf is exempted for this view for security reasons
class Webhook_handler(APIView):

    def post(self, request, *args, **kwargs):
        # 1. Retrieve the raw request body
        payload = request.body

        # 2. Retrieve the signature from the header
        paystack_signature = request.headers.get('x-paystack-signature')# we also get the signature from the header to ensure the request is from paystack

        # 3. we verify the signature , if theres no signature,then it probably not from paystack we return an error
        if not paystack_signature:
            return JsonResponse({'error': 'No signature header'}, status=400)

        # Ensure the secret key is configured
        secret_key = settings.PAYSTACK_SECRET_KEY
        if not secret_key:
            # Handle the case where the secret key is not set
            print("PAYSTACK_SECRET_KEY is not configured in settings.py")
            return JsonResponse({'error': 'Internal server error'}, status=500)

        # Hash the payload with your secret key
        secret = secret_key.encode('utf-8')
        hash_object = hmac.new(secret, payload, digestmod=hashlib.sha512)
        expected_signature = hash_object.hexdigest()

        # Use hmac.compare_digest for a constant-time comparison to
        # prevent timing attacks.
        if not hmac.compare_digest(expected_signature, paystack_signature):
            print("Signature verification failed.")
            return JsonResponse({'error': 'Signature verification failed'}, status=400)

        # If the signature is valid,then we can parse the JSON payload, else we do not parse it
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            print("Invalid JSON payload.")
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

        # 5. Handle the event based on its type
        event_type = event.get('event')
        data = event.get('data')
        try:
            if event_type == 'charge.success':
                reference = data.get('reference')
                print(f"Successfully received 'charge.success' for transaction reference: {reference}")
                # Here we will use these to update our transaction history
                amount_in_currency = data.get('amount', 0) / 100
                transaction_status = data.get('status')
                transaction_channel = data.get('channel')

                # wec heck if the transaction already exists, if not it is created 
                if not Transaction.objects.filter(reference=reference):
                    Transaction.objects.create(
                        reference=reference,
                        amount=amount_in_currency,  
                        status=transaction_status,
                        channel=transaction_channel,
                    )
        except Exception as e:
            print(f"Error processing event: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
        
        # We always make sure to return a 200 OK response to acknowledge receipt else more webhooks will be sent
        return HttpResponse(status=200)

