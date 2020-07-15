from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone



class PostManager(models.Manager):
    def all (self,*args,**kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())





# Create your models here.
class Post(models.Model):

    author=models.ForeignKey('auth.user', related_name='snippets', on_delete=models.CASCADE,)
    title = models.CharField(max_length=250)
    content = models.TextField()
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, default = timezone.now().date())
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, blank=True) 


    objects= PostManager()



    def __str__(self):
        return self.title
     

    class Meta:
        ordering = ['-added']


        '''
        auto_now vs auto_now_add
        auto_now
        changes value of the field whenevr it is resaved in the dtabase

        auto_now_add
        assigns the initial time it is saved automatically

        '''


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    slug_exist=qs.exists()
    if slug_exist:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
        




def pre_save_post(sender, instance, *args, **kwargs): 
   if not instance.slug:
       instance.slug=create_slug(instance)


pre_save.connect(pre_save_post, sender=Post)