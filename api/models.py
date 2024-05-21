from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator

class Event(models.Model):
    BOARDGAME = 'BOARDGAME'
    COOKING = 'COOKING'
    EQUIPMENT_RENTAL = 'EQUIPMENT_RENTAL'
    OTHER = 'OTHER'
    SHOPPING = 'SHOPPING'
    SOCIAL_WORK = 'SOCIAL_WORK'
    SPORT = 'SPORT'
    TRAVELING = 'TRAVELING'
    TUDOR = 'TUDOR'
    VIDEGAME = 'VIDEOGAME'


    TYPE_CHOICES = [
        (BOARDGAME , 'Boardgame'),
        (COOKING , 'Cooking'),
        (EQUIPMENT_RENTAL , 'Equipment rental'),
        (OTHER , 'Other'),
        (SHOPPING , 'Shopping'),
        (SOCIAL_WORK , 'Social work'),
        (SPORT , 'Sport'),
        (TRAVELING , 'Traveling'),
        (TUDOR , 'Tudor'),
        (VIDEGAME , 'Videogame'),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    max_participants =models.IntegerField( default=1, validators=[MinValueValidator(0)])
    starting_time = models.DateTimeField(auto_now_add=False)
    location = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User,  related_name='events',  on_delete=models.CASCADE)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES, default=OTHER)
    event_registration = models.ManyToManyField(User, through='EventRegister', related_name='eventsattended')    

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} + {self.owner}"
    
    def is_full(self):
        return self.event_registration.count() <= (self.max_participants -1)


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    host_rating = models.IntegerField(default=0)
    quest_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"
    


class EventRegister(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # event = models.ManyToManyField(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('event', 'user'),) 

    def __str__(self):
        return f"{self.event.id} + {self.user.id}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,)

    class Meta:
        unique_together = (('event', 'user'),) 

    def __str__(self):
        return f"{self.user} + {self.event}"

