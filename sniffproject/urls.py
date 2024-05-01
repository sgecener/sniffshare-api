from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from sniffapi.models import *
from sniffapi.views import *
from sniffapi.views.register import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"favorites", FavoriteViewSet, "favorite")
router.register(r"tags", TagViewSet, "tag")
router.register(r"scent_posts", ScentPostViewSet, "scent_post")
router.register(r"scent_review", ScentReviewViewSet, "scent_review")
router.register(r"scent_tags", ScentTagViewSet, "scent_tag")
router.register(r"users", Users, "user")



urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
