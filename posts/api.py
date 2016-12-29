from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.models import Post
from posts.permissions import PostPermission
from posts.serializers import PostSerializer, PostListSerializer
from posts.views import PostListQuerySet


# TODO: convert this in a ViewSet (video Día 6 - Sesión 2 Autorización, Autenticación, Filtrado de da.flv, 1:25

class PostListAPI(ListCreateAPIView):
    """
    Endpoint de listado y creación de artículos
    """
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (PostPermission,)

    # TODO: move order_results to another file...
    def order_results(self, request, *args):
        '''
        Order the queryset by fields
        :param request: request to order
        :param args: fields used to order the queryset
        :return: queryset already ordered
        '''

        fields = []

        for a in args:
            to_order = self.request.query_params.get(a, None)
            if to_order == "asc":
                by_field = a
                fields.append(by_field)
            elif to_order == "des":
                by_field = "-" + a
                fields.append(by_field)
            else:
                by_field = None

        if fields is not None:
            queryset = request.order_by(*fields)
            # para entender *fields: http://agiliq.com/blog/2012/06/understanding-args-and-kwargs/

        return queryset

    def get_queryset(self):

        posts_by_user = PostListQuerySet.get_posts_by_user(user=self.request.user)
        queryset = posts_by_user

        # TODO: send to a function
        # filter by search
        search = self.request.query_params.get('search', None)

        if search is not None:
            queryset = posts_by_user.filter(title__icontains=search)
        #

        queryset = self.order_results(queryset, "title", "publication_date")

        return queryset

    # sobreescribimos el método get_serializer_class para que haga lo que nosotros deseamos,
    # en este caso devuelve PostSerializer si el método es POST o PostListSerializer si no.
    def get_serializer_class(self):
        return PostSerializer if self.request.method == 'POST' else PostListSerializer

    def perform_create(self, serializer):  # obligamos a que se guarde el post con el usuario que
        # está autenticado cuando se está creando uno nuevo
        serializer.save(owner=self.request.user)


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Endpoint de detalle, actualización y borrado de artículos
    """
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (PostPermission,)

    def get_queryset(self):
        return PostListQuerySet.get_posts_by_user(user=self.request.user)

    def perform_update(self, serializer):  # obligamos a que se guarde la foto con el usuario que está autenticado
        # cuando se está actualizando una foto
        return serializer.save(owner=self.request.user)
