from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CommentView,CommentCreateView)







router = DefaultRouter()
router.register('/commentlist', CommentView)
router.register('/create', CommentCreateView)

urlpatterns = [
   path('', include(router.urls))
]
