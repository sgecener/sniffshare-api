from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.http import HttpResponseServerError
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class Users(viewsets.ViewSet):


    def retrieve(self, request, pk=None):
        
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(request, user)
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class UserViewSet(viewsets.ViewSet):
#     queryset = User.objects.all()
#     permission_classes = [permissions.AllowAny]

#     @action(detail=False, methods=['post'], url_path='register')
#     def register_account(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = User.objects.create_user(
#                 username=serializer.validated_data['username'],
#                 first_name=serializer.validated_data['first_name'],
#                 last_name=serializer.validated_data['last_name'],
#                 password=serializer.validated_data['password']
#             )
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=False, methods=['post'], url_path='login')
#     def user_login(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             token = Token.objects.get(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)