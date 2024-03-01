from rest_framework.response import Response
from rest_framework.decorators import api_view
from review.models import *
from .serializer import ReviewSerializer


@api_view(['GET'])
def listReviews(request):
    reviews = Review.review_list()
    serializer = ReviewSerializer(reviews, many=True)
    return Response({'msg': 'accept', 'data': serializer.data})


@api_view(['GET'])
def getReview(request, id):
    review = Review.getReviewById(id)
    serializer = ReviewSerializer(review).data
    return Response({'msg': 'accept', 'data':  serializer})

@api_view(['POST'])
def addReview(request):
    obj = Review()
    obj = ReviewSerializer(data=request.data)
    if (obj.is_valid()):
        obj.save()
        return Response({'msg': 'added'})
    return Response({'msg': 'wrong data', 'error': obj.errors})

