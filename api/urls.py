from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from . import views
from .views import search, search_by_category, UserViewSet, UserAdditionalInfoViewSet, EventViewSet, EventRegisterViewSet, WishlistViewSet


router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event'),
router.register(r'users', views.UserViewSet, basename='user'),
router.register(r'usersadditionalinfo', views.UserAdditionalInfoViewSet, basename='useradditionalinfo'),
router.register(r'eventsregister', views.EventRegisterViewSet, basename='eventsregister'),
router.register(r'wishlistlist', views.WishlistViewSet, basename='wishlistlist'),




event_list = EventViewSet.as_view({
    'get': 'list',
    'post': 'create'
    # 'post': 'perform_create'
})
event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


eventregister_list = EventRegisterViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'post': 'delete_registration'

})
eventregister_detail = EventRegisterViewSet.as_view({
    'get': 'retrieve',
})



wish_list = WishlistViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'post': 'delete_wishlist'
})
wish_detail = WishlistViewSet.as_view({
    'get': 'retrieve',
})



user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
useradditionalinfo_list = UserAdditionalInfoViewSet.as_view({
    'get': 'list',
    'post': 'perform_create'
})
useradditionalinfo_detail = UserAdditionalInfoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns =([
    path('', include(router.urls)),
    # api authentication, users
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    # path('usersadditionalinfo/', useradditionalinfo_list, name='useradditional-list'),
    # path('usersadditionalinfo/<int:pk>/', useradditionalinfo_detail, name='useradditional-detail'),
    path('search/', search, name='search'),
    path('search_by_category/', search_by_category, name='search_by_category'),
    # # events, 
    path('events/', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('wishlist/', wish_list, name='wishlist-list'),
    path('wishlist/<int:pk>/', wish_detail, name='wishlist-detail'),
    path('eventsregister/', eventregister_list, name='eventregister-list'),
    path('eventsregister/<int:pk>/', eventregister_detail, name='eventregister-detail'),
 
])
