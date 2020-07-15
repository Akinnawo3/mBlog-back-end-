from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
     path('posts/',include('Posts.urls')),
     path('comments/',include('Comments.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# router.register ('admin/', )