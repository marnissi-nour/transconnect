import django.core.validators
from django.db import migrations, models

import EntreprisesApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('EntreprisesApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entreprise',
            old_name='raison_sociale',
            new_name='raison_social',
        ),
        migrations.RenameField(
            model_name='entreprise',
            old_name='matricule_fiscale',
            new_name='matricule_fiscal',
        ),
        migrations.RenameField(
            model_name='utilisateur',
            old_name='id_client',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='user_id',
            field=models.CharField(editable=False, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.EmailField(unique=True, validators=[EntreprisesApp.models.validate_gmail]),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='role',
            field=models.CharField(
                choices=[
                    ('chargeur', 'Chargeur'),
                    ('transporteur', 'Transporteur'),
                    ('administrateur', 'Administrateur'),
                ],
                default='chargeur',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='matricule_fiscal',
            field=models.CharField(max_length=17, unique=True, validators=[EntreprisesApp.models.matricule_validator]),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='type_entreprise',
            field=models.CharField(
                choices=[('chargeur', 'Chargeur'), ('transporteur', 'Transporteur')],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='adresse',
            field=models.TextField(
                validators=[
                    django.core.validators.MinLengthValidator(
                        20,
                        "L'adresse doit contenir au moins 20 caractères.",
                    )
                ]
            ),
        ),
    ]
