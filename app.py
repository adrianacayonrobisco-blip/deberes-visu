import streamlit as st
import pandas as pd
import plotly.express as px

# 1. TÍTULO CON EL NOMBRE DEL ESTUDIANTE (Requisito obligatorio) [cite: 21]
st.set_page_config(page_title="Dashboard Airbnb", layout="wide")
st.title("Nombre y Apellido del Estudiante") # <-- CAMBIA ESTO POR TU NOMBRE

# 2. CARGA DE DATOS (Basado en el lab de clase) [cite: 4]
@st.cache_data
def load_data():
    # Asegúrate de que el nombre del archivo coincida con el tuyo
    df = pd.read_csv("airbnb_data.csv")
    return df

try:
    df = load_data()

    # 3. SIDEBAR Y COLUMNAS (Requisito) [cite: 7]
    st.sidebar.header("Filtros de Datos")
    
    # Selector de barrio (Requisito: Selectores para filtrar) [cite: 6]
    neighborhoods = st.sidebar.multiselect(
        "Selecciona el Barrio:",
        options=df["neighbourhood"].unique(),
        default=df["neighbourhood"].unique()[:3]
    )

    # Selector de rango de precio
    price_range = st.sidebar.slider(
        "Rango de Precio:",
        int(df["price"].min()), int(df["price"].max()), 
        (0, 500)
    )

    # Filtrado de los datos
    df_filtered = df[
        (df["neighbourhood"].isin(neighborhoods)) & 
        (df["price"].between(price_range[0], price_range[1]))
    ]

    # Uso de columnas para métricas rápidas [cite: 7]
    c1, c2, c3 = st.columns(3)
    c1.metric("Apartamentos encontrados", len(df_filtered))
    c2.metric("Precio medio", f"{df_filtered['price'].mean():.2f}€")
    c3.metric("Reviews totales", df_filtered['number_of_reviews'].sum())

    # 4. DOS PESTAÑAS (Requisito) [cite: 8]
    tab1, tab2 = st.tabs(["Análisis de Capacidad", "Precios y Popularidad"])

    with tab1:
        # 5. GRÁFICO OBLIGATORIO: Tipo de listado vs número de personas [cite: 9]
        st.subheader("Relación entre Tipo de Alojamiento y Capacidad")
        fig_capacidad = px.box(
            df_filtered, 
            x="room_type", 
            y="accommodates", 
            color="room_type",
            title="Distribución de Personas por Tipo de Listado"
        )
        st.plotly_chart(fig_capacidad, use_container_width=True)

    with tab2:
        # 6. GRÁFICOS ADICIONALES (Mínimo dos de propia imaginación) [cite: 10]
        
        # Gráfico extra 1: Precio por tipo de listado [cite: 12]
        st.subheader("Exploración de Precios")
        fig_precio = px.violin(
            df_filtered, 
            x="room_type", 
            y="price", 
            color="room_type", 
            box=True, 
            points="all",
            title="Distribución de Precios por Tipo de Apartamento"
        )
        st.plotly_chart(fig_precio, use_container_width=True)

        # Gráfico extra 2: Relación entre Reviews y Precio [cite: 16]
        st.subheader("Relación: Reseñas vs Precio")
        fig_reviews = px.scatter(
            df_filtered, 
            x="price", 
            y="number_of_reviews", 
            size="availability_365", 
            color="room_type",
            hover_name="name",
            title="¿Influye el precio en la cantidad de reseñas?"
        )
        st.plotly_chart(fig_reviews, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que 'airbnb_data.csv' esté en la misma carpeta que este script.")
    
  

  
