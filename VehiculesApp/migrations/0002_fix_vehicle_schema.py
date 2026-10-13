import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VehiculesApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicule',
            name='immatriculation',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='type_vehicule',
            field=models.CharField(
                choices=[
                    ('camionnette', 'Camionnette'),
                    ('camion_porteur', 'Camion porteur'),
                    ('semi_remorque', 'Semi-remorque'),
                    ('fourgon', 'Fourgon'),
                ],
                default='camionnette',
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='capacite_kg',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='vehicule',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
