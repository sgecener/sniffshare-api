from rest_framework import serializers, viewsets
from sniffapi.models import Category
from rest_framework.response import Response


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, pk=None):
        try:
            scent = Category.objects.get(pk=pk)
            serializer = CategorySerializer(scent, context={'request': request})
            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)