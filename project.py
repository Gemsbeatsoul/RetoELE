import streamlit as st
import json
import random

# Estilo CSS para centrar todo el contenido
def estilo_personalizado():
    st.markdown("""
        <style>
            .centered {
                text-align: center;
            }
            .stButton button {
                margin: auto;
                display: block;
            }
        </style>
    """, unsafe_allow_html=True)

# Cargar preguntas desde el archivo JSON
def cargar_preguntas():
    with open("preguntas.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Cargar el récord desde el archivo JSON (solo se carga al inicio)
def cargar_record():
    try:
        with open("record.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("record", 0)
    except FileNotFoundError:
        return 0  # Si no existe el archivo, retornamos 0 como récord inicial

# Guardar el récord en el archivo JSON
def guardar_record(record):
    with open("record.json", "w", encoding="utf-8") as f:
        json.dump({"record": record}, f)

# Inicializar estado del juego
def inicializar_estado():
    if "preguntas" not in st.session_state:
        preguntas = cargar_preguntas()
        random.shuffle(preguntas)
        st.session_state.preguntas = preguntas
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        # Cargar el récord si no está ya en session_state
        if "record" not in st.session_state:
            st.session_state.record = cargar_record()

def main():
    st.set_page_config(page_title="Reto ELE", page_icon="🧠")
    estilo_personalizado()
    inicializar_estado()

    st.markdown("<h1 class='centered'> 🌟 ¡Reto ELE con Gemi! 🌟 </h1>", unsafe_allow_html=True)
    st.markdown("<p class='centered'>Responde correctamente tantas preguntas como puedas. Si fallas, ¡empieza de nuevo!</p>", unsafe_allow_html=True)

    if st.session_state.juego_terminado:
        st.markdown(f"<h2 class='centered'>💥 ¡Has fallado!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='centered'>Tu puntuación: {st.session_state.puntos}</p>", unsafe_allow_html=True)

        if st.session_state.puntos > st.session_state.record:
            st.session_state.record = st.session_state.puntos  # Actualizar el récord en session_state
            guardar_record(st.session_state.record)  # Guardar el nuevo récord en el archivo
            st.markdown("<p class='centered'>🏆 ¡Nuevo récord!</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='centered'>🏅 Récord: {st.session_state.record}</p>", unsafe_allow_html=True)

        if st.button("🔁 Volver a intentarlo"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return

    if st.session_state.indice < len(st.session_state.preguntas):
        pregunta_actual = st.session_state.preguntas[st.session_state.indice]
        st.markdown(f"<h3 class='centered'>{pregunta_actual['pregunta']}</h3>", unsafe_allow_html=True)

        for opcion in pregunta_actual['opciones']:
            if st.button(opcion):
                if opcion == pregunta_actual['respuesta']:
                    st.session_state.puntos += 1
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.session_state.juego_terminado = True
                    st.rerun()
    else:
        st.markdown(f"<h2 class='centered'>🎉 ¡Completaste todas las preguntas!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='centered'>Puntuación final: {st.session_state.puntos}</p>", unsafe_allow_html=True)

        if st.session_state.puntos > st.session_state.record:
            st.session_state.record = st.session_state.puntos  # Actualizar el récord en session_state
            guardar_record(st.session_state.record)  # Guardar el nuevo récord en el archivo
            st.markdown("<p class='centered'>🏆 ¡Nuevo récord!</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='centered'>🏅 Récord: {st.session_state.record}</p>", unsafe_allow_html=True)

        if st.button("🔁 Volver a jugar"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()

