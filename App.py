import streamlit as st
import sys
import os
import tempfile

# Agregar src al path para importar PlagiarismDetector
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from plagiarism_detector import PlagiarismDetector


def comparar_textos(text_a: str, text_b: str, language: str = "spanish"):
    detector = PlagiarismDetector(language=language)

    # Crear archivos temporales con los textos
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f1:
        f1.write(text_a)
        path_a = f1.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f2:
        f2.write(text_b)
        path_b = f2.name

    result = detector.compare_files(path_a, path_b)
    similarity = result.get("similarity_percentage", 0.0)
    return similarity, result


st.set_page_config(
    page_title="Detector de Plagio",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Detector de Plagio con Análisis Multidimensional")

col_a, col_b = st.columns(2)
st.subheader("Cargar documentos para comparar")

file_a = col_a.file_uploader("Documento A (.txt)", type=["txt"])
file_b = col_b.file_uploader("Documento B (.txt)", type=["txt"])

text_a = col_a.text_area("O pega texto A aquí", height=200)
text_b = col_b.text_area("O pega texto B aquí", height=200)

if file_a is not None:
    text_a = file_a.read().decode("utf-8", errors="ignore")

if file_b is not None:
    text_b = file_b.read().decode("utf-8", errors="ignore")

st.markdown("---")

if st.button("Analizar similitud"):
    if not text_a.strip() or not text_b.strip():
        st.warning("Debes proporcionar ambos documentos")
    else:
        with st.spinner("Analizando…"):
            similarity, result = comparar_textos(text_a, text_b)

        st.subheader(" Resultados del análisis")
        st.metric("Similitud total", f"{similarity:.2f}%")
        st.progress(max(0.0, min(similarity / 100.0, 1.0)))

        st.markdown("#### Detalles técnicos")
        st.json(result)
