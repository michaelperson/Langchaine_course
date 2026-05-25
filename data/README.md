# formateurWorkspace — Formation LangChain : De la théorie à la mise en production (Stack 100% Locale)

> **Public :** développeurs juniors à intermédiaires, bases en Python.
> **Durée :** 2 jours / 14 heures.
> **Stack :** Ollama (gemma3:4b) + LangChain + ChromaDB + HuggingFaceEmbeddings — **100% local**, aucune clé API, aucune donnée qui sort du réseau.
> **Fil rouge :** construire un **Assistant Support Technique Local** qui répond depuis votre doc interne et structure des tickets de support.

---

## Vue d'ensemble du fil rouge

L'Assistant Support Technique Local construit au fil des 10 modules :

| Capacité | Module qui l'introduit | Détail |
|----------|-------------------------|--------|
| Réponses techniques précises basées sur la doc interne | J1-M1 → J1-M4 | RAG sur les Markdown de `data/support_kb/` |
| Recherche documentaire automatique (PDF + Markdown) | J1-M5 | Pipeline d'ingestion + chunking + indexation Chroma |
| Structuration de tickets (catégorie / priorité / résumé) | J1-M2, J2-M8 | JsonOutputParser + validation Pydantic |
| Création automatique de tickets via langage naturel | J2-M7 | Agent + tool `creer_ticket` |
| Interface utilisateur conversationnelle | J2-M9 | App Streamlit complète |
| 100% local et sécurisé | tout | Ollama + Chroma local, télémétrie désactivée |

---

## Arborescence

```
formateurWorkspace/
│
├── README.md                       # ← ce fichier (point d'entrée)
│
├── infrastructure/                 # 🐳 Docker stack (Ollama + LangChain + Streamlit)
│   ├── README.md                   # comment démarrer la stack, dépannage
│   ├── Dockerfile                  # image Python + libs LangChain
│   └── docker-compose.yml          # 3 services + volumes persistants
│
├── .devcontainer/                  # 💻 Dev Container VSCode
│   ├── README.md                   # pourquoi & comment "Reopen in Container"
│   └── devcontainer.json           # config Pylance + Jupyter optimisée
│
├── notebooks/                      # 📚 Cours principal (10 modules)
│   ├── README.md                   # programme + astuces formateur
│   ├── jour1/                      # Fondations & RAG
│   │   ├── 01_lcel_intro.ipynb
│   │   ├── 02_ollama_prompts_parsers.ipynb
│   │   ├── 03_embeddings_chromadb.ipynb
│   │   ├── 04_rag_local.ipynb
│   │   └── 05_ingestion_pdf_md.ipynb
│   └── jour2/                      # Workflows, Agents & Interfaces
│       ├── 06_few_shot_cot.ipynb
│       ├── 07_agents_tools.ipynb
│       ├── 08_pydantic_tickets.ipynb
│       ├── 09_streamlit_ui.ipynb
│       └── 10_debogage_limites.ipynb
│
├── examples/                       # 🎬 Démos LIVE pour le formateur
│   ├── README.md                   # quand utiliser quel script
│   ├── demo_lcel_simple.py         # 30s — première chaîne
│   ├── demo_rag_quickstart.py      # RAG complet en 80 lignes
│   ├── demo_agent_tools.py         # agent qui appelle des tools
│   └── demo_streamlit_app.py       # UI complète à lancer
│
├── exercices/                      # ✏️ Pratique apprenants
│   ├── README.md
│   ├── enonces/                    # 10 énoncés (consigne MD + cellules vides)
│   │   ├── README.md
│   │   ├── ex01_premier_lcel.ipynb
│   │   └── … (10 énoncés)
│   └── solutions/                  # 10 solutions + README de démarche
│       ├── README.md
│       ├── ex01_premier_lcel_SOLUTION.ipynb
│       ├── README_ex01.md          # explique COMMENT arriver à la solution
│       └── …
│
└── data/                           # 📂 Dataset fil rouge
    ├── README.md                   # comment ajouter ses propres documents
    └── support_kb/                 # base de connaissance support fictive
        ├── kb_compte.md            # comptes / MDP / MFA
        ├── kb_materiel.md          # imprimantes / écrans / périphériques
        ├── kb_reseau.md            # VPN / Wi-Fi / coupures
        └── kb_logiciel.md          # Outlook / Excel / Teams / ERP
```

---

## Démarrage rapide (formateur)

### La veille de la formation (15 minutes)

1. **Cloner ou copier** `formateurWorkspace/` sur la machine de présentation.
2. **Construire la stack** :
   ```bash
   cd infrastructure
   docker compose up -d --build
   ```
   Ce qui se passe : pull Ollama, téléchargement de **gemma3:4b** (~3.3 Go), construction de l'image Python, démarrage de JupyterLab. **5-10 minutes**.
3. **Précharger les modèles** en exécutant le Module 1 et le Module 3 :
   ```bash
   docker exec -it formation-langchain-app bash
   cd /workspace/notebooks/jour1
   jupyter nbconvert --to notebook --execute 01_lcel_intro.ipynb --output /tmp/_warmup_01.ipynb
   jupyter nbconvert --to notebook --execute 03_embeddings_chromadb.ipynb --output /tmp/_warmup_03.ipynb
   ```
   Tu charges Ollama + le modèle d'embeddings dans le cache. Pas de blanc en formation.
4. **Vérifier** que tout marche :
   ```bash
   docker exec formation-ollama ollama list           # gemma3:4b doit être listé
   curl http://localhost:8888                         # JupyterLab répond
   ```

### Pendant la formation

- **Ouvrir JupyterLab** : http://localhost:8888 (les apprenants y accèdent aussi via leur navigateur si tu fais une session distribuée).
- **Ou ouvrir VSCode** sur le dossier `formateurWorkspace/` puis "Reopen in Container".
- **Garder un terminal ouvert** sur `docker compose logs -f langchain-app` pour voir les requêtes en temps réel.

### À la fin

```bash
docker compose down            # arrête tout (les modèles et l'index sont conservés)
docker compose down -v         # arrête tout ET efface modèles + index (reset complet)
```

---

## Démarrage rapide (apprenant)

### Pré-requis sur ton poste

| Composant | Version | Vérification |
|-----------|---------|--------------|
| Docker Desktop | 24+ | `docker --version` |
| VSCode | 1.80+ | + extension **Dev Containers** |
| RAM dispo | 8 Go (16 Go recommandés) | — |
| Espace disque | 10 Go | — |

### Trois minutes pour démarrer

```bash
git clone <ton_repo>             # ou copier le dossier
cd formateurWorkspace
code .                           # ouvrir VSCode
# Ctrl+Shift+P → "Dev Containers: Reopen in Container"
```

VSCode lance la stack, ouvre Pylance dans le conteneur, tu peux exécuter le premier notebook en moins de 5 minutes.

---

## Programme détaillé (14 heures)

### Jour 1 — Fondations & RAG Local (7 h)

| Module | Durée | Théorie | Pratique |
|--------|-------|---------|----------|
| **M1** Présentation LangChain & LCEL | 1h | Le pipe `\|`, le protocole Runnable, invoke/stream/batch | Première chaîne `prompt \| llm \| parser` |
| **M2** Ollama, Prompts & OutputParsers | 1h30 | ChatPromptTemplate, JsonOutputParser, format_instructions | Classifieur de tickets (catégorie / urgence / résumé) |
| **M3** Embeddings locaux & ChromaDB | 1h30 | Espaces vectoriels, similarité cosinus, sentence-transformers | Index Chroma + recherche sémantique |
| **M4** RAG 100% Local | 1h30 | Pattern RAG, retriever, LCEL avec dict d'entrée | Chaîne RAG complète qui répond depuis la KB |
| **M5** Ingestion PDF & Markdown | 1h30 | DirectoryLoader, RecursiveCharacterTextSplitter, chunking | Pipeline d'ingestion automatique du dossier `data/` |

### Jour 2 — Workflows, Agents & Interfaces (7 h)

| Module | Durée | Théorie | Pratique |
|--------|-------|---------|----------|
| **M6** Few-shot & Chain of Thought | 1h | FewShotChatMessagePromptTemplate, CoT | Renforcement du classifieur de tickets |
| **M7** Agents & Tools | 1h30 | @tool, bind_tools, ReAct, AgentExecutor | Agent qui crée des tickets via tool |
| **M8** Pydantic & Validation | 1h30 | Schémas typés, Literal, with_structured_output | Ticket validé strict |
| **M9** Streamlit UI | 1h30 | session_state, cache_resource, chat_message | App support conversationnelle complète |
| **M10** Debug, Observabilité & Limites | 1h30 | set_debug, callbacks, eval automatique | Mini-eval du RAG |

**Répartition globale : 30% théorie / 70% pratique** (objectif respecté).

---

## Validation des contraintes "100% Local & Sécurisé"

| Contrainte | Statut | Garantie technique |
|------------|--------|--------------------|
| Aucune clé API | ✅ | Aucun import OpenAI/Anthropic/Cohere dans toute la base de code |
| Aucun appel externe par le LLM | ✅ | Ollama local + variable `OLLAMA_HOST=http://ollama:11434` |
| Aucun appel externe par les embeddings | ✅ | sentence-transformers téléchargé une fois, puis offline (HF cache) |
| Pas de télémétrie | ✅ | `ANONYMIZED_TELEMETRY=False` sur Chroma |
| Données indexées restent locales | ✅ | Volume Docker `chroma_data` |
| Pas de fichiers réels d'entreprise | ✅ | Dataset `data/support_kb/` 100% fictif |

> Pour une vérification réseau : démarre la stack puis débranche le wifi → tout continue à fonctionner. C'est le test ultime.

---

## Trainer's Note

Cette formation est conçue pour qu'un développeur puisse, à la fin du Jour 2, **revenir en entreprise lundi matin et démarrer un projet RAG sérieux**. Trois choses sont volontairement appuyées :

1. **L'observabilité** (Module 10, Exercice 10) : sans éval, un projet RAG tourne en aveugle. Insiste sur cette discipline.
2. **L'idempotence** (Exercice 5) : une ingestion qui crée des doublons à chaque cron est un classique. Ce pattern doit devenir un réflexe.
3. **La séparation chaîne / agent** (Module 7) : un junior va sur-utiliser les agents par excitation. Rappelle-leur la règle : *"Si tu peux écrire un graphe fixe, fais une chaîne. Tu choisis un agent quand le chemin dépend du contenu."*

---

## DevOps / Security Check

- [ ] Versionner `formateurWorkspace/` dans git, **avec** le `devcontainer.json` et le `docker-compose.yml`.
- [ ] **Ne pas** versionner `data/chroma_db*/` (ajouter au `.gitignore`).
- [ ] Pour une formation distribuée à plusieurs apprenants en simultané : prévoir un serveur central (4 vCPU, 16 Go RAM) avec un JupyterHub multi-utilisateurs, ou laisser chacun sur son poste avec sa stack locale.
- [ ] Token JupyterLab désactivé : OK formation, à activer en prod (`JUPYTER_TOKEN` env var).
- [ ] Streamlit lancé sur `0.0.0.0` : OK formation, en prod = reverse proxy + auth.
- [ ] Volumes nommés (`ollama_data`, `hf_cache`, `chroma_data`) : performance I/O optimale et survivent aux redémarrages.

---

## Ressources de référence

- LangChain Python : https://python.langchain.com
- Ollama : https://ollama.com
- ChromaDB : https://docs.trychroma.com
- sentence-transformers : https://www.sbert.net
- Streamlit : https://docs.streamlit.io

**Fin du Jour 2** = tu as un assistant support local fonctionnel, debuggable et auditable.
**Lundi matin** = tu démarres ton vrai projet, en t'appuyant sur les patterns de la formation.

Bonne formation 🚀
