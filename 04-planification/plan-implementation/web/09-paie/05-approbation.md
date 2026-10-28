# W09.5 — Paie · Approbation (DIR)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W09.4 · Suite : W09.6 (clôture)

## 1. Objet

Donner à la direction la décision sur la paie d'une période : vue de synthèse (effectif, masses, coût employeur, écarts, anomalies non bloquantes), accès aux bulletins, puis **approbation** ou **renvoi motivé** au gestionnaire de paie. L'approbation fige le calcul : plus aucun recalcul n'est possible. À la fin de W09.5, la période `Approuvée` attend sa clôture (W09.6).

## 2. Ce que la direction reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Période `Contrôlée` et ses bulletins (W09.4), dans la boîte S-81 | `Approuvée` ou renvoi motivé (`Calculée`) | **PAIE** : clôture (W09.6) ou correction (W09.4) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-05 (suite) | `Contrôlée` → `Approuvée` (direction) ; renvoi avant approbation |

À lire : PRD §7.9 ; APPFLOW §4.3, §5.10, §6.6 (S-81) ; BACKEND SCHEMA §5.9 (`approved_by`, `approved_at`), §6 ; UX/UI §6.8.

## 4. Prérequis et décisions

W09.4 livré.

| Sujet | Proposition |
|---|---|
| Mode d'approbation | Par une action dans le web ou l'app, **sans carte** : la carte sert à signer des documents remis à une personne (F-NFC-06), pas une décision de gestion. Approbation journalisée (auteur, heure, IP, appareil) |
| Qui approuve | Toute personne `direction` active ; une seule approbation suffit |
| Renvoi | Motif obligatoire ; période → `calculee` ; le PAIE corrige, recalcule, contrôle de nouveau |
| Après approbation | Aucun recalcul possible ; une erreur découverte entre l'approbation et la clôture se corrige sur la période suivante (rappel ou retenue) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Période | `controlee` → `approuvee` ; `controlee` → `calculee` (renvoi, motif) | DIR |

## 6. Étapes ordonnées

### W09.5.1 — Service

- `PayrollPeriodService::approve(period)` (checklist « approbation » faite, `approved_by`, `approved_at`, journal, notification au PAIE) et `sendBack(period, reason)` ; refus de tout recalcul sur une période `approuvee`.

### W09.5.2 — Écran

- Élément « période de paie à approuver » dans S-81 `/approvals` : synthèse (effectif payé, masse brute, nette, cotisations, coût employeur, comparaison avec la période précédente, anomalies non bloquantes et motifs des écarts), lien vers S-54 en lecture, Approuver, Renvoyer (motif).
- Tableau de bord de la direction : périodes en attente d'approbation.

### W09.5.3 — API et documentation

- `/api/v1/direction/approvals` (périodes : synthèse, approuver, renvoyer).
- `02-reference/` : approbation.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W09.5 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Transitions | Approuver, renvoyer (motif), transitions interdites (`calculee` → `approuvee`, recalcul après approbation) |
| Droits | Direction seulement ; délégation de `approvals` sans accès aux montants pour un rôle non autorisé ; autre entreprise ; API |
| Non-fuite | La synthèse n'apparaît pas dans les notifications |

## 8. Critères de sortie

- Tests ciblés W09.5 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.10 jusqu'à `Approuvée`, avec un renvoi.
- Documentation et livraison de W09.5.3 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Clôture, bulletins publiés | W09.6 |
| Approbation dans l'app | E07 |
