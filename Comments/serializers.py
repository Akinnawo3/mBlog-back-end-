from django.contrib.auth import get_user_model
User = get_user_model()
from Posts.models import Post


from django.contrib.contenttypes.models import ContentType
from .models import Comment
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer,
                                        ValidationError)



def comment_serializer_creator(model_type, parent_id,slug=None , user = None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model=Comment
            fields=['id','content','added']

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug= slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                    self.parent_obj=parent_qs.first()
            return super(CommentCreateSerializer,self).__init__( *args, **kwargs)
                
        def validate(self,data):
            model_type=self.model_type
            model_qs =ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() !=1:
                raise ValidationError("invalid content type " )
            my_model = model_qs.first().model_class()
            obj_qs = my_model.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count()!=1:
                # '''or obj_qs.count !=1
                raise ValidationError("this is not a slug for this content type")
            return data
        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user=user
            else:
                main_user = User.objects.all().first()
            model_type= self.model_type
            slug = self.slug 
            parent_obj = self.parent_obj 
            comment = Comment.objects.create_by_model_type(
                        model_type= model_type,
                        slug = slug,
                        content=content,
                        user= main_user,
                        parent_obj= parent_obj
                    )
            return comment 
    return CommentCreateSerializer








# class CommentChildserializer(ModelSerializer):
#     class Meta:
#         model = Comment
#         fields=['id', 'content', 'added']



class CommentSerializer(ModelSerializer): 
    # url = HyperlinkedIdentityField(view_name='comment-detail') 
    replies = SerializerMethodField()
    author  = SerializerMethodField()
    no_of_replies= SerializerMethodField()
    class Meta: 
        model = Comment
        fields=['content', 'added','author','no_of_replies','replies']
        read_only_fields=['object_id','content_type', 'parent',]

    def get_replies(self,obj):
        # if obj.is_parent:
        #     return CommentChildserializer(obj.children(),  many=True).data
        # return None
        return CommentSerializer(obj.children(),  many=True).data
      
        '''
 i had to comment out the 'if condition' because all the objects comming from the comment class are all parents
 due to the fact that the 'all' method has been overwritten in the comment manager inside the model to only give
  a filtered result of parent items only
'''
    
    def get_no_of_replies(self,obj):
        return obj.children().count()


    
    def get_author(self,obj):
        return obj.author.first_name +" "+ obj.author.last_name