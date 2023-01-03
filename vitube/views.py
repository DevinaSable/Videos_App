from .models import Video, Like
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from .serializers import VideoSerializer, LikeSerializer, VideoListSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q



class VideoList(ListAPIView):
    lookup_field = 'pk'
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    permission_classes = [permissions.AllowAny]


class VideoListCreate(ListCreateAPIView):
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] #IsOwnerOrReadOnly
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    slug_field = 'username'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        request=self.request
        user = request.user

        if user.is_authenticated:
            return qs.filter(user=request.user)
        if user.is_superuser:
            return qs
        return Video.objects.none()

    def perform_create(self, serializer):
        #video = serializer.validated_file()
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description')
        if description is None:
            description = name
        serializer.save(user=self.request.user, description= description)



class VideoDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # def get_queryset(self, *args, **kwargs):
    #     qs =super.


class LikeView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class SearchVideoList(ListAPIView):
    model = Video
    context_object_name = "Videos"
    queryset = Video.objects.all()
    serializer_class = VideoSerializer, VideoListSerializer


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Video.obects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                 user = self.request.user
        results = qs.search(q, user=user)
        return results