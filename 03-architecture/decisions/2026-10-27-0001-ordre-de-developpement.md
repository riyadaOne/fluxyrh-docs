# 0001 — Ordre de développement : web complet, puis Entreprise, Borne, Console

- **Date** : 2026-10-27
- **Statut** : acceptée

## Contexte

Le PRD §8.5 prévoyait un développement domaine par domaine, les écrans mobiles d'un domaine étant développés dans la même phase que ses écrans web. FluxyRH compte une application web (Laravel, web et API) et trois applications React Native (Entreprise, Borne, Console). Dans FluxyRH, les données circulent d'un rôle à l'autre par changement de statut (dossier, congé, contrat, période de paie…), ce qui rend certains modules volumineux.

## Décision

1. L'**application web complète** est développée d'abord : écrans Livewire **et API `/api/v1`** de chaque module, avec leurs tests.
2. Viennent ensuite les applications mobiles, dans cet ordre : **FluxyRH Entreprise**, **FluxyRH Borne**, **FluxyRH Console**, puis la mise en production.
3. Chaque application est découpée **module par module**, un fichier de plan par module, dans l'ordre des dépendances ; un module est terminé avant de passer au suivant.
4. Un module volumineux est découpé **par rôle**, dans l'ordre où la donnée circule d'un rôle au suivant.

Le détail est dans `04-planification/plan-implementation/`.

## Conséquences

- Les phases mobiles ne construisent que les écrans, le hors ligne et le natif : le serveur, l'API et le contrat Scramble sont déjà livrés et testés.
- Les fonctions qui exigent une carte NFC ou un téléphone (activation de carte, pointage QR + carte, signature d'un contrat, accusé de bulletin, push) sont testées par PHPUnit sur l'API pendant la phase web, mais **recettées sur le terrain** seulement dans les phases mobiles.
- La Console arrivant en dernier, une commande de développement crée des cartes de test (W05) écrites avec une application NFC générique.
- Le retour des utilisateurs sur le pointage, cœur de l'usage, arrive après tout le web.

## Alternatives écartées

- **Web et mobile d'un même domaine dans la même phase** (PRD §8.5 initial) : multiplie les changements de contexte entre dépôts et oblige à faire évoluer trois apps à chaque module.
- **Console avant Borne** : permettrait d'encoder de vraies cartes plus tôt, mais retarde l'app Entreprise et la Borne, plus utiles à la recette ; les cartes de test suffisent.
