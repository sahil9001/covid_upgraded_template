"""corona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker.views import home,login
from django.contrib.auth.views import LogoutView

#from tracker.views import pathTracing
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
"""
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'pathtracing/(?P<user_id>[0-9]+)', pathTracing, basename='pathTracing')
"""

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  
    path('admin/', admin.site.urls),
    path('tracker/',include('tracker.urls')),
    path('',home,name="home"),
    path('login/',login,name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    #path('my_tracker/',include(router.urls)),

]
if settings.DEBUG: #Not for production code
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)