from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, \
                    IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, \
                    AnonRateThrottle, ScopedRateThrottle
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from moviesinfo.api.permissions import IsAdminOrReadOnly, \
                        IsReviewUserOrReadOnly
from moviesinfo.models import Movies, Platform, Review
from moviesinfo.api.serializers import MovieSerializer, \
                        PlatformSerializer,ReviewSerializer
from moviesinfo.api.throttling import ReviewCreateThrottle, \
                        ReviewListThrottle
from moviesinfo.api.pagination import MoviePagination, \
                        MovieLOPagination, MovieCPagination


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username = username)
    

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movies = Movies.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            movies=movies, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if movies.number_rating == 0:
            movies.avg_rating = serializer.validated_data['rating']
        else:
            movies.avg_rating = (
                movies.avg_rating + serializer.validated_data['rating'])/2

        movies.number_rating = movies.number_rating + 1
        movies.save()

        serializer.save(movies=movies, review_user=review_user)
        
        
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movies=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'
    
    
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class PlatformVS(viewsets.ViewSet):

    def list(self, request):
        queryset = Platform.objects.all()
        serializer = PlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Platform.objects.all()
        movies = get_object_or_404(queryset, pk=pk)
        serializer = PlatformSerializer(movies)
        return Response(serializer.data)

    def create(self, request):
        serializer = PlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        platform = Platform.objects.all()
        serializer = PlatformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class PlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            platform = Platform.objects.get(pk=pk)
        except Platform.DoesNotExist:
            return Response({'error': 'Not found'}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = Platform.objects.get(pk=pk)
        serializer = PlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = Platform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class MoviesGV(generics.ListAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MovieCPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']
    
    
class MoviesAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class MoviesDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'error': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = Movies.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Movies.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movies.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':

#         try:
#             movie = Movies.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, 
#                       status=status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movies.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, 
#                       status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movies.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)