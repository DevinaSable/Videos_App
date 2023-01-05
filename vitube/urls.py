from django.urls import path
from django.views.decorators.cache import cache_page
from .views import VideoListCreate, VideoDetail, VideoList, SearchVideoList, LikeView


urlpatterns = [
    # path('', cache_page(60*60)(VideoList.as_view())),
    path('<int:pk>/', VideoDetail.as_view(), name='video-detail'),
    path('', VideoListCreate.as_view(), name='home'),
    path('search/', SearchVideoList.as_view(), name='search'),
    path('like/', LikeView.as_view(), name='like'),
]