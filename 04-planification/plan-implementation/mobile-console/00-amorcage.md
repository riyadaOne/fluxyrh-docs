# C00 — FluxyRH Console · Amorçage et connexion

Dépôt : `FluxyRH-mobile/console/` (fluxyrh-m-console) · Dépend de : B03

## 1. Objet

Poser l'application interne de RIYADA ONE : même pile et même organisation que les autres apps, connexion des **admins plateforme** sur `platform.fluxyrh.app` (2FA obligatoire en production), onglets Accueil, Cartes, Entreprises, Journal, Profil. À la fin de C00, un admin plateforme se connecte à la Console et voit ses onglets vides.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-PLT-05 (socle de l'app) | App d'encodage des cartes |
| T-19 | `npm run check` |

À lire : APPFLOW §3.6, §4.1 ; UX/UI §9 ; TRD §17.1 (`/platform/*`) ; `02-reference/` (API plateforme W01.8).

## 3. Prérequis et décisions

B03 livré ; un téléphone Android NFC capable d'écrire des cartes NTAG.

| Sujet | Proposition |
|---|---|
| Plateforme | Android seulement (écriture NFC) |
| Distribution | App **interne** : piste de test interne de Google Play réservée aux admins de RIYADA ONE, jamais publique |
| Verrouillage | Biométrie ou code du téléphone obligatoire à chaque ouverture |

## 4. Étapes ordonnées

### C00.1 — Création du projet (développeur)

- Projet React Native CLI (bare), TypeScript strict, Android seulement, dans `FluxyRH-mobile/console/` ; `git init`, dépôt `riyadaOne/fluxyrh-m-console` ; `CLAUDE.md` du projet.
- Organisation, thème, langues, client d'API typé (espace `/platform`), stockage chiffré : repris d'E00.

### C00.2 — Connexion

- Connexion par mot de passe et 2FA (`/platform/login`), verrouillage obligatoire (§3), déconnexion, version minimale (426).

### C00.3 — Documentation et livraison

- `02-reference/` : architecture de la Console.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut C00 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Connexion | Admin plateforme, utilisateur d'entreprise refusé, 2FA, 426 |
| Verrouillage | Demandé à chaque ouverture |

## 6. Critères de sortie

- `npm run check` vert ; connexion d'un admin plateforme sur un téléphone.
- Documentation et livraison de C00.3 faites.
