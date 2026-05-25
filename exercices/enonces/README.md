# Énoncés d'exercices — Formation LangChain Local

Ce dossier contient les **10 exercices** pratiques de la formation, un par module. Chaque exercice est un notebook Jupyter avec :

- Une **cellule Markdown** détaillant la consigne, le contexte, les données de test, les critères de réussite et un bonus.
- Des **cellules code vides** pour que l'apprenant écrive sa solution.

## Liste des exercices

| # | Notebook | Module ciblé | Concept clé | Durée |
|---|----------|--------------|-------------|-------|
| 1 | `ex01_premier_lcel.ipynb` | J1-M1 | Première chaîne `prompt \| llm \| parser` | 15 min |
| 2 | `ex02_json_parser.ipynb` | J1-M2 | Extraction d'infos en JSON structuré | 20 min |
| 3 | `ex03_recherche_semantique.ipynb` | J1-M3 | Embeddings vs mots-clés | 25 min |
| 4 | `ex04_premier_rag.ipynb` | J1-M4 | RAG complet from scratch | 30 min |
| 5 | `ex05_ingestion_robuste.ipynb` | J1-M5 | IDs stables, ingestion idempotente | 30 min |
| 6 | `ex06_few_shot_intention.ipynb` | J2-M6 | Few-shot pour classification d'intention | 25 min |
| 7 | `ex07_agent_sla.ipynb` | J2-M7 | Agent avec tools métier (SLA) | 30 min |
| 8 | `ex08_pydantic_rapport.ipynb` | J2-M8 | Rapport d'incident validé Pydantic | 25 min |
| 9 | `ex09_streamlit_etendu.ipynb` | J2-M9 | Étendre l'UI Streamlit | 30 min |
| 10 | `ex10_eval_rag.ipynb` | J2-M10 | Harnais d'éval automatique | 30 min |

**Total : ~4h de pratique.** Le reste des 14h se répartit entre théorie + démos.

## Comment utiliser ce dossier

### Côté apprenant

1. Termine le module de cours correspondant (notebooks `notebooks/jourX/`).
2. Ouvre l'énoncé correspondant.
3. **Lis attentivement la consigne ET les critères de réussite** avant de coder.
4. Code dans les cellules vides.
5. Quand tu penses avoir fini, vérifie tes résultats vs les critères.
6. **Seulement ensuite**, ouvre la solution (`solutions/exNN_*_SOLUTION.ipynb`) pour comparer.

### Côté formateur

- Au début du module suivant, demande à 1-2 apprenants de **présenter brièvement** leur solution. Ça consolide les acquis et fait ressortir les variantes.
- Quand un apprenant est bloqué, **n'envoie pas la solution directement**. Pose une question : *"Qu'est-ce que tu as essayé ? Qu'est-ce que ça t'a donné ?"* — ça vaut 10x mieux.
- Garde un œil sur l'horloge : si un exercice prend plus de 1.5x sa durée annoncée pour la majorité, c'est qu'il y a un blocage commun à expliquer collectivement.

## Astuce

Les énoncés ne contiennent **aucun import** — c'est volontaire. Les apprenants doivent identifier eux-mêmes les bons modules à importer. Ça force la consolidation des connaissances.

## Si un apprenant fait planter Chroma

C'est fréquent en exercice (ex5 surtout). Reset rapide :

```bash
docker exec formation-langchain-app rm -rf /workspace/data/chroma_db_exo5
```

Puis re-run la cellule d'indexation.
