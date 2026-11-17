from django.db import models


class Notification(models.Model):
    destinataire = models.ForeignKey(
        "EntreprisesApp.Utilisateur",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    offre = models.ForeignKey(
        "OffersApp.Offre",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    message = models.CharField(max_length=255)
    lue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.message
