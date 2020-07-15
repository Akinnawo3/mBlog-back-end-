from rest_framework import serializers
from .models import Post

from Comments.serializers import CommentSerializer

from Comments.serializers import CommentSerializer
from Comments.models import Comment




class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Post-detail', lookup_field="slug")
    author = serializers.ReadOnlyField(source= 'author.username')
    comments= serializers.SerializerMethodField()
    no_of_comments=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["url","id", "title","content",'publish', 'author','comments', 'no_of_comments' ]
        
    def get_comments(self, obj):
        comment_qs = Comment.objects.filter_by_instance(obj)
        commentz = CommentSerializer(comment_qs, many=True).data
        return commentz

    def get_no_of_comments(self,obj):
        return Comment.objects.filter_by_instance(obj).count()