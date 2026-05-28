"""
Démo LIVE — Première chaîne LCEL.

Objectif : montrer en direct, en moins de 2 minutes, qu'une chaîne LangChain
c'est juste prompt | llm | parser, et que ça marche en local sans clé API.

Usage :
    python demo_lcel_simple.py
    python demo_lcel_simple.py "ta propre question"
"""
import os
import sys

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def main(question: str) -> None:
    # Les 3 briques minimales du LCEL
    llm = ChatOllama(model="gemma3:4b", base_url=OLLAMA_HOST, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant technique pédagogue. Réponds en français en 3 lignes max."),
        ("human", "{question}"),
    ])
    parser = StrOutputParser()

    # L'assemblage par pipe
    chain = prompt | llm | parser

    # Streaming pour l'UX
    print(f"\n>>> Question : {question}\n>>> Réponse  : ", end="", flush=True)
    for chunk in chain.stream({"question": question}):
        print(chunk, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "Explique le RAG en une phrase."
    main(q)
