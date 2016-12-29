from users.views import login, logout, SignUpView, SignupSuccessfulView
from django.conf.urls import url
from users.api import UserListAPI, UserDetailAPI

urlpatterns = [
    #web urls
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^signup$', SignUpView.as_view(), name='signup'),
    url(r'^success$', SignupSuccessfulView.as_view(), name='signup_success'),

    #api urls
    url(r'^api/1.0/users/$', UserListAPI.as_view(), name='api_user_list'),
    url(r'^api/1.0/users/(?P<pk>[0-9]+)$', UserDetailAPI.as_view(), name='api_user_detail')
]