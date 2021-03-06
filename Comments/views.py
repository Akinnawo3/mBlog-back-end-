from .models import Comment
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import mixins
from .serializers import (CommentSerializer,comment_serializer_creator)
from rest_framework import permissions
from myBlog.Permisions import IsOwnerOrReadOnly
from rest_framework.filters import (SearchFilter, OrderingFilter)

# Create your views here.






class CommentListView(mixins.ListModelMixin,
                        GenericViewSet):
    # instance = get_object_or_404(Post)
    # queryset = Comment.objects.filter_by_instance()
    # queryset = Comment.objects.filter(id__gte=0)
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [ 'content','author__first_name','author__last_name']
    ordering_fields = ['content','author__first_name','author__last_name']


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class CommentDetailView(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class=CommentSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    




class CommentCreateView(mixins.CreateModelMixin,
                                GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        model_type= self.request.GET.get("type")
        slug= self.request.GET.get("slug")
        parent_id= self.request.GET.get("parent_id", None)

        return comment_serializer_creator(model_type=model_type,
                                            parent_id=parent_id,    
                                            slug=slug,                                
                                            user = self.request.user)
    