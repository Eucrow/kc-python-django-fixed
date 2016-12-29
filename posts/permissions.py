from rest_framework.permissions import BasePermission


class PostPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Define si un usuario puede ajecutar el método o acceder a la vista/controlador
        Args:
            request:
            view: vista que se está ejecutando

        Returns:
        """

        from posts.api import \
            PostDetailAPI, PostListAPI  # tenemos que importarlo aquí para evitar un problema de importación cíclica

        if request.method == "POST" and request.user.is_authenticated():  # cualquiera autenticado puede crear un post
            return True
        if request.user.is_superuser:
            return True
        if isinstance(view, PostDetailAPI) or isinstance(view, PostListAPI): # si la vista que se está usando es UserDetailAPI
            return True
        return False  # el resto, no tiene permisos

    def has_object_permission(self, request, view, obj):
        """
        Define si un usuario puede realizar la operación que quiere sobre el objeto obj
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return request.user.is_superuser or request.user == obj.owner
