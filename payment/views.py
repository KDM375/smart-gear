from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
import requests, json, uuid
from django.http import HttpResponse

class Checkout(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        email = request.data.get('email')
        amount = request.data.get('amount') 

        #if not email or not amount:
        #    return Response(
        #        {"error": "Email and amount are required."},
        #        status=status.HTTP_400_BAD_REQUEST
        #    )

        # Paystack headers
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        # Paystack payload
        payload = {
            'email': 'mensahkelvin526@gmail.com',
            'amount': 200,
            'currency': 'GHS',
            'channels': ('card', 'mobile_money', 'bank_transfer'),
            'reference': str(uuid.uuid4()),
            'callback_url': f'http://127.0.0.1:8000/payment/success/',#make sure to come change this later Kelvin
        }

        # Send request to Paystack
        try:
            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                data=json.dumps(payload)
            )
            response_data = response.json()

            if response_data.get('status') is True: 
                return Response(
                    {
                        "message": "Payment initialization successful",
                        "authorization_url": response_data['data']['authorization_url']
                    },
                    status=status.HTTP_200_OK # Or HTTP_201_CREATED if you prefer
                )
            else:
                return False, "Payment Initialization Failed"

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "An error occurred while connecting to Paystack."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
def payment_success(request):
    return HttpResponse('Payment Successful')


def payment_failed(request):
    return HttpResponse('Payment Failed')

