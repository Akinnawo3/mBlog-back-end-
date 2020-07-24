# from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from .serializers import AccountCreateSerializer, AccountLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions



# Create your views here.



from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView







User= get_user_model()




class AccountCreateView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class=AccountCreateSerializer
    queryset= User.objects.all()

class AccountLoginView(APIView):
    permission_classes=[permissions.AllowAny]
    serializer_class=AccountLoginSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer= AccountLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data= serializer.data
            return Response(new_data, status = HTTP_200_OK)
        return Response(serializer.error, status = HTTP_404_BAD_REQUEST)