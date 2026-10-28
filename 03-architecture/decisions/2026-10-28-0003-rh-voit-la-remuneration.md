# 0003 — Le RH voit la rémunération, pas la banque

- **Date** : 2026-10-28
- **Statut** : acceptée (modifie le principe P6 du PRD)

## Contexte

Le principe P6 réservait les éléments de rémunération de la paie (rubriques individuelles, bulletins, cumuls, avances, états, masse salariale) au gestionnaire de paie, à la direction et à l'employé concerné ; le RH ne voyait que la rémunération écrite dans le contrat. Or le RH manipule ces informations en permanence (contrats, attestations, variables de paie, suivi des avances, questions des employés) : l'en priver le ralentit sans protéger grand-chose.

## Décision

1. Le RH **voit** toute la rémunération : catégories `remuneration_contractuelle` et `remuneration_paie` (bulletins, rubriques individuelles, cumuls, avances, états de paie, masse salariale).
2. Le RH **ne voit pas** les coordonnées bancaires (`bancaire`), réservées au gestionnaire de paie, à la direction et à l'employé concerné.
3. Le RH **ne saisit pas** les montants de paie : seul le gestionnaire de paie saisit les rubriques individuelles et les montants ponctuels. Le RH continue de rédiger la rémunération du contrat.
4. Le RH accède **en lecture** aux états de paie, aux déclarations, au bilan social et aux analyses et simulations de masse salariale ; ces écrans restent attribués par défaut au gestionnaire de paie et à la direction.
5. L'admin entreprise ne voit **jamais** ni rémunération ni banque ; un manager non plus, même par délégation d'écran.
6. Les montants restent chiffrés en base et chaque consultation d'une rémunération ou d'un bulletin par une autre personne que l'employé reste journalisée.

## Conséquences

- La matrice de `FieldAccess` (TRD §9.1) change : le RH lit `remuneration_paie`, sans l'écrire.
- Les tests de non-fuite portent désormais sur l'admin et le manager pour la rémunération, et sur l'admin, le manager et le RH pour la banque.
- Le RH peut préparer les attestations fondées sur les bulletins.

## Alternatives écartées

- **Le RH voit aussi la banque** : inutile à son travail et donnée la plus exposée à la fraude.
- **Le RH saisit aussi les montants** : supprime la séparation entre celui qui valide les présences et celui qui saisit la rémunération.
