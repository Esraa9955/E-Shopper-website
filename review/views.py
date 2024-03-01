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

