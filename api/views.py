from django.http import JsonResponse
from .models import Event, TYPE_CHOICES, EventRegister, UserAdditionalInfo, Wishlist
from .serializers import EventSerializer, UserSerializer, EventRegisterSerializer, UserAdditionalInfoSerializer, WishlistSerializer
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.db import models
from django.db.models import Q

from django.shortcuts import render
from django.db.models import Q


def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(starting_time__icontains=query) |  # Keresés dátum és idő alapján
            Q(date__icontains=query)  # Keresés dátum alapján
            # |
            # Q(type__icontains=query)             # Keresés típus alapján
        )
    else:
        results = Event.objects.none()

    results_list = list(results.values('id', 'title', 'description',
                        'max_participants', 'starting_time', 'location', 'date'))
    return JsonResponse(results_list, safe=False)


def search_by_category(request):
    category = request.GET.get('category', '')
    types = [choice[0] for choice in TYPE_CHOICES]

    if category:
        if category in types:
            results = Event.objects.filter(type=category)
            if results.exists():
                results_list = list(results.values(
                    'id', 'title', 'description', 'max_participants', 'starting_time', 'location', 'date', 'type'))
                return JsonResponse({'status': 'success', 'data': results_list}, safe=False)
            else:
                return JsonResponse({'status': 'no_data', 'message': f'No events found for category: {category}'}, safe=False)
        else:
            return JsonResponse({'status': 'invalid_category', 'message': 'Invalid category'}, safe=False)
    else:
        return JsonResponse({'status': 'no_category', 'message': 'No category specified'}, safe=False)



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)    


class EventRegisterViewSet(viewsets.ModelViewSet):
    queryset = EventRegister.objects.all()
    serializer_class = EventRegisterSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        #   IsOwnerOrReadOnly]
    

    def create(self, request):
        event = Event.objects.get(id=request.data.get('event_id'))
        user = User.objects.get(id=request.data.get('user_id'))

        if event.is_full():
            try:    
                EventRegister.objects.create(event=event, user=user)
                return Response({'status': 'registered'}, status=status.HTTP_201_CREATED)
            except Event.DoesNotExist:
                return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        else:
            return Response({'error': 'Not enough space'}, status=status.HTTP_400_BAD_REQUEST)
          
    @action(detail=False, methods=['POST'],)
    def delete_registration(self, request):
        event = Event.objects.get(id= request.data.get('event_id'))
        user = User.objects.get(id =request.data.get('user_id'))
        registration = EventRegister.objects.get(event=event, user=user)

        if not event.DoesNotExist or not user.DoesNotExist or not registration.DoesNotExist:
            return Response({'error': 'Event ID and User ID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try: 
                registration.delete()
                return Response({'success': 'Registration deleted successfully.'}, status=status.HTTP_200_OK)
        except (Event.DoesNotExist, User.DoesNotExist, EventRegister.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)



class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request ):
        event = Event.objects.get(id=request.data.get('event_id'))
        user = User.objects.get(id = request.data.get('user_id'))

        try:
            Wishlist.objects.create(event=event, user=user)
            return Response({'status': 'event add to wishlist'}, status=status.HTTP_201_CREATED)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'],)
    def delete_wishlist(self, request):
        event = Event.objects.get(id=request.data.get('event_id'))
        user = User.objects.get(id = request.data.get('user_id'))
        wishlist = Wishlist.objects.get(event=event, user=user)

        if not event or not user or not wishlist:
            return Response({'error': 'Event ID and User ID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try: 
                wishlist.delete()
                return Response({'success': 'Wish deleted successfully.'}, status=status.HTTP_200_OK)
        except (Event.DoesNotExist, User.DoesNotExist, EventRegister.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)




class UserViewSet(viewsets.ModelViewSet):
    queryset =  User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class UserAdditionalInfoViewSet(viewsets.ModelViewSet):
    queryset = UserAdditionalInfo.objects.all()
    serializer_class = UserAdditionalInfoSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)    


