# C02 — FluxyRH Console · Suivi des entreprises

Dépôt : `FluxyRH-mobile/console/` (fluxyrh-m-console) · Dépend de : C01

## 1. Objet

Donner aux admins de RIYADA ONE une vue de poche de la plateforme : **Accueil** (indicateurs du tableau de bord plateforme), **Entreprises** (liste et fiche en lecture : statut, palier, modules, effectif, factures), **Journal** de la plateforme, **Profil**. La gestion (création, abonnement, modules, factures) reste au web. À la fin de C02, la Console est complète.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PLT-04 (mobile) | Indicateurs de la plateforme |

À lire : APPFLOW §4.1 ; UX/UI §9 ; `02-reference/` (W01).

## 3. Prérequis et décisions

C01 livré.

| Sujet | Proposition |
|---|---|
| Périmètre | Lecture seule : tout ce qui modifie une entreprise reste au web plateforme |
| Données | Aucune donnée nominative d'employé ni de salaire (comme le tableau de bord plateforme, W01.10) |

## 4. Étapes ordonnées

### C02.1 — Écrans

- **Accueil** : derniers indicateurs (entreprises, abonnements, revenu récurrent, effectifs, dépassements de palier, cartes à encoder) ; **Entreprises** : liste, fiche (statut, palier, modules, effectif, factures et leur statut) ; **Journal** : filtres ; **Profil**.
- Points d'API `/platform/*` complétés si besoin (dans `FluxyRH-web/app/`, avec leurs tests).

### C02.2 — Documentation et livraison

- `02-reference/` ; `05-recette/` : recette complète de la Console.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut C02 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Écrans | Données cohérentes avec le web plateforme, lecture seule |
| Confidentialité | Aucune donnée nominative ni salariale |

## 6. Critères de sortie

- `npm run check` vert ; recette complète de la Console consignée.
- Documentation et livraison de C02.2 faites.
