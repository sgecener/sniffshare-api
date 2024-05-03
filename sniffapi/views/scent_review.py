from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from sniffapi.models import ScentReview

class ScentReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScentReview
        fields = ['id', 'user_id', 'scent_post_id', 'rating', 'comment']

class ScentReviewViewSet(viewsets.ModelViewSet):
    queryset = ScentReview.objects.all()
    serializer_class = ScentReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

