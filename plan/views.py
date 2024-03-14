from rest_framework import response
from django.http import HttpResponse
import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from .serlializers import PlanSerializer
from .models import  *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework import generics
# Create your views here.


stripe.api_key=settings.STRIPE_SECRET_KEY

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
                success_url=settings.SITE_URL + '?success=true',
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

        print(session)
        customer_email=session['customer_details']['email']
        plan_id=session['metadata']['plan_id']
        plan=Plan.objects.get(id=plan_id)
        #sending confimation mail
        send_mail(
            subject="payment sucessful",
            message=f"thank for your purchase your order is ready.",
            recipient_list=[customer_email],
            from_email="elshriefhanaa@gmail.com"
        )

        #creating payment history
        # user=User.objects.get(email=customer_email) or None

        PaymentHistory.objects.create(plan=plan, payment_status=True)
    # Passed signature verification
    return HttpResponse(status=200)