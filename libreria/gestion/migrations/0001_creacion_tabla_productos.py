# Generated by Django 3.2.7 on 2021-09-22 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoModel',
            fields=[
                ('produtoId', models.AutoField(db_column='id', primary_key=True, serialize=False, unique=True)),
                ('productoNombre', models.CharField(db_column='nombre,', max_length=45)),
                ('productoPrecio', models.DecimalField(db_column='precio', decimal_places=2, max_digits=10)),
                ('productoUnidadMedida', models.TextField(choices=[('UN', 'UNIDADES'), ('DOC', 'DOCENA'), ('CI', 'CIENTO'), ('MI', 'MILLAR')], db_column='unidad_medida', default='UN')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'db_table': 'productos',
                'ordering': ['-productoPrecio'],
            },
        ),
    ]
