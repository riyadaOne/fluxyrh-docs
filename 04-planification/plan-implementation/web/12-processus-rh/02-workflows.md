# W12.2 — Processus RH · Workflows d'entrée, de sortie, de mutation

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W12.1 · Module payant `processus_rh` · Suite : W12.3 (courriers et formulaires)

## 1. Objet

Organiser les moments clés de la vie d'un employé par des **listes de tâches par acteur**, avec échéances, e-mails et notifications : **entrée** (après l'acceptation de l'invitation), **sortie** (à la déclaration de sortie) et **mutation** (à la validation d'un événement de mutation). Les modèles de workflow sont paramétrables ; chaque instance suit ses tâches jusqu'à son terme. À la fin de W12.2, une entrée, une sortie ou une mutation **propose** au RH de lancer le workflow correspondant ; une fois lancé, chaque tâche arrive chez la bonne personne.

## 2. Ce que chacun reçoit, produit, transmet

| Acteur | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **RH** | — | Modèles de workflow (tâches, rôle assigné, échéance, e-mail) | SYS |
| **SYS** | Invitation acceptée (W04.1), sortie déclarée (W04.1.7, W08.4), événement de mutation validé (W12.1) | **Proposition** de lancer le workflow (notification et tâche en attente du RH) | RH |
| **RH** | Proposition | Workflow lancé (ou écarté, avec motif) : instance et tâches datées, assignées | Acteurs |
| **Acteurs** (RH, PAIE, DIR, ADM, manager de l'employé) | Leurs tâches | Tâches `faite` / `ignoree` (note) | SYS : instance `terminee` |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PRO-02 | Workflows d'entrée, de sortie, de mutation : tâches par acteur, échéances, e-mails, notifications |
| F-EMP-07 (avec le module) | Sortie accompagnée d'un workflow |

À lire : PRD §7.11 ; APPFLOW §5.12, §6.7 (S-72) ; BACKEND SCHEMA §5.11 (workflows), §6, §7 (`WorkflowKind`, `WorkflowStatus`, `TaskStatus`).

## 4. Prérequis et décisions

W12.1 livré.

| Sujet | Proposition |
|---|---|
| Rôles assignables | `rh`, `gestionnaire_paie`, `direction`, `admin_entreprise`, `manager` (le manager de l'employé concerné) ; une tâche de l'employé concerné (ex. restituer du matériel) est confiée à son manager |
| Tâche d'un rôle collectif | Pour `rh`, `gestionnaire_paie`, `direction`, `admin_entreprise` : tâche visible de toutes les personnes du rôle, **prise en charge** par l'une d'elles (`assignee`) ou faite directement. Le RH peut **exclure** une ou plusieurs personnes d'une tâche (table `workflow_task_exclusions`, ajoutée au BACKEND SCHEMA) ; l'employé concerné en est toujours exclu automatiquement (ex. un RH qui quitte l'entreprise ne traite pas sa propre sortie) |
| Échéance | `due_offset_days` relatif à la date d'ancrage : date d'embauche (entrée), date de sortie (sortie), date d'effet de l'événement (mutation) ; négatif permis (avant la date) |
| Modèle par défaut | Créé à l'activation du module, **tâches libellées dans la langue officielle** de l'entreprise, modifiable : entrée (accès, matériel, préparation de la carte, contrat, affiliation CNPS), sortie (restitution du matériel, désactivation des accès, solde de tout compte, certificat de travail), mutation (matériel, accès, nouveau site de pointage) |
| Un modèle par nature | Un seul modèle **actif** par nature ; pas de proposition si aucun modèle actif |
| Lancement | **Jamais automatique** : à chaque entrée, sortie ou mutation, le système **notifie le RH et propose** de lancer le workflow ; le RH le lance (date d'ancrage modifiable) ou l'écarte avec un motif. Une proposition non traitée reste dans ses tâches en attente |
| Annulation | Annulation d'une sortie (W04.1.7) ou d'un événement non encore appliqué → instance `annulee` |
| Actions automatiques | Les tâches restent manuelles ; ce que le système fait déjà seul (désactivation de la carte, révocation du rattachement à la date de sortie) n'est pas une tâche |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Instance `workflow_instances.status` | `en_cours` → `termine` (toutes les tâches `faite` ou `ignoree`) / `annule` | SYS |
| Tâche `workflow_tasks.status` | `a_faire` → `faite` / `ignoree` (note obligatoire) | Acteur assigné |

## 6. Étapes ordonnées

### W12.2.1 — Enums et permissions

- `WorkflowKind`, `WorkflowStatus`, `TaskStatus` ; permission `workflows` liée au module.

### W12.2.2 — Modèles

- Migrations `workflow_templates`, `workflow_template_tasks`.
- Modèles par défaut (§4) créés à l'activation du module dans la langue officielle.
- S-72 `/workflows`, onglet Modèles : tâches ordonnées, rôle, échéance relative, e-mail ; activation (un actif par nature).

### W12.2.3 — Instances et tâches

- Migrations `workflow_instances`, `workflow_tasks`.
- `App\Services\Tenant\WorkflowService` : `start(kind, employee, anchorDate, ?event)` (copie des tâches du modèle actif, échéances calculées), `take(task)`, `exclude(task, person)`, `complete(task, note)`, `skip(task, note)`, `cancel(instance)` ; terminaison automatique ; journal.
- Propositions de lancement (§4) : acceptation d'une invitation (W04.1.4), déclaration de sortie et résiliation (W04.1.7, W08.4), validation d'un événement à effet de mutation (W12.1) ; `propose()`, `launch(proposal, anchorDate)`, `dismiss(proposal, reason)` ; annulations (§4).
- Notifications et e-mails à la création des tâches ; rappel des tâches en retard (tâche planifiée quotidienne).

### W12.2.4 — Écrans

- S-72 `/workflows` (RH) : instances en cours par nature, avancement, tâches en retard ; détail d'une instance.
- « Mes tâches » dans l'accueil de chaque rôle (W10.4) : tâches de workflow assignées ou de son rôle.
- Fiche S-21 : onglet **Workflows**.

### W12.2.5 — API et documentation

- `/api/v1/{espace}/workflow-tasks` (mes tâches, prendre, faire, ignorer), `/hr/workflows`.
- `02-reference/` : workflows ; article d'aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W12.2 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Propositions | Entrée, sortie (déclaration et résiliation), mutation proposées au RH sans lancement automatique ; lancement, écart motivé ; aucun modèle actif ; module non souscrit (aucune proposition, sortie directe conservée) |
| Tâches | Rôles collectifs, prise en charge, manager concerné, exclusion manuelle et exclusion automatique de l'employé concerné, échéances relatives, note obligatoire pour ignorer |
| Instances | Terminaison automatique, annulation |
| Rappels | Tâches en retard, une relance par jour |
| Droits | Un acteur ne voit que ses tâches et celles de son rôle ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W12.2 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.12 (workflows d'entrée, de sortie, de mutation).
- Documentation et livraison de W12.2.5 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Tâches dans l'app | E09 |
