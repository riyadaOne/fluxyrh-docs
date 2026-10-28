# E07 — FluxyRH Entreprise · Paie

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : E06

## 1. Objet

Donner à chacun sa paie dans la poche : **bulletins** et **cumuls annuels**, consultables hors ligne, **accusé de réception** du bulletin ; **avances** (demande et suivi) si l'entreprise les a activées. Pour le PAIE : avances à accepter et état de la période en lecture. Pour la direction : approbation de la période de paie et des avances. Le calcul, le contrôle et la clôture restent au web (UX/UI §7.5).

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PAY-07 | Bulletins publiés, accusé de réception |
| F-EMP-08 | Cumuls annuels |
| F-PAY-10 | Avances : demande, acceptation, approbation |
| F-PAY-05 (mobile) | Approbation de la période par la direction |

À lire : APPFLOW §4.3, §4.5, §5.10, §5.11 ; UX/UI §7.4, §7.5 ; `02-reference/` (W09).

## 3. Prérequis et décisions

E06 livré.

| Sujet | Proposition |
|---|---|
| Bulletins hors ligne | Le PDF des 12 derniers bulletins est conservé dans le stockage **chiffré** de l'app, effacé à la déconnexion |
| Montants | Masqués par défaut (`SensitiveValue`), révélés d'un appui par l'employé lui-même |
| Approbation de la période | Synthèse en lecture et bouton « Approuver » ou « Renvoyer » (motif), sans carte (décision de W09.5) |

## 4. Étapes ordonnées

### E07.1 — Employé

- Onglet **Documents**, bulletins par année (PDF), cumuls annuels, accusé de réception (`SignSheet`).
- Onglet **Demandes**, avances : règles de l'entreprise affichées, demande en file hors ligne, suivi, échéancier.

### E07.2 — PAIE

- Onglet **Validations**, avances à accepter ou refuser ; onglet **Paie**, état de la période en cours (statut, checklist, sans montant détaillé hors droits).

### E07.3 — Direction

- **Approbations** : période de paie (synthèse, approuver, renvoyer), avances acceptées (approuver, refuser).

### E07.4 — Documentation et livraison

- `02-reference/` : écrans de la paie.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E07 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Bulletins | Liste, PDF hors ligne, effacement à la déconnexion, accusé |
| Avances | Politique désactivée, plafond, file hors ligne, circuit complet |
| Direction | Approuver, renvoyer avec motif |
| Confidentialité | Montants masqués par défaut, aucun montant pour un rôle non autorisé |

## 6. Critères de sortie

- `npm run check` vert ; recette APPFLOW §5.10 (approbation, publication, accusé) et §5.11 sur téléphone.
- Documentation et livraison d'E07.4 faites.
