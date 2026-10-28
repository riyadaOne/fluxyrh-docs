# W06.2 — Temps de travail · Pointage (EMP, borne, SYS)

Dépôt : `FluxyRH-web/app/` (fluxyrh-w-app) · Dépend de : W06.1 · Suite : W06.3 (manager)

## 1. Objet

Recevoir et juger chaque pointage, puis en tirer les journées de présence et les minutes réalisées des heures supplémentaires établies. Le serveur vérifie le **code temporel** de la borne, la **carte** de l'employé, le site, l'appareil, l'anti-rejeu et la fenêtre hors ligne, corrige l'horloge de l'appareil, enregistre le pointage `Accepté` ou `Refusé` avec motif, puis recalcule la journée. C'est le cœur anti-fraude du produit (NF-05). À la fin de W06.2, des pointages simulés (téléphone et borne, en ligne et hors ligne) produisent des journées et des heures sup réalisées exactes ; les apps qui les émettront arrivent en E04 et B02.

## 2. Ce que le pointage reçoit, produit, transmet

| Acteur | Reçoit | Produit | Transmet à |
|---|---|---|---|
| **EMP** (téléphone) | QR de la borne, sa carte active, son téléphone enregistré (W05) | Un pointage signé par sa carte | Serveur |
| **Borne** | Sa clé HMAC (W03), la carte posée | Un pointage signé par la borne | Serveur |
| **SYS** | Pointages, plannings, jours fériés, règles (W06.1) | Pointages `acceptee` / `refusee`, journées calculées, minutes réalisées des heures sup établies | **Manager** (W06.3) : refus à corriger ; **RH** (W06.4) ; paie (W09) |

## 3. Exigences couvertes et lectures

| Exigence | Objet |
|---|---|
| F-TPS-02 | Pointage QR + carte, téléphone ou borne |
| F-TPS-03, F-ORG-06 (réception) | Hors ligne, correction d'horloge, fenêtre bornée |
| F-TPS-04 | Heures travaillées, retard, départ anticipé, absence, selon le planning |
| F-TPS-06 (réalisation) | Minutes réalisées des heures sup établies, selon les règles |
| F-NFC-06 (pointage) | Confirmation du pointage par la carte |
| F-TPS-08 (serveur) | Pointage de secours de la borne, statut « à valider » |
| NF-05, T-11, T-15 | Anti-fraude, créations idempotentes par UUID d'appareil |

À lire : PRD §7.6 ; TRD §12 (en entier), §20 ; APPFLOW §5.6, §5.7, §7 ; BACKEND SCHEMA §5.6, §8, §9 (points 3, 8) ; UX/UI §7.3.

## 4. Prérequis et décisions

W06.1 livré.

| Sujet | Proposition |
|---|---|
| Journée de rattachement (travail de nuit) | Un pointage appartient à la journée **planifiée** dont la fenêtre le contient : de X minutes avant le début prévu à Y minutes après la fin prévue, X et Y **réglés par l'entreprise** (W06.1.2), dans le fuseau du site ; à défaut de planning, à la journée de l'entrée ouverte de moins de 16 h, sinon au jour calendaire. Une journée qui passe minuit porte la mention **« travail de nuit »** (colonne `is_night_work` sur `attendance_days`) |
| Demi-journée | **Paramétrable par l'entreprise** (W06.1.2) : statut `demi_journee` activé ou non, seuil minimum d'une demi-journée et seuil d'une journée complète, en % du temps attendu ; sous le premier seuil, sans justification, la journée est `absent` |
| Absence | Constatée par une tâche du lendemain matin (fuseau du site) pour chaque jour ouvré sans pointage ; les congés (W07) et jours fériés remplacent l'absence |
| Inversion du sens | Faite sur l'appareil pendant une durée **réglée par l'entreprise** (W06.1.2), transmise aux apps et aux bornes ; l'appareil envoie le sens et `direction_inverted_at` ; le serveur ne l'accepte que dans ce délai après la capture |
| Heures sup | **Rien n'est compté automatiquement** : le temps passé après l'horaire ne devient une heure sup que si le manager l'a **établie à l'avance** pour cet employé et ce jour (W06.3) ; le système calcule alors les minutes réellement faites, dans la limite de ce qui a été établi |
| Signature du pointage | Chaque pointage accepté crée une `action_signature` (`pointage`, canal, appareil ou borne) |
| Pointage de secours (borne) | Construit ici pour l'app Borne (B03) : « Je n'ai pas ma carte » → matricule → photo prise par la borne → statut **`a_valider`** (nouvelle valeur de `ClockingStatus`), qui ne compte qu'après la validation du manager (W06.3) ; nombre maximal par employé et par mois réglé par l'entreprise (W06.1.2) ; photo sur le disque privé |
| Confirmation hors ligne sur la borne | La borne garde en cache chiffré la liste des cartes actives des employés autorisés sur son site (empreinte de la carte, nom, photo), fournie par `/kiosk/config` et mise à jour à chaque signal de vie (décision de B02) |
| Carte inconnue | Un pointage dont la carte n'est rattachée à aucun employé de l'entreprise est refusé **sans être stocké** (pas d'employé à qui l'attribuer) et compté dans le journal de la borne |
| Période de paie clôturée | Le refus « période clôturée » est ajouté en W09.6, quand les périodes existent |

## 5. Statuts traversés

| Objet | Transitions | Acteur |
|---|---|---|
| Pointage `clockings.status` | (réception) `acceptee` / `refusee` + motif ; jamais modifié ensuite, sauf l'inversion du sens dans les 10 s | SYS |
| Journée `attendance_days.status` | recalculée : `present`, `retard`, `demi_journee`, `absent`, `ferie`, `repos` (`conge` en W07) | SYS |
| Heures sup | minutes réalisées recalculées tant que le RH n'a pas décidé | SYS |

Motifs de refus (liste fermée, traduits) : code invalide ou expiré, carte inactive, carte d'un autre employé, site non autorisé, appareil non enregistré, pointage par téléphone désactivé, rejeu, fenêtre hors ligne dépassée, borne révoquée ou suspendue.

## 6. Étapes ordonnées

### W06.2.1 — Enums

- `ClockingStatus`, `ClockingDirection`, `ClockingRefusal` (motifs, à ajouter au BACKEND SCHEMA §7), `AttendanceDayStatus`, `OvertimeStatus` (`OvertimeSource` retiré : toute heure sup est établie par le manager).

### W06.2.2 — Code temporel

- `App\Support\TimeBasedCode` : `code(secret, step)` = HMAC-SHA256 tronqué ; `stepAt(instant, stepSeconds)` ; `verify(secret, step, code, expectedStep, tolerance)` avec comparaison à temps constant.
- Clé de la borne au moment de la capture : clé courante, ou clé précédente pour un pointage capturé avant son renouvellement (W03, décision sur le renouvellement).
- Suite de tests **codes temporels** (TRD §24) : limites de pas, ±1 pas en ligne, ±2 pas hors ligne, horloge de l'appareil en avance et en retard, changement de pas pendant le scan, clé renouvelée, code d'une autre borne.

### W06.2.3 — Réception des pointages

- Migration `clockings` (sans `payroll_period_id` : les journées portent la période en W09.3).
- `App\Services\Tenant\ClockingService::receive()` : pour chaque pointage, dans l'ordre :
  1. identifiant déjà connu → renvoi du résultat déjà enregistré (idempotence) ;
  2. correction d'horloge : `effective_at = captured_at + (reçu − sent_at)` (TRD §12.4) ;
  3. borne active (ou capture antérieure à sa révocation, refusée avec un motif qui permet la correction du manager) ;
  4. carte connue, active, appartenant à l'employé ;
  5. site de la borne parmi les sites autorisés de l'employé ;
  6. téléphone : pointage par téléphone autorisé, appareil enregistré au nom de l'employé ; code valide pour le pas ;
  7. anti-rejeu `(employé, borne, pas)` ;
  8. fenêtre hors ligne ;
  9. sens (alternance sur la journée de rattachement, inversion contrôlée) ;
  10. écriture `acceptee` ou `refusee`, signature d'action, journal ; recalcul de la journée mis en file après commit.
- Traitement par lots (file hors ligne d'un appareil) : chaque pointage jugé séparément, ordre par `captured_at`.

**Critère de fin** : chaque motif de refus produit par un test dédié ; un lot rejoué deux fois ne crée aucun doublon.

### W06.2.4 — API de pointage

- `/api/v1/employee/clockings` (POST, lot, UUID générés par l'appareil ; GET, historique personnel) ; `/employee/clockings/{id}` (résultat).
- `/api/v1/kiosk/clockings` (POST, lot signé par la borne, W03.6) ; `/kiosk/heartbeat` enrichi du nombre de pointages reçus et refusés.
- `/api/v1/kiosk/config` enrichi : durée du bouton « Inverser » (W06.1.2) et liste des cartes actives des employés autorisés sur le site (§4).
- `/api/v1/kiosk/emergency-clockings` : pointage de secours (matricule, photo, signé par la borne), limite mensuelle contrôlée, statut `a_valider` (§4).
- Réponse par pointage : statut, motif traduit, nom et photo vérifiés pour l'écran de confirmation.
- Limites de débit adaptées aux bornes (arrivées groupées le matin).
- Contrat Scramble à jour.

### W06.2.5 — Calcul des journées

- Migration `attendance_days` (sans `payroll_period_id`, ajouté en W09.3).
- `App\Services\Tenant\AttendanceComputationService::recompute(employee, workDate)` : journée de rattachement (§4), planning et jour attendu (W06.1), première entrée, dernière sortie, minutes travaillées (pauses déduites selon le planning), retard (au-delà de la tolérance), départ anticipé, statut (§4) ; une journée corrigée par le manager (`is_corrected`) n'est plus recalculée depuis les pointages.
- Tâche planifiée de constat des absences (§4), par entreprise et par fuseau de site.
- Recalcul d'une plage (commande) après un changement de planning ou de jour férié, limité aux journées non corrigées.

**Critère de fin** : jeu de journées types (normale, retard, départ anticipé, demi-journée, absence, jour férié travaillé, repos travaillé, nuit à cheval sur minuit, sans planning) calculé exactement.

### W06.2.6 — Heures supplémentaires réalisées

- Migration `overtime_entries` (sans `payroll_period_id`) : les heures sup sont **établies à l'avance** par le manager (W06.3) ; sans heure sup établie, le temps passé au-delà du planning **n'est pas compté** (§4).
- `App\Services\Tenant\OvertimeService::computeRealised(day)` : pour une heure sup établie, minutes réellement faites d'après les pointages (au plus le nombre établi), découpées par nature (jour ouvré, nuit, repos, férié) et par tranche selon les règles ; recalculées tant que le RH n'a pas décidé.

**Critère de fin** : jeu de semaines types (heures établies et faites, établies mais non faites, faites sans être établies, nuit, jour férié) donne les minutes attendues.

### W06.2.7 — Mes pointages

- S-63 `/me/clockings` : pointages acceptés et refusés (motif), journées du mois, heures sup établies et réalisées ; aucune modification.

### W06.2.8 — Outils de développement

- Commande `fluxyrh:dev-kiosk-code {borne}` : affiche le code et le QR courant d'une borne de démonstration ; client de pointage simulé (téléphone et borne, en ligne et hors ligne avec horloge décalée) utilisé par les tests et la recette ; **refusés en production**.

### W06.2.9 — Documentation et livraison

- `02-reference/` : protocole de pointage (charges utiles, en-têtes, signatures, codes de refus) écrit pour l'équipe mobile ; règles de calcul.
- Livraison dans `06-livraisons/`, ligne au `JOURNAL.md`, statut W06.2 dans la ROADMAP.

## 7. Tests attendus

| Domaine | Cas |
|---|---|
| Codes temporels | Suite dédiée (W06.2.2) |
| Réception | Chaque motif de refus ; carte inconnue non stockée ; idempotence ; lot désordonné ; borne révoquée avant ou après la capture |
| Hors ligne | Correction d'horloge, ±2 pas, fenêtre dépassée de peu |
| Sens | Alternance, inversion dans le délai réglé acceptée, au-delà refusée |
| Journées | Jeu de journées types (W06.2.5), fenêtre du travail de nuit réglée, mention « travail de nuit », journée corrigée non recalculée, recalcul de plage |
| Heures sup | Jeu de semaines types ; temps hors heures sup établies jamais compté |
| Signature | Une signature `pointage` par pointage accepté |
| Droits | Employé : ses seuls pointages ; borne : sa seule entreprise ; autre entreprise ; version d'app |
| Performance | 500 pointages d'une borne reçus en un lot en moins de 10 s |

## 8. Critères de sortie

- Tests ciblés W06.2 verts, dont la suite des codes temporels ; suite complète lancée par le développeur ; Pint et Larastan sans erreur.
- Recette APPFLOW §5.6 avec le client simulé (téléphone et borne, en ligne et hors ligne).
- Documentation et livraison de W06.2.9 faites.

## 9. Reporté

| Élément | Module |
|---|---|
| Correction motivée, heures sup établies par le manager | W06.3 |
| Validation des heures sup, feuilles de temps | W06.4 |
| Statut `conge` des journées | W07 |
| Rattachement à la période de paie, refus « période clôturée » | W09.3, W09.6 |
| Écrans de pointage | E04 (téléphone), B02 (borne) |
