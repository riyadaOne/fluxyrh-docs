# E00 — FluxyRH Entreprise · Amorçage

Dépôt : `FluxyRH-mobile/entreprise/` (fluxyrh-m-entreprise) · Dépend de : W16 (application web complète, API `/api/v1` livrée)

## 1. Objet

Poser le socle de l'application mobile de l'entreprise : projet React Native, organisation du code, thème et composants communs, trois langues avec l'arabe de droite à gauche, client d'API **typé** depuis le contrat Scramble, jeton et cache **chiffrés**, fonctionnement **hors ligne** (consultation et file d'envois), version minimale imposée par le serveur, onglets selon le rôle, les permissions et les modules. **Aucun écran métier** : à la fin d'E00, l'app démarre, affiche l'écran de connexion dans les trois langues, en clair et en sombre, et sait parler à l'API d'une entreprise de démonstration.

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-MOB-03 (socle) | Cache chiffré, file d'envois hors ligne, UUID client |
| F-MOB-05 (version) | Version minimale imposée par le serveur (426) |
| F-MOB-06 | Onglets et boutons des modules non souscrits masqués |
| T-07, T-14, T-15, T-16, T-19 | Trois langues sans texte en dur, types générés du contrat, créations idempotentes, secrets hors dépôt, `npm run check` |
| NF-06, NF-07 | Connectivité faible, multilingue |

À lire : TRD §3.2, §17, §18, §20 ; APPFLOW §3.3, §4, §7 ; UX/UI §4, §7, §10, §11, §12, §17 ; `02-reference/` (API livrée en W02 à W16).

## 3. Prérequis et décisions

- Application web W00 à W16 livrée ; contrat OpenAPI à jour (`php artisan api:contract`).
- Poste du développeur : Node LTS, JDK et Android SDK, un téléphone Android NFC en USB (`adb reverse`), chemin de projet court (piège 12 du TRD §26) ; pour iOS : macOS et Xcode (décision « Build iOS » ci-dessous), un iPhone 7 ou plus récent, un compte Apple Developer.
- Versions des bibliothèques relevées à jour au démarrage, dans la documentation (MCP `context7`).

| Sujet | Proposition |
|---|---|
| Plateformes | **Android et iOS en v1** pour l'app Entreprise ; les apps Borne et Console restent Android (mode kiosque, écriture des cartes). Sur iPhone, la carte est lue par Core NFC (lecture NDEF, iPhone 7 et plus récents) : la feuille système « Approchez votre carte » remplace la zone NFC d'Android. TRD §18 complété pour iOS |
| Build iOS | Le poste de développement est sous Windows, or un build iOS exige macOS et Xcode : **soit un Mac** (achat ou location), **soit un service de build en ligne** pour React Native (Codemagic, Bitrise…). Les deux options restent envisagées ; le choix est fait au démarrage d'E00.1 (coût, délais, disponibilité) |
| Entreprise de l'app | Une app = une entreprise (marque blanche) : l'URL de l'API vient de la configuration du flavor, jamais d'une saisie. Un flavor **`demo`** sert au développement, pointé vers l'entreprise de démonstration ; les flavors des clients sont créés en E10 |
| Rôles avec un espace personnel | Les onglets suivent l'APPFLOW §4 ; les écrans personnels d'un DIR, RH, PAIE, MGR sont regroupés sous l'onglet **Moi** |
| Hors ligne | Consultation : cache de 7 jours, effacé à la déconnexion. Envois en file : pointages, demandes de congé, saisies du dossier, demandes d'avance et de formulaire ; chacun porte un UUID v7 généré par l'appareil, `captured_at` et `sent_at` (T-15). Les validations (RH, manager, direction) exigent le réseau |

## 4. Étapes ordonnées

### E00.1 — Création du projet (développeur)

- Projet React Native CLI (bare), TypeScript strict, dans `FluxyRH-mobile/entreprise/` ; commandes exactes vérifiées dans la documentation au moment de l'étape et données au développeur (cmd.exe).
- Projet iOS : CocoaPods, capacités NFC Tag Reading, Associated Domains, Push Notifications, Face ID, configurées sur le Mac ou le service de build (§3).
- `git init`, dépôt `riyadaOne/fluxyrh-m-entreprise`.
- `CLAUDE.md` du projet : conventions de l'app (organisation, composants, langues, hors ligne, interdits), copiées d'UnivPlus et adaptées.

### E00.2 — Organisation et qualité

- Arborescence `src/app`, `src/shared`, `src/features/<fonctionnalité>`, imports par alias, frontières vérifiées par ESLint (TRD §18.2).
- `npm run check` = `tsc --noEmit` + ESLint + Prettier + Jest (TRD §18.4).
- Jest et React Native Testing Library configurés ; premier test.

### E00.3 — Thème et composants communs

- Tokens UX/UI §4 dans `src/shared/ui/theme.ts` (clair, sombre, système), polices embarquées (Instrument Sans, IBM Plex Sans Arabic, IBM Plex Mono).
- Composants `@shared/ui` (UX/UI §7.1) : `Screen`, `ScreenHeader` (logo de l'entreprise), `AppText`, `Button`, `TextField`, `SearchField`, `Card`, `Badge` (couleurs de statut), `ListItem`, `ListGroup`, `Banner`, `EmptyState`, `ErrorState`, `Loading` (squelettes libellés), `Avatar`, `ChipSelect`, `SegmentedControl`, `CheckboxRow`, `SettingsRow`, `OfflineBanner`, `Icon`, `Logo`, barre d'onglets. Les composants propres au métier (`QrScanner`, `NfcZone`, `SignSheet`, `CountdownButton`…) arrivent avec leurs modules.
- Aucune couleur, taille ni marge en dur : `themed(...)` partout.

### E00.4 — Langues

- i18next, fichiers par fonctionnalité, fr, en, ar ; langue du compte (W02 `/me/locale`), sinon langue de l'appareil, sinon langue officielle de l'entreprise.
- Arabe : `I18nManager` de droite à gauche, redémarrage de l'app au changement de sens.
- Test qui échoue sur une clé manquante ou un texte en dur (TRD §18.4).

### E00.5 — Client d'API typé

- `api:sync` : copie de `openapi.json` produit par le web, génération des types (openapi-typescript), client `openapi-fetch` et hooks `openapi-react-query`.
- En-têtes `X-App-Id: entreprise`, `X-App-Version`, `Accept-Language` ; réponse 426 → écran « Mettre à jour » ; 401 / 403 de session → retour à la connexion avec le message du serveur ; erreurs de validation traduites par le serveur affichées sous les champs.
- Test qui échoue si les types ne correspondent plus au contrat.

### E00.6 — Stockage sécurisé et cache

- Jeton Sanctum dans le Keystore (`react-native-keychain`).
- MMKV chiffré (AES-256, clé dans le Keystore) ; TanStack Query avec persistance sur MMKV, durée de vie 7 jours, effacé à la déconnexion.
- NetInfo branché sur TanStack Query ; `OfflineBanner` « Hors ligne · synchronisé le … à … ».

### E00.7 — File d'envois hors ligne

- `src/shared/offline` : file chiffrée des créations (UUID v7 appareil, `captured_at`, `sent_at` au moment de l'envoi), envoi au retour du réseau dans l'ordre, nouvelles tentatives, réponses rangées en **acceptées** et **refusées avec motif** ; badge sur l'onglet Profil (UX/UI §7.2).
- Utilisée par E02 (dossier), E04 (pointage), E05 (congés), E07 (avances), E09 (formulaires).

### E00.8 — Navigation par rôle

- React Navigation 7 ; onglets construits depuis `/me` (rôle, permissions, modules souscrits, droits par champ) : APPFLOW §4.2 à §4.7 ; **Profil** toujours en dernier ; écrans d'un module non souscrit absents (F-MOB-06).
- Écrans d'attente provisoires pour chaque onglet, remplacés par E01 à E09.

### E00.9 — Environnement de développement

- Flavor `demo` (react-native-config) : URL de l'entreprise de démonstration ; `adb reverse` pour le serveur local ; MCP `metro-mcp` vérifié pour le débogage.
- Procédure d'installation du poste dans `07-exploitation/`.

### E00.10 — Documentation et livraison

- `02-reference/` : architecture de l'app, client d'API, hors ligne.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut E00 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Qualité | `npm run check` vert |
| Langues | Clé manquante, texte en dur, sens de droite à gauche |
| API | Types à jour, en-têtes, 426, 401, erreurs de validation |
| Hors ligne | Mise en file, envoi dans l'ordre, idempotence (même UUID renvoyé), refus motivé rangé |
| Cache | Chiffré, expiré après 7 jours, effacé à la déconnexion |
| Navigation | Onglets par rôle, module non souscrit masqué |

## 6. Critères de sortie

- `npm run check` vert ; l'app `demo` démarre sur un téléphone Android et sur un iPhone, affiche la connexion en fr, en, ar, en clair et en sombre.
- Documentation et livraison d'E00.10 faites.

## 7. Reporté

| Élément | Fichier |
|---|---|
| Connexion, verrouillage, écrans d'administration | E01 |
| Flavors des entreprises clientes, publication | E10 |
