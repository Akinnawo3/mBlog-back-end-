from rest_framework import serializers
from .models import Post

from Comments.serializers import CommentSerializer

from Comments.serializers import CommentSerializer
from Comments.models import Comment




class PostSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='Post-detail', lookup_field="slug")
    # author = serializers.ReadOnlyField(source= 'author.username')
    author =serializers.SerializerMethodField()
    comments= serializers.SerializerMethodField()
    no_of_comments=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id", 'slug',"title","content",'publish', 'author','comments', 'no_of_comments', 'draft' ]
        read_only_fields=['slug']
    def get_comments(self, obj):
        comment_qs = Comment.objects.filter_by_instance(obj).filter(parent=None)
        # comment_qs = Comment.objects.all()
        commentz = CommentSerializer(comment_qs, many=True).data
        return commentz

    def get_no_of_comments(self,obj):
        return Comment.objects.filter_by_instance(obj).filter(parent=None).count()

    def get_author(self,obj):
        return obj.author.first_name +" "+ obj.author.last_name