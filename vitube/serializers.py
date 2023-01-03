from rest_framework import serializers
from .models import Video, Like, User
from .permissions import UserPublicSerializer


# class User(serializers.ModelSerializer):
#     class Meta:
#         model : User
#         fields : ['username','password', 'url', 'liked_video']

class VideoSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source = 'user', read_only = True)
    username = serializers.StringRelatedField(source='user', read_only=True)

    #my_user_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Video
        fields = ('pk',
                  'video',
                  'name',
                  'description',
                  'category',
                  'tags',
                  'upload_date',
                  #'my_user_data',
                  'owner',
                  'likes_count',
                  'username',
                  )
        slug_filed = 'username'

    # def get_username(self, obj):
    #     return{
    #         "username" : obj.user.username
    #         }




class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ( 'name',
                  'video',
                  'description',
                  'category',
                  'tags',
                  # 'upload_date',
                  )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'owner', 'video')
