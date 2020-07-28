from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from Accounts.views import AccountLoginView
from rest_framework_jwt.views import obtain_jwt_token


# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()







urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/',include('Posts.urls')),
    path('comments/',include('Comments.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('login/', AccountLoginView.as_view()),
    path('register/', include('Accounts.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# router.register ('admin/', )