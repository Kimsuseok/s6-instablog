from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^posts/create/$', views.create_post, name='create'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.detail_post, name='detail'),
    url(r'^posts/(?P<pk>[0-9]+)/edit/$', views.edit_post, name='edit'),
    url(r'^posts/(?P<pk>[0-9]+)/delete/$', views.delete_post, name='delete'),
    url(r'^posts/(?P<pk>[0-9]+)/comment/$', views.create_comment, name='comment'),
    url(r'^posts/(?P<pk>[0-9]+)/comment/delete/$', views.delete_comment, name='delete_comment'),
    url(r'^$', views.list_posts, name='list'),
]