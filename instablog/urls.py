"""instablog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^login/', login, name='login_url', kwargs={'template_name' : 'login.html'}), # template_name을 지정해주지 않으면 기본 화면은 'registration/login.html' 를 사용한다.
    url(r'^logout/', logout, name='logout_url', kwargs={'next_page' : '/login'}),   # next_page는 로그아웃 한 이후에 이동할 화면이다.
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', app_name='blog', namespace='blog')),
]

# static 파일들을 경로를 위함..
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)