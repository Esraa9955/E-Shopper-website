

from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import *
from .serlizer import ProductsSerlizer
from django.shortcuts import get_object_or_404
from .filiters import ProductFilter
from rest_framework.pagination import PageNumberPagination

@api_view(['GET'])
def allProducts(request):
    filterproducts=ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 2
    queryset =  paginator.paginate_queryset(filterproducts.qs, request)
    productsjson=ProductsSerlizer(queryset,many=True).data
    return Response({'products':productsjson})

@api_view(['GET'])
def getproductbyid(request, id):
    product=get_object_or_404(Product,id=id)
    productjson = ProductsSerlizer(product,many=False).data
    return Response({'product': productjson})


