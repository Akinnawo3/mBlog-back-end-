# from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from .serializers import AccountCreateSerializer
from django.contrib.auth import get_user_model
# Create your views here.



User= get_user_model()




class AccountCreateView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class=AccountCreateSerializer
    queryset= User.objects.all()