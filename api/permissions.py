from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Olvasási engedélyek minden kérésre engedélyezettek,
        # így mindig engedélyezni fogja a GET, HEAD vagy OPTIONS kéréseket.
        if request.method in permissions.SAFE_METHODS:
            return True

        #Ellenőrizi, hogy az objektum rendelkezik-e „owner” attribútummal
        if hasattr(obj, 'owner'):
            # Az írási engedélyek akkor engedélyezettek, ha az objektum tulajdonosa a kérés felhasználója.
            return obj.owner == request.user
        else:
            # Ha nincs „owner” attribútum, ellenőrzi, hogy az objektum azonosítója megegyezik-e a kérés felhasználói azonosítójával.
            return obj.id == request.user.id

    
