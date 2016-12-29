from blogs.api import BlogListAPI
from blogs.views import Blog, BlogList
from django.conf.urls import url

urlpatterns = [
    #web urls
    url(r'^blogs/(?P<user_blog>.+).html$', Blog.as_view()),
    url(r'^blogs$', BlogList.as_view()),

    #api urls
    url(r'^api/1.0/blogs/$', BlogListAPI.as_view(), name='api_blog_list'),
]