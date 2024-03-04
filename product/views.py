

from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import *
from .serlizer import ProductsSerlizer
from django.shortcuts import get_object_or_404
from .filiters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from rest_framework import status

parser_classes = (MultiPartParser, FormParser)


@api_view(['GET'])
def allProducts(request):
    filterproducts=ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 12
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


@api_view(['POST'])
def addRate(request, pk):
    product = get_object_or_404(Product, id=pk)
    data = request.data
 
    if 'rating' not in data:
        return Response({"error": "Rating data is missing"}, status=status.HTTP_400_BAD_REQUEST)

    rate = product.rates
    
    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({"error": 'Please select between 1 to 5 only'}, status=status.HTTP_400_BAD_REQUEST) 
    elif rate.exists():
        new_rate = {'rating': data['rating']}
        rate.update(**new_rate)

        rating = product.rates.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()

        return Response({'details': 'Product rate updated'})
    else:
        Rates.objects.create(
            product=product,
            rating=data['rating'],
        )
        rating = product.rates.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details': 'Product rate created'})
