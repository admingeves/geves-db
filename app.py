import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from APIbodega import response
from APIconsumos import response_consumo
from APIobras import response_obras
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np


# DICCIONARIO p4 (FECHA INICIO)
meses_dict = {
    'Enero': '2024/01/01',
    'Febrero': '2024/01/02',
    'Marzo': '2024/01/03',
    'Abril': '2024/01/04',
    'Mayo': '2024/01/05',
    'Junio': '2024/01/06',
    'Julio': '2024/01/07',
    'Agosto': '2024/01/08',
    'Septiembre': '2024/01/09',
    'Octubre': '2024/01/10',
    'Noviembre': '2024/01/11',
    'Diciembre': '2024/01/12'
}
# DICCIONARIO p5 (FECHA FIN)
meses_dict_fin = {
    'Febrero': '2024/01/02',
    'Marzo': '2024/01/03',
    'Abril': '2024/01/04',
    'Mayo': '2024/01/05',
    'Junio': '2024/01/06',
    'Julio': '2024/01/07',
    'Agosto': '2024/01/08',
    'Septiembre': '2024/01/09',
    'Octubre': '2024/01/10',
    'Noviembre': '2024/01/11',
    'Diciembre': '2024/01/12'
}
# DICCIONARIO (FECHA CONSUMO)
mese_dict_consumo = {
    'Enero': '1',
    'Febrero': '2',
    'Marzo': '3',
    'Abril': '4',
    'Mayo': '5',
    'Junio': '6',
    'Julio': '7',
    'Agosto': '8',
    'Septiembre': '9',
    'Octubre': '10',
    'Noviembre': '11',
    'Diciembre': '12'
}


#CONFIG PAGINA
st.set_page_config(page_icon='📊', layout='wide', page_title='Dashboard')

#FUNCION PARA PANTALLA DE INICIO DE SESIÓN
def show_login_form():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form(key='login_form'):
            logo_geves = st.image('assets/geves.png')
            username = st.text_input(label="Usuario", key='username', label_visibility='hidden', placeholder='Usuario')
            password = st.text_input("Contraseña", type="password", key='password', label_visibility='hidden', placeholder='Contraseña')
            submit_button = st.form_submit_button(label='Iniciar Sesión')
            if submit_button:
                if username == "admin" and password == "admin1111":
                    st.session_state.logged_in = True
                else:
                    st.error("Usuario/Contraseña incorrecto")

# FUNCION PARA CERRAR SESIÓN
def logout():
    st.session_state.logged_in = False

#FUNCION INTERFAZ PRINCIPAL
def main_interface():
    # SIDEBAR
    with st.sidebar:
        st.image('assets/Incoprovil.png')
        if st.button("Cerrar Sesión"):
            logout()
        
#MENU DEL SIDEBAR

        selected = option_menu(menu_title=None, options=['EPP', 'Costos', 'Kardex', 'Maquinaria'], icons=['person-badge-fill', 'coin', 'receipt', 'truck-front'])
        p1 = st.selectbox(label='Cliente', options=['INCOPROV'], label_visibility='hidden', placeholder='Cliente')
        p2 = st.selectbox(label='Empresa', options=['INCOPROV', 'HGM'], label_visibility='hidden', placeholder='Empresa')
        
        
        
#CLICK BODEGA SIDEBAR

    if selected == 'EPP':
        st.title('EPP')
               
        mes_inicio,mes_fin=st.select_slider(label='Rango Fecha Bodega', options=list(meses_dict.keys()), value=['Enero','Diciembre'], label_visibility='hidden' )
        fecha_inicio = meses_dict[mes_inicio]
        fecha_fin = meses_dict_fin[mes_fin]
        p4=fecha_inicio
        p5=fecha_fin
    
#-------------------------------------------BODEGA INICIO------------------------------------------------------------------------------------------
#LLAMADA APIbodega.py

        APIbodega = response(p1, p2, p4, p5)
        data = APIbodega.json()['datos']
        # Columnas que voy a llamar de 'datos'
        selected_columns = ['obra', 'recibe', 'nombreRecurso', 'undRecurso', 'cantidad', 'precio', 'subTotal', 'clase', 'nombreClase', 'fecha']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_data = [{column: entry[column] for column in selected_columns} for entry in data]

    
#RESULTADO APIbodega.py (DATOS)

#-------------------------------------------BODEGA (FILTROS INICIO)------------------------------------------------------------------------------------------

    #FILTRO DATOS API CLASE, OBRA, RECURSO y RECIBE

        filtered_data_clases = pd.DataFrame(filtered_data)
    
        col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
        with col1:
            filtered_clases_epp= filtered_data_clases[filtered_data_clases['clase'].str.startswith('0404')]
            nombre_clases_epp= filtered_clases_epp['nombreClase'].unique()
            epp_seleccionado = st.selectbox(label='Tipo EPP', options=[''] + list(nombre_clases_epp), placeholder='Tipos de EPP')
            filtered_data_clase = filtered_data_clases[filtered_data_clases['nombreClase'] == epp_seleccionado] if epp_seleccionado else filtered_data_clases
    
        with col2:
            obra = (filtered_data_clase['obra'].unique())
            obra_seleccionada = st.selectbox(label='Obra', options=[''] + list(obra), placeholder='Obra')
            filtered_data_obra = filtered_data_clase[filtered_data_clase['obra'] == obra_seleccionada] if obra_seleccionada else filtered_data_clase
    
        with col3:
            recursos = (filtered_data_obra['nombreRecurso'].unique())
            recurso_seleccionado = st.selectbox(label='Recurso', options=[''] + list(recursos), placeholder='Recursos')
            filtered_data_recurso = filtered_data_obra[filtered_data_obra['nombreRecurso'] == recurso_seleccionado] if recurso_seleccionado else filtered_data_obra
    
        with col4:
            recibe = (filtered_data_recurso['recibe'].unique())
            trabajador_seleccionado = st.selectbox(label='Trabajador', options=[''] + list(recibe), placeholder='Nombre Trabajador')
            filtered_data_trabajador = filtered_data_recurso[filtered_data_recurso['recibe'] == trabajador_seleccionado] if trabajador_seleccionado else filtered_data_recurso

#-------------------------------------------BODEGA (FILTROS FIN)------------------------------------------------------------------------------------------

#-------------------------------------------BODEGA (SUBMENU INICIO)------------------------------------------------------------------------------------------
    
    #MENU RESUMEN, FLUJO ECONOMICO, USO RECURSO
        
        selected = option_menu(menu_title=None, options=['Cantidad', 'Monto', 'Ver Datos'], icons=['123', 'cash-coin', 'database'], orientation='horizontal')

#-------------------------------------------BODEGA (SUBMENU FIN------------------------------------------------------------------------------------------
    
#-------------------------------------------BODEGA (CANTIDAD INICIO)------------------------------------------------------------------------------------------
  
        #CLICK MENU CANTIDAD, MONTO, DATOS
        if selected == 'Cantidad':
    #TOTAL CANTIDAD
            data_bodega=pd.DataFrame(filtered_data_trabajador)           
            #data_bodega['cantidad'] = data_bodega['cantidad'].astype(int)
            data_bodega['cantidad']=pd.to_numeric(data_bodega['cantidad'])
            data_bodega['fecha'] = pd.to_datetime(data_bodega['fecha'], dayfirst=True).dt.date
            
            suma_data_bodega=data_bodega.groupby('fecha')['cantidad'].sum().reset_index()
            suma_obra_bodega=data_bodega.groupby('obra')['cantidad'].sum().reset_index()
            suma_recibe_bodega=data_bodega.groupby('recibe')['cantidad'].sum().reset_index()
            suma_recurso_bodega=data_bodega.groupby('nombreRecurso')['cantidad'].sum().reset_index()            

            total_cantidad = data_bodega['cantidad'].sum()
            
            st.markdown("""
            <style>
            div[data-testid="metric-container"] {
                text-align: center;
            }
            div[data-testid="stMetricValue"] {
                font-size: 20px;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)
            col1,col2,col3 = st.columns([2,3,1])
            with col3:
                st.metric(label='Total Cantidad', value=f"{total_cantidad:,}")
            
        
    #GRAFICO CANTIDAD 

            graficoCantidad=st.bar_chart(suma_data_bodega.set_index('fecha'))
    
    #GRAFICOS OBRA, RECURSO, RECIBE
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObra = st.bar_chart(suma_obra_bodega.set_index('obra'))
            with col2:
                graficoRecibe = st.bar_chart(suma_recibe_bodega.set_index('recibe'))
            with col3:
                graficoRecurso = st.bar_chart(suma_recurso_bodega.set_index('nombreRecurso'))

#-------------------------------------------BODEGA (CANTIDAD FIN)------------------------------------------------------------------------------------------

#-------------------------------------------BODEGA (MONTO INICIO)------------------------------------------------------------------------------------------

        if selected == 'Monto':
    #TOTAL MONTO
            data_bodega=pd.DataFrame(filtered_data_trabajador)
            data_bodega['subTotal'] = data_bodega['subTotal'].astype(int)
            data_bodega['fecha'] = pd.to_datetime(data_bodega['fecha'], dayfirst=True).dt.date
            total_monto = data_bodega['subTotal'].sum()
            
            st.markdown("""
            <style>
            div[data-testid="metric-container"] {
                text-align: center;
            }
            div[data-testid="stMetricValue"] {
                font-size: 20px;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)
            col1,col2,col3 = st.columns([2,3,1])
            with col3:
                st.metric(label='Total Monto', value=f"{total_monto:,}")
    
    #GRAFICO MONTO    
            
            graficoMonto = st.bar_chart(data_bodega, x='fecha', y='subTotal', width=0, height=0, use_container_width=True)
    
    #GRAFICOS OBRA, RECURSO, RECIBE MONTO
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObraMonto = st.bar_chart(filtered_data_trabajador, x='obra', y='subTotal', width=0, height=0, use_container_width=True)
    
            with col2:
                graficoRecibeMonto = st.bar_chart(filtered_data_trabajador, x='recibe', y='subTotal', width=0, height=0, use_container_width=True)
            with col3:
                graficoRecursoMonto = st.bar_chart(filtered_data_trabajador, x='nombreRecurso', y='subTotal', width=0, height=0, use_container_width=True)

#-------------------------------------------BODEGA (MONTO FIN)------------------------------------------------------------------------------------------

#-------------------------------------------BODEGA (VER DATOS INICIO)------------------------------------------------------------------------------------------

        if selected == 'Ver Datos':
    #TABLA DATOS            
            datos_bodega= pd.DataFrame(filtered_data_trabajador).reset_index(drop=True)
            st.dataframe(filtered_data_trabajador)

#-------------------------------------------BODEGA (VER DATOS FIN)------------------------------------------------------------------------------------------


#-------------------------------------------BODEGA FIN------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS INICIO------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS (LLAMADA APIS INICIO)------------------------------------------------------------------------------------------

#CLICK SIDEBAR COSTOS

    if selected == 'Costos':

#LLAMADA APIobras
        APIobras = response_obras(p1, p2)
    
        if APIobras is None:
            st.error("Error: No se pudo obtener los datos de obras.")
        else:
            datos_obra = APIobras.json().get('datos', [])
            columns_obra = ['codObra']
            if datos_obra is not None:
                filtered = [{column: entry[column] for column in columns_obra} for entry in datos_obra]
            else:
                filtered = []
            
        filtered_data_obra = pd.DataFrame(filtered)
        
        st.title('Costos')
        
        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 2])
        
        with col1:
            
            par3 = st.selectbox(label='Periodo', options=['2024', '2023'], label_visibility='visible')
            filtro_obra = filtered_data_obra['codObra'].unique()
        
        with col2:
            par4 = st.selectbox(label='Obra', options=[''] + list(filtro_obra), label_visibility='visible', placeholder='Obra')


#LLAMADA APIconsumos
        
        APIconsumos = response_consumo(p1, p2, par3, par4)
        datos = APIconsumos.json()['datos']
        # Columnas que voy a llamar de 'datos'
        columns = ['obra', 'cantidad', 'tipoCosto', 'codigoArea', 'nombrePartida', 'nombreRecurso', 'fecha', 'total', 'unidad', 'precio','mes']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered = [{column: entry[column] for column in columns} for entry in datos]

#-------------------------------------------COSTOS (LLAMADA APIS FIN)------------------------------------------------------------------------------------------


#DATA FRAME PARA HACER LOS CALCULOS DE CONSUMOS

        filtered_data_consumos = pd.DataFrame(filtered)
        
 #-------------------------------------------COSTOS (FILTROS INICIO)------------------------------------------------------------------------------------------
       
#FILTROS APIconsumos

        with col3:
            t_costo=(filtered_data_consumos['tipoCosto'].unique())
            t_costo_seleccionado=st.selectbox(label='Tipo Costo', options=[''] + list(t_costo), placeholder='Tipo de Costos', label_visibility='visible' )
            filtered_t_costo = filtered_data_consumos[filtered_data_consumos['tipoCosto'] == t_costo_seleccionado] if t_costo_seleccionado else filtered_data_consumos
        with col4:
            area_consumo= (filtered_t_costo['codigoArea'].unique())
            area_consumo_seleccionada=st.selectbox(label='Área', options=[''] + list(area_consumo), placeholder='Nombre Área', label_visibility='visible')
            filtered_area_consumo = filtered_t_costo[filtered_t_costo['codigoArea'] == area_consumo_seleccionada] if area_consumo_seleccionada else filtered_t_costo
        with col5:
            partida_consumo= (filtered_area_consumo['nombrePartida'].unique())
            partida_consumo_seleccionada=st.selectbox(label='Partida', options=[''] + list(partida_consumo), placeholder='Nombre Partida', label_visibility='visible')
            filtered_partida_consumo = filtered_area_consumo[filtered_area_consumo['nombrePartida'] == partida_consumo_seleccionada] if partida_consumo_seleccionada else filtered_area_consumo
        with col6:
            recurso_consumo= (filtered_partida_consumo['nombreRecurso'].unique())
            recurso_consumo_seleccionada=st.selectbox(label='Recurso', options=[''] + list(recurso_consumo), placeholder='Nombre Recurso', label_visibility='visible')
            filtered_recurso_consumo = filtered_partida_consumo[filtered_partida_consumo['nombreRecurso'] == recurso_consumo_seleccionada] if recurso_consumo_seleccionada else filtered_partida_consumo
            
#-------------------------------------------COSTOS (FILTROS FIN)------------------------------------------------------------------------------------------
#-------------------------------------------COSTOS (SUBMENU INICIO)------------------------------------------------------------------------------------------

        selected = option_menu(menu_title=None, options=['','Resumen', 'Flujo Económico', 'Uso Recursos'], icons=['house','list-ol', 'cash-coin', 'tools'], orientation='horizontal')

#-------------------------------------------COSTOS (SUBMENU FIN)------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS (INDICADORES INICIO)------------------------------------------------------------------------------------------
#----DATAFRAME PARA CONSUMOS-----
        #fecha_consumo= (filtered_recurso_consumo['mes'].unique())
        #fecha_consumo_seleccionado= st.select_slider(label='Mes', options=list(mese_dict_consumo.keys()))
        #filtered_fecha_consumo = filtered_recurso_consumo[filtered_recurso_consumo['mes'] == fecha_consumo_seleccionado] if fecha_consumo_seleccionado else filtered_recurso_consumo
        

        data_consumo=pd.DataFrame(filtered_recurso_consumo)
        data_consumo['total'] = data_consumo['total'].astype(int)
        data_consumo['precio'] = data_consumo['precio'].astype(int)
        data_consumo['cantidad'] = data_consumo['cantidad'].astype(int)
#-------------------------------------------------------------------------------------------------------------------------------------
        
        suma_data_consumo = data_consumo.groupby('fecha')['total'].sum().reset_index()
        suma_tipocosto_consumo = data_consumo.groupby('tipoCosto')['total'].sum().reset_index()
        suma_area_consumo = data_consumo.groupby('codigoArea')['total'].sum().reset_index()
        suma_partida_consumo = data_consumo.groupby('nombrePartida')['total'].sum().reset_index()       
             
        suma_data_consumo['fecha'] = pd.to_datetime(suma_data_consumo['fecha'], dayfirst=True).dt.date

        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)
        antes_ayer = hoy - timedelta(days=2)
        hoy_menos3 = hoy - timedelta(days=3)
        
        df_hoy = suma_data_consumo[suma_data_consumo['fecha'] == hoy]
        df_ayer = suma_data_consumo[suma_data_consumo['fecha'] == ayer]
        df_antes_ayer = suma_data_consumo[suma_data_consumo['fecha'] == antes_ayer]
        df_hoy_menos3 = suma_data_consumo[suma_data_consumo['fecha'] == hoy_menos3]
        
        suma_total_hoy = df_hoy['total'].sum() if not df_hoy.empty else 0
        suma_total_ayer = df_ayer['total'].sum() if not df_ayer.empty else 0
        suma_total_antes_ayer = df_antes_ayer['total'].sum() if not df_antes_ayer.empty else 0
        suma_total_hoy_menos3 = df_hoy_menos3['total'].sum() if not df_hoy_menos3.empty else 0

        st.markdown("""
        <style>
        div[data-testid="metric-container"] {
            text-align: center;
        }
        div[data-testid="stMetricValue"] {
            font-size: 20px;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container(border=False):
        
            col1, col2, col3, col4, col5 = st.columns([0.7, 1, 1, 1, 1])
            with col1:
                st.metric(label='Total 3 días', value=f"{suma_total_hoy_menos3:,}")
                mes_inicio,mes_fin=st.select_slider(label='Rango Fecha Consumos', options=['1','2','3','4','5','6','7','8','9','10','11','12'], value=['1','12'], label_visibility='hidden' )

            with col2:
                st.metric(label='Total Costo antes ayer', value=f"{suma_total_antes_ayer:,}")

            with col3:
                st.metric(label='Total Costo ayer', value=f"{suma_total_ayer:,}")

            with col4:
                st.metric(label='Total Costo hoy', value=f"{suma_total_hoy:,}")

            with col5:
                total_suma_consumo = suma_data_consumo['total'].sum()
                st.metric(label= 'Total Consumos', value=f"{total_suma_consumo:,}")
            

            

#-------------------------------------------COSTOS (INDICADORES FIN)------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS (GRAFICOS)------------------------------------------------------------------------------------------

#----GRAFICO CONSUMOS---

#-------------------------------------------COSTOS (RESUMEN INICIO)------------------------------------------------------------------------------------------

        if selected == '':
            
            tabla_total = data_consumo[['codigoArea', 'total', 'fecha', 'mes']]
            tabla_total = tabla_total.rename(columns={'codigoArea': 'Área', 'total': 'Total', 'fecha':'Fecha', 'mes':'Mes'})
            
            df_tabla_total= pd.DataFrame(tabla_total)
            df_tabla_total['Total']=pd.to_numeric(df_tabla_total['Total'])
            df_tabla_total['Fecha'] = pd.to_datetime(df_tabla_total['Fecha'], dayfirst=True).dt.date
            df_tabla_total['Mes']=pd.to_numeric(df_tabla_total['Mes'])
            mes_inicio= pd.to_numeric(mes_inicio)
            mes_fin= pd.to_numeric(mes_fin)


            df_filtrado = df_tabla_total[(df_tabla_total['Mes'] >= mes_inicio) & (df_tabla_total['Mes'] <= mes_fin)]

            pivot_df_total = df_filtrado.pivot_table(index='Área', columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
            st.dataframe(pivot_df_total, width=1100)

            df_tabla_total_suma=df_tabla_total['Total'].sum()
            
            grafico_consumos= st.bar_chart(df_tabla_total, x='Fecha', y='Total')

            col1,col2,col3 = st.columns([1,1,1])
            with col1:
                    st.bar_chart(suma_tipocosto_consumo.set_index('tipoCosto'))
            with col2:
                    st.bar_chart(suma_area_consumo.set_index('codigoArea'))
            with col3:
                    st.bar_chart(suma_partida_consumo.set_index('nombrePartida'))


        if selected == 'Resumen':

            tabla_resumen = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso','unidad', 'cantidad', 'precio', 'total']]
            tabla_resumen = tabla_resumen.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'nombreRecurso': 'Recurso', 'unidad':'Unidad', 'cantidad': 'Cantidad', 'precio': 'Precio', 'total': 'Total'})
            tabla_resumen['Total']=pd.to_numeric(tabla_resumen['Total'])
            tabla_resumen['Precio']=pd.to_numeric(tabla_resumen['Precio'])

            with st.container(border=False, height=600):
                st.dataframe(tabla_resumen, width=1100)

        if selected == 'Flujo Económico':

            tabla_flujo_economico = data_consumo[['codigoArea', 'nombrePartida', 'total', 'fecha', 'mes']]
            tabla_flujo_economico = tabla_flujo_economico.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'total': 'Total', 'fecha':'Fecha', 'mes':'Mes'})            
           
            df_flujo_economico= pd.DataFrame(tabla_flujo_economico)
            df_flujo_economico['Total']=pd.to_numeric(df_flujo_economico['Total'])
            df_flujo_economico['Fecha'] = pd.to_datetime(df_flujo_economico['Fecha'], dayfirst=True).dt.date            
            df_flujo_economico['Mes']=pd.to_numeric(df_flujo_economico['Mes'])
            mes_inicio= pd.to_numeric(mes_inicio)
            mes_fin= pd.to_numeric(mes_fin)

            df_filtrado_fe = df_flujo_economico[(df_flujo_economico['Mes'] >= mes_inicio) & (df_flujo_economico['Mes'] <= mes_fin)]
               # Crear la pivot table
            pivot_df_fe = df_filtrado_fe.pivot_table(index=['Área', 'Partida'], columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)

            formatted_pivot_df_fe = pivot_df_fe.applymap(lambda x: f'{x:,}')

                # Mostrar la pivot table
                
            st.dataframe(formatted_pivot_df_fe, width=1100)            
            

        if selected == 'Uso Recursos':

            tabla_uso_recurso = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso', 'unidad', 'cantidad','fecha', 'mes']]
            tabla_uso_recurso = tabla_uso_recurso.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida','nombreRecurso': 'Recurso', 'unidad':'Unidad', 'cantidad': 'Cantidad', 'fecha':'Fecha', 'mes':'Mes'})                
           
            df_uso_recurso= pd.DataFrame(tabla_uso_recurso)
            df_uso_recurso['Cantidad']=pd.to_numeric(df_uso_recurso['Cantidad'])
            df_uso_recurso['Fecha'] = pd.to_datetime(df_uso_recurso['Fecha'], dayfirst=True).dt.date
            df_uso_recurso['Mes']=pd.to_numeric(df_uso_recurso['Mes'])
            mes_inicio= pd.to_numeric(mes_inicio)
            mes_fin= pd.to_numeric(mes_fin)

            df_filtrado_uso = df_uso_recurso[(df_uso_recurso['Mes'] >= mes_inicio) & (df_uso_recurso['Mes'] <= mes_fin)]
               # Crear la pivot table
            pivot_df = df_filtrado_uso.pivot_table(index=['Área', 'Partida', 'Recurso', 'Unidad'], columns='Fecha', values='Cantidad', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)

            formatted_pivot_df = pivot_df.applymap(lambda x: f'{x:,}')

                # Mostrar la pivot table
                
            st.dataframe(formatted_pivot_df, width=1100)



#-------------------------------------------COSTOS FIN------------------------------------------------------------------------------------------


    if selected == 'kardex':

    
        if selected == 'Maquinaria':


#LLAMADA APIkardex.py

            APIkardex = response(p1, p2,par3,kardex4,kardex5,kardex6)
        data = APIbodega.json()['datos']
        # Columnas que voy a llamar de 'datos'
        selected_columns = ['obra', 'recibe', 'nombreRecurso', 'undRecurso', 'cantidad', 'precio', 'subTotal', 'clase', 'nombreClase', 'fecha']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_data = [{column: entry[column] for column in selected_columns} for entry in data]




















#----------------PRUEBA TOTALES!!!!!!

    
        st.title('Seguimiento') 
        APIobras = response_obras(p1, p2)
        datos_obra = APIobras.json()['datos']
    # Columnas que voy a llamar de 'datos'
        columns_obra = ['codObra']
    # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_obra = [{column: entry[column] for column in columns_obra} for entry in datos_obra]
        filtered_data_obra = pd.DataFrame(filtered_obra)

        col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,1])
        with col1:
            par3=st.selectbox(label='Periodo', options=['2024','2023'], label_visibility='visible')
            filtro_obra = (filtered_data_obra['codObra'].unique())
        with col2:
            par4=st.selectbox(label='Obra', options=[''] + list(filtro_obra), label_visibility='visible', placeholder='Obra')

#LLAMADA APIconsumos
        
        APIconsumos = response_consumo(p1, p2, par3, par4)
        datos = APIconsumos.json()['datos']
        # Columnas que voy a llamar de 'datos'
        columns = ['obra', 'cantidad', 'tipoCosto', 'codigoArea', 'nombrePartida', 'nombreRecurso', 'fecha', 'total']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered = [{column: entry[column] for column in columns} for entry in datos]
        df= pd.DataFrame(filtered)
#DATA FRAME PARA HACER LOS CALCULOS DE CONSUMOS
        
        df['total'] = df['total'].astype(int) #transformar a numero entero el total
        df['fecha'] = pd.to_datetime(df['fecha']) #transformar la fecha a tipo fecha      
        hoy= datetime.now().date() #traer la fecha de hoy
        df_hoy = df[df['fecha'].dt.date == hoy] #columna fecha sea igual a la fecha hoy
        df_suma_hoy = df_hoy['total'].sum()
        df_suma= df['total'].sum() #suma de la columna total
        st.write(hoy)
        st.write(df.dtypes) #muestra los tipos de las columnas
        st.text(df_suma) #muestra la suma en texto
        st.metric(label='Total Suma', value=f"{df_suma:,}") #muestra la suma como metrica
        st.metric(label='Total Suma Hoy', value=f"{df_suma_hoy:,}") #muestra la suma como metrica de hoy


        suma_df= df.groupby('fecha')['total'].sum().reset_index()
        grafico_consumos=st.bar_chart(suma_df.set_index('fecha'))
        
        st.table(df)

        




       







# Comprobación de estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if st.session_state.logged_in:
    main_interface()
else:
    st.session_state.show_login = True
    show_login_form()
