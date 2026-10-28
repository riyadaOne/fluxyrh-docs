# UX/UI DESIGN — FluxyRH

| | |
|---|---|
| **Produit** | FluxyRH — SIRH SaaS multi-entreprises |
| **Éditeur** | RIYADA ONE TECHNOLOGIES SARL |
| **Version du document** | 1.1 (brouillon) — 2026-10-28 : aligné sur les décisions du plan d'implémentation |
| **Lecteurs** | Équipe technique (web et mobile) |
| **Statut** | Règles **cibles** ; les maquettes sont proposées par Claude et validées module par module (§16) |
| **Documents liés** | PRD, TRD, APPFLOW (écrans `S-xx`, navigation par rôle), BACKEND SCHEMA (statuts) |

---

## Sommaire

1. Objet
2. Principes d'expérience
3. Surfaces et langage visuel unique
4. Système de design commun (tokens)
5. Back-office web : mises en page
6. Back-office web : modèles d'écran et composants
7. Application Entreprise (mobile)
8. Application Borne
9. Application Console
10. Codes de statut
11. Langues et sens d'écriture
12. Accessibilité
13. Documents, bulletins et carte employé
14. Pages publiques
15. Rédaction de l'interface
16. Maquettes à produire
17. Liste de contrôle avant de livrer un écran
18. Décisions

---

## 1. Objet

Ce document fixe **les règles d'interface** de FluxyRH : tokens, mises en page, composants, comportements et rédaction, pour le web, les trois applications mobiles, les documents et les pages publiques. Il reprend les règles d'UnivPlus qui ont fait leurs preuves et corrige sa principale dette UX (deux identités visuelles différentes entre le web et le mobile).

**Ordre de priorité** : demande explicite du porteur du projet → maquette validée de l'écran → ce document → valeurs par défaut de Flux UI (web) ou du socle `@shared/ui` (mobile). On n'introduit jamais un autre système de design. Les règles **[OBLIGATOIRE]** se vérifient avant toute livraison.

---

## 2. Principes d'expérience

| # | Principe | Traduction concrète |
|---|---|---|
| U1 | **Une personne, un rôle, un menu** | Seul ce que le rôle, les permissions et les modules permettent apparaît ; rien de grisé « pour information » dans les menus |
| U2 | **Le statut d'abord** | Tout élément à cycle de vie affiche son statut en badge ; l'action suivante possible est le bouton principal |
| U3 | **Liste + modale** | Gérer = une liste ; créer, modifier, confirmer = une modale |
| U4 | **Aucune boîte de dialogue native** | Jamais `confirm()` ni `alert()` ; toujours une modale ou une feuille de l'application |
| U5 | **Bloquer avec une raison** | Une action impossible (dossier incomplet, période clôturée, checklist) dit pourquoi et quoi faire |
| U6 | **Rien ne se perd** | Corbeille restaurable sur chaque liste ; onglet Historique pour ce qui a fini son cycle |
| U7 | **Choisir plutôt que taper** | Listes déroulantes larges avec « Autre », téléphone international, sélecteurs de période |
| U8 | **Terrain d'abord sur mobile** | Pointer, demander un congé, approuver : à une main, en quelques gestes, hors ligne |
| U9 | **Trois langues sans compromis** | Chaque écran est vérifié en arabe (droite à gauche) |
| U10 | **Valeur en vigueur, modification en attente** | Une donnée vérifiable montre toujours la valeur qui fait foi et, à côté, la modification « À vérifier » s'il y en a une |
| U11 | **Le secret se voit** | Une valeur sensible non autorisée est remplacée par `••••` avec une icône cadenas et une info-bulle « Information réservée » ; jamais une cellule vide qui ferait croire à une donnée manquante |
| U12 | **Signer est un geste** | Toute signature passe par un écran dédié qui montre ce qui est signé, puis demande la preuve : la carte, le mot de passe (web) ou le code ou la biométrie du téléphone ; le résultat est confirmé visuellement. Le pointage exige toujours la carte |
| U13 | **Sobriété** | Interface noir et blanc ; la couleur est réservée aux statuts et aux alertes |

---

## 3. Surfaces et langage visuel unique

FluxyRH a **une seule identité visuelle**, neutre et noir et blanc, sur toutes ses surfaces.

| Surface | Intention | Base |
|---|---|---|
| **Back-office web** (plateforme et entreprise) | Outil de travail dense, lisible des heures durant | Starter kit Livewire + Flux UI, palette `zinc`, accent noir / blanc, mode sombre |
| **Espace personnel web** (`/me`) | Simple et rassurant pour un employé non initié | Même base, mises en page plus aérées |
| **App Entreprise** | Outil de terrain lisible en plein soleil | Mêmes tokens que le web, transposés dans `@shared/ui` |
| **App Borne** | Lisible à 1,5 m, utilisable sans formation | Mêmes tokens, tailles agrandies, contraste maximal |
| **App Console** | Outil interne RIYADA ONE | Mêmes tokens |
| **Documents** (bulletins, contrats, attestations, courriers) | Pièces officielles sobres | **Charte de l'entreprise** : neutre noir et blanc au socle ; modèle, couleur, cachet, filigrane avec le module Identité (§13.5) |
| **Carte employé** | Badge d'identité | Design neutre au socle ; 20 designs aux couleurs de la charte avec le module Identité (§13.3) |
| **Pages publiques** | Badge vérifiable ; présentation de FluxyRH | Même base |

**Marque blanche** : l'app Entreprise porte le **nom et le logo de l'entreprise cliente** (icône, écran de démarrage, en-tête), mais garde le langage visuel FluxyRH (tokens identiques pour toutes les entreprises). Le logo FluxyRH apparaît seulement dans « À propos ».

La **charte graphique** de l'entreprise (module Identité) ne s'applique **qu'aux documents générés** : PDF, e-mails, carte. L'interface ne change jamais d'une entreprise à l'autre.

---

## 4. Système de design commun (tokens)

Les mêmes valeurs servent au web (`resources/css/app.css`) et au mobile (`src/shared/ui/theme.ts`).

### 4.1 Couleurs de base

| Token | Clair | Sombre | Usage |
|---|---|---|---|
| `background` | `zinc-50` `#fafafa` | `zinc-950` `#09090b` | Fond de page |
| `surface` | `#ffffff` | `zinc-900` `#18181b` | Cartes, listes, champs, modales |
| `sunken` | `zinc-100` `#f4f4f5` | `zinc-800` `#27272a` | Zones en retrait, pistes, avatars |
| `border` | `zinc-200` `#e4e4e7` | `zinc-700` `#3f3f46` | Séparateurs |
| `text` | `zinc-900` `#18181b` | `zinc-50` `#fafafa` | Texte principal |
| `textMuted` | `zinc-600` `#52525b` | `zinc-400` `#a1a1aa` | Texte secondaire |
| `textSubtle` | `zinc-500` `#71717a` | `zinc-500` `#71717a` | Indications, placeholders |
| `accent` | `zinc-900` `#18181b` | `#ffffff` | Bouton principal, sélection, focus |
| `accentForeground` | `#ffffff` | `zinc-900` `#18181b` | Texte sur accent |

### 4.2 Couleurs de statut (seules couleurs de l'interface)

| Token | Clair (texte / fond) | Sombre (texte / fond) | Sens |
|---|---|---|---|
| `success` | `#15803d` / `#dcfce7` | `#4ade80` / `#14532d` | Validé, actif, vérifié, présent |
| `warning` | `#a16207` / `#fef9c3` | `#facc15` / `#422006` | En attente d'un tiers, à vérifier, retard |
| `danger` | `#b91c1c` / `#fee2e2` | `#f87171` / `#450a0a` | Refusé, bloquant, absent, révoqué |
| `info` | `#1d4ed8` / `#dbeafe` | `#60a5fa` / `#172554` | En cours de traitement, demandé |
| `neutral` | `zinc-700` / `zinc-100` | `zinc-300` / `zinc-800` | Brouillon, inactif, terminé |

Ces couleurs ne servent **jamais** à la décoration. Les graphiques des tableaux de bord utilisent la gamme `zinc` et une seule couleur de statut quand il faut signaler un écart.

### 4.3 Typographie

| Rôle | Latin | Arabe |
|---|---|---|
| Texte et titres | **Instrument Sans** (comme UnivPlus, starter kit Livewire) | IBM Plex Sans Arabic |
| Titres éditoriaux (page d'accueil `fluxyrh.app`) | Instrument Serif | Instrument Sans semi-gras |
| Chiffres, matricules, montants, codes | Instrument Sans avec `tabular-nums` ; IBM Plex Mono pour les codes et matricules | IBM Plex Mono |

Sur mobile, les polices sont embarquées dans l'application (Android et iOS), comme pour UnivPlus.

Tailles mobiles : caption 12 · small 13 · body 15 · input 16 · title 17 · heading 20 · display 24 · figure 32. Borne : multiplier par 2 (§8).

### 4.4 Espacements, rayons, ombres

`spacing` : 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48. `radius` : 6 (champs, badges) · 8 (boutons) · 12 (cartes, modales) · plein (avatars). Ombres très légères au clair, aucune au sombre (bordures seulement).

### 4.5 Thème

**Clair / Sombre / Système** (par défaut : Système) ; réglé dans Paramètres (web) ou Profil (mobile) ; mémorisé sur l'appareil. La Borne suit un thème **clair forcé** pour la lisibilité du QR (§8).

**[OBLIGATOIRE]** Aucune couleur, taille ni marge écrite directement dans un écran : tokens uniquement (classes Tailwind de la palette au web, `themed(...)` au mobile).

---

## 5. Back-office web : mises en page

### 5.1 Layouts

| Layout | Usage |
|---|---|
| `app/sidebar` | Back-office de l'entreprise : barre latérale, menu utilisateur en bas |
| `platform` | Back-office plateforme (jumeau) |
| `me` | Espace personnel : barre latérale réduite aux écrans personnels (ou section « Mon espace » de la barre principale) |
| `auth/*` | Connexion, invitation, 2FA, changement de mot de passe imposé |
| `public` | Badge public, page d'accueil `fluxyrh.app` |

### 5.2 Barre latérale

Groupes, dans l'ordre (chaque entrée n'apparaît que si le rôle, une délégation ou le module l'autorisent) :

1. **Tableau de bord**
2. **Mon espace** : mon dossier, mes pointages, mes congés, mes bulletins, mon contrat, mes demandes, à signer (badge du nombre)
3. **Mon équipe** (MGR) : équipe, approbations, corrections, heures sup, événements
4. **Collaborateurs** : employés, invitations, vérifications (badge du nombre en attente), organigramme, contrats
5. **Temps** : présences, plannings, jours fériés, heures sup, congés
6. **Paie** : périodes, rémunérations, vérifications bancaires, paiements, avances, paramétrage
7. **Processus et talents** (modules) : événements, workflows, courriers, formulaires, évaluations, compétences, recrutement
8. **Conformité** (module) : déclarations, export comptable
9. **Pilotage** (module) : rapports, simulations, modèles de rémunération
10. **Communication** : annonces
11. **Administration** : utilisateurs, invitations, rôles et permissions, connectés, structure, postes, sites, bornes, cartes, journal

**Menu utilisateur** (bas) : Paramètres (profil, sécurité : mot de passe, 2FA, passkeys ; apparence ; langue), **Configuration** de l'entreprise (ADM), Aide, Déconnexion. **[OBLIGATOIRE]** Aucun libellé ne déborde.

### 5.3 Pages de réglages

Configuration, Paramètres, paramétrage de paie : `flux:navlist` à gauche (≈ 220 px), contenu à droite avec titre et sous-titre par onglet.

---

## 6. Back-office web : modèles d'écran et composants

### 6.1 Écran de liste

```
┌──────────────────────────────────────────────────────────────┐
│ Titre de la page                                [+ Action]   │
│ Sous-titre : ce que l'écran permet de faire                  │
├──────────────────────────────────────────────────────────────┤
│ [Actifs] [Historique] [Corbeille]  Site ▾ Structure ▾ Période ▾ 🔍 │
├──────────────────────────────────────────────────────────────┤
│ Colonne ⇅ │ Colonne ⇅ │ Statut ⇅   │ Actions                 │
│ …         │ …         │ [badge]    │ ⋯ (menu)                │
├──────────────────────────────────────────────────────────────┤
│                                             pagination  < >  │
└──────────────────────────────────────────────────────────────┘
```

**[OBLIGATOIRE]** : titre + sous-titre ; toutes les colonnes triables (statut compris ; les colonnes chiffrées sont triées après déchiffrement, TRD §9.3) ; onglet Corbeille sur tout CRUD ; onglet Historique pour les éléments à cycle de vie ; actions de ligne dans un menu ; action principale en haut à droite ; état vide explicite. Un employé est toujours affiché avec **photo (ou initiales), nom, matricule et poste**.

### 6.2 Modales et formulaires

- Création, modification, confirmation dans une `flux:modal` ; confirmation = `confirmX(id)` puis `x()`. Jamais `wire:confirm`.
- Modales larges, champs courts sur deux colonnes.
- Listes déroulantes larges + « Autre » (civilité, lien de parenté, type de pièce, motif de sortie…).
- Téléphone : composant `x-phone-input` ; indicatif par défaut celui choisi dans la Configuration de l'entreprise, aucun indicatif codé (décision 0002).
- Montants : saisie avec séparateurs de milliers, devise affichée à droite, jamais tapée.
- Erreurs sous le champ, traduites.

### 6.3 Dossier employé (fiche RH et « Mon dossier »)

```
┌──────────────────────────────────────────────────────────────┐
│ [photo] Nom Prénom · EMP-2026-0012 · Poste · [Actif]         │
│ Structure · Site · Manager · Type · Embauché le …            │
│ Complétude ████████░░ 80 %  · 2 pièces manquantes            │
├──────────────────────────────────────────────────────────────┤
│ [Identité] [Coordonnées] [Famille] [Diplômes] [Banque]        │
│ [Documents] [Contrat] [Affectations] [Carte] [Journal]       │
├──────────────────────────────────────────────────────────────┤
│ Bloc « Identité »                         [Vérifiée ✓]       │
│  Valeur en vigueur …                                          │
│  ┌ Modification en attente [À vérifier] ─────────────────┐   │
│  │ Nom : Mansouri → Mansouri-Ali   · justificatif 📎      │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

- Chaque bloc affiche son badge (`Vérifiée`, `À vérifier`, `Rejetée` avec le motif).
- Côté employé, le bouton du bloc est « Modifier » ; une modification crée une version en attente (U10).
- L'onglet Banque n'existe que pour les rôles autorisés (U11) ; pour les autres, l'onglet est absent.
- Le justificatif est demandé ou non selon le réglage de l'entreprise, bloc par bloc ; les listes (situation matrimoniale, type de pièce) sont celles de l'entreprise.
- Selon les modules : onglets Événements, Workflows, Compétences, Carrière, Rémunération (PAIE, DIR, RH en lecture).

### 6.4 Liste de vérification (S-22, S-56)

Liste des versions en attente, filtrable par bloc, site, structure et ancienneté de la demande. Chaque ligne s'ouvre dans un **panneau latéral** :

| Gauche | Centre | Droite |
|---|---|---|
| Valeur en vigueur | Nouvelle valeur (champs modifiés surlignés) | Justificatif (aperçu image / PDF, zoom) |

Boutons **Vérifier** et **Rejeter** (motif obligatoire), raccourcis clavier, passage automatique à la demande suivante.

La vérification se fait **une demande à la fois**, jamais par lot ; le justificatif est toujours visible avant la décision.

### 6.5 Assistant de complétion (S-60)

Barre d'étapes horizontale (identité → coordonnées → famille → contacts d'urgence → diplômes → banque → pièces), chaque étape avec son état (à faire, soumise, vérifiée, rejetée). L'employé peut sauter une étape et revenir ; « Enregistrer et continuer plus tard » est toujours visible. Le récapitulatif final liste les pièces manquantes et ce que leur absence bloque (congés, attestations, virements).

### 6.6 Période de paie (S-52 à S-55)

```
┌──────────────────────────────────────────────────────────────┐
│ Paie · Octobre 2026 · Mensuelle                [Calculée]    │
│ ① Ouverte ─ ② Variables ─ ③ Calculée ─ ④ Contrôlée ─ ⑤ Approuvée ─ ⑥ Clôturée │
├───────────────────────┬──────────────────────────────────────┤
│ Checklist             │ Contenu de l'étape courante          │
│ ✅ Embauches          │ (variables / bulletins / écarts)     │
│ ✅ Sorties            │                                      │
│ ❌ Heures sup (3)     │                                      │
│ ⬜ …                  │                                      │
│ ⬜ Ouvrir la suivante │                [Action de l'étape]   │
└───────────────────────┴──────────────────────────────────────┘
```

Frise des statuts en haut ; checklist à gauche (bloquants ❌ avec lien pour résoudre) ; contenu de l'étape à droite ; un seul bouton principal, celui de la transition suivante, désactivé avec raison tant qu'un bloquant reste. Le contrôle (S-54) montre les **écarts** avec la période précédente par employé (variation du net en %, rubriques nouvelles ou disparues).

### 6.7 Éditeur de contrat (S-40)

Deux panneaux : à gauche la **bibliothèque de blocs**, avec en tête les **blocs proposés** pour la nature du contrat et le type d'employé (recherche, glisser pour insérer) ; à droite le **contrat** en blocs ordonnés (poignée de déplacement, retirer, « + Bloc libre », « Enregistrer dans la bibliothèque »). Les champs de fusion apparaissent comme des **pastilles** `{{Nom de l'employé}}` insérables depuis un menu (éditeur Tiptap). Un panneau **Signataires** permet d'ajouter l'employé et les signataires de l'entreprise, et de fixer leur ordre. Aperçu PDF à tout moment. Une fois `À signer`, l'éditeur reste modifiable : un bandeau prévient que toute modification crée une nouvelle version et annule les signatures déjà faites ; les signatures attendues et faites sont listées, avec le téléchargement des copies à imprimer et le dépôt du scan signé.

### 6.8 Approbations (S-81)

Boîte de réception unique de la direction : périodes de paie, avances, contrats, courriers et formulaires à signer, vérifications des données des RH (et de la banque des PAIE), heures sup et congés des RH quand aucun autre RH n'existe. Chaque élément montre le résumé, les montants (autorisés) et ses actions : « Approuver » / « Renvoyer » (motif) pour une décision, « Signer » pour un document (mot de passe sur le web, carte ou code dans l'app).

### 6.9 Matrice des droits (S-04)

Tableau écrans × rôles, cases à cocher ; défauts du rôle signalés ; écrans de modules non souscrits grisés ; panneau « Exclusions » par personne. Une ligne fixe rappelle que les **champs sensibles** ne se délèguent pas.

### 6.10 Tableaux de bord

- Module Pilotage : widgets choisis par l'utilisateur, widgets par défaut par rôle ; indicateurs chiffrés en colonnes de 6 à gauche des graphiques ; graphiques ApexCharts en `zinc`.
- Sans le module : page d'accueil « **À faire** » (vérifications, approbations, signatures, congés en attente, étapes de checklist) + soldes et raccourcis personnels.
- Admin : liste de démarrage tant que la mise en place n'est pas terminée.

### 6.11 Composants transverses

| Composant | Rôle |
|---|---|
| `x-employee-chip` | Photo / initiales, nom, matricule, poste |
| `x-status-badge` | Badge de statut, couleur tirée de l'enum (`color()`) — jamais choisie dans la vue |
| `x-sensitive` | Affiche une valeur sensible ou `••••` + cadenas selon `FieldAccess` |
| `x-version-diff` | Valeur en vigueur / modification en attente |
| `x-blocked-reason` | Encadré « Pourquoi c'est bloqué » + lien d'action |
| `x-phone-input`, `x-money-input` | Saisies normalisées |
| `x-mobile-app-invite` | Encart d'installation de l'app quand les liens des stores existent |
| `x-sign-panel` | Signature d'un document sur le web : résumé, empreinte courte, confirmation par le mot de passe |
| `x-rich-editor` | Éditeur Tiptap maison (contrats, courriers, annonces), avec pastilles de champs |
| Cloche de notifications | Compteur, liste, tout marquer lu |

---

## 7. Application Entreprise (mobile)

### 7.1 Composants `@shared/ui`

Socle repris d'UnivPlus et adapté aux tokens FluxyRH : `Screen`, `ScreenHeader` (logo de l'entreprise), `AppText`, `Button`, `TextField`, `SearchField`, `Card`, `Badge`, `ListItem` / `ListGroup`, `Banner`, `EmptyState`, `Loading` (squelettes libellés), `Avatar`, `ChipSelect`, `SegmentedControl`, `CheckboxRow`, `SettingsRow`, `OfflineBanner`, `Icon`, `Logo`, barre d'onglets. Nouveaux : `QrScanner`, `NfcZone` (pose de carte), `SignSheet` (signature avec la carte, le code ou la biométrie), `VersionDiff`, `SensitiveValue`, `Stepper`, `CountdownButton` (« Inverser », durée réglée par l'entreprise), `BalanceCard` (solde de congé).

**[OBLIGATOIRE]** Un nouveau besoin commun = un nouveau composant ici.

L'app Entreprise existe sur **Android et iOS** : sur iPhone, la pose de la carte passe par la feuille système Core NFC (« Approchez votre carte ») et le verrouillage accepte Face ID ; le reste de l'interface est identique.

### 7.2 Navigation

Barre d'onglets en bas, propre à chaque rôle (APPFLOW §4) ; **Profil** toujours en dernier ; onglet **Moi** pour les rôles qui ont aussi un espace personnel. Le Profil regroupe : langue, thème, verrouillage, connexion par carte (PIN), téléphones enregistrés, **envois en attente** et **refusés à l'envoi** (badge sur l'onglet).

### 7.3 Écran « Pointer »

```
┌───────────────────────────┐
│  Pointer                  │
│  Site : Agence centrale   │
│ ┌───────────────────────┐ │
│ │                       │ │
│ │   [ viseur caméra ]   │ │   1. Scanner le QR de la borne
│ │                       │ │
│ └───────────────────────┘ │
│  ─────────────────────────│
│        ( ◉ NFC )          │   2. Poser la carte au dos
│  Posez votre carte        │
└───────────────────────────┘
          ↓
┌───────────────────────────┐
│  ✓ Entrée enregistrée      │
│  [photo] Nom Prénom       │
│  07:58 · Agence centrale  │
│  [ Inverser (10) ]        │   compte à rebours
│  En attente d'envoi 🕓     │   si hors ligne
└───────────────────────────┘
```

Retours explicites en cas de refus (code expiré : « Rescannez le QR », carte non active, site non autorisé, téléphone non enregistré).

### 7.4 Motifs d'écran

| Motif | Règle |
|---|---|
| Chargement | Squelettes + libellé de ce qui se charge |
| Hors ligne | `OfflineBanner` « Hors ligne · synchronisé le … à … » ; consultation du cache ; pointages et demandes en file |
| Erreur | `ErrorState` avec le message traduit du serveur et « Réessayer » |
| Vide | `EmptyState` qui explique |
| Signature | `SignSheet` : résumé de ce qui est signé (titre, empreinte courte), « Posez votre carte » ou code / biométrie du téléphone, confirmation |
| Action définitive | Confirmation dans l'écran, jamais une alerte native |
| Formulaire | Bouton principal pleine largeur collé au-dessus du clavier |
| Valeur sensible | `SensitiveValue` (masquée par défaut, révélée d'un appui pour l'employé lui-même : bulletins, banque) |

### 7.5 Ce qui reste au web

Configuration, matrice des droits, paramétrage de paie, calcul et contrôle de la paie, éditeur de contrat, clauses, courriers en masse, déclarations, exports : tâches de bureau. Le mobile permet de **consulter** et d'**approuver**, pas de paramétrer.

---

## 8. Application Borne

| Règle | Détail |
|---|---|
| Orientation | Portrait par défaut (tablette ou téléphone fixé au mur), paysage accepté |
| Thème | **Clair forcé**, contraste maximal ; QR noir sur blanc pur |
| Lisibilité | Lisible à 1,5 m : heure en 64 pt, consignes en 28 pt |
| Écran d'attente | Nom de l'entreprise et du site, heure, date, **QR dynamique** (≥ 60 % de la largeur), barre de renouvellement de 30 s, « Posez votre carte ici » avec flèche vers le lecteur NFC |
| Confirmation | Plein écran pendant la durée d'inversion réglée par l'entreprise (la carte suivante la ferme) : photo, nom, **Entrée** (fond `success`) ou **Sortie** (fond `neutral`), heure, bouton « Inverser » avec compte à rebours |
| Refus | Plein écran `danger` 3 s, motif en une phrase |
| Hors ligne | Pastille discrète « Hors ligne · N pointages en attente » ; le pointage continue normalement |
| Révocation / suspension | Écran « Borne désactivée · contactez l'administrateur » |
| Sortie du mode kiosque | Appui long de 5 s dans un coin + code choisi par l'admin pour cette borne ; jamais de bouton visible |
| Pointage de secours | Bouton discret « Je n'ai pas ma carte » : matricule, photo prise par la borne, message « Pointage à valider par votre manager » |
| Activation de carte | Bouton discret « Activer ma carte » : pose de la carte, PIN saisi deux fois sur un clavier à l'écran |
| Son | Bip court distinct pour succès et refus, activé ou non par l'admin pour chaque borne |

---

## 9. Application Console

Mêmes tokens et composants ; onglets Accueil (indicateurs), Cartes (file à encoder → `NfcZone` d'écriture avec étapes écrire, relire, verrouiller ; le verrouillage est **définitif** et demande une confirmation), Entreprises (lecture, factures comprises), Journal, Profil. Verrouillage de l'app à chaque ouverture. Android seulement.

---

## 10. Codes de statut

Une même famille de sens garde la même couleur partout ; la couleur est définie **dans l'enum** (`color()`), jamais dans la vue.

| Sens | Exemples (BACKEND SCHEMA §7) | Token |
|---|---|---|
| Neutre / brouillon / terminé | Brouillon, Terminé, Archivée, Inactif, Sortie (pointage) | `neutral` |
| En cours de traitement | Demandée, Ouverte, Calculée, En préparation, En cours | `info` |
| En attente d'un tiers | Invité, À vérifier, À valider (pointage de secours), Approuvée manager, Déclarée, Proposé, Proposée (workflow), À payer (facture), À signer, Remise, En attente d'appairage, À payer, Contrôlée | `warning` |
| Validé / actif / réussi | Actif, Vérifiée, Validée, Signé, Approuvée, Clôturée, Payé, Prête, Remis, Lancée (workflow), Payée (facture), Entrée (pointage), Présent | `success` |
| Refusé / bloquant / échec | Refusée, Rejetée, Annulée, Révoqué, Désactivée, Suspendu, Échec, Absent, Pointage refusé, Écartée (workflow), Annulée (facture) | `danger` |

Le badge porte **toujours** le libellé traduit du statut (la couleur n'est jamais le seul signal).

---

## 11. Langues et sens d'écriture

- **[OBLIGATOIRE]** Aucun texte affiché en dur : web `__('module.key')`, mobile `t('module:key')` ; fr, en, ar livrés ensemble ; un test échoue sur une clé manquante ou un « FCFA » en dur.
- Arabe : `dir="rtl"` au web, `direction` à la racine sur mobile et sur la Borne ; icônes directionnelles inversées ; frises d'étapes et tableaux vérifiés en arabe.
- Séparateurs dans les clés (`'{{label}} : {{value}}'`).
- Langue de l'interface = choix de la personne ; langue des documents, e-mails, push et de la Borne = **langue officielle** de l'entreprise (la Borne peut proposer un sélecteur de langue discret).
- Données saisies (noms de postes, de structures, blocs de contrat, modèles de courrier) : une seule langue, celle de l'entreprise ; libellés des rubriques de paie et articles d'aide : traduisibles ; valeurs créées par le système (types par défaut, listes de départ) : dans la langue officielle (décision 0002).

---

## 12. Accessibilité

- Contraste ≥ 4,5:1 pour le texte dans les deux thèmes (palette `zinc` choisie en ce sens) ; ≥ 7:1 sur la Borne.
- Focus visible (anneau `accent` 2 px) sur tous les contrôles web ; navigation clavier complète dans la liste de vérification.
- Mobile : éléments cliquables avec `role` et libellé ; cibles de 48 px minimum ; tailles de police système respectées.
- La couleur n'est jamais le seul porteur d'information.
- Pointage utilisable par une personne qui ne lit pas : pictogrammes d'entrée / sortie, photo de la personne, son de confirmation.

---

## 13. Documents, bulletins et carte employé

### 13.1 Règles communes

- Documents rédigés dans la **langue officielle** de l'entreprise.
- En-tête de l'entreprise : logo, raison sociale, identifiants légaux choisis par l'entreprise (libellé et valeur), adresse ; pied de page avec référence, date de génération et empreinte courte pour les documents signés.
- Charte neutre par défaut (noir et blanc), ou charte de l'entreprise (§13.5) ; imprimable en A4 portrait ; tableaux et positions en px (contraintes dompdf : ni flexbox, ni grid, ni variables CSS) ; polices sous `storage/app/public/fonts/documents` ; arabe par ar-php.
- Toujours générés depuis des **données vérifiées** (P3).

### 13.2 Bulletin de paie

Une page : identité de l'employé (matricule, poste, structure, date d'embauche, identifiants marqués « affiché sur le bulletin », type), période et date de paiement ; tableau des rubriques (code, libellé, base, taux, gains, retenues salariales, part patronale) ; totaux (brut, cotisations, imposable, impôt, net à payer) ; **net en lettres** ; cumuls annuels ; mode de paiement ; mention de l'accusé de réception le cas échéant.

### 13.3 Carte employé

- Recto : logo de l'entreprise, photo, nom, poste, matricule ; verso : mentions de l'entreprise, consigne « Si vous trouvez cette carte… », zone NFC.
- **Socle** : un design neutre (noir et blanc, logo, photo).
- **Module Identité** : couleur de la charte active (palette §13.5), déclinée en teintes claires et foncées par le gabarit.
- **20 designs recto / verso** (module Identité) (mécanique d'UnivPlus : `config/cards.php`), choisis par l'admin entreprise dans la Configuration avec **aperçu en direct** ; photo affichée ou non ; export PDF avec traits de coupe pour l'impression.
- **[OBLIGATOIRE]** Chaque design est testé avec un nom long (au moins 40 caractères) et un poste long : réduction de la taille ou passage à la ligne, jamais de texte coupé (dette connue d'UnivPlus).
- « Ma carte » (web et mobile) affiche la carte à l'identique (HTML rendu par le serveur, WebView sur mobile).

### 13.4 Contrats, attestations, courriers

Mise en page texte sobre, numérotation des pages, bloc des signataires avec la mention « Signé électroniquement dans FluxyRH le … » et le moyen (carte, mot de passe, code), et l'empreinte du document ; mention de la version signée.

### 13.5 Chartes des documents (module Identité)

**Socle : charte neutre**. Noir et blanc, logo et mentions légales en en-tête, pied de page standard. C'est aussi l'aperçu montré à une entreprise sans le module.

**12 modèles** (gabarits fixes, l'entreprise ne déplace aucun élément) :

| Code | Nom | Caractère |
|---|---|---|
| `classique` | Classique | En-tête centré, filet fin sous l'en-tête |
| `moderne` | Moderne | Logo à gauche, mentions à droite, titres en couleur |
| `institutionnel` | Institutionnel | En-tête centré, double filet, cartouche de référence |
| `epure` | Épuré | Beaucoup de blanc, couleur limitée aux titres |
| `bandeau` | Bandeau | Bandeau plein en couleur en haut de la première page |
| `encadre` | Encadré | Cadre fin sur la page, en-tête dans un cartouche |
| `lateral` | Latéral | Barre verticale colorée à gauche |
| `minimal` | Minimal | Pas de filet, petit logo, pied réduit |
| `corporate` | Corporate | En-tête et pied en aplat, tableaux à en-tête coloré |
| `elegant` | Élégant | Titres en petites capitales, filets fins |
| `technique` | Technique | Tableaux denses, numérotation des sections |
| `contemporain` | Contemporain | Bloc de couleur en angle, titres larges |

**Palette fermée** (chaque couleur : contraste ≥ 4,5:1 sur blanc, lisible imprimée en niveaux de gris) :

| Code | Nom | Hex |
|---|---|---|
| `noir` | Noir | `#18181b` |
| `ardoise` | Ardoise | `#334155` |
| `marine` | Marine | `#1e3a8a` |
| `bleu` | Bleu | `#1d4ed8` |
| `petrole` | Pétrole | `#0f766e` |
| `foret` | Forêt | `#166534` |
| `bordeaux` | Bordeaux | `#881337` |
| `rouge` | Rouge | `#b91c1c` |
| `ocre` | Ocre | `#9a3412` |
| `brun` | Brun | `#78350f` |
| `violet` | Violet | `#6d28d9` |

**Réglages** : couleur ; logo affiché ou non ; lignes de mentions légales, site web, texte du pied ; cachet (image) ; filigrane (aucun, logo, « Confidentiel », « Copie », texte court).

**Signature de la direction** : déposée par le directeur dans « Ma signature » (S-08), apposée seulement à côté de la mention de sa signature dans le système. Cachet et signature : fond transparent, 300 dpi minimum, aperçu avant enregistrement.

**Écran S-19** : à gauche les réglages, à droite l'aperçu avec des onglets Bulletin · Contrat · Attestation · E-mail · Carte ; bouton **Activer** avec confirmation (« Les documents générés à partir de maintenant utiliseront cette charte ; les documents existants ne changent pas »). Sans le module : la charte neutre en lecture seule et une présentation du module.

**E-mails** : logo en haut, bouton d'action et filet dans la couleur de la charte, pied avec les mentions ; même structure pour les 12 modèles.

**[OBLIGATOIRE]** Chaque modèle est testé avec chaque couleur sur les cinq documents de l'aperçu, en français et en arabe (RTL), avec une raison sociale longue et un filigrane : rien ne se chevauche ni n'est coupé.

---

## 14. Pages publiques

- **Badge** `/badge/{id}` : page minimale, logo et nom de l'entreprise, photo, nom, poste, grand badge `En poste` (`success`) / `Plus en poste` (`danger`) / `Inconnue` (`neutral`), date et heure de la vérification ; aucune autre donnée ; `noindex`.
- **Accueil `fluxyrh.app`** : page de présentation noir et blanc, sans prix ni formulaire, coordonnées de RIYADA ONE, trois langues, mode sombre ; maquette proposée par Claude et validée avant W01.12, page construite en W01.

---

## 15. Rédaction de l'interface

- Français clair et direct, vouvoiement, phrases courtes ; un verbe d'action sur chaque bouton (« Vérifier la donnée », « Approuver la paie », pas « OK »).
- Sous-titre de page = ce que la personne peut faire ici.
- Un blocage dit **pourquoi** et **quoi faire** (« Dossier incomplet : la copie de la pièce d'identité n'est pas encore vérifiée. Déposez-la dans Mon dossier → Documents »).
- Côté employé, éviter le jargon RH : « Ma fiche de paie » plutôt que « Bulletin » dans les titres, « Pièces à fournir » plutôt que « Documents obligatoires ».
- Les actions automatiques s'affichent au nom de « Système ».
- Dates et heures dans le fuseau de l'entreprise (ou du site pour les pointages) ; montants dans sa devise, au format de la langue.
- Les messages d'erreur de l'API sont rédigés et traduits côté serveur.

---

## 16. Maquettes à produire

Proposées par Claude **module par module**, avant le développement de chaque module du plan d'implémentation (`04-planification/plan-implementation/`), et validées par le porteur du projet.

| Module | Maquettes |
|---|---|
| W01 | Plateforme (connexion, entreprises, abonnements, factures, tableau de bord), **accueil `fluxyrh.app`** |
| W02 | Connexion, invitation, changement de mot de passe imposé, utilisateurs, matrice des droits, connectés, configuration, journal |
| W03 | Structure, postes, sites, **Bornes** (gestion, appairage, code de sortie), organigramme |
| W04 | **Assistant de complétion**, **Mon dossier**, fiche RH, **liste de vérification**, approbations |
| W05 | Cartes (préparation, remise, Ma carte), badge public, design neutre de la carte |
| W06 | Plannings, jours fériés, règles d'heures sup, présences, corrections, heures sup établies, feuille de temps |
| W07 | Congés (employé, manager, RH), calendrier d'équipe |
| W08 | Bibliothèque de blocs, **éditeur de contrat** (blocs proposés, signataires), signature sur le web |
| W09 | **Période de paie**, paramétrage des rubriques, rémunérations, bulletin PDF, paiements, avances, états |
| W10 | Annonces, notifications, accueils par rôle, aide |
| W11 à W15 | Écrans des modules (déclarations et modèles, bilan social, événements, workflows, courriers, formulaires, tableaux de bord, rapports, simulations, évaluations, compétences, imports) |
| W16 | **Charte graphique** (S-19), **12 modèles de charte** sur bulletin, contrat, attestation et e-mail, **20 designs de carte**, « Ma signature » (S-08) |
| E00 à E10 | App Entreprise : connexion, onglets par rôle, **Pointer**, dossier, carte, congés, contrats, paie, communication, modules |
| B00 à B03 | **Écran de la Borne** (attente, confirmation, refus, secours, activation, hors ligne, désactivée) |
| C00 à C02 | Console (file des cartes, encodage, entreprises) |

**[OBLIGATOIRE]** Lire la maquette de l'écran avant de le coder ; l'écran livré lui est fidèle.

---

## 17. Liste de contrôle avant de livrer un écran

**Web**

- [ ] Fidèle à la maquette ; titre + sous-titre
- [ ] Liste : colonnes triables, corbeille, historique si cycle de vie, filtres utiles
- [ ] Création, modification, confirmation en modale Flux ; aucun dialogue natif
- [ ] Statuts en badge, couleur issue de l'enum
- [ ] Valeurs sensibles via `x-sensitive` ; vérifié avec un compte ADM et RH (aucune fuite)
- [ ] Blocages expliqués
- [ ] Aucune chaîne en dur ; fr, en, ar ; vérifié en arabe et en mode sombre
- [ ] Menu filtré par rôle, permission et module

**Mobile et Borne**

- [ ] Fidèle à la maquette ; composants `@shared/ui` uniquement ; aucun style en ligne
- [ ] Chargement libellé, état vide, erreur, hors ligne traités
- [ ] Rôles d'accessibilité et libellés ; cibles de 48 px
- [ ] fr, en, ar ; vérifié en arabe, en clair et en sombre (Borne : clair seulement)
- [ ] Boutons masqués si permission ou module absents
- [ ] `npm run check` vert ; contrôle sur téléphone (et sur tablette pour la Borne)

---

## 18. Décisions (2026-10-27)

| Sujet | Décision |
|---|---|
| Identité | Noir et blanc ; accent noir (clair) / blanc (sombre) ; couleur réservée aux statuts |
| Mobile | Même style que le web (une seule identité) ; marque blanche = nom et logo du client |
| Carte employé | Design neutre au socle ; 20 designs recto / verso aux couleurs de la charte avec le module Identité (§13.3) |
| Charte graphique | Documents générés seulement (PDF, e-mails, carte), jamais l'interface ; 12 modèles, palette fermée de 11 couleurs, cachet, signature, filigrane ; module Identité hors pack (§13.5) |
| Police | Instrument Sans (+ IBM Plex Sans Arabic, IBM Plex Mono) (§4.3) |
| Logo FluxyRH | **Nouveau logo**, dessiné par le porteur du projet (SVG, traits en `currentColor` pour suivre les thèmes clair et sombre) ; composant `x-app-logo` réservé en attendant |
| Maquettes | Proposées par Claude et validées module par module (§16) |
| Signature | Écran dédié avec la carte, le mot de passe (web) ou le code / la biométrie (app) ; carte obligatoire pour le pointage (U12) |
| Applications | Entreprise sur Android et iOS ; Borne et Console sur Android |
| Éditeur de texte | Tiptap dans un composant maison `x-rich-editor` (pas de licence Flux Pro) |
| Vérification | Une demande à la fois, jamais par lot |
| Rémunération et RH | Le RH voit la rémunération et les bulletins en lecture ; la banque reste masquée pour lui (décision 0003) |
| Documents | Rédigés dans la langue officielle de l'entreprise, identifiants légaux choisis par elle |
