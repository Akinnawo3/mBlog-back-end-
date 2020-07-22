from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CommentListView,CommentCreateView,CommentDetailView)







router = DefaultRouter()
router.register('', CommentListView,basename='comment')
router.register('create', CommentCreateView,basename='comment')
router.register('', CommentDetailView, basename='comment')

urlpatterns = [
   path('', include(router.urls)),
]
