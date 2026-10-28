# W06.3 — Temps de travail · Manager

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W06.2 · Suite : W06.4 (RH)

## 1. Objet

Donner au manager la main sur le temps de son équipe : présences du jour, pointages refusés, **corrections motivées** des journées (oubli, carte perdue, borne en panne) et **établissement à l'avance des heures supplémentaires** de son équipe. À la fin de W06.3, chaque anomalie de pointage a un traitement, et seules les heures sup établies par le manager peuvent être comptées.

## 2. Ce que le manager reçoit, produit, transmet

| Reçoit | Produit | Transmet à |
|---|---|---|
| Journées calculées, pointages refusés de son équipe (W06.2) | Journées corrigées (motif) ; heures sup établies à l'avance (`declaree`) | **RH** (W06.4) : heures sup réalisées à valider ; **employé** : correction notifiée ; paie (W09) : journées définitives |

Le manager agit sur son **équipe directe** ; son supérieur n'agit qu'en son absence (construit en W07). Personne ne corrige sa propre journée ni ne déclare ses propres heures sup.

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-TPS-05 | Correction de pointage motivée, journalisée |
| F-TPS-06 (établissement) | Heures sup établies à l'avance par le manager |
| F-ORG-04 | Décision au manager direct |

À lire : PRD §7.6 ; APPFLOW §4.6, §5.6 (fin), §5.7, §6.3 (S-33, S-34), §7 ; BACKEND SCHEMA §5.6 (`attendance_corrections`, `overtime_entries`), §6 ; UX/UI §6.1.

## 4. Prérequis et décisions

W06.2 livré.

| Sujet | Proposition |
|---|---|
| Heures sup établies à l'avance | Le manager établit une heure sup pour un employé, un jour et un nombre de minutes, **avant la journée ou le jour même** ; c'est la seule façon qu'un temps au-delà du planning soit compté (W06.2). Les statuts `proposee` et la source `pointage` sont retirés (BACKEND SCHEMA §6 et §7 mis à jour) |
| Correction de sa propre journée | Refusée : la journée d'un manager est corrigée par **son** manager |
| Correction d'une journée ancienne | Possible seulement sur les **X derniers jours**, X réglé par l'entreprise (W06.1.2), et jamais sur une période de paie clôturée (contrôle ajouté en W09.6) |
| Effet d'une correction sur les heures sup | Les minutes réalisées d'une heure sup établie sont recalculées à partir de la journée corrigée, tant que le RH n'a pas décidé |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Journée | calculée → corrigée (`is_corrected`, motif, valeurs avant et après dans `attendance_corrections`) ; une journée peut être corrigée plusieurs fois | MGR |
| Heures sup | (création) `declaree` : établie à l'avance, modifiable ou annulable par le manager tant que la journée n'est pas passée | MGR |

## 6. Étapes ordonnées

### W06.3.1 — Enums, permissions, spécification

- `OvertimeStatus` ramené à `declaree`, `validee`, `refusee` ; permissions `attendance_corrections`, `overtime`.
- BACKEND SCHEMA §6 et §7, APPFLOW §5.7 (heures sup établies à l'avance) mis à jour.

### W06.3.2 — Corrections

- Migration `attendance_corrections`.
- `App\Services\Tenant\AttendanceCorrectionService::correct(day, in, out, status, reason)` : manager direct (ou délégation), jamais sa propre journée, dans le délai réglé (§4), motif obligatoire ; enregistre les valeurs avant et après, marque la journée `is_corrected`, recalcule minutes, retard et départ anticipé à partir des heures corrigées, recalcule les minutes réalisées des heures sup établies (§4) ; journal ; notification à l'employé.
- Création d'une journée absente du calcul (oubli complet de pointage) par la même correction.

**Critère de fin** : une correction sur un pointage refusé (carte perdue, borne en panne) donne une journée juste ; un manager ne peut corriger ni sa journée ni celle d'une personne hors de son équipe.

### W06.3.3 — Heures sup établies à l'avance

- `OvertimeService` : `establish(employee, date, minutes, ?reason)`, modification et annulation tant que la journée n'est pas passée ; journal ; notification à l'employé. Après la journée, les minutes réalisées (W06.2) sont présentées au RH pour validation.

### W06.3.4 — Écrans

- S-24 `/team` enrichi : présences du jour (présent, en retard, absent, pas encore pointé), pointages refusés à traiter.
- S-33 `/team/attendance` : journées de l'équipe par semaine et par mois, filtre « anomalies » (refus, absences, retards), panneau de correction avec les pointages bruts et leurs motifs de refus.
- S-34 `/team/overtime` : établir des heures sup pour un ou plusieurs membres de l'équipe, suivre les minutes réalisées.
- Barre latérale : groupe « Mon équipe » avec compteurs.

### W06.3.5 — API

- `/api/v1/manager/team/attendance` (journées, anomalies), corrections, `/manager/overtime` (établir, modifier, annuler, suivre).
- Contrat Scramble à jour.

### W06.3.6 — Documentation et livraison

- `02-reference/` : corrections, déclaration des heures sup.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W06.3 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Correction | Motif obligatoire, valeurs avant / après, journée créée, journée corrigée plusieurs fois, correction hors délai refusée, recalcul des heures sup réalisées |
| Heures sup | Établir, modifier, annuler avant la journée ; refus après la journée ; minutes réalisées recalculées après correction |
| Périmètre | Équipe directe, hors équipe, sa propre journée, ses propres heures sup, délégation et exclusion |
| Transitions interdites | Modification d'une heure sup après la journée ; correction sur un employé sorti |
| API | Mêmes refus qu'au web ; autre entreprise |

## 8. Critères de sortie

- Tests ciblés W06.3 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.6 (correction) et §5.7 (déclaration).
- Documentation et livraison de W06.3.6 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Validation des heures sup par le RH | W06.4 |
| Décision du supérieur en l'absence du manager direct | W07 |
| Refus sur période clôturée | W09.6 |
| Écran Équipe dans l'app | E04 |
