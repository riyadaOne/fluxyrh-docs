# W13 — Module Pilotage

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W12 · Module payant `pilotage`

## 1. Objet

Donner aux décideurs leurs outils de lecture : **tableaux de bord à widgets** par rôle et personnalisables, **rapports standard** (effectifs, présences, absences, heures sup, paie, contrats, turnover, événements) avec filtres et exports, **états personnalisés** (champs, filtres, regroupements, sauvegarde, partage) et **accès externe aux données** par jetons d'intégration. Tout respecte `FieldAccess` : un widget, un rapport ou un jeu de données n'affiche jamais un champ sensible à qui n'y a pas droit (P6). À la fin de W13, la direction pilote l'entreprise sans export manuel.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PIL-01 | Tableaux de bord par rôle, widgets personnalisables |
| F-PIL-02 | Rapports standard, filtres, export |
| F-PIL-03 | États personnalisés, sauvegarde, partage |
| F-PIL-04 | Accès externe aux données, respectant P6 |

À lire : PRD §7.15 ; TRD §9.2, §9.3, §16.4, §17.1 (`/data/*`) ; APPFLOW §4.3, §6.6 (S-80, S-84, S-86) ; BACKEND SCHEMA §5.15 (widgets, rapports, jetons), §7 (`ReportDataset`), §9 (point 6) ; UX/UI §6.10.

## 3. Prérequis et décisions

W12 livré. Paquet installé par le développeur : ApexCharts (npm).

| Sujet | Proposition |
|---|---|
| Catalogue des widgets | **Aussi large que possible** : au moins un indicateur et un graphique par domaine du socle et de chaque module souscrit (organisation, dossiers et complétude, cartes, temps et pointage, heures sup, congés, contrats et échéances, paie et masse salariale, avances, communication, processus RH, talents, conformité), filtrés par `FieldAccess` ; défauts par rôle ; liste détaillée établie au démarrage de W13 |
| Jeux de données | `effectifs`, `presences`, `absences`, `heures_sup`, `paie`, `contrats`, `evenements` ; chacun avec sa liste **fermée** de champs, chaque champ portant sa catégorie sensible éventuelle |
| Colonnes chiffrées | Filtres, tris et agrégats sur un champ chiffré faits en PHP après déchiffrement (TRD §9.3) ; un état personnalisé est limité à 10 000 lignes avant agrégation, au-delà l'utilisateur affine ses filtres |
| Partage d'un état | Partagé = visible des personnes qui ont la permission `reports` ; chacun ne voit que les colonnes qu'il a le droit de lire |
| Jetons d'intégration | S-86 ouvert à l'ADM pour les jeux de données sans champ sensible ; les jeux sensibles exigent un jeton créé par le PAIE ou la direction (TRD §16.4). Les droits sont réévalués **à chaque appel** avec ceux du créateur : s'il perd ses droits, le jeton les perd |
| Export planifié | F-PIL-04 laisse le choix entre API de lecture et export planifié : **API de lecture seulement** en v1, plus l'export manuel des rapports |

## 4. Étapes ordonnées

### W13.1 — Enums, permissions, module

- `ReportDataset`, `DashboardWidget` ; permissions `reports`, `integrations` liées au module `pilotage` ; le tableau de bord à widgets remplace l'accueil « À faire » quand le module est souscrit (l'accueil du socle reste sinon, W10.4).

### W13.2 — Tableaux de bord

- Migration `dashboard_widget_selections`.
- `App\Services\Reporting\DashboardWidgetService` : catalogue (§3), défauts par rôle, calcul des valeurs dans le périmètre de l'utilisateur (équipe pour un manager), `FieldAccess` ; mise en cache courte.
- S-80 `/dashboard` : widgets choisis, ordonnés, type de graphique (ApexCharts, gamme `zinc`, UX/UI §6.10).

### W13.3 — Rapports standard

- `App\Services\Reporting\ReportingService` : un rapport par jeu de données avec ses filtres (période, structure, site, type, statut) et ses regroupements ; turnover (entrées, sorties, effectif moyen).
- S-84 `/reports` : choix du rapport, filtres, tableau et graphique, export XLSX, CSV, PDF ; exports journalisés.

### W13.4 — États personnalisés

- Migrations `custom_reports`, `custom_report_columns`, `custom_report_filters`.
- `App\Services\Reporting\CustomReportService` : jeu de données, colonnes choisies dans la liste fermée (§3), filtres, regroupements, agrégats ; sauvegarde, partage, exécution et export ; refus d'un champ sensible non autorisé à l'enregistrement, masquage à l'exécution.
- S-84, onglet États personnalisés.

### W13.5 — Accès externe aux données

- Migrations `integration_tokens`, `integration_token_datasets`.
- S-86 `/integrations` : création d'un jeton (jeux de données, expiration), affichage du secret **une seule fois**, révocation, dernière utilisation.
- API `/api/v1/data/{dataset}` : ability `data:read`, jeux autorisés du jeton, pagination, filtres de date, droits du créateur réévalués (§3), limite de débit, journal des appels.

### W13.6 — Documentation et livraison

- `02-reference/` : widgets, rapports, états, API de données (documentation destinée aux intégrateurs) ; article d'aide.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W13 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Widgets | Défauts par rôle, personnalisation, périmètre du manager, widget de rémunération absent pour ADM et MGR, aucune donnée bancaire dans un widget |
| Rapports | Exactitude sur le jeu de démonstration (effectifs, turnover, absentéisme, heures sup, masse salariale), filtres, exports |
| États | Colonnes fermées, champ sensible refusé ou masqué, partage, limite de lignes |
| Jetons | Secret affiché une fois, révocation, expiration, jeu non autorisé, jeu sensible créé par l'ADM refusé, créateur ayant perdu ses droits |
| Non-fuite | Suite complète sur widgets, rapports, états, exports et API de données |
| Module | Tout est fermé sans le module ; l'accueil du socle revient |
| Droits | `reports`, `integrations` ; autre entreprise |

## 6. Critères de sortie

- Tests ciblés W13 verts, dont la non-fuite ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Rapports vérifiés à la main sur le jeu de démonstration.
- Documentation et livraison de W13.6 faites.

## 7. Reporté

| Élément | Module |
|---|---|
| Analyses et simulations de la masse salariale | W14 |
| Accueil à indicateurs dans l'app | E09 |
| Export planifié vers un outil externe | Évolution future (extension datée) |
