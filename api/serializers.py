from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventRegister, UserAdditionalInfo, Wishlist


class UserSerializer(serializers.HyperlinkedModelSerializer):
    events = serializers.HyperlinkedRelatedField(many=True, view_name='event-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username','last_name', 'first_name','email', 'events', ]



class UserAdditionalInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserAdditionalInfo
        fields = '__all__'



class EventRegisterSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField( view_name='user-detail',  read_only=True)
    event = serializers.HyperlinkedRelatedField(view_name='event-detail',  read_only=True )

    class Meta:
        model = EventRegister
        fields = ['url', 'id', 'user', 'event', 'registration_date']
        extra_kwargs = {
            'url': {'view_name': 'eventregister-detail', 'lookup_field': 'pk'}
        }

class EventSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.HyperlinkedIdentityField(source='owner.id', view_name='user-detail')
    event_registration = EventRegisterSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['url', 'id', 'title', 'description', 'starting_time', 'max_participants','image', 'owner', 'location','type', 'event_registration']
       



class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField( view_name='user-detail',  read_only=True)
    event = serializers.HyperlinkedRelatedField(view_name='event-detail',  read_only=True )
    
    class Meta:
        model = Wishlist
        fields = ['url', 'id', 'event', 'user', ]
        extra_kwargs = {'url': {'view_name': 'wishlist-detail', 'lookup_field': 'pk'}}

