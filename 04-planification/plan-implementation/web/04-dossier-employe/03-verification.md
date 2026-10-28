# W04.3 — Dossier employé · Vérification

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W04.2 · Clôt le module W04

## 1. Objet

Rendre les données du dossier **authentiques** : le vérificateur habilité compare la valeur soumise, la valeur précédente et le justificatif, puis vérifie ou rejette ; seule une version vérifiée devient la valeur en vigueur. W04.3 construit aussi la complétude du dossier et ce qu'elle débloque, les relances, les alertes d'expiration des pièces, le dépôt de documents par le RH, et le **centre de notifications** (cloche), utilisé ici pour la première fois. À la fin de W04.3, le cycle complet du dossier fonctionne : invitation → complétion → vérification → dossier complet.

## 2. Ce que les vérificateurs reçoivent, produisent, transmettent

| Rôle | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **RH** | Versions `À vérifier` des employés (hors banque, hors RH) ; pièces | `Vérifiée` / `Rejetée` (motif) ; documents déposés pour l'employé | Employé : valeur en vigueur ou motif à corriger ; tous les modules suivants : données vérifiées |
| **PAIE** | Versions bancaires (hors la sienne) | Banque vérifiée | Paie (W09) : compte en vigueur pour les paiements |
| **DIR** | Données de tout RH (hors banque) ; banque de tout PAIE | Idem | Idem |

Règle absolue : **personne ne vérifie ses propres données** (BACKEND SCHEMA §8).

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-EMP-03 (vérification) | `À vérifier` → `Vérifiée` / `Rejetée`, valeur en vigueur |
| F-EMP-04 | Liste de travail, justificatif à côté de la valeur, comparaison, règles du vérificateur |
| F-EMP-05 (alertes) | Pièces déposées par le RH, alerte avant expiration |
| F-EMP-06 | Taux de complétude par employé et pour l'entreprise |
| F-EMP-09 | Complétude par pièces obligatoires ; blocages réglables (congés, attestations, paiement) ; `isComplete()` utilisé par les modules qui bloquent |
| F-EMP-10 | Relances de l'employé, indicateur pour le RH |
| F-COM-01 (in-app) | Notifications in-app et cloche web (le push est en W10) |
| T-10 | Seule la version vérifiée fait foi |

À lire : PRD §7.4, §11 (risques) ; TRD §10, §19 ; APPFLOW §5.3, §5.4, §6.2 (S-22), §6.5 (S-56), §6.6 (S-81), §7 ; BACKEND SCHEMA §5.1 (`reminder_settings`), §5.4, §5.14 (`notifications`), §8 ; UX/UI §6.4, §6.8, §6.11.

## 4. Prérequis et décisions

W04.2 livré.

| Sujet | Proposition |
|---|---|
| Entreprise sans direction | Les données d'un RH et la banque d'un PAIE n'ont alors aucun vérificateur : elles restent `À vérifier` ; l'admin voit l'étape « nommer une direction » dans la **checklist de configuration de l'entreprise** (liste de démarrage) et reçoit une alerte dans la cloche. L'ADM ne peut jamais vérifier à la place (P6) |
| Pièce obligatoire expirée | Comptée comme **manquante** pour la complétude dès sa date d'expiration ; l'employé est relancé avant l'échéance |
| Vérification groupée | **Non** : chaque demande est vérifiée une par une, avec son justificatif ; l'écran enchaîne sur la demande suivante pour aller vite |
| Boîte des approbations de la direction (S-81) | Créée ici avec son premier type d'élément (vérifications des données des RH et de la banque des PAIE) ; les contrats (W08.3), périodes de paie (W09.5) et avances (W09.7) s'y ajoutent |
| Contenu des notifications | Jamais de valeur : « Votre identité a été vérifiée », « 3 données à vérifier » (TRD §19) |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Version d'un bloc ⟨V⟩ | `a_verifier` → `verifiee` (pointeur `current_*` mis à jour) / `rejetee` (motif) | RH, PAIE, DIR selon la règle ; jamais le propriétaire |
| Pièce | `a_verifier` → `verifiee` / `rejetee` ; expirée à sa date (calculé) | Idem ; SYS |
| Dossier (calculé) | incomplet ⇄ complet | SYS (`CompletenessService`) |

## 6. Étapes ordonnées

### W04.3.1 — Enums et permissions

- Permissions `verifications`, `bank_verifications`, `approvals`.
- APPFLOW §8 (entreprise sans direction, pièce expirée) mis à jour.

### W04.3.2 — Vérification

- `VerifiableDataService::verify()` et `reject(reason)` : vérificateur résolu selon la nature du bloc et le rôle du propriétaire (BACKEND SCHEMA §8), jamais le propriétaire ; en transaction : statut, pointeur `current_*` (vérification), journal ; notification à l'employé.
- Les modules suivants lisent **toujours** la valeur en vigueur : accesseurs `Employee::currentIdentity()` etc. ; le nom affiché passe de l'identité du compte à l'identité vérifiée.
- Test de cohérence des pointeurs (BACKEND SCHEMA §9 point 4).

**Critère de fin** : matrice des vérificateurs testée pour chaque rôle de propriétaire et chaque nature de bloc ; une version rejetée laisse l'ancienne valeur en vigueur.

### W04.3.3 — Listes de travail

- S-22 `/verifications` (RH ; DIR pour les seuls dossiers des RH) et S-56 `/bank-verifications` (PAIE ; DIR pour la banque des PAIE) : versions en attente, filtres bloc, site, structure, ancienneté ; panneau latéral valeur en vigueur | nouvelle valeur (champs modifiés surlignés) | justificatif (aperçu image ou PDF, zoom) ; Vérifier, Rejeter (motif obligatoire), raccourcis clavier, passage automatique à la suivante (UX/UI §6.4).
- S-81 `/approvals` (DIR) : boîte des approbations avec les vérifications qui lui reviennent (UX/UI §6.8).
- Compteur des demandes en attente dans la barre latérale.

**Critère de fin** : un vérificateur ne voit que ce qu'il a le droit de vérifier ; ses propres données n'y figurent jamais ; la banque n'apparaît jamais dans S-22.

### W04.3.4 — Documents déposés par le RH

- Dépôt par le RH des pièces de type `uploaded_by` = `rh` dans la fiche (onglet Documents), visibles ou non de l'employé selon le type ; non soumis à vérification (le RH en est l'auteur).
- L'accusé de réception (avec ou sans carte) est ajouté en W05.

### W04.3.5 — Complétude

- `App\Services\Tenant\CompletenessService` : pièces obligatoires du type d'employé, toutes `verifiee` et non expirées ; `isComplete(employee)`, `missing(employee)`, taux par employé et pour l'entreprise ; calcul à la volée, mis en cache par requête.
- Jauge et pièces manquantes dans l'en-tête de la fiche (UX/UI §6.3), dans S-60 et dans la liste des employés (filtre « incomplet ») ; taux de l'entreprise sur le tableau de bord du RH.
- Migration `incomplete_file_settings` (`block_leave`, `block_forms`, `block_payment`, tous vrais par défaut) et réglage dans l'onglet **Dossier** de S-15 ; décocher un blocage affiche l'explication du risque et demande une confirmation, journalisée (décision 0004).
- `isComplete()` et `blocks(employee, action)` sont **exposés** ici et **appliqués** par les congés (W07), les formulaires types (W12.3) et l'enregistrement des paiements (W09.6).

**Critère de fin** : un dossier devient complet à la vérification de sa dernière pièce obligatoire et redevient incomplet à son expiration.

### W04.3.6 — Notifications in-app

- Migration d'entreprise `notifications`.
- `App\Services\Tenant\NotificationCenterService::send()` : point d'entrée unique (TRD §19), destinataire = rattachement, titre, corps sans valeur sensible, lien ; e-mail associé quand l'événement le prévoit.
- Cloche dans la barre supérieure (compteur, liste, marquer comme lu), page `/notifications`.
- Événements branchés : donnée vérifiée / rejetée (employé), données à vérifier (vérificateurs, regroupées), borne silencieuse (reporté de W03), dépassement de palier (reporté de W04.1), aucune direction active (§4).

**Critère de fin** : chaque événement produit une notification au bon destinataire, sans valeur sensible (test de non-fuite appliqué aux notifications).

### W04.3.7 — Relances et alertes d'expiration

- Migration d'entreprise `reminder_settings` avec `incomplete_file_every_days` et `document_expiry_notice_days` (`contract_end_notice_days` est ajouté en W08.4).
- Onglet **Relances** de la Configuration.
- Tâche planifiée quotidienne : relance des dossiers incomplets (notification et e-mail, selon la fréquence), récapitulatif des demandes en attente aux vérificateurs, alerte avant expiration d'une pièce (employé et RH), journal `logAsSystem`.

**Critère de fin** : avec horloge simulée, chaque relance part une fois à la bonne date, dans la langue officielle.

### W04.3.8 — API

- `/api/v1/hr/verifications` (liste, détail, vérifier, rejeter), `/payroll/bank-verifications`, `/direction/approvals` (vérifications) ; `/employee/completeness` ; `/notifications` (liste, lu).
- Contrat Scramble à jour.

### W04.3.9 — Mise en place, documentation et livraison

- Liste de démarrage de l'admin : présence d'une direction active.
- `02-reference/` : vérification, complétude, notifications, relances.
- `05-recette/` : scénario complet du dossier sur le jeu de démonstration (un employé, un RH, un PAIE, une direction).
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W04.3 (et W04) dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Vérificateur | Employé → RH ; banque → PAIE ; RH → DIR ; banque d'un RH → PAIE ; banque d'un PAIE → DIR ; propriétaire jamais ; entreprise sans direction |
| Vérification | Pointeur mis à jour, rejet avec motif, version rejetée sans effet, transitions interdites (`verifiee` → tout) |
| Non-fuite | Listes, panneau, notifications, journal : aucune valeur bancaire pour RH et ADM |
| Complétude | Pièces obligatoires par type, expiration, taux employé et entreprise, `isComplete()`, blocages réglables avec confirmation du risque |
| Relances | Fréquences, expiration, une seule relance par échéance, langue officielle |
| Notifications | Destinataire, lien, lecture, aucun contenu sensible |
| Droits | Permissions `verifications`, `bank_verifications`, `approvals` ; délégation, exclusion ; autre entreprise ; API |

## 8. Critères de sortie

- Tests ciblés W04.3 verts ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.3 et §5.4 de bout en bout sur le jeu de démonstration.
- Documentation et livraison de W04.3.9 faites ; W04 complet dans la ROADMAP.

## 9. Reporté

| Élément | Module |
|---|---|
| Accusé de réception d'un document | W05 |
| Application des blocages : congés, formulaires, marquage « Payé » | W07, W12.3, W09.6 |
| Notifications push | W10 (serveur), E08 (app) |
| Vérifications dans l'app (RH, PAIE, DIR) | E02 |
