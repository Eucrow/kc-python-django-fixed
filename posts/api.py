from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.permissions import PostPermission
from posts.serializers import PostSerializer, PostListSerializer
from posts.views import PostListQuerySet

from rest_framework.filters import OrderingFilter, SearchFilter


# TODO: convert this in a ViewSet (video Día 6 - Sesión 2 Autorización, Autenticación, Filtrado de da.flv, 1:25

class PostListAPI(ListCreateAPIView):
    """
    Endpoint de listado y creación de artículos
    """
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (PostPermission,)

    # django filter backends:
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ('title', 'publication_at')
    search_fields = ('title', 'content')

    def get_queryset(self):
        posts_by_user = PostListQuerySet.get_posts_by_user(user=self.request.user)
        queryset = posts_by_user

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
