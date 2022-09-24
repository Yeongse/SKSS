# Generated by Django 4.1 on 2022-09-24 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('substitute', '0006_substituteask_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='classleader',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='substitute.grade'),
        ),
        migrations.AlterField(
            model_name='course',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='substitute.grade'),
        ),
    ]