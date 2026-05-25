# Exercices — Formation LangChain Local

Ce dossier contient les **10 exercices pratiques** de la formation, un par module de cours.

## Structure

```
exercices/
├── README.md          # ce fichier
├── enonces/           # 10 énoncés (Markdown + cellules code vides)
│   ├── README.md
│   ├── ex01_premier_lcel.ipynb
│   ├── ex02_json_parser.ipynb
│   ├── … (10 énoncés)
│   └── ex10_eval_rag.ipynb
```

## Philosophie pédagogique

Chaque exercice cible **un concept clé** d'un module de cours. La progression suit l'avancée du fil rouge (Assistant Support Technique Local) :

| # | Module ciblé | Brique du fil rouge construite |
|---|--------------|-------------------------------|
| 1 | J1-M1 LCEL | Reformulation de tickets bruts |
| 2 | J1-M2 Parsers | Extraction d'infos depuis emails |
| 3 | J1-M3 Embeddings | Recherche sémantique vs naïve |
| 4 | J1-M4 RAG | Premier RAG complet |
| 5 | J1-M5 Ingestion | Pipeline d'ingestion idempotent |
| 6 | J2-M6 Few-shot | Détecteur d'intention |
| 7 | J2-M7 Agents | Agent SLA avec tools métier |
| 8 | J2-M8 Pydantic | Rapport d'incident validé |
| 9 | J2-M9 Streamlit | Extension de l'UI |
| 10 | J2-M10 Eval | Harnais d'éval automatique |