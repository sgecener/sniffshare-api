from rest_framework import serializers, viewsets
from sniffapi.models import ScentTag


class ScentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScentTag
        fields = ['id', 'scent_post', 'tag', 'created_at']


class ScentTagViewSet(viewsets.ModelViewSet):
    queryset = ScentTag.objects.all()
    serializer_class = ScentTagSerializer