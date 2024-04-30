from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from sniffapi.models import *
from sniffapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"favorites", FavoriteViewSet, "favorite")
router.register(r"tags", TagViewSet, "tag")
router.register(r"scent_posts", ScentPostViewSet, "scent_post")
router.register(r"scent_review", ScentReviewViewSet, "scent_review")
router.register(r"scent_tags", ScentTagViewSet, "scent_tag")
router.register(r"users", UserViewSet, "user")



urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]
