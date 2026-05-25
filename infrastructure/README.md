# Infrastructure Docker — Formation LangChain Local

Ce dossier contient toute l'infrastructure nécessaire pour faire tourner la stack **100% locale** de la formation : Ollama (LLM), ChromaDB (base vectorielle), JupyterLab et Streamlit, le tout orchestré par Docker Compose.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Hôte (Windows / Mac / Linux)            │
│                                                          │
│   ┌────────────┐    ┌──────────────┐   ┌──────────────┐  │
│   │  Ollama    │    │ ollama-init  │   │ langchain-app│  │
│   │  :11434    │◄───┤ (pull gemma) │   │  :8888 (Jup) │  │
│   │            │    │              │   │  :8501 (Str) │  │
│   └─────┬──────┘    └──────────────┘   └──────┬───────┘  │
│         │                                      │         │
│         └──────────► réseau Docker ◄───────────┘         │
│                                                          │
│   Volumes persistants :                                  │
│   - ollama_data  (modèles LLM)                           │
│   - hf_cache     (embeddings HuggingFace)                │
│   - chroma_data  (index vectoriel)                       │
└──────────────────────────────────────────────────────────┘
```

## Pré-requis

| Composant | Version minimale | Vérification |
|-----------|------------------|--------------|
| Docker Engine | 24.0+ | `docker --version` |
| Docker Compose | v2.20+ | `docker compose version` |
| RAM disponible | 8 Go (16 Go recommandés) | — |
| Espace disque | 10 Go libres | — |
| Ports libres | 8888, 8501, 11434 | `netstat -ano \| findstr "8888"` |

> **Windows** : Docker Desktop avec WSL2 backend activé.
> **Mac Apple Silicon** : Docker Desktop natif ARM64.

## Démarrage — Étape par étape

### 1. Construire les images et lancer la stack

Depuis le dossier `infrastructure/` :

```bash
docker compose up -d --build
```

Ce qui se passe en arrière-plan :

1. **Ollama** démarre (image officielle, ~500 Mo).
2. **ollama-init** attend que l'API Ollama réponde, puis télécharge `gemma3:4b` (~3.3 Go). Compter **5 à 10 minutes** selon la connexion.
3. **langchain-app** se construit (~5 minutes la première fois — installation des paquets Python LangChain, ChromaDB, sentence-transformers, etc.).
4. Une fois l'init terminé, JupyterLab démarre sur le port 8888.

### 2. Vérifier l'état des services

```bash
docker compose ps
```

Tous les services doivent être en `running` (sauf `ollama-init` qui doit être en `exited (0)` — c'est normal, il a fini son boulot).

```bash
docker compose logs -f langchain-app
```

Cherche la ligne `Jupyter Server is running at: http://0.0.0.0:8888/lab`.

### 3. Tester Ollama

```bash
docker exec -it formation-ollama ollama list
```

Doit afficher `gemma3:4b`. Si tu veux tester une inférence :

```bash
docker exec -it formation-ollama ollama run gemma3:4b "Bonjour en français"
```

### 4. Accéder à JupyterLab

Ouvre dans ton navigateur : **http://localhost:8888/lab**

Tu débarques dans `/workspace` qui contient les dossiers `notebooks/`, `examples/`, `exercices/`, `data/`.

### 5. (Optionnel) Lancer Streamlit (Jour 2 — Module 9)

Streamlit n'est pas démarré automatiquement. Depuis l'intérieur du conteneur :

```bash
docker exec -it formation-langchain-app bash
cd /workspace/examples
streamlit run demo_streamlit_app.py --server.address=0.0.0.0
```

Puis ouvre **http://localhost:8501**.

## Commandes utiles

| Action | Commande |
|--------|----------|
| Démarrer | `docker compose up -d` |
| Arrêter (sans perdre les données) | `docker compose down` |
| Tout effacer (modèles, vectoriels, cache) | `docker compose down -v` |
| Logs en temps réel | `docker compose logs -f` |
| Reconstruire après modif Dockerfile | `docker compose up -d --build` |
| Shell dans le conteneur app | `docker exec -it formation-langchain-app bash` |
| Pull d'un autre modèle Ollama | `docker exec -it formation-ollama ollama pull <nom>` |

## URL Ollama dans les notebooks

À l'intérieur du conteneur `langchain-app`, Ollama est joignable via :

```python
OLLAMA_HOST = "http://ollama:11434"   # nom du service Docker
```

> Variable déjà injectée comme `os.environ["OLLAMA_HOST"]` par le docker-compose.

Si tu travailles **hors Docker** (Python local sur l'hôte qui parle au conteneur Ollama), utilise :

```python
OLLAMA_HOST = "http://localhost:11434"
```

## Points d'attention pour le formateur

1. **Le premier `up` est lent.** Préviens les apprenants. Idéalement, fais tourner le `up --build` la veille de la formation.
2. **Si gemma3:4b échoue à télécharger** (réseau d'entreprise filtrant), tu peux pré-télécharger l'image localement et la copier sur les machines via `docker save / docker load`.
3. **Apple Silicon** : Ollama tourne en CPU dans Docker (pas de Metal acceleration). Compte 2-5 secondes par token sur gemma3:4b. C'est utilisable mais lent. Pour de meilleures perfs, installe Ollama nativement sur le Mac et fais pointer le `OLLAMA_HOST` sur `http://host.docker.internal:11434`.
4. **Windows + Defender** : exclus le dossier `formateurWorkspace` du scan temps-réel pour gagner 30-50% sur les I/O.

## Trainer's Note

Le pattern "init container" (`ollama-init` qui pull le modèle puis s'éteint) est un classique Kubernetes qu'on retrouve souvent dans les stacks ML d'entreprise. Pédagogiquement, c'est une bonne porte d'entrée pour parler **séparation des responsabilités** : un service = une responsabilité, et l'initialisation est un service à part entière.

## DevOps / Security Check

- [ ] Token Jupyter désactivé : OK pour formation, **JAMAIS** en prod (utiliser `JUPYTER_TOKEN` env var).
- [ ] Volumes nommés (pas de bind mount sur les modèles) : performance I/O optimale.
- [ ] Healthcheck Ollama configuré : évite les races au démarrage.
- [ ] Télémétrie ChromaDB désactivée : conformité RGPD pour environnements sensibles.
- [ ] `host.docker.internal` mappé : permet de pointer un Ollama natif si besoin.
