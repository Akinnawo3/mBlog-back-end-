from django.contrib import admin
from .models import Post

# Register your models here.



class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'added', 'updated']
    search_fields =['title']
    list_filter = ['title', 'added']
    
    # list_display_links = ['added'] the attribute tht can be clicked to get into the detailed display ..*(this is title by defaullt)
    class Meta:
        model = Post
admin.site.register(Post, PostModelAdmin)