# FluxyRH — documentation et orchestration

Dépôt d'orchestration du projet FluxyRH (créé le 2026-10-27).

| Dossier | Contenu |
|---|---|
| `00-cadrage/` | note de cadrage, contexte client, périmètre initial, glossaire |
| `01-specifications/` | `CDC.md` (référence fonctionnelle) et `extensions/` (un fichier daté par évolution) |
| `02-reference/` | PRD, TRD, APPFLOW, UX/UI DESIGN, BACKEND SCHEMA : ce que le code fait réellement |
| `03-architecture/` | `decisions/` (une décision par fichier) et `diagrammes/` |
| `04-planification/` | `ROADMAP.md`, plans d'implémentation |
| `05-recette/` | cahier de recette, scénarios de test, comptes de démonstration |
| `06-livraisons/` | `JOURNAL.md` (index) et un fichier par livraison |
| `07-exploitation/` | déploiement, serveurs, sauvegardes, procédures d'incident |
| `08-commercial/` | offres, grilles tarifaires, présentations client, FAQ |
| `assets/` | images légères utilisées par les documents |
| `archive/` | anciennes versions et documents abandonnés |
| `claude/` | originaux de la configuration Claude Code de l'espace |
| `scripts/` | scripts d'outillage (`installer-espace.cmd`) |

## Règles

- Pas de `_v1`, `_v2` dans les noms : git garde l'historique.
- On n'efface pas un document, on le déplace dans `archive/`.
- Une extension, une décision ou une livraison = un fichier daté (`AAAA-MM-JJ-titre.md`).
- Noms en minuscules avec des tirets.
- Pas de binaires lourds (vidéos, exports) : ils vont dans `FluxyRH-marketing` ou `_local`.
