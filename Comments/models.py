from django.db import models



from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from Posts.models import Post

# Create your models here.


'''
the model manager (comment manager in this case) helps generate a custom *(filtered) queryset
'''
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id = obj_id)
        return qs
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs =ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            my_model= model_qs.first().model_class()
            obj_qs = my_model.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() ==1:
                instance = self.model()
                instance.content = content
                instance.author = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent=parent_obj
                instance.save()
                return instance


class Comment(models.Model):
    author=models.ForeignKey('auth.user',   on_delete=models.CASCADE,)



    content_type = models.ForeignKey(ContentType ,on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    
    parent = models.ForeignKey('self', null=True, blank=True,on_delete= models.CASCADE,)
    added  = models.DateTimeField(auto_now_add=True)


    content = models.TextField()
    # parentPost = models.ForeignKey(Post)
    # added = models.DateField(auto_now_add=True)



    objects = CommentManager()


    def __str__(self):
        return 'comment from' +  self.author.username + str(self.pk)

    class Meta:
        ordering =['-added']





    def children(self):
        return  Comment.objects.filter(parent = self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True 


    # def __str__(self):
    #     # return str(self.author.username)
    #     # return self.author.username