from django.urls import path
from .views import PlanPreview, CreateCheckOutSession ,ListAllPlans,stripe_webhook_view
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('plans/', ListAllPlans.as_view(), name='list-all-plans'),
    path('PlanPreview/<pk>/', PlanPreview.as_view(), name="product"),
    path('create-checkout-session/<pk>/',CreateCheckOutSession.as_view(), name='checkout_session'),
    path('webhook/', stripe_webhook_view, name='stripe-webhook'),


    ]