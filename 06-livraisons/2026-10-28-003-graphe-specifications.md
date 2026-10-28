# Livraison #003 — Graphe de connaissances des spécifications — 2026-10-28

- **Réf. proposition** : #003 (option B : intégration de graphify dans la configuration versionnée)
- **Réf. CDC** : aucune exigence ; outillage de l'espace de travail
- **Dépôts touchés** : docs

## Fichiers créés

- `scripts/graphify-fusion.py` : relie par une arête `same_as` les copies d'un même concept cité dans plusieurs documents (code de phase, exigence, écran, classe, table, décision), puis recalcule communautés, rapport et `graph.json`. À lancer après chaque mise à jour du graphe.

## Fichiers modifiés

- `claude/CLAUDE-racine.md` : section `graphify` (graphe des spécifications seulement, vérification dans le fichier source, mise à jour proposée et jamais lancée d'office, fusion après mise à jour).
- `.gitignore` : `graphify-out/` (cache d'extraction de graphify, créé dans le dépôt docs).
- `claude/settings.json` : hooks `PreToolUse` de graphify (`graphify hook-guard search` sur Bash et Grep, `graphify hook-guard read` sur Read et Glob, délai 10 s).

## Tests ajoutés

Aucun test automatisé. Vérifications faites :
- chemin W04.3 → W09.6 : aucun avant la fusion, 5 étapes après (via `CompletenessService`) ;
- chemin décision 0004 → `PaymentRecordService` : 2 étapes ;
- hooks lancés à la main sous cmd.exe : code de sortie 0.

## Écarts

- `CLAUDE.md` du dépôt docs lu à 62 lignes sur 70 lors de l'extraction : repris à la prochaine mise à jour du graphe.
- Les noms des communautés sont ceux de leur nœud principal : le regroupement varie d'un calcul à l'autre, des noms écrits à la main se décaleraient.

## Notes pour la suite

- Graphe produit dans `graphify-out/` à la racine de l'espace (non versionné) : 85 fichiers, 1 471 nœuds, 2 258 arêtes ; extraction d'environ 1,36 million de jetons en entrée.
- Graphe du code à envisager quand le code Laravel aura de la matière (après W01).
