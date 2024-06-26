# Generated by Django 4.2.6 on 2023-12-14 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import facetix_api.events.models.events_media


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utils', '0004_alter_codigootp_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.TextField(blank=True, max_length=150, verbose_name='Name')),
                ('date', models.DateField(help_text='Date the event will take place.', verbose_name='Event Date')),
                ('time', models.TimeField(help_text='Time the event will take place.', verbose_name='Event Time')),
                ('place', models.TextField(blank=True, max_length=250, verbose_name='Place')),
                ('address', models.TextField(blank=True, max_length=150, verbose_name='Address')),
                ('description', models.TextField(blank=True, max_length=150, verbose_name='Description')),
                ('capacity', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='utils.city')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'db_table': 'event',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.TextField(blank=True, max_length=150, verbose_name='Name')),
                ('guest_type', models.CharField(blank=True, choices=[('1', 'EXPOCITOR'), ('2', 'ARTISTA'), ('3', 'DEPORTISTA')], default='2', max_length=1, null=True)),
            ],
            options={
                'verbose_name': 'Guest',
                'verbose_name_plural': 'Guests',
                'db_table': 'guests',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TypeEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('name', models.TextField(blank=True, max_length=150, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Type Event',
                'verbose_name_plural': 'Type Events',
                'db_table': 'type_events',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GuestEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='events.guest')),
            ],
            options={
                'verbose_name': 'Guest Event',
                'verbose_name_plural': 'Guests Events',
                'db_table': 'guests_events',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EventTicketCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('cost', models.FloatField()),
                ('category', models.CharField(blank=True, choices=[('1', 'GENERAL'), ('2', 'VIP')], default='1', max_length=1, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'verbose_name': 'Event Ticket Cost',
                'verbose_name_plural': 'Event Ticket Cost',
                'db_table': 'events_ticket_cost',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EventMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('file', models.FileField(null=True, upload_to=facetix_api.events.models.events_media.directory_path)),
                ('type', models.CharField(blank=True, choices=[('1', 'GALLERY'), ('2', 'COVER')], default='1', max_length=1, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'verbose_name': 'Event Media',
                'verbose_name_plural': 'Event Media',
                'db_table': 'events_media',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='events.typeevent'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
