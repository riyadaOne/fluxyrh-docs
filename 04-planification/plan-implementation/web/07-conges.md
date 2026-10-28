# W07 — Congés et absences

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W06

## 1. Objet

Gérer les congés et absences de bout en bout : types paramétrables, demande de l'employé, approbation du manager, validation du RH, annulation, soldes calculés à la volée, calendrier d'équipe, et effet sur les journées de présence. W07 construit aussi la règle « **le supérieur décide en l'absence du manager direct** », qui s'applique désormais à toutes les décisions du manager (congés, corrections, heures sup). Module de taille moyenne : un seul fichier, étapes ordonnées par rôle.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ABS-01 | Types de congé et d'absence : droits, acquisition, justificatif, impact sur la paie |
| F-ABS-02 | `Demandée` → `Approuvée manager` → `Validée` ; `Refusée` à chaque étape ; `Annulée` |
| F-ABS-03 | Jours calculés selon le planning et les jours fériés ; solde calculé à la volée |
| F-ABS-04 | Calendrier d'équipe |
| F-EMP-09 (application) | Pas de demande de congé sur dossier incomplet (selon le type) |
| F-ORG-04 (fin) | Décision du supérieur en l'absence du manager direct |

À lire : PRD §7.7 ; TRD §11 ; APPFLOW §4.6, §4.7, §5.8, §6.3 (S-35, S-36), §7 ; BACKEND SCHEMA §5.7, §6, §8 ; UX/UI §6.1, §6.3.

## 3. Prérequis et décisions

W06 livré.

| Sujet | Proposition |
|---|---|
| Types de congé | **Aucun type livré** (décision 0002) : le RH crée ceux de sa législation et de sa politique ; la liste de démarrage le signale ; le jeu de démonstration en contient pour les tests |
| Acquisition | `annuelle` : droit entier au 1er janvier (au prorata l'année d'embauche) ; `mensuelle` : droit / 12 par mois travaillé révolu ; `aucune` : pas de solde (absences) |
| Solde disponible | Droit acquis + ajustements − jours `validee` − jours en cours (`demandee`, `approuvee_manager`), pour que deux demandes ne consomment pas le même solde |
| Reliquat de l'année précédente | Aucun report automatique (non prévu par les spécifications) : le RH reporte par un ajustement motivé (`leave_allocations`) ; une aide « reporter les reliquats » propose les ajustements en début d'année |
| Employé sans manager | La demande passe directement au RH (`demandee` → `validee` / `refusee`) |
| Congé d'un RH | Validé par un autre RH ou, à défaut, par la direction (boîte S-81), comme ses heures sup (W06.4) |
| Absence du manager | Un manager est **absent** un jour donné s'il a un congé `validee` qui couvre ce jour. Les décisions qui lui reviennent passent alors à son propre manager, en remontant tant que le décideur est absent. La décision reste au manager direct dès son retour pour ce qui est encore en attente |
| Justificatif | Document de type système `justificatif_absence` (non obligatoire au dossier), déposé avec la demande |
| Chevauchement | Refus d'une demande qui chevauche une autre demande en cours ou validée du même employé |
| Annulation d'un congé validé | Par le RH, tant que la période de paie concernée n'est pas clôturée (contrôle ajouté en W09.6) |

## 4. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Demande `leave_requests.status` | `demandee` → `approuvee_manager` → `validee` ; `refusee` (motif) depuis `demandee` ou `approuvee_manager` ; `annulee` depuis `demandee` ou `approuvee_manager` (EMP) ou depuis `validee` (RH) | EMP, MGR (ou son supérieur en son absence), RH |
| Journée | `conge` pour chaque jour décompté d'une demande `validee` ; recalculée à l'annulation | SYS |

## 5. Étapes ordonnées

### W07.1 — Enums, permissions, spécification

- `LeaveCategory`, `LeaveAccrual`, `LeavePayrollImpact`, `LeaveCountBasis`, `LeaveRequestStatus` ; permission `leave_requests` (`leave_settings` existe depuis W06.1).
- APPFLOW §5.8 et §8 (absence du manager, employé sans manager, congé d'un RH) mis à jour.

### W07.2 — Paramétrage (RH)

- Migrations `leave_types`, `leave_allocations`.
- Type de document système `justificatif_absence` créé au provisionnement (donnée technique) ; commande de rattrapage pour les entreprises existantes ; liste de démarrage du RH : créer les types de congé.
- S-35 `/leave-types`, onglet **Types de congé** : droits, acquisition, justificatif requis, impact sur la paie, base de décompte, durée maximale consécutive, dossier complet exigé ; corbeille.
- Ajustements par employé (fiche S-21, onglet Congés) avec motif ; aide au report des reliquats.

### W07.3 — Calculs

- `App\Services\Tenant\LeaveService` :
  - `countDays(employee, type, start, end, halfDays)` : jours ouvrés du planning de l'employé (W06.1) hors jours fériés, ou jours calendaires selon le type ; demi-journées ;
  - `balance(employee, type, date)` : à la volée (§3), jamais stocké ;
  - contrôles de demande : dossier complet si l'entreprise bloque les congés et si le type l'exige (`CompletenessService::blocks()`), solde suffisant, justificatif, durée maximale, chevauchement, employé `actif`.

**Critère de fin** : jeu de cas (semaine avec jour férié, demi-journées, planning à temps partiel, jours calendaires, embauche en cours d'année, acquisition mensuelle) calculé exactement.

### W07.4 — Absence du manager et décideur

- `TeamScope::decisionMaker(employee, date)` : manager direct, ou premier supérieur présent (§3) ; sans manager : RH.
- Branchement sur toutes les décisions du manager : approbation de congé (W07), corrections de journée (W06.3), heures sup établies à l'avance (W06.3), validation des pointages de secours (W06.3) ; le supérieur voit les éléments de l'équipe de son subordonné absent dans ses propres écrans, signalés « en remplacement de… ».

**Critère de fin** : un manager en congé ne reçoit plus de décisions ; son supérieur les reçoit pendant l'absence ; au retour, ce qui reste en attente revient au manager direct.

### W07.5 — Demande et annulation (employé)

- Migration `leave_requests` (avec `client_uuid`).
- `LeaveService::request()` (idempotent par `client_uuid`), `cancel()` ; notification au décideur.
- S-64 `/me/leave` : soldes par type, demande (type, dates, demi-journées, motif, justificatif) avec calcul des jours en direct et contrôles expliqués (pièces manquantes, solde), historique, annulation.

### W07.6 — Approbation (manager)

- `LeaveService::approveByManager()`, `refuseByManager(reason)` : décideur (W07.4), jamais sa propre demande.
- S-36 `/leave-requests` côté manager (aussi sous `/team`) : demandes à décider avec le solde, le calendrier de l'équipe sur la période et les autres absents ce jour-là ; sélection multiple « Approuver la sélection » (décision 0004).
- Calendrier d'équipe (F-ABS-04) dans S-24 : absences prévues et validées de l'équipe directe et indirecte, par semaine et par mois.

### W07.7 — Validation (RH)

- `LeaveService::validate()`, `refuseByHr(reason)`, `cancelValidated(reason)` : RH, jamais sa propre demande (§3).
- Effet de la validation : journées concernées passées en `conge` (recalcul W06.2, l'absence est remplacée), solde à jour ; l'impact « non payé » devient une variable de paie en W09.3.
- S-36 côté RH : demandes approuvées par les managers (et demandes des employés sans manager), filtres, validation groupée ; calendrier de l'entreprise.
- Élément « congé d'un RH » dans la boîte S-81 de la direction.

**Critère de fin** : APPFLOW §5.8 recetté de bout en bout ; une annulation par le RH rend les jours au solde et recalcule les journées.

### W07.8 — API

- `/api/v1/employee/leave` (types, soldes, demandes, création idempotente, annulation), `/manager/leave-requests` (décider, calendrier), `/hr/leave-requests` (valider, refuser, annuler) ; contrôle définitif du solde par le serveur même pour une demande envoyée hors ligne.
- Contrat Scramble à jour.

### W07.9 — Documentation et livraison

- `02-reference/` : types, calculs, soldes, décideur en cas d'absence.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W07 dans la ROADMAP.

## 6. Tests attendus

| Domaine | Cas |
|---|---|
| Calculs | Jeu de cas de W07.3 ; solde avec demandes en cours ; ajustements |
| Contrôles | Dossier incomplet (type qui l'exige ou non), solde insuffisant, justificatif manquant, durée maximale, chevauchement, employé sorti |
| Circuit | Chaque transition ; transitions interdites (`validee` → `refusee`, annulation par un tiers…) ; employé sans manager ; congé d'un manager, d'un RH |
| Absence du manager | Remontée d'un niveau, de deux niveaux, retour du manager |
| Effets | Journées `conge`, annulation, recalcul |
| Idempotence | Même `client_uuid` envoyé deux fois |
| Droits | `leave_settings`, `leave_requests` ; périmètre d'équipe ; délégation, exclusion ; autre entreprise ; API |

## 7. Critères de sortie

- Tests ciblés W07 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.8 sur le jeu de démonstration, y compris un manager en congé.
- Documentation et livraison de W07.9 faites.

## 8. Reporté

| Élément | Module |
|---|---|
| Congé non payé en variable de paie | W09.3 |
| Refus d'annulation sur période clôturée | W09.6 |
| Rapports d'absentéisme | W13 |
| Demandes et approbations dans l'app | E05 |
