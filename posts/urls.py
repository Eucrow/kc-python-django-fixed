from posts.api import PostListAPI, PostDetailAPI
from posts.views import PostDetail, PostCreationView
from django.conf.urls import url

urlpatterns = [
    # web urls
    url(r'^posts/(?P<pk>[0-9]+)$', PostDetail.as_view(), name='post_detail'),
    url(r'^newpost$', PostCreationView.as_view()),

    # api urls
    url(r'^api/1.0/posts/$', PostListAPI.as_view(), name='api_post_list'),
    url(r'^api/1.0/posts/(?P<pk>[0-9]+)$', PostDetailAPI.as_view(), name='api_post_list'),
]
