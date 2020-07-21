from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CommentListView,CommentCreateView,CommentDetailView)







router = DefaultRouter()
router.register('', CommentListView, basename='Comment')
router.register('create', CommentCreateView)
router.register('', CommentDetailView)

urlpatterns = [
   path('', include(router.urls)),
]
