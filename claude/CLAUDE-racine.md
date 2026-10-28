@FluxyRH-docs/CLAUDE.md

## graphify

Un graphe de connaissances des **spécifications** (`FluxyRH-docs/` : PRD, TRD, APPFLOW, BACKEND SCHEMA, UX/UI, décisions, plan, ROADMAP) est dans `graphify-out/` à la racine de l'espace (non versionné).

- Question sur les spécifications, le plan, les décisions ou les dépendances entre phases : interroger d'abord le graphe (`graphify query "..."`, `graphify path "A" "B" --undirected`, `graphify explain "X"`), puis **vérifier dans le fichier source** avant d'affirmer : les liens `INFERRED` et `same_as` sont déduits.
- Le code (`FluxyRH-web/`, `FluxyRH-mobile/`) n'est **pas** dans le graphe : pour le code, lire les fichiers.
- Après une modification de `FluxyRH-docs/`, ne pas reconstruire le graphe de soi-même (l'extraction coûte des jetons) : le proposer. Mise à jour, depuis la racine de l'espace : `/graphify FluxyRH-docs --update`, puis `python FluxyRH-docs/scripts/graphify-fusion.py` avec l'interpréteur de graphify (chemin dans `graphify-out/.graphify_python`), puis `graphify export html`. Sans la fusion, les concepts cités dans plusieurs documents ne sont plus reliés.
