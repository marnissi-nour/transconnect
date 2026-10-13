import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffersApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offre',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offre',
            name='prix',
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0.01)],
            ),
        ),
        migrations.AlterField(
            model_name='offre',
            name='delai_jours',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='offre',
            name='date_proposition',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='offre',
            name='statut',
            field=models.CharField(
                choices=[
                    ('proposee', 'Proposée'),
                    ('acceptee', 'Acceptée'),
                    ('refusee', 'Refusée'),
                    ('retiree', 'Retirée'),
                ],
                default='proposee',
                max_length=20,
            ),
        ),
        migrations.AddConstraint(
            model_name='offre',
            constraint=models.UniqueConstraint(
                condition=models.Q(('statut', 'proposee')),
                fields=('transporteur', 'expedition'),
                name='unique_offre_proposee_transporteur_expedition',
            ),
        ),
    ]
