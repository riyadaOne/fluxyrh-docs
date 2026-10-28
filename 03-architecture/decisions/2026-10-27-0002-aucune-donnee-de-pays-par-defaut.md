# 0002 — Aucune donnée propre à un pays livrée par défaut

- **Date** : 2026-10-27
- **Statut** : acceptée

## Contexte

Les spécifications prévoyaient de charger à la création de chaque entreprise des données tchadiennes : pré-paramétrage de la paie (CNPS, IRPP, taxes), jours fériés, règles d'heures sup, types de congé, clauses de contrat, liste des banques, plan comptable. Or FluxyRH s'adresse à toute entreprise, qu'elle soit tchadienne, camerounaise, ivoirienne, centrafricaine ou autre.

## Décision

1. Le provisionnement d'une entreprise ne charge **aucune donnée métier propre à un pays** : ni paramétrage de paie, ni jours fériés, ni règles d'heures sup, ni types de congé, ni clauses de contrat, ni liste de banques, ni plan comptable.
2. Chaque entreprise saisit ces données selon sa législation et sa politique ; la **liste de démarrage** de chaque rôle signale ce qui manque.
3. Les seules données créées par le système sont des **valeurs génériques**, toutes modifiables : types système dont le code a besoin (ex. type de document `justificatif_bancaire`), les 9 types d'employé par défaut (désactivables, l'entreprise en ajoute), planning « Standard », et, à l'activation du module Processus RH, ses types d'événements, modèles de workflow et formulaires types.
4. Les jeux d'exemple, dont le paramétrage de paie tchadien de l'annexe 14.3 du PRD, deviennent des **seeders de démonstration et de test**, jamais chargés en production.
5. Les colonnes de l'entreprise (devise, langue officielle, fuseau) n'ont pas de valeur par défaut : elles sont choisies à la création.
6. **Aucun libellé n'est figé dans une langue** : toute donnée créée par le système l'est dans la **langue officielle** de l'entreprise, à partir des fichiers de langue fr, en, ar ; les documents générés sont rédigés dans cette langue. Un changement ultérieur de langue officielle ne retraduit pas les données déjà créées : l'entreprise les modifie.
7. Les dates et heures suivent le **fuseau** de l'entreprise (et celui du site pour le pointage), jamais un fuseau codé.

## Conséquences

- La mise en place d'une entreprise demande plus de saisie ; RIYADA ONE peut l'accompagner, et la liste de démarrage guide chaque rôle.
- Les bulletins dorés (TRD §14.4) reposent sur un paramétrage de test, pas sur des valeurs officielles d'un pays.
- La validation des taux tchadiens par un expert n'est plus un prérequis de la mise en production.

## Alternatives écartées

- **Pré-paramétrage par pays à choisir à la création** : utile, mais demande de maintenir des données légales de plusieurs pays ; pourra être ajouté plus tard comme modèle importable (extension datée).
