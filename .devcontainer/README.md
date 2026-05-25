# Dev Container VSCode — Formation LangChain

Ce dossier permet à VSCode de **s'attacher directement à l'intérieur** du conteneur Docker `langchain-app`. Plus de problèmes de lenteur Pylance, plus de désync entre IDE et kernel : tout l'environnement Python tourne côté Linux.

## Pourquoi un Dev Container ?

Quand tu ouvres un notebook depuis VSCode sur Windows alors que le kernel tourne dans Docker, tu cumules deux pénalités :

1. **Pylance scanne ton venv local** (qui n'est même pas le bon — les libs sont dans le conteneur).
2. **L'extension Jupyter requête des variables** à travers la frontière Windows/WSL/Docker.

Avec un Dev Container, VSCode lance Pylance, l'extension Jupyter et le terminal **dans le conteneur**. C'est instantané, et tu travailles dans le même environnement que le code en exécution. C'est aussi le pattern recommandé en entreprise pour garantir la reproductibilité (un seul `Reopen in Container` et tout fonctionne, peu importe l'OS de la machine).

## Pré-requis

| Composant | Vérification |
|-----------|--------------|
| Docker Desktop (lancé) | `docker info` |
| VSCode | 1.80+ |
| Extension VSCode **Dev Containers** (id `ms-vscode-remote.remote-containers`) | À installer depuis le Marketplace |

## Démarrage — Étape par étape

### 1. Cloner ou ouvrir le dossier formation dans VSCode

Ouvre `formateurWorkspace/` comme dossier racine dans VSCode (`File → Open Folder`).

### 2. Reopen in Container

VSCode détecte automatiquement le `.devcontainer/devcontainer.json` et propose en bas à droite :

> **Folder contains a Dev Container configuration file. Reopen folder to develop in a container.**

Clique sur **Reopen in Container**.

Si la notification a disparu : `Ctrl+Shift+P` → **"Dev Containers: Reopen in Container"**.

### 3. Premier démarrage (~5 minutes)

VSCode va :

1. Lancer la stack `docker compose up` complète (Ollama + init + langchain-app).
2. Télécharger `gemma4` (~3.3 Go) si pas déjà fait — patience.
3. Installer les extensions VSCode listées dans le `devcontainer.json` à l'intérieur du conteneur.
4. Ouvrir un terminal pointant directement sur `/workspace`.

À la fin, tu vois en bas à gauche : **Dev Container: LangChain Formation (Local Stack)**.

### 4. Vérification

Dans le terminal VSCode (qui est maintenant un bash Linux du conteneur) :

```bash
python --version          # Python 3.11.x
pip list | grep langchain # toutes les libs LangChain installées
echo $OLLAMA_HOST         # http://ollama:11434
curl $OLLAMA_HOST/api/tags # liste des modèles Ollama disponibles
```

Ouvre n'importe quel notebook dans `notebooks/jour1/` — le kernel `Python 3` est sélectionné automatiquement.

## Workflow quotidien

| Action | Comment |
|--------|---------|
| Réouvrir le dossier en local (sortir du conteneur) | `Ctrl+Shift+P` → "Dev Containers: Reopen Folder Locally" |
| Reconstruire le conteneur après modif Dockerfile | `Ctrl+Shift+P` → "Dev Containers: Rebuild Container" |
| Redémarrer la stack complète | Ferme VSCode, `docker compose down && docker compose up -d` puis ré-ouvre |

## Points d'attention

1. **Le port 8888 (JupyterLab) reste accessible** depuis ton navigateur sur `http://localhost:8888` même quand tu utilises le Dev Container — c'est pratique pour les apprenants qui préfèrent l'interface web.
2. **Les fichiers que tu modifies** dans le Dev Container sont sauvegardés dans `formateurWorkspace/` sur ton disque (volume monté) — rien n'est perdu si le conteneur est détruit.
3. **`pip install`** dans le terminal du Dev Container persiste **uniquement le temps du conteneur**. Pour ajouter une dépendance permanente, modifie le `Dockerfile` et reconstruis.

## Trainer's Note

Le Dev Container est un excellent vecteur pédagogique pour parler de **environnements reproductibles**. Demande à un apprenant qui a installé Python 3.10 + un autre qui a installé Python 3.12 d'ouvrir le même dev container : ils obtiennent **exactement** la même version de Python, des libs et de l'OS. C'est exactement ce qui distingue un setup amateur d'un setup d'équipe.

## DevOps / Security Check

- [ ] `devcontainer.json` versionné dans git : reproductibilité totale pour tous les apprenants.
- [ ] Aucun secret en dur dans `devcontainer.json` (utiliser `runArgs` + variables d'env si besoin).
- [ ] Le conteneur tourne en root (acceptable pour formation, à changer en prod via `remoteUser`).
- [ ] Extensions VSCode épinglées dans `customizations.vscode.extensions` : pas de surprise sur la version d'une extension.
