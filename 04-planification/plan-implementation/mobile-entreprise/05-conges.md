# E05 — FluxyRH Entreprise · Congés

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E04

## 1. Objet

Demander, suivre et décider les congés depuis le téléphone : soldes par type, demande avec calcul des jours et justificatif, même hors ligne ; approbation par le manager (ou son supérieur pendant son absence) avec le calendrier de l'équipe ; validation par le RH. À la fin d'E05, le circuit des congés se fait entièrement dans l'app.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ABS-02 | Demande, approbation, validation, refus, annulation |
| F-ABS-03 | Jours calculés, soldes |
| F-ABS-04 | Calendrier d'équipe |
| F-MOB-03, 04 | Demande hors ligne, décisions du manager et du RH |

À lire : APPFLOW §5.8 ; UX/UI §7.1 (`BalanceCard`), §7.4 ; `02-reference/` (W07).

## 3. Prérequis et décisions

E04 livré.

| Sujet | Proposition |
|---|---|
| Calcul des jours hors ligne | Estimation affichée à partir du planning et des jours fériés en cache, marquée « estimation » ; le serveur fait le calcul et le contrôle de solde définitifs à l'envoi (APPFLOW §5.8) |
| Décisions | Approbation et validation exigent le réseau |

## 4. Étapes ordonnées

### E05.1 — Employé

- Onglet **Demandes**, congés : soldes (`BalanceCard`), nouvelle demande (type, dates, demi-journées, motif, justificatif en photo), contrôles expliqués (pièces manquantes du dossier, solde), historique, annulation.
- Création en file hors ligne avec `client_uuid` (E00.7).

### E05.2 — Manager

- Onglet **Équipe**, demandes à décider (y compris « en remplacement de… » pendant l'absence d'un manager), solde, calendrier de l'équipe sur la période, approuver, refuser avec motif ; calendrier d'équipe par semaine et par mois.

### E05.3 — RH

- Onglet **Validations**, congés approuvés et demandes des employés sans manager : valider, refuser avec motif.

### E05.4 — Documentation et livraison

- `02-reference/` : écrans des congés.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E05 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Demande | Demi-journées, justificatif, dossier incomplet, solde insuffisant, chevauchement |
| Hors ligne | Estimation, envoi, refus du serveur affiché |
| Décisions | Manager, supérieur en remplacement, RH, refus motivé, annulation |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.8 sur téléphone, y compris un manager en congé.
- Documentation et livraison d'E05.4 faites.
