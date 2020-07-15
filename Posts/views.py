from .models import Post
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from rest_framework import permissions
from myBlog.Permisions import IsOwnerOrReadOnly
# from django.utils import timezone
from .pagination import PostPageNumberPagination


from rest_framework.filters import (SearchFilter, OrderingFilter)

# Q lookup import below
from django.db.models import Q








class PostView(ModelViewSet):

    serializer_class=PostSerializer
    lookup_field='slug'
    permission_classes =[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class= PostPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content','author__first_name','author__last_name']
    ordering_fields = ['title', 'content','author__first_name','author__last_name']


    def get_queryset(self):
        queryset=Post.objects.all()
        searchString = self.request.GET.get("q")
        if searchString:
            queryset = Post.objects.filter(
            Q(title__icontains=searchString) |
            Q(content__icontains=searchString) |
            Q(author__first_name__icontains=searchString) |
            Q(author__last_name__icontains=searchString) 
            ).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

