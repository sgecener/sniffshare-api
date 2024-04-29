from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sniffapi.models import ScentPost
from .categories import CategorySerializer
from .tags import TagSerializer

class ScentPostSerializer(serializers.ModelSerializer):

    # is_owner = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user
    
    class Meta:
        model = ScentPost
        fields = ['id', 'user', 'title', 'description', 'category', 'tags', 'created_at', 'updated_at', 'category']

class ScentPostViewSet(viewsets.ModelViewSet):
    queryset = ScentPost.objects.all()
    serializer_class = ScentPostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        scents = ScentPost.objects.all()
        serializer = ScentPostSerializer(scents, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            scent = ScentPost.objects.get(pk=pk)
            serializer = ScentPostSerializer(scent, context={'request': request})
            return Response(serializer.data)

        except ScentPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get('title')
        description = request.data.get('description')
        category = request.data.get('category')
        # Create a scent database row first, so you have a
        # primary key to work with
        scent = ScentPost.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category
            )

        # Establish the many-to-many relationships
        

        tag_ids = request.data.get('tags', [])
        scent.tags.set(tag_ids)
        

        serializer = ScentPostSerializer(scent, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            scent = ScentPost.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this book?
            self.check_object_permissions(request, scent)

            serializer = ScentPostSerializer(data=request.data)
            if serializer.is_valid():
                scent.title = serializer.validated_data['title']
                scent.author = serializer.validated_data['description']
                scent.save()

                category_ids = request.data.get('categories', [])
                scent.categories.set(category_ids)

                serializer = ScentPostSerializer(scent, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except ScentPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            scent = ScentPost.objects.get(pk=pk)
            self.check_object_permissions(request, scent)
            scent.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ScentPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
