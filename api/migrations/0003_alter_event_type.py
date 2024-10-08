# Generated by Django 5.0.3 on 2024-05-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_event_max_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('BOARDGAME', 'Boardgame'), ('COOKING', 'Cooking'), ('EQUIPMENT_RENTAL', 'Equipment rental'), ('OTHER', 'Other'), ('SHOPPING', 'Shopping'), ('SOCIAL_WORK', 'Social work'), ('SPORT', 'Sport'), ('TRAVELING', 'Traveling'), ('TUDOR', 'Tudor'), ('VIDEOGAME', 'Videogame')], default='OTHER', max_length=20),
        ),
    ]
