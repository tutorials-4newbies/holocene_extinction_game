from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS


class IsCreatorMutatingOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Allows access only to authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        obj is the object we're accessing, probably the Animal

        """
        return (
                request.method in SAFE_METHODS or
                (request.user and request.user.is_authenticated and (request.user.is_superuser or request.user == obj.creator))

        )
