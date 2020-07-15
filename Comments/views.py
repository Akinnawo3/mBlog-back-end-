from .models import Comment
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentSerializer
from rest_framework import permissions
from myBlog.Permisions import IsOwnerOrReadOnly
from rest_framework.filters import (SearchFilter, OrderingFilter)

# Create your views here.




class CommentView(ModelViewSet):
    # instance = get_object_or_404(Post)
    # queryset = Comment.objects.filter_by_instance()
    queryset = Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [ 'content','author__first_name','author__last_name']
    ordering_fields = ['content','author__first_name','author__last_name']
