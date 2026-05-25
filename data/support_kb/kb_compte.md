# Gestion des comptes utilisateurs et mots de passe

## Réinitialiser un mot de passe Active Directory

Pour réinitialiser un mot de passe Active Directory :

1. Rendez-vous sur le portail self-service interne : **password.entreprise.local**.
2. Authentifiez-vous avec votre identifiant Windows et répondez à vos questions de sécurité.
3. Choisissez un nouveau mot de passe respectant la politique :
   - Minimum 12 caractères.
   - Majuscules + minuscules + chiffres + caractère spécial.
   - Pas de réutilisation des 5 derniers mots de passe.
4. Le nouveau mot de passe est synchronisé sur l'annuaire AD en moins de 5 minutes.

## Compte verrouillé après plusieurs tentatives

Le compte est automatiquement verrouillé après **5 tentatives infructueuses**. Le déverrouillage se fait :

- Automatiquement après 30 minutes.
- Manuellement via le portail self-service (en répondant aux questions de sécurité).
- En contactant le support N1 si les questions de sécurité sont oubliées.

## Création d'un nouveau compte (arrivée collaborateur)

Le manager doit faire la demande **5 jours ouvrés avant l'arrivée** via le portail RH (`rh.entreprise.local`). Le formulaire demande :

- Nom, prénom, date d'arrivée.
- Service et manager direct.
- Logiciels d'accès nécessaires (Office 365, ERP, applications métier).
- Niveau d'habilitation pour les dossiers partagés.

Le compte est créé automatiquement la veille au soir, et l'identifiant + mot de passe initial sont envoyés au manager.

## Désactivation de compte (départ collaborateur)

À la date de départ, le compte est **désactivé automatiquement** (pas supprimé). La boîte mail reste consultable pendant 90 jours par le manager via une délégation.

Au-delà de 90 jours, suppression définitive après archivage légal selon la politique RGPD interne.

## Authentification à deux facteurs (MFA)

L'activation du MFA est **obligatoire** pour tous les comptes accédant aux applications cloud (Office 365, VPN, ERP). L'application recommandée est **Microsoft Authenticator**.

Pour réinscrire un appareil après changement de téléphone :

1. Connectez-vous depuis un poste interne au portail `mfa.entreprise.local`.
2. Cliquez sur "Réinitialiser mes facteurs".
3. Scannez le nouveau QR code avec Microsoft Authenticator.
