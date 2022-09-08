from rest_framework.routers import DefaultRouter

from .views import HeroViewSet

router = DefaultRouter()

router.register("", HeroViewSet, basename="heros")
