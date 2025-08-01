# Generated by Django 4.2.6 on 2023-10-23 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='areas.area', verbose_name='上级行政区划')),
            ],
            options={
                'verbose_name': '省市区',
                'verbose_name_plural': '省市区',
                'db_table': 'tb_areas',
            },
        ),
    ]
