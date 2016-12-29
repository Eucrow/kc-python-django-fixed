from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView
from blogs.serializers import BlogSerializer



class BlogListAPI(ListCreateAPIView):
    """
    Endpoint de listado de blogs
    """

    user_list = User.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        # filter by search
        search = self.request.query_params.get('search', None)

        if search is not None:
            queryset = self.user_list.filter(username__icontains=search)
            return queryset
        else:
            return self.user_list
