# Procédures matériel — Imprimantes, écrans, périphériques

## Imprimante en panne — Procédure de premier niveau

En cas de panne d'imprimante (ne s'allume pas, n'imprime que des pages blanches, bourrage répété) :

1. **Vérifier l'alimentation** : câble bien branché, prise testée avec un autre appareil.
2. **Vérifier le câble réseau** ou le Wi-Fi (selon le modèle). Le voyant réseau doit être vert et fixe.
3. **Vérifier les niveaux de toner / d'encre** depuis l'écran de l'imprimante.
4. **Redémarrer le spooler Windows** sur le poste qui imprime :
   - `Touche Windows + R` → taper `services.msc` → Entrée.
   - Trouver "Spouleur d'impression" (Print Spooler).
   - Clic droit → Redémarrer.
5. **Réinstaller la file d'impression** si le redémarrage ne suffit pas (Panneau de configuration → Périphériques et imprimantes → Supprimer → Ajouter une imprimante).

Si la panne persiste après ces 5 étapes, créer un ticket P3 catégorie "materiel" en précisant le **modèle** et le **numéro de série** (étiquette à l'arrière de l'imprimante).

## Pages blanches uniquement

Symptôme : l'imprimante avance le papier mais sort des pages vierges.

Causes typiques :
- Cartouche de toner vide ou mal insérée.
- Tambour à remplacer (visible sur l'écran).
- Buses encrassées sur les imprimantes jet d'encre → lancer le **cycle de nettoyage des buses** depuis le menu maintenance.

## Écran secondaire non détecté

1. Vérifier le câble vidéo (HDMI / DisplayPort) — essayer un autre câble si possible.
2. Forcer la détection : `Touche Windows + P` → choisir "Étendre".
3. Mettre à jour le pilote graphique (Intel / NVIDIA / AMD) via le Gestionnaire de périphériques.
4. Si l'écran reste noir, essayer sur un autre poste pour isoler le défaut écran vs poste.

## Demande de matériel (commande)

Toute demande de **nouveau matériel** (souris, clavier, casque, écran) passe par le **portail Achats** (`achats.entreprise.local`). Il faut :

- L'accord du manager direct.
- Une justification métier.
- Le code analytique du service.

Délai de livraison standard : 5 à 10 jours ouvrés.

## Casque audio — Problème de micro

1. Vérifier que le casque est bien sélectionné dans **Paramètres → Son → Périphérique d'entrée**.
2. Tester le micro dans **Sons → Onglet Enregistrement → Niveaux**.
3. Sur Teams / Zoom : vérifier dans les paramètres de l'application elle-même.
4. Si rien : essayer le casque sur un autre poste pour isoler le défaut.
