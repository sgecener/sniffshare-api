from rest_framework import serializers, viewsets
from rest_framework.response import Response
from sniffapi.models import ScentTag


class ScentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScentTag
        fields = ['id', 'scent_post', 'tag']


class ScentTagViewSet(viewsets.ModelViewSet):
    queryset = ScentTag.objects.all()
    serializer_class = ScentTagSerializer

    def destroy(self, request, pk=None):
        try:
            scent = ScentTag.objects.get(pk=pk)
            self.check_object_permissions(request, scent)
            scent.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ScentTag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)