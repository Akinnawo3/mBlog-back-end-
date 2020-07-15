from .models import Comment
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        HyperlinkedIdentityField)





class CommentChildserializer(ModelSerializer):
    class Meta:
        model = Comment
        fields=['id', 'content', 'added']



class CommentSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(view_name='comment-detail', )
    replies = SerializerMethodField()
    no_of_replies= SerializerMethodField()
    class Meta:
        model = Comment
        fields ='__all__'
       

    def get_replies(self,obj):
        # if obj.is_parent:
        #     return CommentChildserializer(obj.children(),  many=True).data
        # return None
        return CommentChildserializer(obj.children(),  many=True).data
      
        '''
 i had to comment out the 'if condition' because all the objects comming from the comment class are all parents
 due to the fact that the 'all' method has been overwritten in the comment manager inside the model to only give
  a filtered result of parent items only
'''
    
    def get_no_of_replies(self,obj):
        return obj.children().count() 


