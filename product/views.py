

from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from product.models import *
from .serlizer import ProductsSerlizer
from django.shortcuts import get_object_or_404
from .filiters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated 

parser_classes = (MultiPartParser, FormParser)


@api_view(['GET'])
def allProducts(request):
    filterproducts=ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 12
    queryset =  paginator.paginate_queryset(filterproducts.qs, request)
    productsjson=ProductsSerlizer(queryset,many=True).data
    return paginator.get_paginated_response({'products': productsjson})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getproductbyid(request, id):
    product=get_object_or_404(Product,id=id)
    productjson = ProductsSerlizer(product,many=False).data
    return Response({'product': productjson})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addProduct(request):
    serializer = ProductsSerlizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'added'})
    else:
        print(serializer.errors)
        return Response({'msg': 'wrong data', 'error': serializer.errors})






@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
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
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteProduct(request, id):
    pro = Product.objects.filter(id=id).first()
    if pro is not None:  # Check if pro exists
        pro.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'product not found'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def addRate(request, pk):
    product = get_object_or_404(Product, id=pk)
    data = request.data

    if 'rating' not in data:
        return Response({"error": "Rating data is missing"}, status=status.HTTP_400_BAD_REQUEST)

    new_rating = data['rating']
    
    if new_rating <= 0 or new_rating > 5:
        return Response({"error": 'Please select between 1 to 5 only'}, status=status.HTTP_400_BAD_REQUEST) 

    # Check if the user has already rated this product
    existing_rating = product.rates.filter(user=request.user).first()

    if existing_rating:
        # Update the existing rating
        existing_rating.rating = new_rating
        existing_rating.save()
    else:
        # Create a new rating
        Rates.objects.create(
            product=product,
            user=request.user,
            rating=new_rating,
        )

    # Recalculate the average rating for the product
    avg_rating = product.rates.aggregate(avg_rating=Avg('rating'))['avg_rating']
    product.ratings = avg_rating
    product.save()

    return Response({'details': 'Product rate updated'})
