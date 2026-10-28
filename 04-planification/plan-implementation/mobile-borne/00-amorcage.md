# B00 — FluxyRH Borne · Amorçage

Dépôt : `FluxyRH-mobile/borne/` (fluxyrh-m-borne) · Dépend de : E10

## 1. Objet

Poser le socle de l'application **Borne**, une app unique (une seule fiche store) installée sur un appareil Android NFC **fourni par l'entreprise** et fixé sur un site : même pile et même organisation que l'app Entreprise, **thème clair forcé** et tailles lisibles à 1,5 m, **mode kiosque**, écran toujours allumé, redémarrage automatique, sortie protégée par un code admin. À la fin de B00, l'app démarre en mode kiosque sur une tablette et affiche l'écran « Borne non appairée ».

## 2. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-ORG-03 | Appareil fourni par l'entreprise, app en mode borne |
| T-19 | `npm run check` |

À lire : TRD §3.2, §12.5, §18 ; UX/UI §4, §8 ; APPFLOW §4.8 ; `CLAUDE.md` et code commun de l'app Entreprise (E00), recopié ici (TRD §4.1 : pas de bibliothèque commune).

## 3. Prérequis et décisions

E10 livré ; une tablette ou un téléphone Android NFC de test.

| Sujet | Proposition |
|---|---|
| Version Android minimale | **La plus basse version qui prend en charge toutes les fonctions** de la borne : clés matérielles ECDSA P-256 et RSA-OAEP dans le Keystore, NFC, mode kiosque « propriétaire de l'appareil », caméra. Vérifiée dans la documentation au démarrage de B00 (Android 8.0 attendu) et publiée dans la procédure d'achat des tablettes |
| Verrouillage de l'appareil | **Retenu** : l'app devient « propriétaire de l'appareil » (Device Owner) à l'installation, par une commande `adb` donnée dans la procédure (tablette remise à zéro) : verrouillage complet, impossible de quitter l'app sans le code admin, redémarrage automatique dans l'app |
| Code de sortie du mode kiosque | Défini par l'admin de l'entreprise pour chaque borne (écran Bornes, W03) ; seul son empreinte est envoyée à la borne avec sa configuration |
| Distribution | Fiche unique sur Google Play (une app pour toutes les entreprises) |

## 4. Étapes ordonnées

### B00.1 — Création du projet (développeur)

- Projet React Native CLI (bare), TypeScript strict, Android seulement, dans `FluxyRH-mobile/borne/` ; `git init`, dépôt `riyadaOne/fluxyrh-m-borne` ; `CLAUDE.md` du projet.
- Organisation, qualité, langues, client d'API typé (espace `/kiosk`), stockage chiffré : repris d'E00.

### B00.2 — Thème et écrans de base

- Thème clair forcé, contraste maximal, tailles × 2 (UX/UI §4.3, §8) ; écrans « Borne non appairée », « Borne désactivée · contactez l'administrateur ».

### B00.3 — Mode kiosque

- Mode kiosque selon la décision du §3, application de lancement, écran toujours allumé, redémarrage automatique, sortie par appui long de 5 s dans un coin + code admin (vérifié contre l'empreinte reçue), jamais de bouton visible.
- Procédure d'installation d'une borne dans `07-exploitation/`.

### B00.4 — Documentation et livraison

- `02-reference/` : architecture de l'app Borne.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut B00 dans la ROADMAP.

## 5. Tests attendus

| Domaine | Cas |
|---|---|
| Kiosque | Impossible de quitter sans code ; redémarrage dans l'app ; écran toujours allumé |
| Thème | Lisibilité à 1,5 m, en fr, en, ar |

## 6. Critères de sortie

- `npm run check` vert ; une tablette de test reste en mode kiosque après redémarrage.
- Documentation et livraison de B00.4 faites.
