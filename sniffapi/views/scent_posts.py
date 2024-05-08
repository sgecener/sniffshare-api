from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sniffapi.models import ScentPost, Category, ScentUser, Favorite, Tag, ScentTag
from .tags import TagSerializer
from rest_framework.decorators import action

class ScentPostSerializer(serializers.ModelSerializer):

    is_owner = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user == obj.user
    
    class Meta:
        model = ScentPost
        fields = ['id', 'user_id', 'is_owner', 'title', 'description', 'category_id', 'tags', 'created_at', 'updated_at']

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
        category_id = request.data.get('category')
    
        # Retrieve or create the Category instance
        category = Category.objects.get(id=category_id)
        # Create a scent database row first, so you have a
        # primary key to work with
        scent = ScentPost.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category
            )

        # Establish the many-to-many relationships
        

        # tag_ids = request.data.get('tags', [])
        # scent.tags.set(tag_ids)

        tags_data = request.data.get('tags', [])
        tag_names = [tag_data['name'] for tag_data in tags_data if 'name' in tag_data]


        for tag_name in tag_names:
        # Check if the tag already exists
            tag, created = Tag.objects.get_or_create(name=tag_name)
            # If it's a new tag, add it to the scent's tags
            if tag or created:
                scent.tags.add(tag)
        

        serializer = ScentPostSerializer(scent, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:

            scent = ScentPost.objects.get(pk=pk)
            
            # Is the authenticated user allowed to edit this book?
            if scent.user != request.user:
                return Response({"detail": "You do not have permission to update this scent post."}, status=status.HTTP_403_FORBIDDEN)


            serializer = ScentPostSerializer(scent, data=request.data, context={'request': request})
            if serializer.is_valid():
                scent.title = serializer.validated_data['title']
                scent.description = serializer.validated_data['description']

                category_id = request.data.get('category')
                category = Category.objects.get(id=category_id)
                scent.category = category
                

                tags_data = request.data.get('tags', [])
                tag_names = [tag_data['name'] for tag_data in tags_data if 'name' in tag_data]


                 # Retrieve the existing tag instances associated with the scent post
                existing_tags = scent.tags.all()

            # Remove tag instances that are not present in the new tag names
                tags_to_remove = existing_tags.exclude(name__in=tag_names)
                scent.tags.remove(*tags_to_remove)

            # Add any new tag instances that are not already associated with the scent post
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    if tag not in existing_tags:
                        scent.tags.add(tag)

                scent.save()

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
        
    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        """Like Products"""

        if request.method == "POST":
            try:
                scent_post = ScentPost.objects.get(pk=pk)
                scent_user = ScentUser.objects.get(user=request.auth.user)
                if not Favorite.objects.filter(scent_user=scent_user, scent_post=scent_post).exists():
                    favorite = Favorite(scent_user=scent_user, scent_post=scent_post)
                    favorite.save()

                    return Response({"message": "Scent liked successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Scent already liked"}, status=status.HTTP_400_BAD_REQUEST)
            except ScentPost.DoesNotExist:
                return Response({"error": "Scent not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["delete"], detail=True)
    def unlike(self, request, pk=None):
        """Unlike Products"""

        if request.method == "DELETE":
            try:
                scent_post = ScentPost.objects.get(pk=pk)
                scent_user = ScentUser.objects.get(user=request.auth.user)
                favorite = Favorite.objects.filter(scent_user=scent_user, scent_post=scent_post)
                if favorite.exists():
                    favorite.delete()
                    return Response({"message": "Scent unliked successfully"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"message": "Scent not liked by the user"}, status=status.HTTP_400_BAD_REQUEST)
            except ScentPost.DoesNotExist:
                return Response({"error": "Scent not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)