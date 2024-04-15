# Generated by Django 4.2.6 on 2023-12-15 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_event_file_cover_alter_eventmedia_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventticketcost',
            name='category',
            field=models.CharField(choices=[('1', 'GENERAL'), ('2', 'VIP')], default='1', max_length=1),
        ),
        migrations.CreateModel(
            name='BuyEventTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date on which it was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date it was last updated.', verbose_name='updated at')),
                ('category', models.CharField(choices=[('1', 'GENERAL'), ('2', 'VIP')], default='1', max_length=1)),
                ('number', models.IntegerField()),
                ('cost', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'verbose_name': 'Buy Event Ticket',
                'verbose_name_plural': 'Buy Event Tickets',
                'db_table': 'buy_event_tickets',
                'managed': True,
            },
        ),
    ]
