from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from sniffapi.models import *
from sniffapi.views import *
from sniffapi.views import automation_view
from sniffapi.views.register import register_user, login_user

from apscheduler.schedulers.background import BackgroundScheduler

bg_scheduler = BackgroundScheduler()

from django_apscheduler.jobstores import register_events, register_job


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"favorites", FavoriteViewSet, "favorite")
router.register(r"tags", TagViewSet, "tag")
router.register(r"scent_posts", ScentPostViewSet, "scentpost")
router.register(r"scent_reviews", ScentReviewViewSet, "scentreview")
router.register(r"scent_tags", ScentTagViewSet, "scenttag")
router.register(r"users", Users, "user")
router.register(r"profile", Profile, "profile")
router.register(r"scent_users", ScentUserViewSet, "scentuser")



urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("scent_posts", automation_view.automate_new_scent, name="scentpost")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


register_events(bg_scheduler)
register_job(bg_scheduler)