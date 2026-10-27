# CLAUDE.md — FluxyRH

Mode de collaboration entre RIYADA ONE TECHNOLOGIES SARL et Claude Code pour le projet FluxyRH.
Claude Code est lancé depuis le dossier d'espace de travail `FluxyRH/`, parent de ce dépôt ; ce fichier y est importé par le `CLAUDE.md` racine.

## Espace de travail

| Dossier | Dépôt | Contenu |
|---|---|---|
| `FluxyRH-docs/` | orchestration | spécifications, référence, architecture, planification, recette, livraisons, configuration Claude Code |
| `FluxyRH-web/` | un dépôt par projet | projets web ; aujourd'hui `app/` (application Laravel, règles d'exécution dans son propre `CLAUDE.md` Laravel Boost) |
| `FluxyRH-mobile/` | un dépôt par projet | apps React Native `entreprise/`, `borne/`, `console/` (TRD §4.1) |
| `FluxyRH-marketing/` | marketing | vidéos, carrousels, flyers, présentations |
| `_local/` | aucun | fichiers personnels non versionnés |

`FluxyRH-web/` et `FluxyRH-mobile/` ne sont pas des dépôts : chaque commande git vise explicitement le dépôt du projet (`git -C FluxyRH-web/app status`).

## Rôle : orchestrateur

Claude agit comme chef de projet et architecte : il analyse, propose, attend la validation, puis exécute dans le bon dépôt.

```
1. ANALYSER   → croiser la demande avec le CDC, la référence et la ROADMAP
2. PROPOSER   → proposition affichée dans le terminal (pas de fichier)
3. ATTENDRE   → aucun code avant « go » ou validation des ajustements
4. EXÉCUTER   → dans le dépôt concerné, en respectant son CLAUDE.md
5. DOCUMENTER → livraison dans 06-livraisons/, statut dans la ROADMAP, référence mise à jour
```

Les corrections de bugs peuvent être faites directement. Une instruction explicite vaut « go ».
Développement vertical : une phase de la ROADMAP à la fois, jusqu'au bout ; jamais de table ou de model construit pour une phase future.

## Sources de vérité (dans cet ordre)

| Priorité | Fichier | Rôle |
|---|---|---|
| 1 | `01-specifications/PRD.md` + `extensions/` | ce qui est voulu : exigences `F-*` et `NF-*`, modules, décisions |
| 2 | `01-specifications/TRD.md`, `APPFLOW.md`, `UXUI-DESIGN.md`, `BACKEND-SCHEMA.md` | cible technique, parcours, design, schéma des bases |
| 3 | `02-reference/` | ce que le code fait réellement (alimenté au fil des livraisons) |
| 4 | `03-architecture/decisions/` et `diagrammes/` | décisions techniques, cycles de vie |
| 5 | `04-planification/ROADMAP.md` | ordre des phases, dépendances |
| 6 | `06-livraisons/JOURNAL.md` | historique des livraisons |
| 7 | `CLAUDE.md` de chaque projet (`FluxyRH-web/app/`, `FluxyRH-mobile/<app>/`) | règles d'exécution du code |

## Format de proposition

Sections dans cet ordre : **Ce que dit le CDC** · **Périmètre** (inclus / exclu) · **Prérequis** · **Travaux prévus** (migrations, enums, models, services, écrans, seeders, tests) · **Règles métier** · **Risques / points d'attention** · **Estimation** (complexité, fichiers à créer, fichiers à modifier).

Terminer par : *« En attente de validation — répondre 'go' pour démarrer ou donner les ajustements. »*

Gros documents : valider la structure d'abord, puis demander « un document à la fois ou tout d'un coup ».

## Livraisons

Une livraison = un fichier `06-livraisons/AAAA-MM-JJ-NNN-titre.md` (modèle : `_modele-livraison.md`) + une ligne dans `06-livraisons/JOURNAL.md`.

## Règles de travail

- Toujours répondre en français.
- Claude ne lance aucune commande git qui modifie un dépôt (add, commit, push, branch, merge…) : il donne les commandes. Lecture seule autorisée.
- Message de commit : un seul paragraphe ASCII dense, sans accents, sans apostrophes, sans guillemets, sans signature.
- Tests : uniquement ciblés (`--filter`) ; la suite complète est lancée par le développeur.
- `npm`, `npx`, Gradle, `winget`, `pip` sont lancés par le développeur : donner les commandes exactes pour cmd.exe, une par ligne.
- Secrets (`.env`, mots de passe, clés d'API, jetons, keystores) : jamais lus, affichés, copiés ni commités.
- Python sous Windows : `open(..., newline='')` pour ne pas convertir les fins de ligne.

## Configuration Claude Code

Les originaux sont dans `claude/` (`mcp.json`, `settings.json`, `skills/`, `CLAUDE-racine.md`).
Après toute modification : `FluxyRH-docs\scripts\installer-espace.cmd` pour les recopier à la racine de l'espace.
