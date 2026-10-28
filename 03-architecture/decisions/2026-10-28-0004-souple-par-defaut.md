# 0004 — Souple par défaut, durcissable par l'entreprise

- **Date** : 2026-10-28
- **Statut** : acceptée

## Contexte

En validant le plan, les règles se sont accumulées une à une ; bout à bout, elles alourdissent le travail des utilisateurs. Il faut distinguer les règles qui protègent l'entreprise de celles qui ne sont que des contraintes de confort.

## Décision

1. **Principe** : une règle contraignante qui ne touche pas à la sécurité devient un **réglage de l'entreprise** ; quand l'entreprise choisit de relâcher une protection, l'écran lui **explique les risques**.
2. **Règles de sécurité, jamais réglables** : personne ne valide ses propres données ; l'admin ne voit jamais les salaires ni la banque ; le pointage exige la carte ; une paie clôturée est verrouillée ; tout est journalisé.
3. **Règles maintenues telles quelles** (choix du porteur du projet) : vérification une demande à la fois ; heures sup établies à l'avance ; congés en trois étapes (employé → manager → RH) ; paie en six étapes ; avances en trois validations ; une notification par événement ; aucun modèle de démarrage par pays dans ce projet.
4. **Allègements retenus** :
   - **Contrats** : signataires pré-remplis (l'employé et le signataire de l'entreprise par défaut, réglé une fois) ; le RH ne les change que si besoin.
   - **Validation par sélection** : « Valider la sélection » partout où il n'y a pas d'argent en jeu (congés, heures sup, pointages de secours) ; tout montant reste une décision par élément.
   - **Évaluations** : la règle de clôture se choisit à la création de chaque campagne (bloquée tant qu'un évaluateur n'a pas répondu, ou permise après la date de fin avec les poids recalculés).
   - **2FA** : jamais imposée par l'entreprise ; chaque utilisateur l'active lui-même. La politique de mot de passe garde 12 caractères et la complexité par défaut.
5. **Dossier incomplet** : bloque par défaut les congés, les attestations et la paie ; l'entreprise peut lever chacun de ces blocages, l'écran lui expliquant les risques.

## Conséquences

- De nouveaux réglages apparaissent dans la Configuration (contrats, blocages du dossier incomplet) et dans la création d'une campagne d'évaluation.
- La table `two_factor_required_roles` disparaît.

## Alternatives écartées

- **Tout assouplir par défaut** (vérification groupée, congés à deux étapes, paie raccourcie…) : écarté par le porteur du projet pour garder la fiabilité des données et des décisions.
