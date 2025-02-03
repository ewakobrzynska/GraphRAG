import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langchain_community.graphs import Neo4jGraph

URI = "neo4j+s://5fdbd7a7.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "qprn5T7m96j2vd6Jeq2XKRIyvBzzZiC902qLSjWZOIs"
graph = Neo4jGraph(URI, USER, PASSWORD)

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def generate_cypher_query(value):
    return f"""
    MATCH (a:Artifact)-[:BELONGS_TO]->(e:Era), (a)-[:LOCATED_IN]->(l:Location)
    WHERE a.name CONTAINS '{value}' OR e.name CONTAINS '{value}' OR l.name CONTAINS '{value}'
    RETURN a.name AS artifact, e.name AS era, l.name AS location
    """

def query_graph(cypher_query):
    try:
        results = graph.query(cypher_query)
        return results
    except Exception as e:
        return f"Error: {str(e)}"

def display_results(results):
    if isinstance(results, list) and results:
        st.success("Wyniki zapytania:")
        for idx, result in enumerate(results):
            st.write(f"{idx + 1}. Artefakt: {result['artifact']}, Epoka: {result['era']}, Lokalizacja: {result['location']}")
    else:
        st.error("Brak wyników dla zapytania.")

st.set_page_config(
    page_title="Neo4j Artifact Finder",
    page_icon="🗿",
    layout="wide",
)

st.title("🗿 Neo4j Artifact Finder")
st.markdown("Zaawansowana aplikacja do wyszukiwania artefaktów w bazie danych Neo4j.")

st.sidebar.header("Opcje wyszukiwania")
value = st.sidebar.text_input("Czego szukasz? Informacji o artefakcie, epoce a moze lokalizacji?")

if st.sidebar.button("🔍 Szukaj"):
    if not value.strip():
        st.error("Proszę wprowadzić wartość w polu tekstowym.")
    else:
        st.info(f"Generowanie zapytania dla wartości: {value}")
        
        cypher_query = generate_cypher_query(value)
        #st.code(cypher_query, language="cypher")
        st.info("Wysyłanie zapytania do bazy Neo4j...")
        results = query_graph(cypher_query)
        display_results(results)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **Wersja aplikacji:** 1.0")
st.sidebar.markdown("📖 **Twórca:** Ewa Kobrzynska")

st.markdown("---")
st.info(
    "Ta aplikacja wykorzystuje **Streamlit**, **Transformers** i **Neo4j**. "
    "Wybierz rodzaj zapytania w menu bocznym, wpisz wartość i kliknij **Szukaj**."
)
