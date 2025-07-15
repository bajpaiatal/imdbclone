from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from moviesinfo.api.views import movie_list, movie_details
from moviesinfo.api.views import ReviewList, ReviewDetail, \
            ReviewCreate, MoviesAV, MoviesDetailAV, PlatformAV, \
            PlatformDetailAV, PlatformVS, UserReview, MoviesGV

router = DefaultRouter()
router.register('stream', PlatformVS, basename='platform')


urlpatterns = [
    path('list/', MoviesAV.as_view(), name='movie-list'),
    path('<int:pk>/', MoviesDetailAV.as_view(), name='movie-detail'),
    path('list2/', MoviesGV.as_view(), name='watch-list'),

    path('', include(router.urls)),

    # path('stream/', PlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', PlatformDetailAV.as_view(), name='stream-detail'),
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReview.as_view(), name='user-review-detail'),

]