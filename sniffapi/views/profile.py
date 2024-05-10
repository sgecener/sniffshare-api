
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from sniffapi.models import ScentUser, Favorite
from sniffapi.views import ScentPostSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        depth = 1

class ScentUserSerializer(serializers.ModelSerializer):
    """JSON serializer for recommendation customers"""

    user = UserSerializer()

    class Meta:
        model = ScentUser
        fields = (
            "id",
            "user",
        )


class FavoriteSerializer(serializers.ModelSerializer):

    scent_post = ScentPostSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'scent_user', 'scent_post']


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    favorite_posts = FavoriteSerializer(many= True)

    class Meta:
        model = ScentUser
        fields = ('id', 'url', 'user', 'favorite_posts')
        depth = 1



class Profile(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        
        try:
            current_user = ScentUser.objects.get(user=request.auth.user)
            current_user.favorite_posts = Favorite.objects.filter(scent_user=current_user)

            serializer = ProfileSerializer(
                    current_user, many=False, context={"request": request}
                )
            return Response(serializer.data)
         
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):

        current_user = ScentUser.objects.get(pk=pk)
        self.check_object_permissions(request, current_user)
        current_user.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    


