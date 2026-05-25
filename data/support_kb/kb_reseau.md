# Réseau et connectivité

## VPN d'entreprise — GlobalProtect

L'entreprise utilise **GlobalProtect** comme client VPN. Le portail d'authentification est : **vpn.entreprise.local**.

### Première installation

1. Téléchargez GlobalProtect depuis le portail self-service `software.entreprise.local`.
2. À la première ouverture, saisissez le portail : `vpn.entreprise.local`.
3. Authentifiez-vous avec votre identifiant Windows et le code MFA (Microsoft Authenticator).

### Échec de connexion VPN — Diagnostic

Si la connexion VPN échoue, vérifier dans cet ordre :

1. **Connexion Internet locale** : tester en ouvrant un site web sans VPN.
2. **Antivirus / pare-feu** : certains antivirus tiers (Norton, McAfee) bloquent GlobalProtect. Ajouter une exception.
3. **VPN concurrent** : désactiver tout autre VPN actif (NordVPN, ExpressVPN, etc.) — un seul tunnel à la fois.
4. **Code MFA** : vérifier que l'heure du téléphone est synchronisée (un décalage de plus de 30s casse les codes TOTP).
5. **Logs GlobalProtect** : clic droit sur l'icône → Settings → Troubleshooting → Collect Logs.

Si rien ne fonctionne, créer un ticket catégorie "reseau" avec :
- Capture d'écran de l'erreur.
- Logs GlobalProtect.
- Localisation (domicile, hôtel, autre entreprise…).

## Wi-Fi entreprise — SSID et certificats

Trois SSID disponibles dans les locaux :

| SSID | Usage | Authentification |
|------|-------|------------------|
| `ENTREPRISE-CORP` | Postes de travail managés | Certificat machine + identifiant Windows |
| `ENTREPRISE-BYOD` | Téléphones et ordinateurs personnels | Identifiant + MFA |
| `ENTREPRISE-GUEST` | Visiteurs | Code temporaire fourni à l'accueil |

### Le Wi-Fi est instable dans une salle

Symptômes : déconnexions fréquentes, débit lent, perte du signal.

Avant de signaler le problème, faire un **test de débit** (`speedtest.net`) à plusieurs endroits de la salle pour cartographier la zone faible. Joindre cette info au ticket — ça permet à l'équipe réseau d'identifier les bornes Wi-Fi à renforcer.

## Coupure d'accès aux serveurs de fichiers

Si **plusieurs utilisateurs simultanément** ne peuvent plus accéder aux serveurs de fichiers :

- C'est probablement une **panne réseau** ou un incident sur le serveur de fichiers principal.
- **Ne pas créer plusieurs tickets** : un seul ticket P1 suffit (le support détectera l'incident global).
- Communiquer le périmètre exact : étage, service, application impactée.

## Lenteur réseau persistante (1 utilisateur)

Si **un seul utilisateur** a une lenteur :

1. Tester un câble Ethernet différent.
2. Tester un autre port réseau (changer de prise murale).
3. Mesurer le débit en filaire vs Wi-Fi.
4. Si la lenteur est uniquement sur certaines applications cloud → souvent un problème **DNS**, pas réseau pur.
