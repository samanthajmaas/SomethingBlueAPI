# Generated by Django 3.1.4 on 2020-12-16 21:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image_url', models.ImageField(blank='true', null='true', upload_to='profile_img/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_for', models.CharField(max_length=200)),
                ('default', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toDo', models.CharField(max_length=200)),
                ('default', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=75, null=True)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('budget', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('bride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.bride')),
            ],
        ),
        migrations.CreateModel(
            name='WeddingChecklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('checklist_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.checklistitem')),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.wedding')),
            ],
        ),
        migrations.CreateModel(
            name='WeddingBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimated_cost', models.FloatField(null=True)),
                ('actual_cost', models.FloatField(null=True)),
                ('paid', models.BooleanField()),
                ('budget_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.budgetitem')),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.wedding')),
            ],
        ),
        migrations.CreateModel(
            name='VisionBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vb_img', models.ImageField(upload_to='visionboard/')),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.wedding')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_first_name', models.CharField(max_length=75)),
                ('guest_last_name', models.CharField(max_length=75)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=75)),
                ('number_of_guests_in_party', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('rsvp_status', models.CharField(max_length=75)),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='somethingblueapi.wedding')),
            ],
        ),
    ]
