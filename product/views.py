

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




@api_view(['POST'])
def addProduct(request):
    serializer = ProductsSerlizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'added'})
    else:
        print(serializer.errors)
        return Response({'msg': 'wrong data', 'error': serializer.errors})



@api_view(['PUT'])
def updateProduct(request, id):
    updateobj = Product.objects.filter(id=id).first()
    if updateobj:
        serializedProduct = ProductsSerlizer(
            instance=updateobj, data=request.data)
        if serializedProduct.is_valid():
            print(serializedProduct.validated_data)  
            serializedProduct.save()  
            return Response(data=serializedProduct.data)



@api_view(['DELETE'])
def deleteProduct(request, id):
    pro = Product.objects.filter(id=id).first()
    if pro is not None:  # Check if pro exists
        pro.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'product not found'})

