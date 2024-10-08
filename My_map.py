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
image_path = 'Imagenes/Isotipo_Super.png'
ruta_imagen = "Imagenes/ubicacion.png"  
ruta_mapa_pedregal="Imagenes/Imagen_Pedregal.png"
ruta_imagen_charo="Imagenes/Imagen_Charo.png"
ruta_imagen_beronesa="Imagenes/Imagen_Beronesa.png"
ruta_imagen_jesus_monte="Imagenes/Imagen_Jesus_monte.png"
ruta_imagen_tenencia="Imagenes/Imagen_Tenencia_morelos.png"
st.set_page_config(page_title="DENUE dashboard", page_icon=str(icon_path),layout='wide')
st.markdown('<div id="top"></div>', unsafe_allow_html=True)


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

def mapa_charo():
    url="https://docs.google.com/spreadsheets/d/1VQZSrnytv0zytAWMgbkEsShxKW1qHfFw/pubhtml"
    html=pd.read_html(url,header=1)
    df=html[0]
    return df
casas_Ped=mapa_pedregal()
df = generadore_clientes()
casas_charo=mapa_charo()
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
    <a href="https://app.powerbi.com/groups/4c07734f-f271-4be1-903b-cfa6cb10c07c/reports/2eb52716-7702-4c09-aefd-c6c2fe07e3ed/3757ea1fa3d08184590d?experience=power-bi" target="_blank" style="text-decoration: none;">
        <button style="position: fixed; background-color: #f2c811; border: none; color: black; padding: 10px 20px; text-align: center; display: inline-block; font-size: 16px; border-radius: 5px; z-index:9999;">
            <!-- Icono de flecha izquierda -->
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
            </svg>
            <!-- Icono de gráfico de barras -->
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 16">
                <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1z"/>
            </svg>
        </button>
    </a>
    """, unsafe_allow_html=True)
filtro_ubi=st.sidebar.multiselect('Filtro para ubicación',df['Ubicacion'].unique())

if filtro_ubi:
    df = df[df['Ubicacion'].isin(filtro_ubi)]
#    catalogo_suc=catalogo_suc[catalogo_suc['Sucursal'].isin(filtro_ubi)]

filtro_tipo=st.sidebar.multiselect('Filtro de segmentación',df['Tipo'].unique())

if filtro_tipo:
    df=df[df['Tipo'].isin(filtro_tipo)]

filtro_descripsion_sec=st.sidebar.multiselect('Filtro descripción de sectores de la segmentación',df['Descripcion_del_Sector_Economico'].unique())

map_type = st.sidebar.radio(
    "Selecciona el tipo de mapa",
    ( 'Mapa estándar', 'Satelital')
)
st.sidebar.markdown("""
    <a href="#pedregal">
        <button style="bottom: 10px; center: 10px; background-color: #84817c; border: None; color: white; padding: 10px 12px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px;">
            <i class="bi bi-plus-lg"></i>        
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
                </svg>       
        Mapa Pedregal     
        </button>            
    </a>    
    <a href="#crucero_charo">
        <button style="bottom: 10px; center: 10px; background-color: #84817c; border: None; color: white; padding: 10px 18px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px;">
            <i class="bi bi-plus-lg"></i>        
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
                </svg>       
        Mapa crucero Charo     
        </button>            
    </a>                               
 """, unsafe_allow_html=True)
st.sidebar.markdown("")
st.sidebar.markdown("""
    <a href="#beronesa">
        <button style="bottom: 10px; center: 10px; background-color: #84817c; border: None; color: white; padding: 10px 10px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px;">
            <i class="bi bi-plus-lg"></i>        
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
                </svg>       
        Mapa Beronesa     
        </button>            
    </a>    
    <a href="#jesus_monte">
        <button style="bottom: 10px; center: 10px; background-color: #84817c; border: None; color: white; padding: 10px 10px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px;">
            <i class="bi bi-plus-lg"></i>        
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
                </svg>       
        Mapa Jesus del monte     
        </button>            
    </a>                               
 """, unsafe_allow_html=True)
st.sidebar.markdown("")
st.sidebar.markdown("""
    <button style="align:center; bottom: 10px; background-color: transparent; border: none; color: white; padding: 10px 35px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px; pointer-events: none;">
    </button>            
    <a href="#tenencia">
        <button style="aling:center ;bottom: 10px; center: 10px; background-color: #84817c; border: None; color: white; padding: 10px 10px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 5px;">
            <i class="bi bi-plus-lg"></i>        
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"/>
                </svg>       
        Mapa Tenencia Morelos     
        </button>            
    </a>                                
 """, unsafe_allow_html=True)
if map_type == 'Satelital':
    tiles_option = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    tiles_attr = 'Tiles © Esri — Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
else:
    tiles_option = 'OpenStreetMap'
    tiles_attr = None

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
    tiles=tiles_option,
    attr=tiles_attr
)

folium.Circle(
    radius=250,  
    location=[latitud_cluster, longitud_cluster],
    color="#b5b5b5",
    fill=True,
    fill_opacity=0.3
).add_to(mapa)

folium.Circle(
    radius=500,  
    location=[latitud_cluster, longitud_cluster],
    color="#b5b5b5",
    fill=True,
    fill_opacity=0.3
).add_to(mapa)

folium.Circle(
    radius=1000,  
    location=[latitud_cluster, longitud_cluster],
    color="#b5b5b5",
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
        return '#0b7365'
    elif tipo == 'Generador':
        return '#1c4373'
    else:
        return '#5e0001'

def obtener_bounds(centro, radio_km):
    norte = geodesic(kilometers=radio_km).destination(centro, 0).latitude
    sur = geodesic(kilometers=radio_km).destination(centro, 180).latitude
    este = geodesic(kilometers=radio_km).destination(centro, 90).longitude
    oeste = geodesic(kilometers=radio_km).destination(centro, 270).longitude
    return [(sur, oeste), (norte, este)]


def filtrar_por_distancia(df, centro, radio_metros):
    return df[df.apply(lambda row: geodesic(centro, (row['Latitud'], row['Longitud'])).meters <= radio_metros, axis=1)]

def filtrar_por_distancia_rango(df, centro, radio_min_metros, radio_max_metros):
    return df[df.apply(lambda row: radio_min_metros < geodesic(centro, (row['Latitud'], row['Longitud'])).meters <= radio_max_metros, axis=1)]   



mymap = folium.Map(
    location=centro,
    zoom_start=15,
    tiles=tiles_option,
    attr=tiles_attr
)

icono = CustomIcon(
    image_path, 
    icon_size=(20, 20)  
)

folium.Marker(
    location=centro,
    icon=icono
).add_to(mymap)

radio_km = 1000 
folium.Circle(location=centro, radius=radio_km, color='#b5b5b5', fill=True, fill_color="#b5b5b5",fill_opacity=0.4).add_to(mymap)
radio_km = 500 
folium.Circle(location=centro, radius=radio_km, color='#b5b5b5', fill=True, fill_color="#b5b5b5",fill_opacity=0.4).add_to(mymap)
radio_km = 250 
folium.Circle(location=centro, radius=radio_km, color='#b5b5b5', fill=True, fill_color="#b5b5b5",fill_opacity=0.4).add_to(mymap)
bounds = obtener_bounds(centro, 1) 
mymap.fit_bounds(bounds)


if 'selected_buttons' not in st.session_state:
    st.session_state.selected_buttons = []

def select_button(button_id):
    if button_id == 'btn3':  
        st.session_state.selected_buttons = ['btn3'] 
    else:
        st.session_state.selected_buttons = [button_id] 

st.markdown("<h1 style='text-align: center;'>Mapa</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col2:
    if 'btn1' in st.session_state.selected_buttons:
        st.button('1 km', key='btn1', on_click=select_button, args=('btn1',), use_container_width=True, disabled=False)
        df_coordenadas = filtrar_por_distancia_rango(df_coordenadas, centro, 500, 1000)
        for index, row in df_coordenadas.iterrows():
            folium.CircleMarker(
                location=(row['Latitud'], row['Longitud']),
                radius=8,
                color=asignar_color(row['Tipo']),
                fill=True,
                fill_color=asignar_color(row['Tipo']),
                fill_opacity=0.8,
                tooltip=folium.Tooltip(f"Establecimiento: {row['Nombre Establecimiento']}<br>Latitud: {row['Latitud']}<br>Longitud: {row['Longitud']}<br>Tipo: {row['Tipo']}")
            ).add_to(mymap)
    else:
        st.button('1 km', key='btn1', on_click=select_button, args=('btn1',), use_container_width=True)

with col1:
    if 'btn2' in st.session_state.selected_buttons:
        st.button('500 mts', key='btn2', on_click=select_button, args=('btn2',), use_container_width=True, disabled=False)
        df_coordenadas = filtrar_por_distancia(df_coordenadas, centro, 500)
        for index, row in df_coordenadas.iterrows():
            folium.CircleMarker(
                location=(row['Latitud'], row['Longitud']),
                radius=8,
                color=asignar_color(row['Tipo']),
                fill=True,
                fill_color=asignar_color(row['Tipo']),
                fill_opacity=0.8,
                tooltip=folium.Tooltip(f"Establecimiento: {row['Nombre Establecimiento']}<br>Latitud: {row['Latitud']}<br>Longitud: {row['Longitud']}<br>Tipo: {row['Tipo']}")
            ).add_to(mymap)
    else:
        st.button('500 mts', key='btn2', on_click=select_button, args=('btn2',), use_container_width=True)

with col3:
    if 'btn3' in st.session_state.selected_buttons:
        st.button('Todo', key='btn3', on_click=select_button, args=('btn3',), use_container_width=True, disabled=False)
        for index, row in df_coordenadas.iterrows():
            folium.CircleMarker(
                location=(row['Latitud'], row['Longitud']),
                radius=8,
                color=asignar_color(row['Tipo']),
                fill=True,
                fill_color=asignar_color(row['Tipo']),
                fill_opacity=0.8,
                tooltip=folium.Tooltip(f"Establecimiento: {row['Nombre Establecimiento']}<br>Latitud: {row['Latitud']}<br>Longitud: {row['Longitud']}<br>Tipo: {row['Tipo']}")
            ).add_to(mymap)
    else:
        st.button('Todo', key='btn3', on_click=select_button, args=('btn3',), use_container_width=True)



num_clientes = df_coordenadas[df_coordenadas['Tipo'] == 'Clientes'].shape[0]
num_generadores = df_coordenadas[df_coordenadas['Tipo'] == 'Generador'].shape[0]
num_competencia = df_coordenadas[df_coordenadas['Tipo'] == 'Competencia'].shape[0]

weights=[3,2,1]
col1, col2, col3=st.columns(weights)
with col1:
    
    folium_static(mymap)

with col3:
    st.markdown(
    f"""
    <div style="background-color: #0b7365; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center;color: white; ">Clientes</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center; color: white">{num_clientes}</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("")

    st.markdown(
    f"""
    <div style="background-color: #1c4373; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center; color:white;">Generadores</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center; color:white">{num_generadores}</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("")

    st.markdown(
    f"""
    <div style="background-color: #5e0001; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h4 style="text-align: center; color:white">Competencia</h4>
        <p style="font-size: 24px; font-weight: bold; text-align: center; color:white">{num_competencia}</p>
    </div>
    """,
    unsafe_allow_html=True
    )

imagen_pedregal = Image.open(ruta_mapa_pedregal)
st.markdown('<div id="pedregal"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Mapa Pedegral</h1>", unsafe_allow_html=True)

weights=[2,1]
col1, col2=st.columns(weights)
with col1:
    st.image(imagen_pedregal, 
            # caption='Imagen Pedregal',
             use_column_width=True)

with col2:
    casas_Ped

st.markdown('<div id="crucero_charo"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Mapa Crucero Charo</h1>", unsafe_allow_html=True)

imagen_charo = Image.open(ruta_imagen_charo)
col1, col2=st.columns(weights)
with col1:
    st.image(imagen_charo, 
            # caption='Imagen Pedregal',
             use_column_width=True)

with col2:
    for _ in range(15):  
        st.markdown("")
    casas_charo = casas_charo.sort_values('Numero', ascending=True)
    casas_charo

st.markdown('<div id="beronesa"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Mapa Beronesa</h1>", unsafe_allow_html=True)

imagen_beronesa = Image.open(ruta_imagen_beronesa)
col1, col2=st.columns(weights)
with col1:
    st.image(imagen_beronesa, 
             use_column_width=True)
    
st.markdown('<div id="jesus_monte"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Mapa Jesus del monte</h1>", unsafe_allow_html=True)

imagen_jesus_monte = Image.open(ruta_imagen_jesus_monte)
col1, col2=st.columns(weights)
with col1:
    st.image(imagen_jesus_monte, 
             use_column_width=True)

st.markdown('<div id="tenencia"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Mapa Tenencia Morelos</h1>", unsafe_allow_html=True)


imagen_tenencia = Image.open(ruta_imagen_tenencia)
col1, col2=st.columns(weights)
with col1:
    st.image(imagen_tenencia, 
             use_column_width=True)
    
st.markdown("""
     <footer style ="text-align: center">
         <a href="#top">
             <button style="position: fixed; bottom: 10px; center: 10px; background-color: transparent; border: None; color: white; padding: 10px 10px; text-align: center; text-decoration: none; font-size: 16px; border-radius: 50%;">
                 <i class="bi bi-arrow-up-circle"></i>
                     <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#e7276f" class="bi bi-arrow-up-circle" viewBox="0 0 16 16">
                         <path fill-rule="evenodd" d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-7.5 3.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707z"/>
                     </svg>
             </button>
         </a>
     </footer>    
 """, unsafe_allow_html=True)