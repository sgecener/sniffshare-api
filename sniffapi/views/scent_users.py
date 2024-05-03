
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sniffapi.models import ScentUser


class ScentUserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ScentUsers"""
    class Meta:
        model = ScentUser
        url = serializers.HyperlinkedIdentityField(
            view_name='scentuser-detail', lookup_field='id'
        )
        fields = ('id', 'url', 'user')
        depth = 1


class ScentUserViewSet(viewsets.ModelViewSet) :

    queryset = ScentUser.objects.all()
    serializer_class = ScentUserSerializer

    def update(self, request, pk=None):
        
        scent_user = ScentUser.objects.get(user=request.auth.user)
        scent_user.user.first_name = request.data["first_name"]
        scent_user.user.last_name = request.data["last_name"]
        scent_user.user.email = request.data["email"]
        scent_user.user.save()
        scent_user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
