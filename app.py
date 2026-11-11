import streamlit as st

from easy_leaflet.pipeline import build_assistant, load_leaflet_info

st.set_page_config(page_title="Easy Leaflet", page_icon="💊")

st.title("Easy Leaflet")
st.write("Faz uma pergunta sobre o folheto de um medicamento. A resposta usa apenas o folheto oficial.")
st.warning("Projeto de estudo. Não é aconselhamento médico. Fale sempre com o seu médico ou farmacêutico.")


@st.cache_resource
def get_assistant():
    # Runs only once: loading the PDFs and the embedding model is slow
    return build_assistant()


leaflets = load_leaflet_info()

# The user sees the medicine name; the code needs the short name ("brufen")
medicine = st.selectbox("Medicamento", list(leaflets["medicine"]))
info = leaflets[leaflets["medicine"] == medicine].iloc[0]

question = st.text_input("A sua pergunta", placeholder="Posso beber álcool?")

if st.button("Perguntar") and question:
    try:
        with st.spinner("A procurar no folheto..."):
            answer = get_assistant().answer(question, leaflet_name=info["name"])
    except Exception:
        st.error("O serviço está ocupado. Por favor, tente novamente daqui a um minuto.")
        st.stop()

    if answer.found:
        st.success(answer.text)
    else:
        st.info(answer.text)

    # The link comes from leaflets.csv, never from the LLM
    st.markdown(f"Folheto original: [{info['medicine']}]({info['url']})")

    if answer.sources:
        with st.expander("Ver o texto do folheto usado"):
            for chunk in answer.sources:
                st.text(chunk.text)