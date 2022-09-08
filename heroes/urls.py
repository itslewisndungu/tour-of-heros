from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_or_create_hero),
    path("<int:id>/", views.get_update_delete_hero_by_id),
]
