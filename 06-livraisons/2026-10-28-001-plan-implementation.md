# Livraison #001 — Plan d'implémentation — 2026-10-28

- **Réf. proposition** : #001 (plan d'implémentation, validé module par module les 2026-10-27 et 2026-10-28)
- **Réf. CDC** : PRD §8.5 (ordre de développement), toutes les exigences `F-*`, `NF-*`, TRD §28 (`T-*`)
- **Dépôts touchés** : docs

## Fichiers créés

- `04-planification/plan-implementation/README.md` : décisions de découpage, numérotation, ordre global, dépendances, gabarit, règles d'exécution, fonctions recettées en mobile, matrice de couverture des exigences.
- `04-planification/plan-implementation/web/` : 34 fichiers, W00 à W16 (modules découpés par rôle : W04, W06, W08, W09, W12).
- `04-planification/plan-implementation/mobile-entreprise/` : 11 fichiers, E00 à E10.
- `04-planification/plan-implementation/mobile-borne/` : 4 fichiers, B00 à B03.
- `04-planification/plan-implementation/mobile-console/` : 3 fichiers, C00 à C02.
- `04-planification/plan-implementation/mise-en-production.md`.
- `03-architecture/decisions/2026-10-27-0001-ordre-de-developpement.md` : web complet, puis Entreprise, Borne, Console.
- `03-architecture/decisions/2026-10-27-0002-aucune-donnee-de-pays-par-defaut.md` : aucune donnée propre à un pays, libellés dans la langue officielle de l'entreprise, fuseau de l'entreprise.

## Fichiers modifiés

- `04-planification/ROADMAP.md` : 54 entrées (W00 à W16 et sous-fichiers, E00 à E10, B00 à B03, C00 à C02, MEP), seul endroit où les statuts sont suivis.
- `01-specifications/PRD.md` : §8.5 (ordre de développement), F-PAY-02 (aucun paramétrage de pays), F-PAY-08 (paiements hors système), F-EMP-02 (types par défaut modifiables), F-EMP-09, F-NFC-05 (connexion par carte choisie par l'utilisateur), F-NFC-06 (signature avec ou sans carte), F-PLT-06 et NF-09 (archives hors système), F-TPS-06 (heures sup établies à l'avance), §10, §11, §13 (décisions), annexe 14.3 (jeu de démonstration).
- `01-specifications/TRD.md` : §4.1 (noms des dépôts `fluxyrh-w-app`, `fluxyrh-m-*`), §5.3 (provisionnement), §14.1 (aucun paramétrage de pays).
- `FluxyRH-web/README.md`, `FluxyRH-mobile/README.md` (dossiers de l'espace de travail, hors dépôt git) : noms des dépôts.

## Tests ajoutés

Aucun (livraison documentaire).

## Écarts

Les décisions prises en validant le plan modifient les spécifications sur de nombreux points (environ quarante). Le PRD et le TRD sont déjà mis à jour pour les décisions de fond ; les autres compléments (BACKEND SCHEMA, APPFLOW, UX/UI, TRD détaillé) sont listés dans l'étape « spécification » de chaque module et seront faits **au démarrage du module concerné**, comme prévu par le plan.

## Notes pour la suite

- Prochaine étape : W00 (amorçage technique), sur proposition puis « go ».
- Choix restant à faire au démarrage des modules concernés : construction des apps iOS (Mac ou service de build en ligne, E00), version Android minimale des bornes (B00), commande du serveur (MEP).
- Maquettes à proposer par Claude : page d'accueil `fluxyrh.app` (avant W01.12), 12 modèles de charte et 20 designs de carte (avant W16).
