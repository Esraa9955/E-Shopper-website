

from rest_framework import response
from django.http import HttpResponse
import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from .serlializers import *
from .models import  *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework import generics
# Create your views here.
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status


stripe.api_key=settings.STRIPE_SECRET_KEY
User = get_user_model()
API_URL="http/locahost:8000"

class ListAllPlans(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

class PlanPreview(RetrieveAPIView):
    serializer_class=PlanSerializer
    permission_classes=[permissions.AllowAny]
    queryset=Plan.objects.all()



class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        prod_id=self.kwargs["pk"]
        try:
            plan=Plan.objects.get(id=prod_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'usd',
                             'unit_amount':int(plan.price) * 100,
                             'product_data':{
                                 'name':plan.name,
                                 'description':plan.description,
                                 
                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "plan_id":plan.id
                },
                mode='payment',
                success_url=settings.SITE_URL + 'vendorprofile',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)
        
@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session['customer_details']['email']
        plan_id = session['metadata']['plan_id']
        plan = Plan.objects.get(id=plan_id)

       
        User = get_user_model()
        vendor = User.objects.filter(email=customer_email).first()

        # Check if vendor exists
        if vendor:
            # Create PaymentHistory with vendor ID and current date
            PaymentHistory.objects.create(
                vendor=vendor,
                plan=plan,
                payment_status=True,
                date=timezone.now()
            )
        

            # Sending confirmation mail
            send_mail(
                subject="Payment successful",
                message=f"Thank you for subscribtion",
                recipient_list=[customer_email],
                from_email="elshriefhanaa@gmail.com"
            )

    return HttpResponse(status=200)



class PaymentHistoryListAPIView(generics.ListAPIView):
    queryset = PaymentHistory.objects.all()
    serializer_class = PaymentHistorySerializer


class LastVendorAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentHistorySerializer
    queryset = PaymentHistory.objects.all()

    def get_object(self):
        vendor_id = self.request.query_params.get('vendor')
        last_payment = PaymentHistory.objects.filter(vendor=vendor_id).order_by('-id').first()
        return last_payment
        

class UpdateStockAPIView(APIView):

    def post(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor')
        new_stock = request.data.get('stock')

        if vendor_id is None or new_stock is None:
            return Response({"error": "Vendor ID and new stock are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_history = PaymentHistory.objects.filter(vendor=vendor_id).latest('date')
            payment_history.stock = new_stock
            payment_history.save()
            return Response({"success": "Stock updated successfully"}, status=status.HTTP_200_OK)
        except PaymentHistory.DoesNotExist:
            return Response({"error": "No payment history found for this vendor"}, status=status.HTTP_404_NOT_FOUND)
