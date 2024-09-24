import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
from folium.plugins import MarkerCluster
from folium.features import CustomIcon
from pathlib import Path

icon_path = Path("Imagenes/Isotipo_Super.png")
st.set_page_config(page_title="DENUE dashboard", page_icon=str(icon_path),layout='wide')

ruta_imagen = "Imagenes/ubicacion.png"  
ruta_mapa="Imagenes/Imagen Pedregal.png"

@st.cache_data

def generadore_clientes():
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQUE20irmSfnYGbW0oxCnLe0Vbbtpt-k1X8LMk7c0DWOQDKu92z9mcYOViaJDyVSQ/pubhtml"
    html=pd.read_html(url, header=1)
    df=html[0]
    return df
    
def mapa_pedregal():
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRcjT15FQ5qZHFrQGO-O7JKHgpmuDzQ8oPZMX8eLQosk1prKKa7rWwab0gUelyAFw/pubhtml"
    html=pd.read_html(url, header=1)
    df=html[0]
    
    return df

casas_Ped=mapa_pedregal()
df = generadore_clientes()
#weights=[1.5,1,1]
#col1, col2, col3=st.columns(weights)

#with col2:
#    st.markdown("""
#        <a href="https://app.powerbi.com/groups/4c07734f-f271-4be1-903b-cfa6cb10c07c/reports/2eb52716-7702-4c09-aefd-c6c2fe07e3ed/3757ea1fa3d08184590d?experience=power-bi" target="_blank">
#            <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px;
#            text-align: center; text-decoration: none; display: inline-block; font-size: 16px; border-radius: 5px;">
#                Ir al powerBI
#            </button>
#        </a>
#        """, unsafe_allow_html=True)
st.markdown("""
    <a href="https://app.powerbi.com/groups/4c07734f-f271-4be1-903b-cfa6cb10c07c/reports/2eb52716-7702-4c09-aefd-c6c2fe07e3ed/3757ea1fa3d08184590d?experience=power-bi" target="_blank">
        <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px;
        text-align: center; text-decoration: none; display: inline-block; font-size: 16px; border-radius: 5px;">
            Ir al PowerBI
        </button>
    </a>
    """, unsafe_allow_html=True)

filtro_ubi=st.sidebar.multiselect('Filtro',df['Ubicacion'].unique())

if filtro_ubi:
    df = df[df['Ubicacion'].isin(filtro_ubi)]
#    catalogo_suc=catalogo_suc[catalogo_suc['Sucursal'].isin(filtro_ubi)]

filtro_tipo=st.sidebar.multiselect('Filtro tipo',df['Tipo'].unique())

if filtro_tipo:
    df=df[df['Tipo'].isin(filtro_tipo)]

filtro_descripsion_sec=st.sidebar.multiselect('Filtro descripción de sectores',df['Descripcion_del_Sector_Economico'].unique())


if filtro_descripsion_sec:
    df=df[df['Descripcion_del_Sector_Economico'].isin(filtro_descripsion_sec)]

df_coordenadas=df[['Nombre Establecimiento','Latitud','Longitud','Tipo']]
df[['latitud_clus', 'longitud_clus']] = df['Coordenadas'].str.split(',', expand=True)
df_clusters=df[['latitud_clus','longitud_clus']]
df_clusters=df_clusters.drop_duplicates()
latitud_cluster=df_clusters['latitud_clus'].iloc[0]
longitud_cluster=df_clusters['longitud_clus'].iloc[0]
centro = (latitud_cluster, longitud_cluster)

mapa = folium.Map(
    location=[latitud_cluster, longitud_cluster],
    zoom_start=15,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles © Esri — Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
)

folium.Circle(
    radius=500,  # 0.5 km
    location=[latitud_cluster, longitud_cluster],
    color="blue",
    fill=True,
    fill_opacity=0.3
).add_to(mapa)

folium.Circle(
    radius=1000,  # 1 km
    location=[latitud_cluster, longitud_cluster],
    color="blue",
    fill=True,
    fill_opacity=0.2
).add_to(mapa)

def convertir_imagen_a_base64(ruta_imagen):

    img = Image.open(ruta_imagen)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str

imagen_base64 = convertir_imagen_a_base64(ruta_imagen)

icono_html = f'<img src="data:image/png;base64,{imagen_base64}" width="20px" height="20px">'
icono = folium.DivIcon(html=icono_html)

folium.Marker(location=[latitud_cluster, longitud_cluster], icon=icono).add_to(mapa)
st.markdown("<h1 style='text-align: center;'>Mapa satelital</h1>", unsafe_allow_html=True)
weights=[1,2,1]
col1, col2, col3=st.columns(weights)
with col2:
    st_data = folium_static(mapa, width=725)


def asignar_color(tipo):
    if tipo == 'Clientes':
        return 'green'
    elif tipo == 'Generador':
        return 'lightblue'
    else:
        return 'red'

def obtener_bounds(centro, radio_km):
    norte = geodesic(kilometers=radio_km).destination(centro, 0).latitude
    sur = geodesic(kilometers=radio_km).destination(centro, 180).latitude
    este = geodesic(kilometers=radio_km).destination(centro, 90).longitude
    oeste = geodesic(kilometers=radio_km).destination(centro, 270).longitude
    return [(sur, oeste), (norte, este)]

    
mymap = folium.Map(location=centro)
radio_km = 1 * 1000 
folium.Circle(location=centro, radius=radio_km, color=None, fill=True, fill_color="blue",fill_opacity=0.4).add_to(mymap)
radio_km = 1 * 500 
folium.Circle(location=centro, radius=radio_km, color=None, fill=True, fill_color="blue",fill_opacity=0.6).add_to(mymap)
bounds = obtener_bounds(centro, 1) 
mymap.fit_bounds(bounds)

for index, row in df_coordenadas.iterrows():
    folium.CircleMarker(
       location=(row['Latitud'], row['Longitud']),
        radius=8, 
        color=asignar_color(row['Tipo']),
        fill=True, 
        fill_color=asignar_color(row['Tipo']),  
        fill_opacity=0.8,
        tooltip=folium.Tooltip(f"Establecimiento:{row['Nombre Establecimiento']}<br>Latitud: {row['Latitud']}<br>Longitud: {row['Longitud']}<br>Tipo: {row['Tipo']}")
    ).add_to(mymap)


#for index, row in df.iterrows():
#    icono_imagen = CustomIcon(
#        icon_image=row['Ruta Imagen'],  # Usar la ruta de imagen asignada en el Excel
#        icon_size=(30, 30)  # Ajustar el tamaño de la imagen
#    )
#    
#    # Crear un marcador con la imagen
#    folium.Marker(
#        location=(row['Latitud'], row['Longitud']),
#        icon=icono_imagen,
#        tooltip=folium.Tooltip(f"Establecimiento: {row['Nombre Establecimiento']}<br>Latitud: {row['Latitud']}<br>Longitud: {row['Longitud']}<br>Tipo: {row['Tipo']}")
#    ).add_to(mymap)

st.markdown("<h1 style='text-align: center;'>Mapa</h1>", unsafe_allow_html=True)
num_clientes = df[df['Tipo'] == 'Clientes'].shape[0]
num_generadores = df[df['Tipo'] == 'Generador'].shape[0]
num_competencia = df[df['Tipo'] == 'Competencia'].shape[0]

weights=[3,2,1]
col1, col2, col3=st.columns(weights)
with col1:
    
    folium_static(mymap)

with col3:
    st.markdown(
    f"""
    <div style="background-color: lightgreen; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center;">Clientes</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center;">{num_clientes}</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("")

    st.markdown(
    f"""
    <div style="background-color: lightblue; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center;">Generadores</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center;">{num_generadores}</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("")

    st.markdown(
    f"""
    <div style="background-color: #e60000; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center;">Competencia</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center;">{num_competencia}</p>
    </div>
    """,
    unsafe_allow_html=True
    )

imagen = Image.open('Imagenes/Imagen_Pedregal.png')
st.markdown("<h1 style='text-align: center;'>Mapa Pedegral</h1>", unsafe_allow_html=True)
weights=[2,1]
col1, col2=st.columns(weights)
with col1:
    st.image(imagen, 
            # caption='Imagen Pedregal',
             use_column_width=True)

with col2:
    casas_Ped