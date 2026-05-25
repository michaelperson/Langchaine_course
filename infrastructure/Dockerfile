# ============================================================
# Image de base : Python 3.11 slim (légère, stable, LTS)
# ============================================================
FROM python:3.11-slim
# On met à jour les index, on upgrade, et on nettoie tout de suite après
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Répertoire de travail à l'intérieur du conteneur
WORKDIR /workspace

# ============================================================
# Dépendances système
# - build-essential : compilation de paquets natifs (chromadb, tokenizers)
# - curl            : utilisé par le healthcheck du docker-compose
# - git             : nécessaire pour certains paquets HuggingFace
# - poppler-utils   : extraction d'images depuis les PDF (utile en RAG)
# ============================================================
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# Dépendances Python — Kit de Formation LangChain
# Installation en une seule couche pour optimiser le cache Docker
# ------------------------------------------------------------
# Strategie deux-niveaux :
#   - requirements.lock.txt (genere par lock.sh) : si present,
#     installe TOUTES les versions exactes (deps directes + transitives)
#     => reproductibilite parfaite
#   - requirements.txt (fallback) : versions exactes des deps directes
#     uniquement, pip resoud les transitives au moment du build
# ============================================================
COPY requirements*.txt ./
RUN pip install --upgrade pip && \
    if [ -f requirements.lock.txt ]; then \
      echo ">> Installation depuis requirements.lock.txt (reproductibilite totale)" && \
      pip install --no-cache-dir -r requirements.lock.txt; \
    else \
      echo ">> Installation depuis requirements.txt (deps directes pinnees)" && \
      pip install --no-cache-dir -r requirements.txt; \
    fi

# ============================================================
# Ports exposés
# - 8888 : Jupyter Lab
# - 8501 : Streamlit
# ============================================================
EXPOSE 8888
EXPOSE 8501

# ============================================================
# Commande par défaut : lancement de Jupyter Lab
# --ip=0.0.0.0    : accessible depuis l'hôte (hors conteneur)
# --allow-root    : requis car on tourne en root dans le conteneur
# --no-browser    : pas d'ouverture auto (environnement headless)
# --NotebookApp.token='' : désactive l'authentification par token
#                          (acceptable en environnement local fermé de formation)
# ============================================================
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--allow-root", \
     "--no-browser", \
     "--ServerApp.token=''", \
     "--ServerApp.password=''", \
     "--ServerApp.root_dir=/workspace"]
