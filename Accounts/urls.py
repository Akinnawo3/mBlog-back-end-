from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountCreateView





router = DefaultRouter()


router.register('register', AccountCreateView)



urlpatterns = [
   path('', include(router.urls)),
]






