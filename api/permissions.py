from rest_framework.permissions import BasePermission


class IsTransactionOwner(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            view.queryset = view.queryset.filter(user=request.user)
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAccountOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            view.queryset == view.queryset.filter(user=request.user)
            return True
        return super().has_permission(request, view)


class IsCategoryOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            view.queryset = view.queryset.filter(user=request.user)
            return True
        return super().has_permission(request, view)
