## Entrée [2026-10-13]
- Outil IA utilisé : GitHub Copilot (VS Code / Copilot SDK)
- Prompt : "Créer les modèles Django pour TransConnect en respectant le cahier des charges et corriger les anomalies du premier jet sur l'entité Offre."
- Sortie obtenue (résumé) : Un premier jet de modèles Django a été généré avec les champs métiers de base, mais il contenait plusieurs incohérences par rapport au cahier des charges du workshop.
- Écarts identifiés vs cahier des charges :
  1. `Offre.prix` a été défini comme `CharField` au lieu d'un `DecimalField`, ce qui est incompatible avec un prix monétaire.
  2. `Offre.delai_jours` a été déclaré comme `IntegerField` simple alors que le cahier des charges impose un `PositiveIntegerField` avec validation positive.
  3. `Offre.date_proposition` utilisait `auto_now=True` au lieu de `auto_now_add=True`, ce qui modifie la date à chaque sauvegarde au lieu de la figer à la création.
  4. `Offre.vehicule` était nullable (`null=True`), alors que le TP exige une relation obligatoire entre une offre et un véhicule utilisable pour l'expédition.
- Correction apportée et justification :
  - `prix` est maintenant un `DecimalField(max_digits=10, decimal_places=2)` avec validation `MinValueValidator(0.01)` pour respecter le type monétaire et les contraintes de validité.
  - `delai_jours` est un `PositiveIntegerField` avec validation minimum à 1 pour empêcher les délais nuls ou négatifs.
  - `date_proposition` est un `DateField(auto_now_add=True)` pour enregistrer la date de création et non la date de dernière modification.
  - `vehicule` est obligatoire dans le modèle final, ce qui garantit qu'une offre propose toujours un véhicule admissible par le transporteur.

## Entrée [2026-10-13] (vérification finale)
- Outil IA utilisé : GitHub Copilot (VS Code / Copilot SDK)
- Prompt : "Vérifier la cohérence du TP Django TransConnect, corriger les migrations désynchronisées et valider la base de données avant de déclarer le projet terminé."
- Sortie obtenue (résumé) : Les modèles métier étaient globalement conformes, mais les migrations initiales du projet ne correspondaient plus à la version finale du code. Un correctif de synchronisation était nécessaire pour rendre le projet migrable et conforme au cahier des charges.
- Écarts identifiés vs cahier des charges :
  - Les migrations initiales de chaque application contenaient des anciens noms de champs (`raison_sociale`, `matricule_fiscale`, `id_client`, `ville_arrivee`, `en cours`, etc.) qui ne correspondaient pas aux modèles finaux.
  - Certaines colonnes avaient des types obsolètes (par exemple `DateTimeField` pour `date_proposition`, `PositiveIntegerField` pour `poids_kg`, `CharField` pour `prix`).
- Correction apportée et justification :
  - Ajout de migrations de correction (`0002_*`) pour réaligner les schémas avec les modèles actuels du TP.
  - Validation du projet par `python manage.py check` et `python manage.py migrate` pour confirmer que le schéma est cohérent et migrable.
