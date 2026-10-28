# W06.1 — Temps de travail · Paramétrage (ADM, RH)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W05 · Suite : W06.2 (pointage)

## 1. Objet

Poser les règles du temps de travail avant que le premier pointage n'arrive : plannings (jours, horaires, pauses, tolérance de retard) appliqués à une structure, un site ou un employé, jours fériés de l'entreprise, règles d'heures supplémentaires et réglages du pointage. À la fin de W06.1, le système sait dire, pour tout employé et toute date, quel planning s'applique, si le jour est ouvré, férié ou de repos, et quelles majorations s'appliqueraient.

## 2. Ce que l'ADM et le RH reçoivent, produisent, transmettent

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **ADM** | Entreprise configurée (W02), bornes (W03) | Réglages du pointage : pas du code, fenêtre hors ligne, pointage par téléphone | Pointage (W06.2) |
| **RH** | Structure, sites, employés (W03, W04) | Plannings et affectations, jours fériés, règles d'heures sup | Pointage et calculs (W06.2), manager (W06.3), congés (W07), paie (W09) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-TPS-01 | Plannings par structure, site ou employé ; jours fériés |
| F-TPS-06 (règles) | Seuils, majorations par tranche, nuit, repos, jour férié, plafonds |
| F-ORG-02 (fin) | Plannings applicables à un site |

À lire : PRD §7.6 ; TRD §12.1, §12.3, §20 (fuseaux) ; APPFLOW §5.2 (G), §6.3 (S-30, S-31, S-35) ; BACKEND SCHEMA §5.1 (`clocking_settings`), §5.6, §7, §8 ; UX/UI §6.1, §6.2.

## 4. Prérequis et décisions

W05 livré.

| Sujet | Proposition |
|---|---|
| Écran des règles d'heures sup | L'APPFLOW les place dans S-35 « Types de congé et règles d'heures sup » (permission `leave_settings`) : S-35 est créé ici avec l'onglet **Règles d'heures sup** ; l'onglet Types de congé arrive en W07 |
| Jours fériés | **Aucune liste livrée** (décision 0002) : le RH saisit les jours fériés de son pays ; fêtes à date fixe en `is_recurring` ; fêtes à date variable saisies par année, avec un rappel au RH en fin d'année pour celles de l'année suivante |
| Règles d'heures sup | **Aucune règle par défaut** (décision 0002) : le RH saisit celles de sa législation ; tant qu'aucune règle n'existe, aucune heure sup n'est proposée et la liste de démarrage le signale |
| Planning par défaut | Un planning « Standard » (lundi-vendredi, 8 h, 1 h de pause), nommé dans la langue officielle de l'entreprise, créé au provisionnement, **entièrement modifiable** (nom, jours, horaires, pause) ou supprimable, affecté à aucune cible : le RH l'adapte et l'affecte |
| Chevauchement d'affectations | Pour une même cible, deux affectations ne se chevauchent pas : si une nouvelle affectation en chevauche une autre, l'écran le **signale** et demande au RH s'il faut clore la précédente à la veille du début de la nouvelle ; sans confirmation, l'enregistrement est refusé |
| Employé sans planning | Ses journées sont calculées sans attendu (heures travaillées seulement, ni retard ni absence) et signalées au RH |

## 5. Étapes ordonnées

### W06.1.1 — Enums et permissions

- `ScheduleTarget`, `OvertimeKind` ; permissions `work_schedules`, `holidays`, `leave_settings`.

### W06.1.2 — Réglages du pointage

- Migration : ajout à `clocking_settings` de `code_step_seconds` = 30, `offline_window_hours` = 48, `phone_clocking_enabled` = 1, et les réglages de la demi-journée (`half_day_enabled`, `half_day_min_percent`, `full_day_min_percent`), du travail de nuit (`shift_window_before_minutes`, `shift_window_after_minutes`), de la durée du bouton « Inverser » (`direction_inversion_seconds`) du délai de correction des journées (`correction_window_days`) et du nombre maximal de pointages de secours par employé et par mois (`emergency_monthly_limit`), tous ajoutés au BACKEND SCHEMA.
- Onglet **Pointage** de la Configuration (ADM) : pas du code, fenêtre hors ligne, pointage par téléphone autorisé, demi-journée (activation et seuils), fenêtre du travail de nuit, durée du bouton « Inverser », délai de correction des journées, pointages de secours, délai d'alerte d'une borne silencieuse (créé en W03).
- Les bornes reçoivent le pas du code par `/kiosk/config` (W03.6).

### W06.1.3 — Jours fériés

- Migration `holidays` ; `App\Services\Tenant\HolidayService` : jours fériés d'une période (récurrents projetés sur l'année), est-ce un jour férié.
- S-31 `/holidays` : calendrier annuel, ajout, modification, récurrence, corbeille ; rappel au RH en fin d'année pour confirmer les fêtes à date variable de l'année suivante.

### W06.1.4 — Plannings

- Migrations `work_schedules`, `work_schedule_days`, `work_schedule_assignments`.
- `App\Services\Tenant\WorkScheduleService` :
  - création et modification d'un planning (7 jours, horaires, pause, tolérance de retard ; heures hebdomadaires recalculées et contrôlées) ;
  - affectation à une structure, un site ou un employé, avec dates ; une seule cible ; pas de chevauchement (§4) ;
  - `applicableSchedule(employee, date)` : priorité employé > site principal > structure (TRD §12.3), en tenant compte des dates d'effet ;
  - `expectedDay(employee, date)` : ouvré, repos ou férié, horaires attendus, dans le fuseau du site.
- Seeder du planning « Standard ».
- S-30 `/work-schedules` : liste, éditeur de la semaine, affectations par cible avec dates, aperçu « qui suit ce planning », corbeille ; signalement des employés sans planning.

**Critère de fin** : pour le jeu de démonstration, chaque employé a un planning résolu correctement, y compris quand une affectation employé remplace celle de son site à une date donnée.

### W06.1.5 — Règles d'heures supplémentaires

- Migration `overtime_rules`.
- `App\Services\Tenant\OvertimeRuleService` : règles par nature (`jour_ouvre`, `nuit`, `repos_hebdomadaire`, `jour_ferie`), seuils journaliers et hebdomadaires, plage de nuit, plafond hebdomadaire, ordre des tranches ; contrôles de cohérence (tranches sans trou ni chevauchement, plage de nuit valide).
- S-35 `/leave-types`, onglet **Règles d'heures sup**.

**Critère de fin** : une configuration incohérente est refusée avec un message clair ; sans règle d'heures sup, le manager ne peut pas en établir.

### W06.1.6 — Mise en place et API

- Liste de démarrage : réglages du pointage (ADM) ; plannings adaptés et affectés, jours fériés saisis, règles d'heures sup saisies (RH).
- API `/api/v1/employee/schedule` (planning de la semaine et jours fériés, pour l'écran mobile) ; contrat Scramble à jour.

### W06.1.7 — Documentation et livraison

- `02-reference/` : plannings, priorité des affectations, jours fériés, règles d'heures sup.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W06.1 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Plannings | Priorité employé > site > structure ; dates d'effet ; chevauchement signalé, clos sur confirmation, refusé sinon ; employé sans planning ; fuseau du site |
| Jours fériés | Récurrents, à date variable, projection sur l'année, unicité de la date |
| Heures sup | Cohérence des tranches, plage de nuit, plafond ; aucune règle livrée |
| Réglages | Valeurs par défaut, bornes informées du pas |
| Droits | `work_schedules`, `holidays`, `leave_settings`, `configuration` ; délégation ; autre entreprise |

## 7. Critères de sortie

- Tests ciblés W06.1 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.2 (branche G : plannings, jours fériés, règles d'heures sup).
- Documentation et livraison de W06.1.7 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Pointage, calcul des journées, heures sup réalisées | W06.2 |
| Types de congé (onglet de S-35) | W07 |
| Planning dans l'app | E04 |
