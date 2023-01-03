from rest_framework import permissions, serializers
#
# class IsOwnerPermission(permissions.DjangoModelPermissions):
#     def has_permission(self, request, view):
#         return  True
#
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)