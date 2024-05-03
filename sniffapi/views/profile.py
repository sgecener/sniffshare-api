
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from sniffapi.models import ScentUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = User
        fields = ('id', 'url', 'user' )



class Profile(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        
        try:
            current_user = ScentUser.objects.get(user=request.auth.user)

            serializer = ProfileSerializer(
                    current_user, many=False, context={"request": request}
                )
            return Response(serializer.data)
         
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def destroy(self, request, pk=None):

        current_user = User.objects.get(pk=pk)
        current_user.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    


