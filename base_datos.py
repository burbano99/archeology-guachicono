import pandas as pd
import plotly.express as px
import streamlit as st
import glob 
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("base de datos.xlsx")
print(df.columns)


st.set_page_config(page_title= "Base de datos Guachicono", layout= "wide")
st.title("Base de datos Guachicono")

df.columns= (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("á", "a")
    .str.replace("é", "e")
    .str.replace("í", "i")
    .str.replace("ó", "o")
    .str.replace("ú", "u")
    .str.replace("(", "")
    .str.replace(")", "")
)
df["grosor_mm"] = pd.to_numeric(df["grosor_mm"], errors= "coerce")
df["peso_g"] = pd.to_numeric(df["peso_g"], errors= "coerce")
df["radio_cm"] = pd.to_numeric(df["radio_cm"], errors= "coerce")
df["nivel"] = (
    df["nivel"]
    .str.strip()
    .str.replace(" ", "", regex= False)
    .str.replace(r"\)", "", regex= True)
)

df["nivel"] = df["nivel"].replace("6(50-60cm", "6(60-70cm")
df["nivel"] = df["nivel"].replace("6(40-50cm", "6(60-70cm")
st.subheader("material")




#sidebar
st.sidebar.header("filtro")
corte= st.sidebar.multiselect("Seleccionar corte", options= df["corte"].dropna().unique())
if corte:
    df_filtrado = df[df["corte"].isin(corte)]
else: 
    df_filtrado = df
st.subheader("datos")
st.dataframe(df_filtrado)



st.subheader("Distribución de bordes")
fig1, ax1 = plt.subplots()
df_filtrado["borde"].value_counts(). plot(
    kind = "bar", ax= ax1
)
ax1.set_title("Distribución de tipos de borde")
ax1.set_xlabel("Tipo de borde")
ax1.set_ylabel("Cantidad")

st.pyplot(fig1)

st.subheader("Distribución de material por nivel")
fig2, ax2 = plt.subplots()
df_filtrado["nivel"].value_counts().sort_index(). plot(
    kind = "bar", ax= ax2
)
ax2.set_title("Distribución de material por nivel")
ax2.set_xlabel("Nivel")
ax2.set_ylabel("Cantidad")

st.pyplot(fig2)


fig3, ax3 = plt.subplots()
tabla = df_filtrado.groupby(["nivel","parte"]).size().unstack()
tabla.plot(kind= "bar", ax= ax3)
ax3.set_title("Material agupado por parte de la vasija y nivel")
ax3.set_xlabel("Nivel")
ax3.set_ylabel("Cantidad")

st.pyplot(fig3)

st.subheader("Grosor de los fragmentos")
fig4, ax4 = plt.subplots()
df_filtrado["grosor_mm"].value_counts().sort_index(). plot(
    kind = "barh", ax= ax4
)
ax4.set_title("Grosor")
ax4.set_xlabel("Cantidad")
ax4.set_ylabel("Grosor en mm")

st.pyplot(fig4)



#color
st.subheader("Radio de las vasijas")
fig5, ax5 = plt.subplots()

df["radio_cm"].plot(
    kind="hist",
    bins=15,
    ax=ax5
)

ax5.set_title("Distribución del radio de vasijas")
ax5.set_xlabel("Radio (cm)")
ax5.set_ylabel("Frecuencia")
st.pyplot(fig5)

#DESGRASANTE

st.subheader("Materia prima, tamaño y frecuencia (%)") 
tabla1 = pd.crosstab( [df_filtrado["materia_prima"], df_filtrado["tamano_mm"]], df_filtrado["frecuencia"] ) 
tabla_porcentaje1 = tabla1 / tabla1.values.sum() * 100
fig6, ax6 = plt.subplots()
tabla_porcentaje1.plot( kind="bar", ax=ax6 )
ax6.set_title("Materia prima, tamaño y frecuencia (%)") 
ax6.set_xlabel("Materia prima y tamaño") 
ax6.set_ylabel("Porcentaje") 
st.pyplot(fig6)

