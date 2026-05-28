"""
Démo LIVE — Interface Streamlit pour l'Assistant Support Technique Local.

Lancement :
    streamlit run demo_streamlit_app.py --server.address=0.0.0.0
    -> http://localhost:8501

Fonctionnalités :
- Chat conversationnel branché sur le RAG local (gemma3:4b + Chroma).
- Sidebar pour régler les paramètres (k du retriever, température).
- Bouton pour transformer la dernière question en ticket structuré.
"""
import os
from datetime import datetime
from typing import Literal

import streamlit as st
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
PERSIST_DIR = "/workspace/data/chroma_db_demo"


# ============================================================
# Schéma Pydantic du ticket (cf. Module 8)
# ============================================================
class Ticket(BaseModel):
    titre: str = Field(..., max_length=80)
    categorie: Literal["materiel", "logiciel", "reseau", "compte"]
    priorite: Literal["P1", "P2", "P3", "P4"]
    impact_utilisateurs: int = Field(..., ge=1)
    actions_essayees: list[str] = Field(default_factory=list)


# ============================================================
# Setup lourd : caché par Streamlit pour ne pas recharger
# à chaque interaction (sinon = catastrophe perf).
# ============================================================
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@st.cache_resource
def get_vectorstore():
    return Chroma(
        collection_name="demo_kb",
        embedding_function=get_embeddings(),
        persist_directory=PERSIST_DIR,
    )


def get_llm(temperature: float = 0.0):
    """Pas mis en cache car la temperature change avec le slider."""
    return ChatOllama(model="gemma3:4b", base_url=OLLAMA_HOST, temperature=temperature)


def build_rag_chain(k: int = 3, temperature: float = 0.0):
    """Construit la chaîne RAG. Exposé au top-level pour pouvoir être testé hors Streamlit."""
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": k})
    llm = get_llm(temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es l'assistant support technique. Réponds en français, en t'appuyant "
         "uniquement sur le contexte fourni. Si la réponse n'y est pas, dis-le "
         "honnêtement plutôt que d'inventer.\n\nContexte :\n{context}"),
        ("human", "{question}"),
    ])

    def fmt(docs):
        return "\n\n".join(f"[{d.metadata.get('source', '?')}] {d.page_content}" for d in docs)

    return (
        {
            "context": (lambda x: x) | retriever | fmt,
            "question": (lambda x: x),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def description_to_ticket(description: str) -> Ticket:
    """Transforme une description libre en Ticket validé Pydantic."""
    llm = get_llm(temperature=0)
    structured = llm.with_structured_output(Ticket)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es l'analyste support. Transforme la description en ticket structuré."),
        ("human", "{description}"),
    ])
    return (prompt | structured).invoke({"description": description})


# ============================================================
# UI Streamlit
# ============================================================
def main():
    st.set_page_config(
        page_title="Assistant Support Technique Local",
        page_icon="🛠️",
        layout="wide",
    )
    st.title("🛠️ Assistant Support Technique — 100% Local")
    st.caption("Powered by Ollama (gemma3:4b) + LangChain + ChromaDB — aucune donnée ne sort du réseau.")

    # --- Sidebar : paramètres ---
    with st.sidebar:
        st.header("Paramètres")
        k = st.slider("Nombre de docs à récupérer (k)", 1, 6, 3)
        temperature = st.slider("Température LLM", 0.0, 1.0, 0.0, 0.1)
        st.divider()
        st.markdown("### Aide formateur")
        st.info(
            "Ce chatbot s'appuie sur la base de connaissances `data/support_kb/`.\n\n"
            "Pose une vraie question support pour voir la magie opérer."
        )

    # --- Init session state ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_user_query" not in st.session_state:
        st.session_state.last_user_query = ""

    # --- Colonnes : chat à gauche, ticket à droite ---
    col_chat, col_ticket = st.columns([2, 1])

    with col_chat:
        st.subheader("💬 Conversation")

        # Affichage de l'historique
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Nouvelle question
        if user_input := st.chat_input("Pose ta question support…"):
            st.session_state.last_user_query = user_input
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            chain = build_rag_chain(k=k, temperature=temperature)

            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""
                for chunk in chain.stream(user_input):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

    with col_ticket:
        st.subheader("🎫 Génération de ticket")
        if st.session_state.last_user_query:
            st.markdown(f"**Dernière demande :**\n> {st.session_state.last_user_query}")
            if st.button("Transformer en ticket structuré", use_container_width=True):
                with st.spinner("Génération du ticket…"):
                    try:
                        ticket = description_to_ticket(st.session_state.last_user_query)
                        st.success("Ticket généré :")
                        st.json(ticket.model_dump())
                    except Exception as e:
                        st.error(f"Erreur de génération : {e}")
        else:
            st.info("Pose d'abord une question dans le chat.")


if __name__ == "__main__":
    main()
