# Logiciels — Outlook, Office 365, ERP

## Outlook plante au démarrage — "Profil corrompu"

Symptôme : Outlook se ferme brutalement au démarrage, ou affiche le message **"Le profil Outlook est corrompu"** ou **"Impossible de démarrer Microsoft Outlook"**.

### Procédure de réparation

1. Fermer complètement Outlook (vérifier dans le Gestionnaire des tâches qu'aucune instance `outlook.exe` ne tourne).
2. Ouvrir le **Panneau de configuration** Windows.
3. Cliquer sur **Mail** (si pas visible : changer l'affichage en "Petites icônes").
4. Cliquer sur **Afficher les profils**.
5. Cliquer sur **Ajouter** pour créer un nouveau profil :
   - Donner un nom (ex: `Outlook2`).
   - Saisir l'adresse mail professionnelle.
   - Laisser Outlook auto-configurer (Exchange Online).
6. Définir le nouveau profil comme **profil par défaut** : "Toujours utiliser ce profil".
7. Redémarrer Outlook — il devrait se synchroniser avec Exchange Online (5 à 30 minutes selon la taille de la boîte).

Une fois le nouveau profil fonctionnel, l'ancien profil corrompu peut être supprimé pour libérer de l'espace.

### Si la création du profil échoue

- Vérifier la connexion Internet.
- Vérifier que le compte n'est pas verrouillé (cf. `kb_compte.md`).
- Lancer **Outlook en mode sans échec** : `Ctrl + clic` sur l'icône Outlook → confirmer le mode sans échec. Si Outlook démarre, le problème vient d'un complément (add-in).

## Excel plante en ouvrant un fichier

Symptôme : Excel se fige ou se ferme brutalement à l'ouverture d'un fichier précis.

### Premiers réflexes

1. **Désactiver les compléments** : Fichier → Options → Compléments → Gérer "Compléments COM" → Atteindre → décocher tout.
2. **Ouvrir en mode sans échec** : `excel.exe /safe` depuis un Run.
3. **Réparer Office** : Panneau de configuration → Programmes → Microsoft Office → Modifier → Réparation rapide (puis Réparation en ligne si nécessaire).

### Si le fichier est lourd

Au-delà de 50 Mo, Excel peut planter sur des macros lourdes ou des liens externes. Solutions :
- Diviser le fichier en plusieurs onglets ou fichiers.
- Convertir les formules en valeurs (`Ctrl+C` → Coller spécial → Valeurs).
- Migrer vers Power BI ou Power Query pour les gros volumes.

## ERP métier (Sage X3) — Connexion impossible

Le client Sage X3 utilise une connexion sécurisée vers le serveur applicatif interne `sagex3.entreprise.local`.

### En cas d'échec de connexion

1. Vérifier que le **VPN GlobalProtect est actif** (cf. `kb_reseau.md`) — Sage X3 n'est pas exposé sur Internet.
2. Vérifier l'**heure système** : un décalage casse l'authentification Kerberos.
3. **Vider le cache** du client Sage : `%APPDATA%\Sage\X3\cache` → tout supprimer puis relancer.
4. Vérifier les **droits applicatifs** auprès de votre référent ERP métier.

## Microsoft Teams — Audio ou vidéo qui plante

Symptômes : pas de son, micro qui se coupe, vidéo en mosaïque verte.

### Procédure

1. Vérifier les **autorisations** : Paramètres Windows → Confidentialité → Microphone / Caméra → autoriser Teams.
2. **Réinitialiser Teams** : clic droit sur l'icône Teams → Quitter, puis supprimer le dossier `%AppData%\Microsoft\Teams` puis relancer Teams.
3. Mettre à jour Teams (clic sur l'avatar → "Vérifier les mises à jour").
4. Tester un **appel test** Teams (depuis Paramètres → Périphériques → Effectuer un appel test).

## Politique de patching Office

Les mises à jour Office sont déployées **automatiquement** via Microsoft Update :

- Mises à jour de sécurité : **dans les 48h** suivant publication.
- Mises à jour de fonctionnalités : **mensuelles**, le 2e mardi du mois.

En cas de besoin urgent d'une mise à jour, le support N2 peut forcer le patch via SCCM. Créer un ticket P3 catégorie "logiciel".
