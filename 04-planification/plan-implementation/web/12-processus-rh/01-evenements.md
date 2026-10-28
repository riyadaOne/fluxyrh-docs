# W12.1 — Processus RH · Événements (MGR propose, RH décide)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W11 · Module payant `processus_rh` · Suite : W12.2 (workflows)

## 1. Objet

Tracer la carrière dans le dossier par des **événements datés** (promotion, mutation, augmentation, sanction, avertissement, félicitation…), de types paramétrables : le manager propose, le RH valide ou refuse, et un événement validé **applique son effet** à la date d'effet (poste, structure, site, manager, type d'employé) en mettant à jour l'historique d'affectation. À la fin de W12.1, toute modification d'affectation passe par un événement motivé et daté.

## 2. Ce que chacun reçoit, produit, transmet

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **MGR** | Son équipe (W04.1) | Événement `Proposé` | RH |
| **RH** | Propositions ; ses propres saisies | Événement `Validé` / `Refusé` ; document joint | **SYS** : effet à la date ; **workflows** (W12.2) : mutation ; employé : notification |
| **SYS** | Événements validés | Dossier et historique d'affectation mis à jour | Équipes, organigramme, paie (type d'employé) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PRO-01 | Événements datés, types paramétrables, `Proposé` → `Validé` / `Refusé`, mise à jour du dossier |

À lire : PRD §7.11 ; APPFLOW §4.6, §5.12, §6.7 (S-71) ; BACKEND SCHEMA §5.3 (`employee_position_history.hr_event_id`), §5.11, §6, §7 (`HrEventCategory`, `HrEventEffect`, `HrEventStatus`).

## 4. Prérequis et décisions

W11 livré (pour l'ordre ; W12 ne dépend fonctionnellement que de W04 et W08).

| Sujet | Proposition |
|---|---|
| Types par défaut | Créés à l'activation du module, **libellés dans la langue officielle** de l'entreprise (fichiers de langue), modifiables et désactivables : promotion (poste), mutation (structure, site, manager), changement de type (type), augmentation (aucun effet direct), avertissement, blâme, mise à pied, félicitation (aucun effet) |
| Augmentation | Le salaire vit dans le contrat (W08) : un événement « augmentation » validé **propose au RH de rédiger l'avenant** (W08.4) ; il ne modifie aucun montant |
| Événement créé par le RH | Validé à la création (le RH est le décideur) ; journalisé comme tel |
| Date d'effet | Future : effet appliqué par une tâche planifiée à la date ; passée : appliquée immédiatement, mais jamais avant la fin de la dernière période de paie **clôturée** de l'employé |
| Variables de paie des événements | `PayrollVariableSource` prévoit `evenement`, mais aucun type d'événement ne définit de quantité (ex. jours de mise à pied). **Proposition : pas de variable d'événement en v1** ; une mise à pied non payée passe par une absence (W07). À confirmer |
| Visibilité | Événements validés visibles par l'employé concerné, le RH, la direction et le manager de son équipe ; propositions visibles du proposant et du RH |
| Interdits | Personne ne propose ni ne valide un événement sur soi-même |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Événement `hr_events.status` | `propose` → `valide` / `refuse` (motif) ; création directe en `valide` par le RH | MGR (ou supérieur en son absence) ; RH |
| Effet | en attente → appliqué (à la date d'effet) | SYS |

## 6. Étapes ordonnées

### W12.1.1 — Enums, permissions, module

- `HrEventCategory`, `HrEventEffect`, `HrEventStatus` ; permission `hr_events` liée au module `processus_rh`.

### W12.1.2 — Données et types

- Migrations `hr_event_types`, `hr_events` ; `hr_event_id` ajouté à `employee_position_history` (prévu au BACKEND SCHEMA).
- Types par défaut créés à l'activation du module dans la langue officielle ; S-71, onglet Types : libellé, catégorie, effet, corbeille.

### W12.1.3 — Service

- `App\Services\Tenant\HrEventService` : `propose()` (manager décideur, W07.4), `createByHr()`, `validate()`, `refuse(reason)`, `applyEffect(event)` (en transaction : champs de `employees`, ligne d'historique d'affectation, sites de pointage si le site principal change, journal) ; tâche planifiée des effets du jour ; contrôles de date (§4) ; notification à l'employé et au manager.
- Changement de manager et de structure par le RH (W04.1.5) : passent désormais par un événement quand le module est souscrit ; sans le module, l'édition directe de W04.1 reste.

### W12.1.4 — Écrans

- S-71 `/team/hr-events` (MGR) : proposer pour un membre de l'équipe, suivre ses propositions.
- S-71 `/hr-events` (RH) : propositions à décider, création directe, liste par employé, type, statut, date ; document joint (lettre) déposé comme pièce RH.
- Fiche S-21 : onglet **Événements** ; « Mon dossier » : événements validés de la personne.

### W12.1.5 — API et documentation

- `/api/v1/manager/hr-events`, `/hr/hr-events`, `/employee/hr-events`.
- `02-reference/` : événements, effets, dates ; article d'aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W12.1 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Circuit | Proposer, valider, refuser, création directe ; transitions interdites ; soi-même |
| Effets | Chaque effet appliqué ; date future (tâche), passée, antérieure à une paie clôturée (refus) ; historique d'affectation ; équipes recalculées |
| Augmentation | Invitation à rédiger l'avenant, aucun montant modifié |
| Visibilité | Employé, manager, RH, direction ; propositions privées |
| Module | Fermé sans le module ; édition directe de W04.1 conservée sans le module |
| Droits | `hr_events` ; périmètre d'équipe ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W12.1 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.12 (partie événements).
- Documentation et livraison de W12.1.5 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Workflow de mutation déclenché par l'événement | W12.2 |
| Parcours de carrière | W15 |
| Proposition d'événement dans l'app | E09 |
