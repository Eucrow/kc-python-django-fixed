from categories.views import home as categories_home
from django.conf.urls import url

urlpatterns = [
    url(r'^categories$', categories_home),
]