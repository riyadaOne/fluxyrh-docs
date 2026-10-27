# PRD — Product Requirements Document — FluxyRH

| | |
|---|---|
| **Produit** | FluxyRH — SIRH SaaS multi-entreprises (web + mobile + carte NFC employé) |
| **Éditeur** | RIYADA ONE TECHNOLOGIES SARL (N'Djamena, Tchad) |
| **Version du document** | 1.0 (brouillon) — 2026-10-27 |
| **Lecteurs** | Équipe technique et produit |
| **Statut** | Refonte complète : aucun code existant. FluxyHR v1 sert uniquement de référence fonctionnelle |
| **Documents liés** | TRD, APPFLOW, UX/UI DESIGN, BACKEND SCHEMA (même dossier `01-specifications/`) |

---

## Sommaire

1. Objet du document et conventions
2. Résumé produit
3. Problème et contexte
4. Vision et proposition de valeur
5. Acteurs et personas
6. Principes produit (règles qui ne se négocient pas)
7. Exigences fonctionnelles par domaine
8. Modèle économique et découpage en modules
9. Exigences non fonctionnelles
10. Hors périmètre
11. Hypothèses, risques et dépendances
12. Indicateurs de réussite (proposés)
13. Questions ouvertes
14. Annexes : glossaire, passage FluxyHR v1 → FluxyRH, couverture du cahier des charges SIRH

---

## 1. Objet du document et conventions

Ce PRD décrit **ce que FluxyRH doit faire et pourquoi**. Le « comment » est dans le **TRD**. Les parcours écran par écran sont dans l'**APPFLOW**, les règles d'interface dans l'**UX/UI DESIGN**, et les tables et cycles de vie dans le **BACKEND SCHEMA**.

**Identifiants** : chaque exigence porte un identifiant `F-<DOMAINE>-<nn>` (fonctionnelle) ou `NF-<nn>` (non fonctionnelle), repris par les autres documents.

**Colonne « Offre »** : `Socle` = toujours inclus ; sinon, nom du module payant qui ouvre la fonction (cf. section 8).

**Statuts des cycles de vie** : écrits `Entre guillemets typographiques` → `Statut suivant` ; ils seront des enums dans le code.

---

## 2. Résumé produit

FluxyRH est la **base de données RH centralisée et authentique** d'une entreprise : chaque information est saisie **par la personne qui en est propriétaire** (l'employé pour son état civil, le manager pour son équipe, le RH pour l'affectation, le gestionnaire de paie pour la rémunération), puis **vérifiée** par l'acteur habilité. Rien n'est ressaisi par un intermédiaire.

Le produit se compose de :

- une **application web** (Laravel / Livewire) avec deux espaces : l'espace **plateforme** (RIYADA ONE) et un espace par **entreprise** (sous-domaine `{slug}.fluxyrh.app`) ;
- une **application mobile** (React Native) **en marque blanche** (un build, un nom, une icône et une fiche store par entreprise) pour tous les rôles de l'entreprise, utilisable hors ligne pour le pointage, la consultation et les demandes ;
- une **application Console** (RIYADA ONE) qui encode les cartes NFC et suit les entreprises ;
- une **carte NFC employé** : badge vérifiable, confirmation du pointage, accès rapide au dossier, connexion par carte + PIN, signature d'actions ;
- un **pointage sur site** : QR code dynamique affiché sur chaque site, scanné puis confirmé par la carte NFC.

FluxyRH est vendu **par abonnement à l'entreprise**, sous forme d'un **socle** complet et de cinq **modules payants**.

---

## 3. Problème et contexte

### 3.1 Le problème

1. **Données RH dispersées et non fiables** : dossiers papier, tableurs, informations recopiées par un assistant RH à partir de documents photocopiés. Personne ne sait quelle version fait foi.
2. **Saisie par un intermédiaire** : quand le RH ressaisit tout, il devient un goulot d'étranglement et la source d'erreurs ; l'employé ne voit pas ce qui est enregistré sur lui.
3. **Paie longue et risquée** : 8 à 12 jours par mois pour une PME de 25 employés (calcul CNPS, IRPP, bulletins, présences, congés), avec un risque d'erreur élevé (constat FluxyHR v1).
4. **Pointage contournable** : feuilles de présence signées par un collègue, pointage GPS falsifiable.
5. **Aucune traçabilité** : en cas de litige (sanction, licenciement, contestation de salaire), l'entreprise ne peut pas prouver qui a saisi, validé ou reçu quoi.

### 3.2 Le contexte d'usage (déterminant pour les choix produit)

- **Tchad d'abord, puis zone CEMAC** : la paie doit être **entièrement paramétrable** (cotisations, impôts, primes créés par l'entreprise), aucun barème codé en dur.
- **Connectivité variable** : l'app mobile fonctionne hors ligne pour le pointage, la consultation et les demandes.
- **Trois langues** : français, arabe (droite à gauche), anglais.
- **Android majoritaire** ; employés de terrain parfois sans smartphone NFC → **borne de site** comme alternative.
- **Entreprises multi-sites** : agences, succursales, chantiers.
- **Cible** : PME et ETI de 10 à plusieurs centaines d'employés (cliniques, écoles privées, BTP, distribution, hôtellerie, sécurité, cabinets).
- **Acheteur** : DG ou DAF, qui juge sur le ROI, la conformité de la paie et la fiabilité des données.

---

## 4. Vision et proposition de valeur

### 4.1 Les quatre piliers

| Pilier | Ce que FluxyRH fait |
|---|---|
| **Authentifier** | Chaque donnée a un propriétaire qui la saisit et un vérificateur qui la valide, sur justificatif |
| **Centraliser** | Un dossier unique par employé, consultable par chaque acteur selon ses droits, champ par champ |
| **Fluidifier** | Circuits de validation (congés, heures sup, événements, paie) sans papier ni ressaisie |
| **Prouver** | Pointage QR + carte, signature d'actions par carte, journal d'audit complet |

### 4.2 Différenciateurs

1. **Saisie par le propriétaire + vérification** : l'inverse d'un SIRH classique où le RH saisit tout.
2. **Pointage infalsifiable à distance** : QR dynamique du site + carte NFC personnelle.
3. **Carte NFC employé** : badge vérifiable publiquement, connexion, signature de contrats et d'accusés de réception.
4. **Confidentialité des salaires** : ni l'admin ni le RH ne voient les salaires et les coordonnées bancaires.
5. **Paie 100 % paramétrable** : rubriques, cotisations et barèmes créés par l'entreprise, pré-paramétrage Tchad fourni.
6. **Cloisonnement strict** : une base de données par entreprise.

---

## 5. Acteurs et personas

### 5.1 Vue d'ensemble

| Rôle | Code (proposé) | Espace | Web | Mobile | Création du compte |
|---|---|---|---|---|---|
| Administrateur plateforme | (garde `platform`) | Plateforme | ✅ | ✅ Console | Par un autre admin plateforme |
| Administrateur entreprise | `admin_entreprise` | Entreprise | ✅ | ✅ | Invité par la plateforme (le premier) ou par un admin entreprise |
| Direction (DG / DAF) | `direction` | Entreprise | ✅ | ✅ | Invitation |
| Responsable RH | `rh` | Entreprise | ✅ | ✅ | Invitation |
| Gestionnaire de paie / Comptable | `gestionnaire_paie` | Entreprise | ✅ | ✅ | Invitation |
| Manager hiérarchique | `manager` | Entreprise | ✅ | ✅ | Invitation (rôle `manager` ; son équipe = les employés qui lui sont rattachés) |
| Employé | `employe` | Entreprise | ✅ | ✅ | Invitation (ou import Jobyflow suivi d'une invitation) |

Une personne n'a **qu'une identité** (base générale) mais un **rattachement par entreprise**, avec son rôle et son statut. Tout acteur de l'entreprise (y compris RH, manager, direction) est aussi un **employé** avec son propre dossier. Seule exception : l'**admin entreprise**, dont le dossier est **optionnel** (admin interne avec dossier, ou prestataire externe sans dossier).

### 5.2 Personas

**Administrateur plateforme (RIYADA ONE)** : crée les entreprises et leur base, gère les abonnements et les modules, encode les cartes NFC avec la Console, assure les sauvegardes et produit les archives mensuelles demandées. *Attente* : piloter plusieurs entreprises sans voir leurs données internes.

**Administrateur entreprise** : invitations et comptes, configuration (identité, sites, structure, types de documents, politique de mot de passe), matrice des droits, demandes de cartes NFC, journal d'audit, liste des utilisateurs connectés. *Ne voit pas* les salaires ni les coordonnées bancaires. *Attente* : configurer l'entreprise seul.

**Direction (DG / DAF)** : tableaux de bord, masse salariale et simulations, approbation finale de la paie, validation des décisions sensibles. *Attente* : des chiffres fiables et la main sur les décisions qui engagent l'entreprise.

**Responsable RH** : invite les employés et fixe leur affectation (poste, département, site, manager, type, date d'embauche), vérifie les données saisies par les employés, rédige les contrats, valide congés, heures sup et événements, valide les variables de paie. Voit la rémunération contractuelle, *pas* les bulletins ni les coordonnées bancaires. *Attente* : vérifier au lieu de saisir.

**Gestionnaire de paie / Comptable** : paramètre les rubriques de paie, saisit les éléments de rémunération, vérifie les coordonnées bancaires, calcule et contrôle la paie, produit les déclarations et l'export comptable. *Attente* : une paie juste du premier coup, traçable.

**Manager hiérarchique** : approuve les congés de son équipe, corrige le pointage avec motif, déclare les heures supplémentaires, propose des événements (promotion, sanction), évalue. *Attente* : gérer son équipe depuis son téléphone.

**Employé** : complète et tient à jour son dossier (état civil, coordonnées, pièces, diplômes, banque), pointe, demande congés et documents, consulte bulletins, contrat, soldes, cumuls annuels, signe par carte. *Attente* : savoir ce qui est enregistré sur lui et ne plus faire la queue au service RH.

---

## 6. Principes produit (règles qui ne se négocient pas)

| # | Principe | Conséquence concrète |
|---|---|---|
| P1 | **Invitation d'abord** | Aucune inscription publique ; le dossier employé naît à l'acceptation de l'invitation |
| P2 | **Le propriétaire saisit, l'habilité vérifie** | Chaque donnée a un propriétaire défini (cf. 7.4) ; une donnée vérifiable modifiée repasse `À vérifier` |
| P3 | **Seule la donnée vérifiée fait foi** | Tant qu'une modification n'est pas vérifiée, la paie, les documents et les rapports utilisent la dernière valeur vérifiée |
| P4 | **Cloisonnement strict** | Une base par entreprise ; la base générale ne porte que l'identité, les rattachements et la plateforme |
| P5 | **Statut explicite** | Toute donnée qui passe de main en main a un statut et des transitions réservées au rôle habilité, refusées par le serveur sinon |
| P6 | **Confidentialité par champ** | Éléments de rémunération, bulletins et coordonnées bancaires ne sont visibles que du gestionnaire de paie, de la direction et de l'employé concerné, **jamais de l'admin**. Seule exception : le RH voit la **rémunération contractuelle** (celle écrite dans le contrat), pas les bulletins ni la banque |
| P7 | **Traçabilité** | Qui, quand, quoi, valeur avant / après, depuis où ; les actions automatiques sont attribuées au « Système » |
| P8 | **Rien n'est supprimé définitivement** | Corbeille restaurable sur chaque liste ; suppression logique partout |
| P9 | **Le serveur est seul juge** | L'app mobile masque ce qui n'est pas permis, mais chaque règle est vérifiée côté serveur |
| P10 | **Trois langues partout** | Aucun texte affiché codé en dur ; arabe en droite à gauche |
| P11 | **Aucun taux ni montant codé en dur** | Cotisations, impôts, barèmes, primes et heures sup sont paramétrés en base par l'entreprise |
| P12 | **Une période de paie clôturée est verrouillée** | Variables, pointages et bulletins d'une période clôturée ne se modifient plus |
| P13 | **Droits par défaut, délégables** | Chaque rôle a des écrans par défaut ; l'entreprise peut déléguer un écran à un autre rôle ou exclure une personne |

---

## 7. Exigences fonctionnelles par domaine

### 7.1 Plateforme, entreprises et abonnements

| ID | Exigence | Offre |
|---|---|---|
| F-PLT-01 | L'admin plateforme crée une entreprise (raison sociale, slug, fuseau horaire, devise, langue officielle, modules), ce qui provisionne sa base et invite son premier admin entreprise | Plateforme |
| F-PLT-02 | Abonnement `Actif` → `Suspendu` → `Résilié` ; un abonnement non actif bloque l'accès à l'espace entreprise | Plateforme |
| F-PLT-03 | Activation / désactivation des modules par entreprise ; chaque changement est journalisé | Plateforme |
| F-PLT-04 | Tableau de bord plateforme : entreprises, effectifs, activité, revenu récurrent | Plateforme |
| F-PLT-05 | File des cartes NFC à encoder, encodage dans l'app Console | Plateforme |
| F-PLT-06 | Sauvegarde technique quotidienne de chaque base ; l'entreprise peut demander chaque mois une **archive complète** de ses données, préparée et mise à disposition par la plateforme | Plateforme |
| F-PLT-07 | Page d'accueil publique `fluxyrh.app` (présentation) | Plateforme |
| F-PLT-08 | Fiche « Application mobile » par entreprise : identifiants de l'app, export de la configuration de build (flavor), liens des stores qui déclenchent l'invitation à installer l'app | Plateforme |

### 7.2 Administration de l'entreprise et accès

| ID | Exigence | Offre |
|---|---|---|
| F-ADM-01 | Invitations par e-mail avec lien signé, rôle et **date de fin d'accès optionnelle** (stagiaire, intérimaire, consultant) ; une personne déjà connue garde son compte | Socle |
| F-ADM-02 | Rattachement `Invité` → `Actif` → `Suspendu` → `Révoqué` ; la révocation n'efface ni l'identité ni l'historique ; l'accès expire automatiquement à la date de fin | Socle |
| F-ADM-03 | Matrice des droits par écran (comme UnivPlus) : écrans par défaut par rôle, délégation d'un écran à un autre rôle, exclusion d'une personne ; écrans d'un module non souscrit grisés | Socle |
| F-ADM-04 | Droits **par donnée** : les champs sensibles (salaire, rémunération, banque) suivent P6, quelles que soient les délégations d'écran | Socle |
| F-ADM-05 | Politique de mot de passe paramétrable : longueur, complexité, expiration ; 2FA activable et imposable par rôle | Socle |
| F-ADM-06 | Liste des utilisateurs connectés (web et mobile) et déconnexion forcée d'une session | Socle |
| F-ADM-07 | Configuration : identité de l'entreprise (logo, RCCM, NIU, n° CNPS, adresse), format du matricule, langue officielle, fuseau horaire, devise | Socle |
| F-ADM-08 | Journal d'audit en lecture seule : utilisateur, action, donnée, valeurs avant / après, IP, appareil ; filtres et export | Socle |
| F-ADM-09 | Corbeille restaurable sur chaque liste | Socle |

### 7.3 Organisation : structure, sites, organigramme

| ID | Exigence | Offre |
|---|---|---|
| F-ORG-01 | Structure en arbre libre (direction, département, service…), code unique, responsable | Socle |
| F-ORG-02 | Sites (adresse, fuseau, plannings applicables) ; chaque employé a un site principal et une liste de sites où il peut pointer | Socle |
| F-ORG-03 | Chaque site dispose d'une ou plusieurs **bornes** : appareil Android NFC **fourni par l'entreprise**, avec l'app en mode borne, appairé par l'admin ; la borne affiche le QR dynamique et lit les cartes | Socle |
| F-ORG-04 | Rattachement hiérarchique : chaque employé a un manager ; le manager voit son équipe **directe et indirecte** ; les décisions (congés, corrections, heures sup) reviennent au manager direct, le supérieur n'agissant qu'en son absence | Socle |
| F-ORG-05 | Organigramme en arbre (structure et hiérarchie), export PDF | Socle |
| F-ORG-06 | La borne fonctionne **hors ligne** : le QR dynamique est généré localement à partir d'une clé propre à la borne, les pointages sont stockés puis envoyés au retour du réseau (fenêtre F-TPS-03) ; une borne perdue est révoquée et sa clé renouvelée | Socle |
| F-ORG-07 | Écran « Bornes » : appairage sécurisé par QR à usage unique, état et dernier signal de chaque borne, suspension, révocation, renouvellement de la clé ; une seule application Borne pour toutes les entreprises | Socle |

### 7.4 Collaborateurs : dossier authentique

**Propriété des données** (règle P2) :

| Donnée | Saisie par | Vérifiée par |
|---|---|---|
| État civil, photo, coordonnées, situation familiale, contact d'urgence | Employé | RH |
| Pièce d'identité, diplômes, certificats, autres justificatifs (avec fichier) | Employé | RH |
| Coordonnées bancaires | Employé | Gestionnaire de paie |
| Poste, structure, site, manager, type d'employé, date d'embauche | RH (à l'invitation, puis via événements) | — |
| Rémunération contractuelle (salaire de base, avantages écrits au contrat) | RH (dans le contrat) | Employé et direction (signature) |
| Éléments de rémunération de la paie (rubriques, variables) | Gestionnaire de paie | — |
| Documents de l'entreprise remis à l'employé | RH | Employé (accusé de réception par carte) |

| ID | Exigence | Offre |
|---|---|---|
| F-EMP-01 | L'invitation d'un employé porte son affectation (poste, structure, site, manager, type, date d'embauche) ; à l'acceptation, le dossier est créé avec un **matricule automatique** selon le format de l'entreprise | Socle |
| F-EMP-02 | Types d'employé : CDI, CDD, stagiaire, apprenti, journalier, saisonnier, prestataire, intérimaire, consultant ; liste extensible par l'entreprise ; un type indique s'il entre dans la paie interne | Socle |
| F-EMP-03 | L'employé complète son dossier ; chaque donnée vérifiable suit `À vérifier` → `Vérifiée` / `Rejetée` (motif) ; **toute modification ultérieure repasse `À vérifier`** sans effacer la dernière valeur vérifiée (P3) | Socle |
| F-EMP-04 | Liste de travail du vérificateur : données en attente, justificatif à côté de la valeur, comparaison avec la valeur précédente ; personne ne vérifie ses propres données, les coordonnées bancaires sont vérifiées par le gestionnaire de paie (par la direction pour celles d'un gestionnaire de paie), et les autres données d'un RH toujours par la direction | Socle |
| F-EMP-05 | Types de documents **paramétrés par l'entreprise** (obligatoire ou non, avec ou sans date d'expiration, qui les dépose, qui les voit) ; alerte avant expiration | Socle |
| F-EMP-06 | Taux de complétude du dossier par employé et pour l'entreprise | Socle |
| F-EMP-07 | Cycle de l'employé : `Invité` → `Actif` → `En sortie` → `Sorti` ; un employé sorti garde son dossier en lecture seule | Socle |
| F-EMP-08 | Cumuls annuels consultables par l'employé (brut, net, cotisations, impôt) | Socle |
| F-EMP-09 | **Pièces obligatoires paramétrées par l'entreprise** (par type d'employé) ; tant qu'elles ne sont pas toutes `Vérifiées` : pas de demande de congé, pas de formulaire type (attestation), pas d'ordre de virement (le bulletin est calculé, le paiement reste possible hors virement) ; pointage et paie restent possibles | Socle |
| F-EMP-10 | Relances automatiques de l'employé (notification, e-mail) et indicateur de complétude pour le RH | Socle |

### 7.5 Cartes NFC employé

| ID | Exigence | Offre |
|---|---|---|
| F-NFC-01 | Une carte par employé et par entreprise ; identifiant opaque, aucune donnée en clair sur la puce | Socle |
| F-NFC-02 | Cycle `Préparée` (admin entreprise) → `Encodée` (plateforme, Console) → `Livrée` → `Remise` → `Active` ; `Désactivée` (perte, vol, sortie) | Socle |
| F-NFC-03 | Badge vérifiable : page publique indiquant si la personne est **actuellement en poste** dans l'entreprise (nom, photo, poste), sans autre donnée, limitée et journalisée | Socle |
| F-NFC-04 | Accès rapide : un acteur habilité scanne la carte pour ouvrir le dossier, avec le contenu filtré par ses droits | Socle |
| F-NFC-05 | Connexion à l'app par carte + PIN (option de l'entreprise), nombre d'essais limité, appareils révoqués à la désactivation de la carte | Socle |
| F-NFC-06 | Signature d'actions par carte : signature de contrat, accusé de réception (bulletin, document, matériel, courrier), confirmation de pointage ; chaque signature est horodatée et journalisée | Socle |
| F-NFC-07 | Design de la carte imprimée : le socle fournit **un design neutre** (noir et blanc, logo, photo) ; le module Identité ouvre **20 modèles** recto / verso aux couleurs de la charte (F-IDN-04). Aperçu en direct et export PDF pour l'impression dans les deux cas | Socle (neutre) / Identité (20 modèles) |

### 7.6 Temps de travail et présences

| ID | Exigence | Offre |
|---|---|---|
| F-TPS-01 | Plannings de travail (jours, horaires, pauses) par structure, site ou employé ; jours fériés par entreprise | Socle |
| F-TPS-02 | Pointage : l'employé scanne le **QR dynamique** du site (renouvelé toutes les N secondes) puis confirme avec sa **carte NFC** ; sur son téléphone ou sur la borne du site | Socle |
| F-TPS-03 | Pointage hors ligne : QR et carte vérifiés à l'envoi, accepté s'il est transmis dans une fenêtre configurable (48 h proposées) | Socle |
| F-TPS-04 | Calcul automatique : heures travaillées, retard, départ anticipé, absence non justifiée, selon le planning | Socle |
| F-TPS-05 | Correction de pointage par le manager, motif obligatoire, journalisée ; jamais sur une période de paie clôturée | Socle |
| F-TPS-06 | Heures supplémentaires : règles **paramétrables par l'entreprise** (seuils, majorations par tranche, nuit, jour férié, plafonds) ; déclarées par le manager → `Validées` / `Refusées` par le RH → intégrées aux variables de paie | Socle |
| F-TPS-07 | Feuille de temps mensuelle par employé, export | Socle |

### 7.7 Congés et absences

| ID | Exigence | Offre |
|---|---|---|
| F-ABS-01 | Types de congé et d'absence paramétrables (droits annuels, acquisition, justificatif requis, impact sur la paie) | Socle |
| F-ABS-02 | Demande par l'employé : `Demandée` → `Approuvée manager` → `Validée RH` ; `Refusée` (motif) à chaque étape ; `Annulée` | Socle |
| F-ABS-03 | Calcul des jours selon le planning et les jours fériés ; solde par type calculé à la volée | Socle |
| F-ABS-04 | Calendrier d'équipe pour le manager (absences prévues) | Socle |

### 7.8 Contrats

| ID | Exigence | Offre |
|---|---|---|
| F-CTR-01 | Modèles de contrat rédigés dans l'application (éditeur de texte avec champs de fusion : employé, poste, dates, rémunération…) | Socle |
| F-CTR-02 | Cycle `Brouillon` → `À signer` → `Signé` (employé par carte, puis direction) → `Actif` → `Terminé` / `Résilié` (motif, date, type) | Socle |
| F-CTR-03 | Un seul contrat actif par employé ; avenants ; alerte d'échéance (CDD, période d'essai, stage) | Socle |
| F-CTR-04 | Génération PDF à l'en-tête de l'entreprise ; le RH rédige le contrat, rémunération contractuelle comprise (exception de P6) | Socle |

### 7.9 Paie

| ID | Exigence | Offre |
|---|---|---|
| F-PAY-01 | **Rubriques entièrement paramétrables** par l'entreprise : gains (primes, indemnités), cotisations salariales et patronales, impôts, retenues ; mode de calcul (montant fixe, pourcentage d'une base, barème par tranches, formule), plafond, caractère imposable / soumis à cotisation | Socle |
| F-PAY-02 | **Pré-paramétrage Tchad** livré à la création (CNPS salarié et employeur, IRPP par tranches, CAC, taxes patronales), modifiable ; taux à faire valider par un expert avant mise en production | Socle |
| F-PAY-03 | Historique des versions du paramétrage avec date d'effet : une modification ne change pas les bulletins passés | Socle |
| F-PAY-04 | Le salaire de base vient du contrat actif ; les autres rubriques fixes de l'employé sont saisies par le gestionnaire de paie | Socle |
| F-PAY-05 | Période de paie : `Ouverte` → `Variables validées` (RH : présences, congés, heures sup, événements) → `Calculée` → `Contrôlée` (gestionnaire de paie) → `Approuvée` (direction) → `Clôturée` (bulletins publiés, période verrouillée) ; une période par **fréquence de paie** utilisée (mensuelle, quinzaine, hebdomadaire, journalière), la fréquence étant fixée par employé (défaut issu du type d'employé) | Socle |
| F-PAY-06 | Checklist intégrée à chaque période, avec étapes bloquantes ; sa dernière étape est l'**ouverture de la période suivante**, proposée à la clôture, ou faite par le système si l'entreprise active l'ouverture automatique pour cette fréquence | Socle |
| F-PAY-07 | Bulletin PDF (mentions légales de l'entreprise), publié dans l'espace de l'employé, accusé de réception par carte ; réimpression des périodes passées | Socle |
| F-PAY-08 | Statut de paiement par bulletin (`À payer` → `Payé` / `Échec`) ; ordres de virement par banque, **toutes banques**, formats de fichier paramétrables par l'entreprise | Socle |
| F-PAY-09 | Journal de paie et états de cotisations par période, export | Socle |
| F-PAY-10 | Avances et prêts sur salaire, **activables par l'entreprise** selon sa politique (plafonds, nombre d'échéances) : `Demandé` (employé) → `Accepté` (gestionnaire de paie) → `Approuvé` (direction) / `Refusé` (motif) → `En remboursement` → `Soldé` ; échéances prélevées en retenue sur les paies suivantes | Socle |

### 7.10 Masse salariale (module)

| ID | Exigence | Offre |
|---|---|---|
| F-MSA-01 | Analyses de la masse salariale par structure, site, type d'employé, période | Masse salariale |
| F-MSA-02 | Simulations : hausse globale ou ciblée, ajout / retrait / variation d'une rubrique, **variation d'effectif** par catégorie | Masse salariale |
| F-MSA-03 | Simulations enregistrées et **comparées** côte à côte | Masse salariale |
| F-MSA-04 | **Modèles de rémunération** (assemblage de rubriques) affectés à des populations | Masse salariale |

### 7.11 Processus RH (module)

| ID | Exigence | Offre |
|---|---|---|
| F-PRO-01 | Événements datés sur le dossier (promotion, mutation, augmentation, sanction, avertissement, félicitation…), types paramétrables : `Proposé` (manager) → `Validé` / `Refusé` (RH) ; un événement validé met à jour le dossier | Processus RH |
| F-PRO-02 | Workflows d'entrée, de sortie et de mutation : liste de tâches par acteur, échéances, e-mails et notifications | Processus RH |
| F-PRO-03 | Courriers types avec champs de fusion, envoyés en masse (PDF et e-mail), accusé de réception par carte | Processus RH |
| F-PRO-04 | Formulaires types demandés par l'employé (attestation de travail, de salaire…) : `Demandé` → `Prêt` / `Refusé` → `Remis` | Processus RH |

### 7.12 Talents (module)

| ID | Exigence | Offre |
|---|---|---|
| F-TAL-01 | Évaluations 360° : campagnes, poids par type d'évaluateur, une réponse par évaluateur, rapport, évaluation clôturée immuable | Talents |
| F-TAL-02 | Référentiel de compétences, compétences par employé, recherche par compétence | Talents |
| F-TAL-03 | Parcours de carrière et historique des postes | Talents |
| F-TAL-04 | Import des candidats retenus depuis **Jobyflow (API)** : données pré-remplies, puis invitation | Talents |

### 7.13 Conformité et déclarations (module)

| ID | Exigence | Offre |
|---|---|---|
| F-CNF-01 | Déclaration CNPS : saisie et consolidation des informations requises par période, à partir de la paie clôturée | Conformité |
| F-CNF-02 | Déclaration fiscale (IRPP et taxes) : idem | Conformité |
| F-CNF-03 | Bilan social annuel : indicateurs consolidés | Conformité |
| F-CNF-04 | Export comptable des écritures de paie : **format d'import Sage** et **format générique** (CSV / Excel : journal, date, compte, libellé, débit, crédit) ; plan comptable SYSCOHADA et correspondance rubrique → compte paramétrables | Conformité |

FluxyRH **prépare** les informations ; il ne transmet pas les déclarations aux organismes.

### 7.14 Communication

| ID | Exigence | Offre |
|---|---|---|
| F-COM-01 | Notifications in-app (cloche web, écran mobile) et push pour les événements clés : donnée à vérifier, demande à approuver, bulletin publié, contrat à signer | Socle |
| F-COM-02 | E-mails transactionnels dans la langue officielle (invitation, décisions, workflows) | Socle |
| F-COM-03 | Annonces ciblées (tous, structure, site, rôle, personnes), publication, archivage, accusé de lecture | Socle |

### 7.15 Pilotage et reporting (module)

| ID | Exigence | Offre |
|---|---|---|
| F-PIL-01 | Tableaux de bord par rôle, personnalisables (widgets) | Pilotage |
| F-PIL-02 | Rapports standard (effectifs, présences, absences, paie, turnover) avec filtres et export | Pilotage |
| F-PIL-03 | États personnalisés : choix des champs, filtres, regroupements, sauvegarde et partage | Pilotage |
| F-PIL-04 | Accès aux données pour un outil externe (API de lecture ou export planifié), respectant P6 | Pilotage |

Sans le module, chaque rôle dispose d'une page d'accueil avec ses **tâches en attente** (Socle).

### 7.16 Centre d'aide

| ID | Exigence | Offre |
|---|---|---|
| F-AID-01 | Articles par catégorie, en trois langues, recherche ; articles éditables par l'entreprise | Socle |

### 7.17 Application mobile

| ID | Exigence | Offre |
|---|---|---|
| F-MOB-01 | Marque blanche : une application par entreprise (nom, icône, fiche store), pour tous ses rôles ; écrans selon les droits | Socle |
| F-MOB-02 | Pointage QR + NFC, mode borne de site (appareil partagé, lecture des cartes de tous les employés) | Socle |
| F-MOB-03 | Hors ligne : pointage, consultation (dossier, bulletins, planning, soldes) en cache chiffré, demandes (congés, saisies du dossier) mises en file et envoyées au retour du réseau | Socle |
| F-MOB-04 | Actions de validation du manager et du RH (congés, heures sup, vérification de données) | Socle |
| F-MOB-05 | Verrouillage de l'app par biométrie ou code du téléphone ; version minimale imposée par le serveur | Socle |
| F-MOB-06 | Les fonctions des modules non souscrits sont masquées | Socle |

### 7.18 Identité documentaire (module)

L'**interface** de FluxyRH (web, mobile, borne) garde l'identité neutre FluxyRH avec le nom et le logo du client. La **charte graphique** de l'entreprise s'applique aux **documents générés** par FluxyRH : PDF, e-mails et carte employé.

| ID | Exigence | Offre |
|---|---|---|
| F-IDN-01 | Charte **neutre** par défaut (noir et blanc, logo et mentions légales de l'entreprise), appliquée à tous les PDF (contrats, avenants, bulletins, attestations, courriers, organigramme, rapports), aux e-mails et à la carte | Socle |
| F-IDN-02 | Choix d'un modèle de charte parmi **12 modèles prédéfinis**, avec aperçu sur des documents types (bulletin, contrat, attestation, e-mail) avant activation | Identité |
| F-IDN-03 | Réglages du modèle choisi : **couleur** prise dans une palette fermée de couleurs testées (lisibilité, impression), **en-tête et pied de page** (logo, raison sociale, RCCM, NIU, n° CNPS, adresse, site web, mentions), **cachet** de l'entreprise et **signature** de la direction (images), **filigrane** (logo ou mention « Confidentiel », « Copie ») | Identité |
| F-IDN-04 | Carte employé : 20 designs recto / verso aux couleurs de la charte (F-NFC-07) | Identité |
| F-IDN-05 | La signature d'un directeur est déposée par lui-même et n'est apposée que sur les documents qu'il a signés par carte ; le cachet est apposé sur les documents officiels (contrats, attestations, courriers) | Identité |
| F-IDN-06 | Chaque charte est **versionnée** ; un document garde la charte de sa génération (PDF figé avec empreinte) ; une nouvelle charte ne s'applique qu'aux documents générés après son activation ; à l'arrêt du module, les nouveaux documents reprennent la charte neutre ; chaque changement est journalisé | Socle (versions) / Identité |

---

## 8. Modèle économique et découpage en modules

### 8.1 Socle « FluxyRH Essentiel » (toujours inclus)

Accès par invitation, droits par écran et par donnée, dossiers employés authentiques, structure et sites, cartes NFC, pointage QR + NFC, plannings, heures sup, congés et absences, contrats, paie paramétrable avec bulletins et checklist, annonces, notifications, journal d'audit, centre d'aide, application mobile, trois langues.

### 8.2 Modules payants

| Module | Code (proposé) | Fonctions fermées s'il n'est pas souscrit |
|---|---|---|
| Pilotage | `pilotage` | Tableaux de bord à widgets, rapports, états personnalisés, accès externe aux données |
| Masse salariale | `masse_salariale` | Analyses, simulations, comparaison, modèles de rémunération |
| Talents | `talents` | Évaluations 360°, compétences, carrières, import Jobyflow |
| Conformité | `conformite` | Déclarations CNPS et fiscales, bilan social, export comptable |
| Processus RH | `processus_rh` | Événements, workflows entrée / sortie / mutation, courriers en masse, formulaires types |
| Identité (**option hors pack**) | `identite` | 12 modèles de charte pour les documents, palette, en-tête et pied, cachet, signature, filigrane, 20 designs de carte (sans le module : charte neutre) |

Un module non souscrit renvoie « module non souscrit » au web comme à l'API, quel que soit le rôle.

### 8.3 Grille (mensuel, FCFA)

| Effectif (employés actifs) | Socle seul | Modules | Pack complet |
|---|---|---|---|
| < 25 | 129 900 | prix ci-dessous | **199 900** |
| 25 – 74 | 194 900 | × 1,5 | **299 900** |
| 75 – 199 | 259 900 | × 2 | **399 900** |
| ≥ 200 | sur devis (prix négocié) | — | sur devis |

| Module | Prix mensuel (< 25 employés) |
|---|---|
| Pilotage | 24 900 |
| Conformité | 24 900 |
| Masse salariale | 19 900 |
| Talents | 19 900 |
| Processus RH | 19 900 |
| Identité (option hors pack) | 14 900 |

- Prix = pack complet si les 5 modules sont actifs, sinon socle + modules souscrits ; le pack représente environ −16 % par rapport au socle et aux 5 modules achetés séparément.
- Le module **Identité** est une **option hors pack** : il s'ajoute au socle seul comme au pack complet, au tarif de son palier (14 900 / 22 350 / 29 800). Exemple : pack complet < 25 employés + Identité = 199 900 + 14 900 = **214 800 FCFA / mois** (322 250 et 429 700 pour les paliers suivants).
- Facturation mensuelle ou annuelle (annuel = mensuel × 12 − 10 %).
- Le palier est déterminé par le **nombre d'employés actifs** ; le dépassement d'un palier est signalé à la plateforme et à l'admin entreprise.
- Les prix sont stockés en base (aucun montant codé en dur).

### 8.4 Cartes NFC

La carte est **payée par l'employé** à RIYADA ONE, hors système, comme la carte étudiant d'UnivPlus : **10 000 FCFA** par carte, à l'émission comme à la réémission (perte, vol).

### 8.5 Version et ordre de développement

**Toutes les exigences de ce PRD font partie de la version 1.0** : la première mise en production comprend le socle, les cinq modules et l'option Identité. Le développement avance **domaine par domaine**, chaque phase étant livrée, testée et recettée avant la suivante. Les écrans mobiles d'un domaine sont développés dans la même phase que ses écrans web.

Ordre proposé (à confirmer dans la feuille de route) :

| Phase | Domaines | Exigences |
|---|---|---|
| 1 | Plateforme, administration, accès | F-PLT, F-ADM |
| 2 | Organisation, sites, bornes | F-ORG |
| 3 | Dossier authentique | F-EMP |
| 4 | Cartes NFC | F-NFC |
| 5 | Temps de travail, pointage, heures sup | F-TPS |
| 6 | Congés et absences | F-ABS |
| 7 | Contrats | F-CTR |
| 8 | Paie | F-PAY |
| 9 | Communication, centre d'aide | F-COM, F-AID |
| 10 | Module Conformité | F-CNF |
| 11 | Module Processus RH | F-PRO |
| 12 | Module Pilotage | F-PIL |
| 13 | Module Masse salariale | F-MSA |
| 14 | Module Talents | F-TAL |
| 15 | Module Identité (chartes documentaires, designs de carte) | F-IDN |

L'application mobile (F-MOB) est construite au fil des phases ; la marque blanche et la publication sont finalisées avant la mise en production.

---

## 9. Exigences non fonctionnelles

| ID | Exigence | Cible (proposée, à valider) |
|---|---|---|
| NF-01 | Cloisonnement des données entre entreprises | Une base par entreprise ; aucune jointure entre bases |
| NF-02 | Confidentialité des données de rémunération | P6 vérifié par des tests sur chaque écran, export et point d'API |
| NF-03 | Traçabilité | Journal d'audit non modifiable, valeurs avant / après |
| NF-04 | Intégrité des cycles de vie | Statuts en enums, transitions dans des services, tests des transitions interdites |
| NF-05 | Anti-fraude du pointage | QR à durée de vie courte, carte obligatoire, horodatage serveur, fenêtre hors ligne bornée |
| NF-06 | Connectivité faible | Hors ligne mobile (F-MOB-03), cache chiffré |
| NF-07 | Multilingue | fr / en / ar, RTL, langue par compte, langue officielle par entreprise |
| NF-08 | Sécurité des accès | Invitation signée, 2FA, politique de mot de passe, jetons mobiles liés à l'entreprise, limites de débit |
| NF-09 | Sauvegarde et restauration | Sauvegardes quotidiennes conservées 30 jours, mensuelles conservées 12 mois ; archive mensuelle sur demande ; archive complète restituée à la résiliation |
| NF-10 | Disponibilité | 99,5 % par mois ; support < 24 h ouvrées |
| NF-11 | Performance | Page web < 2 s ; calcul d'une paie de 200 employés < 1 min |
| NF-13 | Conservation | Aucune suppression définitive : dossiers des employés sortis, contrats et bulletins conservés sans limite de durée |
| NF-12 | Qualité | Tests automatisés pour toute fonctionnalité, y compris les refus |

---

## 10. Hors périmètre

| Élément | Raison |
|---|---|
| Import Excel des employés | Remplacé par l'invitation (P1) |
| Demande de modification de profil validée avant enregistrement | Remplacée par la saisie libre + vérification (P2, P3) |
| Recrutement complet (offres, vivier, candidatures) | Couvert par Jobyflow ; FluxyRH importe seulement les candidats retenus |
| Formations, frais professionnels | Non retenus pour cette version |
| Transmission électronique des déclarations aux organismes | FluxyRH prépare les données ; le dépôt reste manuel |
| Virements bancaires automatiques | FluxyRH produit l'ordre de virement ; il ne paie pas |
| Vente et encaissement des cartes NFC | Processus opérationnel de RIYADA ONE, payé par l'employé |
| SMS | In-app, push et e-mail suffisent |
| LDAP / SSO | Non retenu |
| Groupe de sociétés consolidé | Une entreprise = un espace ; pas de consolidation entre entreprises |

---

## 11. Hypothèses, risques et dépendances

**Hypothèses** : les employés acceptent de saisir leurs données ; chaque site peut afficher un QR dynamique (écran, tablette ou borne) ; une partie des employés dispose d'un Android NFC, les autres pointent sur la borne ; un expert valide le pré-paramétrage de la paie tchadienne.

| Risque | Mesure |
|---|---|
| Employés qui ne complètent pas leur dossier | Taux de complétude, relances, blocage des congés, attestations et virements (F-EMP-09) |
| Volume de vérifications trop lourd pour le RH | Liste de travail priorisée, vérification groupée, justificatif affiché à côté de la valeur |
| Barèmes fiscaux mal paramétrés | Pré-paramétrage validé par un expert, versions datées, simulation avant clôture |
| Site sans réseau | Borne hors ligne avec QR généré localement (F-ORG-06) |
| Borne volée ou clé de borne copiée | Révocation de la borne, renouvellement de la clé, carte NFC toujours exigée |
| Perte de carte | Désactivation immédiate, pointage borne de secours avec validation manager |
| Fuite de données de rémunération | P6, tests dédiés, journal des consultations des champs sensibles |

**Dépendances externes** : Jobyflow (API), fournisseur de cartes NFC, Firebase Cloud Messaging, SMTP, Google Play, Cloudflare (DNS joker `*.fluxyrh.app`).

---

## 12. Indicateurs de réussite (proposés, à valider)

| Domaine | Indicateur | Cible proposée |
|---|---|---|
| Authenticité | Part des données du dossier vérifiées | ≥ 90 % à 60 jours |
| Adoption | Employés ayant accepté l'invitation | ≥ 90 % à 30 jours |
| Pointage | Pointages QR + carte / pointages totaux | ≥ 90 % |
| Efficacité | Délai moyen de vérification d'une donnée | < 48 h |
| Paie | Durée ouverture → clôture de la période | < 3 jours ouvrés |
| Paie | Bulletins corrigés après clôture | 0 |
| Congés | Délai demande → décision | < 48 h |

---

## 13. Questions ouvertes

1. **Pré-paramétrage de la paie tchadienne** : barème IRPP et CAC à confirmer, ensemble à faire valider par un expert-comptable ou la DGI (annexe 14.3).
2. **Ordre des phases de développement** (8.5) : à confirmer dans la feuille de route.

### Décisions prises (2026-10-27)

| Sujet | Décision |
|---|---|
| Rémunération dans le contrat | Le RH la voit et la rédige (exception de P6) |
| Application mobile | Marque blanche par entreprise |
| Carte NFC | Payée par l'employé, hors système, 10 000 FCFA (émission et réémission) |
| Versions | Tout dans la v1.0, développement domaine par domaine (8.5) |
| Prix | Grille 8.3, −10 % en annuel |
| Avances et prêts | Circuit employé → paie → direction, activable par l'entreprise (F-PAY-10) |
| Dossier incomplet | Pièces obligatoires paramétrées ; blocage congés, attestations, virements ; relances (F-EMP-09, F-EMP-10) |
| Borne de site | Fournie par l'entreprise, fonctionne hors ligne (F-ORG-03, F-ORG-06) |
| Export comptable | Sage + format générique, SYSCOHADA (F-CNF-04) |
| Rétention, disponibilité, performance | NF-09 à NF-13 |
| Charte graphique | Concerne les documents générés (PDF, e-mails, carte), pas l'interface ; socle = charte neutre ; module **Identité** = 12 modèles, palette, en-tête / pied, cachet, signature, filigrane, 20 designs de carte ; option hors pack à 14 900 (< 25) (7.18, 8.3) |

---

## 14. Annexes

### 14.1 Glossaire

| Terme | Sens |
|---|---|
| Entreprise (tenant) | Client de FluxyRH, avec sa base et son sous-domaine `{slug}.fluxyrh.app` |
| Rattachement | Lien personne ↔ entreprise, avec un rôle, un statut et une date de fin optionnelle |
| Propriétaire d'une donnée | Acteur qui la saisit (cf. 7.4) |
| Vérificateur | Acteur qui valide une donnée saisie par son propriétaire |
| Site | Lieu de travail physique où l'on pointe |
| QR dynamique | QR code d'un site renouvelé toutes les N secondes |
| Borne | Appareil partagé d'un site qui affiche le QR et/ou lit les cartes |
| Rubrique de paie | Élément paramétrable d'un bulletin (gain, cotisation, impôt, retenue) |
| Période de paie | Mois de paie, avec son cycle de validation |
| Socle / module | Partie toujours incluse / option payante de l'abonnement |
| Système | Auteur des actions automatiques dans le journal |

### 14.2 Passage de FluxyHR v1 à FluxyRH

| FluxyHR v1 | FluxyRH |
|---|---|
| Une instance par client | Multi-entreprise, une base par entreprise, sous-domaine |
| Comptes créés par l'admin, identifiants par défaut | Invitation uniquement |
| 4 rôles, 89 permissions | 6 rôles, droits par écran délégables + droits par donnée |
| Le RH saisit les employés, import Excel | L'employé saisit, le RH vérifie |
| Demandes de modification de profil | Saisie libre + vérification, dernière valeur vérifiée en vigueur |
| Pointage GPS (Flutter) | QR dynamique du site + carte NFC (React Native), borne |
| Taux CNPS / IRPP / CAC en retenues structurelles | Moteur de rubriques entièrement paramétrable, versions datées |
| Paie : checklist puis génération | Circuit RH → gestionnaire de paie → direction, période verrouillée |
| Tous modules inclus, paliers d'effectif | Socle + 5 modules + option Identité |
| Admin voit tout | Bulletins et banque invisibles pour l'admin et le RH ; le RH ne voit que la rémunération contractuelle |
| App Flutter unique | App React Native en marque blanche par entreprise |

### 14.3 Pré-paramétrage de la paie tchadienne (proposition à valider par un expert)

Ces valeurs sont chargées à la création d'une entreprise (F-PAY-02). Elles restent **modifiables**, avec une date d'effet (F-PAY-03). La colonne « Fiabilité » indique ce qui reste à confirmer avant la mise en production.

| Rubrique | Part | Taux / montant | Base | Fiabilité | Source |
|---|---|---|---|---|---|
| CNPS — prestations familiales et maternité | Employeur | 7,5 % | Brut plafonné à 500 000 FCFA / mois | Officielle | FAQ CNPS Tchad ; décret n° 1137/PR/PM/MFPT/SG/DTSS/07 (plafond) |
| CNPS — accidents du travail et maladies professionnelles | Employeur | 4 % | Idem | Officielle | FAQ CNPS Tchad |
| CNPS — pension (vieillesse, invalidité, décès) | Employeur | 5 % | Idem | Officielle | FAQ CNPS Tchad |
| CNPS — pension | Salarié | 3,5 % | Idem ; déductible avant l'IRPP | Officielle | FAQ CNPS Tchad |
| Assiette minimale CNPS | — | SMIG (59 995 FCFA, arrondi à 60 000) | — | À confirmer (SMIG peut-être revalorisé depuis 2011) | Guide de l'employeur CNPS ; décret n° 1111/PR/PM/MFPT/2011 |
| IRPP (barème annuel progressif) | Salarié | 0 % ≤ 800 000 ; 10 % ≤ 2 500 000 ; 20 % ≤ 7 500 000 ; 30 % au-delà | Imposable annuel (primes et avantages en nature inclus) | **À confirmer** (des sources divergent : 35 %, autres tranches) | Guides secondaires ; rapport ITIE Tchad 2023 (barème depuis le 01/01/2018) |
| Taxe forfaitaire sur les salaires | Employeur | 7,5 % | Brut + avantages en nature | Probable | PwC Tax Summaries |
| Taxe d'apprentissage et de formation professionnelle | Employeur | 1,2 % | Brut | Probable | Loi de finances 2019 |
| FIR | Salarié | 40 FCFA / mois | Forfait | Probable | PwC, Rivermate |
| CAC (centimes additionnels communaux) | Salarié | **Inconnu** | % de l'IRPP | **À trouver** (aucune source tchadienne ; 10 % au Cameroun, non transposable) | — |
| Avantages en nature (évaluation forfaitaire) | — | Logement 20 %, électricité 4 % du brut… | Brut | Probable | Loi de finances 2019 |

**Avant la mise en production** : faire valider l'ensemble par un expert-comptable ou la DGI tchadienne, en se référant au Code général des impôts et à la loi de finances en vigueur.

### 14.4 Couverture du cahier des charges SIRH (guidescomparatifs)

| § cahier | Thème | FluxyRH |
|---|---|---|
| 2.1.1 | Fichier des collaborateurs | F-ORG, F-EMP (une seule entité juridique par espace) |
| 2.1.2 | Contrats de travail | F-CTR |
| 2.1.3 | Temps partiels, ETP | F-TPS-01 (plannings) |
| 2.1.4 | Événements, processus, workflow, courriers | F-PRO |
| 2.1.5 | Documents administratifs, déclarations | F-CNF |
| 2.2 | Paramétrage et exploitation de la paie, bulletins | F-PAY |
| 2.3.1 | Analyses, simulations, modèles de rémunération | F-MSA |
| 2.3.2 | Campagnes d'augmentation | ⛔ (simulation seulement) |
| 2.4 | Recrutement | F-TAL-04 (import Jobyflow) |
| 2.5 | Carrières, compétences, évaluations | F-TAL |
| 2.6 | Formations | ⛔ |
| 2.7 | Absences | F-ABS |
| 2.8 | Frais | ⛔ |
| 3 | Portail self-service | F-EMP, F-ABS, F-PRO-04, F-MOB |
| 4 | Profils par fonction et par donnée | F-ADM-03, F-ADM-04 |
| 5 | Reporting, états personnalisés, outil externe | F-PIL |
| 6.3–6.4 | Imports / exports, intégrations | F-CNF-04, F-PIL-04, F-TAL-04 |
| 6.5 | Sécurité (mots de passe, accès limité, connectés, journal) | F-ADM-01, F-ADM-05, F-ADM-06, F-ADM-08 |
| 6.6 | Sauvegardes | F-PLT-06 |
| 6.7 | Aide en ligne | F-AID-01 |
