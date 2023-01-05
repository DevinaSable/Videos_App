from .models import Video, Like
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from .serializers import VideoSerializer, LikeSerializer, VideoListSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank



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


class LikeView(APIView):
    # serializer_class = LikeSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return None

    def post(self, pk, request, *args, **kwargs):
        video = self.get_object(pk)
        if video is None:
            return Response({"error : Video not found"}, status = status.HTTP_404_NOT_FOUND)

        like_user = video.likes.all().values_list('user', flat=True)
        if request.user.id in like_user:
            video.likes_count -= 1
            video.likes.filter(user=request.user).delete()
        else:
            video.likes_count +=1
            like = Like(user=request.user, video=video)
            like.save()
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SearchVideoList(ListAPIView):
    model = Video
    context_object_name = "Videos"
    serializer_class = VideoSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_vector = SearchVector("name", "description", "category", "tags", "video")
        search_query = SearchQuery(query)
        return(
            Video.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )

    # queryset = Video.objects.all()
    #
    #
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset()
    #     q = self.request.GET.get('q')
    #     results = Video.objects.none()
    #     if q is not None:
    #         user = None
    #         if self.request.user.is_authenticated:
    #             user = self.request.user
    #         results = qs.search(q, user=user)
    #     return results