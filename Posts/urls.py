from django.urls import path, include
from .views import PostView
from rest_framework.routers import DefaultRouter





router = DefaultRouter()

router.register(r'post', PostView, basename='Post')


urlpatterns = [
    path('', include(router.urls)),
]
