from django.contrib import admin
from .models import Event, EventRegister, UserAdditionalInfo, Wishlist
# Register your models here.

admin.site.register(Event)
admin.site.register(EventRegister)
admin.site.register(UserAdditionalInfo)
admin.site.register(Wishlist)


