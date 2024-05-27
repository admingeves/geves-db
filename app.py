import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from streamlit_option_menu import option_menu
from APIbodega import response
from APIconsumos import response_consumo
from APIobras import response_obras
from APIkardex import response_kardex
from datetime import datetime, timedelta



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

def show_login_form():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form(key='login_form'):
            st.image('assets/geves.png')
            username = st.text_input(label="Usuario", key='username', label_visibility='hidden', placeholder='Usuario')
            password = st.text_input("Contraseña", type="password", key='password', label_visibility='hidden', placeholder='Contraseña')
            submit_button = st.form_submit_button(label='Iniciar Sesión')
            if submit_button:
                if username == "invitado" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                else:
                    st.error("Usuario/Contraseña incorrecto")

# FUNCION PARA CERRAR SESIÓN
def logout():
    st.session_state.logged_in = False
    st.session_state.show_login = True

#FUNCION INTERFAZ PRINCIPAL
def main_interface():
    # SIDEBAR
    with st.sidebar:
        st.image('assets/Incoprovil.png')
        if st.button("Cerrar Sesión"):
            logout()
        
#MENU DEL SIDEBAR
        
        selected = option_menu(menu_title=None, options=['Costos', 'EPP', 'Kardex', 'Maquinaria'], icons=['coin', 'person-badge', 'receipt', 'truck-front'])

        st.markdown(
            """
            <style>
            .stSelectbox {
                margin-top: -20px;
                margin-bottom: -20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        p1 = st.selectbox(label='Cliente', options=['INCOPROV'], label_visibility='hidden', placeholder='Cliente')
        p2 = st.selectbox(label='Empresa', options=['INCOPROV', 'HGM'], label_visibility='hidden', placeholder='Empresa')
        
        
        
#CLICK BODEGA SIDEBAR

    if selected == 'EPP':
        #st.title('EPP')
               
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
        selected_columns = ['obra', 'recibe', 'nombreRecurso', 'undRecurso', 'cantidad', 'precio', 'subTotal', 'clase', 'nombreClase', 'fecha', 'mes']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_data = [{column: entry[column] for column in selected_columns} for entry in data]
        filtered_df=pd.DataFrame(filtered_data)
    
#RESULTADO APIbodega.py (DATOS)

#-------------------------------------------BODEGA (FILTROS INICIO)------------------------------------------------------------------------------------------

    #FILTRO DATOS API CLASE, OBRA, RECURSO y RECIBE
        filtered_clases_epp= filtered_df[filtered_df['clase'].str.startswith('0404')]
        filtered_data_clases = pd.DataFrame(filtered_clases_epp)
        st.markdown(
            """
            <style>
            .stSlider {
                margin-top: -30px;
                margin-bottom: -10px;
            }
            .stSelectbox {
                margin-top: -10px;
                margin-bottom: -10px;
            }
            .block-container {
                padding-top: 20px;
                padding-bottom: 0px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
        with col1:
            nombre_clases_epp= filtered_data_clases['nombreClase'].unique()
            epp_seleccionado = st.selectbox(label='Clase EPP', options=[''] + list(nombre_clases_epp), placeholder='Clases EPP')
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
        selected = option_menu(menu_title=None, options=['Cantidad', 'Monto', 'EPP' ,'Data'], icons=['123', 'cash-coin', 'calendar-date' , 'database'], orientation='horizontal')

#-------------------------------------------BODEGA (SUBMENU FIN------------------------------------------------------------------------------------------
    
#-------------------------------------------BODEGA (CANTIDAD INICIO)------------------------------------------------------------------------------------------


        if selected == 'Cantidad':
            # TOTAL CANTIDAD
            data_bodega = pd.DataFrame(filtered_data_trabajador)
            data_bodega['cantidad'] = pd.to_numeric(data_bodega['cantidad'])
            data_bodega['fecha'] = pd.to_datetime(data_bodega['fecha'], dayfirst=True).dt.date
            data_bodega['mes'] = pd.to_numeric(data_bodega['mes'])

            suma_data_bodega = data_bodega.groupby('fecha')['cantidad'].sum().reset_index()
            suma_data_bodega_mes = data_bodega.groupby('mes')['cantidad'].sum().reset_index()
            suma_obra_bodega = data_bodega.groupby('obra')['cantidad'].sum().reset_index()
            suma_recibe_bodega = data_bodega.groupby('recibe')['cantidad'].sum().reset_index()
            suma_recurso_bodega = data_bodega.groupby('nombreRecurso')['cantidad'].sum().reset_index()

            total_cantidad = data_bodega['cantidad'].sum()

            col1,col2= st.columns([6,1])
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
            with col1:
            # GRÁFICO CANTIDAD
                suma_data_bodega_mes['mes_numerico'] = range(1, len(suma_data_bodega_mes) + 1)
                fig = px.line(suma_data_bodega_mes, x='mes_numerico', y='cantidad', title='Cantidad por Mes')
                fig.update_xaxes(title='Mes', tickvals=suma_data_bodega_mes['mes_numerico'], ticktext=suma_data_bodega_mes['mes'], showgrid=False)
                fig.update_layout(
                    height=250,  # Ajustar la altura de la gráfica
                    margin=dict(l=0, r=0, t=25, b=0),  # Ajustar los márgenes
                    xaxis_title='',  # Quitar el título del eje x
                    yaxis_title='',  # Quitar el título del eje y
                    showlegend=True,  # Mostrar la leyenda
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.metric(label='Total Cantidad', value=f"{total_cantidad:,}")

            # GRÁFICOS OBRA, RECIBE, RECURSO
            col1, col2, col3 = st.columns(3)

            with col1:
                fig1 = px.pie(suma_obra_bodega, values='cantidad', names='obra', title='Distribución por Obra')
                fig1.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                top_5_recibe = suma_recibe_bodega.nlargest(5, 'cantidad')
                fig2 = px.pie(top_5_recibe, values='cantidad', names='recibe', title='Top 5 Trabajadores por Cantidad')
                fig2.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col3:
                top_5_epp = suma_recurso_bodega.nlargest(5, 'cantidad')
                fig3 = px.pie(top_5_epp, values='cantidad', names='nombreRecurso', title='Top 5 EPP por Cantidad')
                fig3.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig3, use_container_width=True)
            cantidad = data_bodega[['obra', 'recibe', 'nombreRecurso', 'fecha', 'cantidad']]
            tabla_total = cantidad.rename(columns={'obra': 'Obra', 'recibe': 'Trabajador', 'nombreRecurso':'EPP', 'fecha':'Fecha', 'cantidad':'Cantidad'})
            pivot_df_cantidad = tabla_total.pivot_table(index=['Obra', 'Trabajador', 'EPP'], columns='Fecha', values='Cantidad', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
            st.dataframe(pivot_df_cantidad, width=1100)

            data_bodega['fecha'] = pd.to_datetime(data_bodega['fecha'])
            data_bodega = data_bodega.sort_values(by=['nombreRecurso', 'fecha'])
            data_bodega['tiempo_diferencia'] = data_bodega.groupby('nombreRecurso')['fecha'].diff().dt.days
            promedio_tiempo_diferencia = data_bodega.groupby('nombreRecurso')['tiempo_diferencia'].mean().reset_index()
            promedio_tiempo_diferencia.columns = ['nombreRecurso', 'promedio_tiempo_diferencia']
            cantidad_salidas = data_bodega['nombreRecurso'].value_counts().reset_index()
            cantidad_salidas.columns = ['nombreRecurso', 'cantidad_salidas']

            resultado = pd.merge(cantidad_salidas,promedio_tiempo_diferencia, on='nombreRecurso')
            #st.dataframe(resultado)
        
        elif selected == 'Monto':
            # TOTAL MONTO
            data_bodega_monto = pd.DataFrame(filtered_data_trabajador)
            data_bodega_monto['subTotal'] = pd.to_numeric(data_bodega_monto['subTotal'])
            data_bodega_monto['fecha'] = pd.to_datetime(data_bodega_monto['fecha'], dayfirst=True).dt.date
            data_bodega_monto['mes'] = pd.to_numeric(data_bodega_monto['mes'])

            suma_data_bodega_monto = data_bodega_monto.groupby('fecha')['subTotal'].sum().reset_index()
            suma_data_bodega_mes_monto = data_bodega_monto.groupby('mes')['subTotal'].sum().reset_index()
            suma_obra_bodega_monto = data_bodega_monto.groupby('obra')['subTotal'].sum().reset_index()
            suma_recibe_bodega_monto = data_bodega_monto.groupby('recibe')['subTotal'].sum().reset_index()
            suma_recurso_bodega_monto = data_bodega_monto.groupby('nombreRecurso')['subTotal'].sum().reset_index()

            total_monto = data_bodega_monto['subTotal'].sum()

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
            col1,col2= st.columns([6,1])
            
            with col1:
            # GRÁFICO MONTO
                suma_data_bodega_mes_monto['mes_numerico'] = range(1, len(suma_data_bodega_mes_monto) + 1)
                fig = px.line(suma_data_bodega_mes_monto, x='mes_numerico', y='subTotal', title='Total Monto por Mes')
                fig.update_xaxes(title='Mes', tickvals=suma_data_bodega_mes_monto['mes_numerico'], ticktext=suma_data_bodega_mes_monto['mes'])
                fig.update_layout(
                    height=250,  # Ajustar la altura de la gráfica
                    margin=dict(l=0, r=0, t=25, b=0),  # Ajustar los márgenes
                    xaxis_title='',  # Quitar el título del eje x
                    yaxis_title='',  # Quitar el título del eje y
                    showlegend=True,  # Mostrar la leyenda
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.metric(label='Total Monto', value=f"{total_monto:,}")


            # GRÁFICOS OBRA, RECIBE, RECURSO MONTO
            col1, col2, col3 = st.columns(3)

            with col1:
                fig1 = px.pie(suma_obra_bodega_monto, values='subTotal', names='obra', title='Distribución por Obra')
                fig1.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                top_5_recibe = suma_recibe_bodega_monto.nlargest(5, 'subTotal')
                fig2 = px.pie(top_5_recibe, values='subTotal', names='recibe', title='Top 5 Trabajadores por Costo')
                fig2.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col3:
                top_5_epp = suma_recurso_bodega_monto.nlargest(5, 'subTotal')
                fig3 = px.pie(top_5_epp, values='subTotal', names='nombreRecurso', title='Top 5 EPP por Costo')
                fig3.update_layout(legend=dict(
                    orientation="h",  # Orientación horizontal
                    yanchor="bottom",  # Anclar en la parte inferior
                    y=-0.2,  # Ajustar la posición vertical (puedes cambiar este valor para ajustar la posición)
                    xanchor="center",  # Anclar en el centro horizontal
                    x=0.5  # Centrar horizontalmente
                    ),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig3, use_container_width=True)

            monto = data_bodega_monto[['obra', 'recibe', 'nombreRecurso', 'fecha', 'subTotal', 'cantidad', 'precio', 'mes']]
            tabla_total = monto.rename(columns={'obra': 'Obra', 'recibe': 'Trabajador', 'nombreRecurso':'EPP', 'fecha':'Fecha', 'subTotal':'Total', 'cantidad': 'Cantidad', 'precio':'Precio', 'mes':'Mes'})
            pivot_df_monto = tabla_total.pivot_table(index=['Obra', 'Trabajador', 'EPP'], columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
            st.dataframe(pivot_df_monto, width=1100)

        elif selected == 'EPP':
            
            data_bodega_monto = pd.DataFrame(filtered_data_trabajador)
            monto = data_bodega_monto[['obra', 'recibe', 'nombreRecurso', 'fecha',  'cantidad']]
            tabla_total = monto.rename(columns={'obra': 'Obra', 'recibe': 'Trabajador', 'nombreRecurso':'EPP', 'fecha':'Fecha', 'cantidad': 'Cantidad'})
            datos_bodega = tabla_total[['Trabajador', 'EPP', 'Cantidad','Fecha']]
            
            datos_bodega['Fecha'] = pd.to_datetime(datos_bodega['Fecha'], dayfirst=True).dt.date
            datos_bodega['Antigüedad EPP (días)'] = (datetime.now().date() - datos_bodega['Fecha']).apply(lambda x: x.days)
            datos_bodega = datos_bodega.sort_values(by='Antigüedad EPP (días)', ascending=False)
            
            st.dataframe(datos_bodega, width=1100)



        elif selected == 'Data':
            # TABLA DATOS
            data_bodega_monto = pd.DataFrame(filtered_data_trabajador)
            monto = data_bodega_monto[['obra', 'recibe', 'nombreRecurso', 'fecha', 'subTotal', 'cantidad', 'precio', 'mes', 'undRecurso']]
            tabla_total = monto.rename(columns={'obra': 'Obra', 'recibe': 'Trabajador', 'nombreRecurso':'EPP', 'fecha':'Fecha', 'subTotal':'Total', 'cantidad': 'Cantidad', 'precio':'Precio', 'mes':'Mes', 'undRecurso':'Unidad'})
            datos_bodega = tabla_total[['Obra', 'Trabajador', 'EPP', 'Unidad', 'Cantidad', 'Precio', 'Total', 'Fecha', 'Mes']]
            
            datos_bodega['Fecha'] = pd.to_datetime(datos_bodega['Fecha'], dayfirst=True).dt.date
            datos_bodega['Antigüedad EPP (días)'] = (datetime.now().date() - datos_bodega['Fecha']).apply(lambda x: x.days)
            
            st.dataframe(datos_bodega, width=1100)
           

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
        
        #st.title('Costos')
        
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
        columns = ['obra', 'cantidad', 'tipoCosto', 'codigoArea', 'nombrePartida', 'nombreRecurso', 'fecha', 'total', 'unidad', 'precio','mes', 'tipoDoc']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered = [{column: entry[column] for column in columns} for entry in datos]

#-------------------------------------------COSTOS (LLAMADA APIS FIN)------------------------------------------------------------------------------------------

        if filtered:

            filtered_data_consumos_con_transferencias = pd.DataFrame(filtered)
            filtered_data_consumos= filtered_data_consumos_con_transferencias[~filtered_data_consumos_con_transferencias['tipoDoc'].str.startswith('Transferencia Obra')]
 #-------------------------------------------COSTOS (FILTROS INICIO)------------------------------------------------------------------------------------------
       
#FILTROS APIconsumos
            st.markdown(
            """
            <style>
            .stSlider {
                margin-top: -40px;
                margin-bottom: -10px;
            }
            .stSelectbox {
                margin-top: 30px;
                margin-bottom: -10px;
            }
            .block-container {
                padding-top: 20px;
                padding-bottom: 0px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

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

            mes_inicio,mes_fin=st.select_slider(label='Rango Fecha Consumos', options=['1','2','3','4','5','6','7','8','9','10','11','12'], value=['1','12'], label_visibility='hidden' )
            selected = option_menu(menu_title=None, options=['', 'Obras' , 'Áreas', 'Partidas','APU'], icons=['bar-chart', 'currency-dollar', 'currency-dollar', 'currency-dollar', 'tools'], orientation='horizontal')

            data_consumo=pd.DataFrame(filtered_recurso_consumo)
            data_consumo['total'] = data_consumo['total'].astype(int)
            data_consumo['precio'] = data_consumo['precio'].astype(int)
            data_consumo['cantidad'] = data_consumo['cantidad'].astype(int)
    #-------------------------------------------------------------------------------------------------------------------------------------
            
            suma_data_consumo = data_consumo.groupby('fecha')['total'].sum().reset_index()
            suma_tipocosto_consumo = data_consumo.groupby('tipoCosto')['total'].sum().reset_index()
            suma_area_consumo = data_consumo.groupby('codigoArea')['total'].sum().reset_index()
            suma_partida_consumo = data_consumo.groupby('nombrePartida')['total'].sum().reset_index()
            suma_data_consumo_mes = data_consumo.groupby('mes')['total'].sum().reset_index()
            suma_obra_consumo= data_consumo.groupby('obra')['total'].sum().reset_index()  
                
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
            suma_total_consumo_general= suma_data_consumo_mes['total'].sum()

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

            if suma_total_ayer > 0:
                variacion_porcentual_hoy = ((suma_total_hoy - suma_total_ayer) / suma_total_ayer) * 100
            else:
                variacion_porcentual_hoy = 0  

            if suma_total_antes_ayer > 0:
                variacion_porcentual_ayer = ((suma_total_ayer - suma_total_antes_ayer) / suma_total_antes_ayer) * 100
            else:
                variacion_porcentual_ayer = 0  

            if suma_total_hoy_menos3 > 0:
                variacion_porcentual_antes_ayer = ((suma_total_antes_ayer - suma_total_hoy_menos3) / suma_total_hoy_menos3) * 100
            else:
                variacion_porcentual_antes_ayer = 0 

            

            if selected == '':
                with st.container(border=False):
            
                    col1, col2, col3, col4, col5 = st.columns([0.7, 1, 1, 1, 1])
                    with col1:
                        st.metric(label=f'{hoy_menos3}', value=f"{suma_total_hoy_menos3:,}")

                    with col2:
                        st.metric(label=f'{antes_ayer}', value=f"{suma_total_antes_ayer:,}", delta=f"{variacion_porcentual_antes_ayer:.2f}%")

                    with col3:
                        st.metric(label=f'{ayer}', value=f"{suma_total_ayer:,}", delta=f"{variacion_porcentual_ayer:.2f}%")

                    with col4:
                        st.metric(label='Hoy', value=f"{suma_total_hoy:,}", delta=f"{variacion_porcentual_hoy:.2f}%")

                    with col5:
                        tabla_flujo_total = data_consumo[['codigoArea', 'nombrePartida', 'total', 'fecha', 'mes', 'obra']]
                        tabla_flujo_total = tabla_flujo_total.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'total': 'Total', 'fecha':'Fecha', 'mes':'Mes'})            
                        df_flujo_total= pd.DataFrame(tabla_flujo_total)
                        df_flujo_total['Total']=pd.to_numeric(df_flujo_total['Total'])
                        df_flujo_total['Fecha'] = pd.to_datetime(df_flujo_total['Fecha'], dayfirst=True).dt.date            
                        df_flujo_total['Mes']=pd.to_numeric(df_flujo_total['Mes'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        df_filtrado_total = df_flujo_total[(df_flujo_total['Mes'] >= mes_inicio) & (df_flujo_total['Mes'] <= mes_fin)]
                        formato_para_total= df_filtrado_total['Total'].sum()       
                        st.metric(label= 'Total Costo', value=f"{formato_para_total:,}")
                
                tabla_total = data_consumo[['obra', 'total', 'fecha', 'mes']]
                tabla_total = tabla_total.rename(columns={'obra': 'Obra', 'total': 'Total', 'fecha':'Fecha', 'mes':'Mes'})
                
                df_tabla_total= pd.DataFrame(tabla_total)
                df_tabla_total['Total']=pd.to_numeric(df_tabla_total['Total'])
                df_tabla_total['Fecha'] = pd.to_datetime(df_tabla_total['Fecha'], dayfirst=True).dt.date
                df_tabla_total['Mes']=pd.to_numeric(df_tabla_total['Mes'])
                mes_inicio= pd.to_numeric(mes_inicio)
                mes_fin= pd.to_numeric(mes_fin)


                df_filtrado = df_tabla_total[(df_tabla_total['Mes'] >= mes_inicio) & (df_tabla_total['Mes'] <= mes_fin)]

                pivot_df_total = df_filtrado.pivot_table(index='Obra', columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
                suma_data_consumo_mes['mes_numerico'] = range(1, len(suma_data_consumo_mes) + 1)
                fig = px.line(suma_data_consumo_mes, x='mes_numerico', y='total', title='Total Costo por Mes')
                fig.update_xaxes(title='Meses', tickvals=suma_data_consumo_mes['mes_numerico'], ticktext=suma_data_consumo_mes['mes'])
                fig.update_layout(
                        height=250,  # Ajustar la altura de la gráfica
                        margin=dict(l=0, r=0, t=25, b=0),  # Ajustar los márgenes
                        xaxis_title='',  # Quitar el título del eje x
                        yaxis_title='',  # Quitar el título del eje y
                        showlegend=True,  # Mostrar la leyenda
                        yaxis=dict(showgrid=False)
                    )
                st.plotly_chart(fig, use_container_width=True)

                col1,col2,col3 = st.columns([1,1,1])
                with col1:
                        suma_obra_consumo_sorted = suma_obra_consumo.sort_values(by='total', ascending=False)
                        top_5_suma_obra_consumo = suma_obra_consumo_sorted.head(5)
                        fig1 = px.pie(top_5_suma_obra_consumo, values='total', names='obra', title='Distribución por Obra')
                        fig1.update_layout(
                        showlegend=False,  # Quitar la leyenda
                        margin=dict(l=40, r=40, t=40, b=40)
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                        
                with col2:
                        suma_area_consumo_sorted = suma_area_consumo.sort_values(by='total', ascending=False)
                        top_5_suma_area_consumo = suma_area_consumo_sorted.head(5)
                        fig2 = px.pie(top_5_suma_area_consumo, values = 'total', names = 'codigoArea', title='Distribución por Área')
                        fig2.update_layout(
                            showlegend=False,  # Quitar la leyenda si es necesario
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        fig2.update_xaxes(title_text='', showgrid=False)  # Quitar el título del eje x
                        fig2.update_yaxes(title_text='', showgrid=False)  # Quitar el título del eje y
                        st.plotly_chart(fig2, use_container_width=True)
                        
                with col3:
                        suma_partida_consumo_sorted = suma_partida_consumo.sort_values(by='total', ascending=False)
                        top_5_suma_partida_consumo = suma_partida_consumo_sorted.head(5)
                        fig3 = px.pie(top_5_suma_partida_consumo, values = 'total', names = 'nombrePartida', title='Distribución por Partida')
                        fig3.update_layout(
                            showlegend=False,  # Quitar la leyenda si es necesario
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        fig3.update_xaxes(title_text='', showgrid=False)  # Quitar el título del eje x
                        fig3.update_yaxes(title_text='', showgrid=False)  # Quitar el título del eje y
                        st.plotly_chart(fig3, use_container_width=True)

               
           # if selected == 'Resumen':

            #    tabla_resumen = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso','unidad', 'cantidad', 'precio', 'total', 'mes']]
             #   tabla_resumen = tabla_resumen.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'nombreRecurso': 'Recurso', 'unidad':'Unidad', 'cantidad': 'Cantidad', 'precio': 'Precio', 'total': 'Total'})
              #  tabla_resumen['Total']=pd.to_numeric(tabla_resumen['Total'])
               # tabla_resumen['Precio']=pd.to_numeric(tabla_resumen['Precio'])
                #mes_inicio= pd.to_numeric(mes_inicio)
                #mes_fin= pd.to_numeric(mes_fin)
                #df_filtrado = tabla_resumen[(tabla_resumen['mes'] >= mes_inicio) & (tabla_resumen['mes'] <= mes_fin)]

                #with st.container(border=False, height=600):
                 #   st.dataframe(df_filtrado, width=1100)

            if selected == 'Obras':
                col1,col2 = st.columns([1,4])
                with col1:
                    selected = option_menu(menu_title=None, options=['Mensual', 'Diario'], icons=['calendar2-month','calendar2-day'], orientation='vertical')
                
                with col2:
                    if selected == 'Mensual':
                        tabla_obras = data_consumo[['obra', 'mes', 'total']]    
                        tabla_obras = tabla_obras.rename(columns={'obra':'Obra', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_obras['Total Costo'] = pd.to_numeric(tabla_obras['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        obras_filtrado = tabla_obras[(tabla_obras['Mes'] >= mes_inicio) & (tabla_obras['Mes'] <= mes_fin)]
                        pivot_obras_filtrado = obras_filtrado.pivot_table(index = ['Obra'], columns = 'Mes', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_obras_filtrado = pivot_obras_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_obras_filtrado, width = 1100)
                    if selected == 'Diario':
                        tabla_obras_dia = data_consumo[['obra', 'mes' ,'fecha', 'total']]
                        tabla_obras_dia = tabla_obras_dia.rename(columns = {'obra':'Obra', 'fecha':'Fecha', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_obras_dia['Total Costo'] = pd.to_numeric(tabla_obras_dia['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        obras_dia_filtrado = tabla_obras_dia[(tabla_obras_dia['Mes'] >= mes_inicio) & (tabla_obras_dia['Mes'] <= mes_fin)]
                        pivot_obras_dia_filtrado = obras_dia_filtrado.pivot_table(index = ['Obra'], columns = 'Fecha', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_obras_dia_filtrado = pivot_obras_dia_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_obras_dia_filtrado, width = 1100)

            if selected == 'Áreas':
                col1,col2 = st.columns([1,4])
                with col1:
                    selected = option_menu(menu_title=None, options=['Mensual', 'Diario'], icons=['calendar2-month','calendar2-day'], orientation='vertical')
                
                with col2:
                    if selected == 'Mensual':
                        tabla_areas = data_consumo[['codigoArea', 'mes', 'total']]    
                        tabla_areas = tabla_areas.rename(columns={'codigoArea':'Área', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_areas['Total Costo'] = pd.to_numeric(tabla_areas['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        areas_filtrado = tabla_areas[(tabla_areas['Mes'] >= mes_inicio) & (tabla_areas['Mes'] <= mes_fin)]
                        pivot_areas_filtrado = areas_filtrado.pivot_table(index = ['Área'], columns = 'Mes', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_areas_filtrado = pivot_areas_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_areas_filtrado, width = 1100)
                    if selected == 'Diario':
                        tabla_areas_dia = data_consumo[['codigoArea', 'mes' ,'fecha', 'total']]
                        tabla_areas_dia = tabla_areas_dia.rename(columns = {'codigoArea':'Área', 'fecha':'Fecha', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_areas_dia['Total Costo'] = pd.to_numeric(tabla_areas_dia['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        areas_dia_filtrado = tabla_areas_dia[(tabla_areas_dia['Mes'] >= mes_inicio) & (tabla_areas_dia['Mes'] <= mes_fin)]
                        pivot_areas_dia_filtrado = areas_dia_filtrado.pivot_table(index = ['Área'], columns = 'Fecha', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_areas_dia_filtrado = pivot_areas_dia_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_areas_dia_filtrado, width = 1100)


            if selected == 'Partidas':
                col1,col2 = st.columns([1,4])
                with col1:
                    selected = option_menu(menu_title=None, options=['Mensual', 'Diario'], icons=['calendar2-month','calendar2-day'], orientation='vertical')
                
                with col2:
                    if selected == 'Mensual':
                        tabla_partidas = data_consumo[['nombrePartida', 'mes', 'total']]    
                        tabla_partidas = tabla_partidas.rename(columns={'nombrePartida':'Partida', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_partidas['Total Costo'] = pd.to_numeric(tabla_partidas['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        partidas_filtrado = tabla_partidas[(tabla_partidas['Mes'] >= mes_inicio) & (tabla_partidas['Mes'] <= mes_fin)]
                        pivot_partidas_filtrado = partidas_filtrado.pivot_table(index = ['Partida'], columns = 'Mes', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_partidas_filtrado = pivot_partidas_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_partidas_filtrado, width = 1100)
                    if selected == 'Diario':
                        tabla_partidas_dia = data_consumo[['nombrePartida', 'mes' ,'fecha', 'total']]
                        tabla_partidas_dia = tabla_partidas_dia.rename(columns = {'nombrePartida':'Partida', 'fecha':'Fecha', 'total':'Total Costo', 'mes':'Mes'})
                        tabla_partidas_dia['Total Costo'] = pd.to_numeric(tabla_partidas_dia['Total Costo'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        partidas_dia_filtrado = tabla_partidas_dia[(tabla_partidas_dia['Mes'] >= mes_inicio) & (tabla_partidas_dia['Mes'] <= mes_fin)]
                        pivot_partidas_dia_filtrado = partidas_dia_filtrado.pivot_table(index = ['Partida'], columns = 'Fecha', values = 'Total Costo', aggfunc='sum', margins=True, margins_name='Total Costo').fillna(0).astype(int)
                        pivot_formato_partidas_dia_filtrado = pivot_partidas_dia_filtrado.applymap(lambda x: f'{x:,}')
                        st.dataframe(pivot_formato_partidas_dia_filtrado, width = 1100)



            #if selected == 'Flujo':

             #   tabla_flujo_economico = data_consumo[['codigoArea', 'nombrePartida', 'total', 'fecha', 'mes']]
              #  tabla_flujo_economico = tabla_flujo_economico.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'total': 'Total', 'fecha':'Fecha', 'mes':'Mes'})            
            
              #  df_flujo_economico= pd.DataFrame(tabla_flujo_economico)
              #  df_flujo_economico['Total']=pd.to_numeric(df_flujo_economico['Total'])
              #  df_flujo_economico['Fecha'] = pd.to_datetime(df_flujo_economico['Fecha'], dayfirst=True).dt.date            
              #  df_flujo_economico['Mes']=pd.to_numeric(df_flujo_economico['Mes'])
              #  mes_inicio= pd.to_numeric(mes_inicio)
              #  mes_fin= pd.to_numeric(mes_fin)

               # df_filtrado_fe = df_flujo_economico[(df_flujo_economico['Mes'] >= mes_inicio) & (df_flujo_economico['Mes'] <= mes_fin)]
                # Crear la pivot table
               # pivot_df_fe = df_filtrado_fe.pivot_table(index=['Área', 'Partida'], columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)

               # formatted_pivot_df_fe = pivot_df_fe.applymap(lambda x: f'{x:,}')

                    # Mostrar la pivot table
                    
               # st.dataframe(formatted_pivot_df_fe, width=1100)            
                

            if selected == 'APU':
                col1,col2 = st.columns([1,4])
                with col1:
                    selected = option_menu(menu_title=None, options=['Mensual', 'Diario'], icons=['calendar2-month','calendar2-day'], orientation='vertical')
                with col2:
                    if selected == 'Mensual':
                        tabla_uso_recurso = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso', 'unidad', 'cantidad','fecha', 'mes']]
                        tabla_uso_recurso = tabla_uso_recurso.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida','nombreRecurso': 'Recurso', 'unidad':'Unidad', 'cantidad': 'Cantidad', 'fecha':'Fecha', 'mes':'Mes'})                            
                        df_uso_recurso= pd.DataFrame(tabla_uso_recurso)
                        df_uso_recurso['Cantidad']=pd.to_numeric(df_uso_recurso['Cantidad'])
                        df_uso_recurso['Fecha'] = pd.to_datetime(df_uso_recurso['Fecha'], dayfirst=True).dt.date
                        df_uso_recurso['Mes']=pd.to_numeric(df_uso_recurso['Mes'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        df_filtrado_uso = df_uso_recurso[(df_uso_recurso['Mes'] >= mes_inicio) & (df_uso_recurso['Mes'] <= mes_fin)]
                        pivot_df = df_filtrado_uso.pivot_table(index=['Área', 'Partida', 'Recurso', 'Unidad'], columns='Mes', values='Cantidad', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
                        formatted_pivot_df = pivot_df.applymap(lambda x: f'{x:,}')
                            
                        st.dataframe(formatted_pivot_df, width=1100)

                    if selected == 'Diario':
                        tabla_uso_recurso_dia = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso', 'unidad', 'cantidad','fecha', 'mes']]
                        tabla_uso_recurso_dia = tabla_uso_recurso_dia.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida','nombreRecurso': 'Recurso', 'unidad':'Unidad', 'cantidad': 'Cantidad', 'fecha':'Fecha', 'mes':'Mes'})                            
                        df_uso_recurso_dia= pd.DataFrame(tabla_uso_recurso_dia)
                        df_uso_recurso_dia['Cantidad']=pd.to_numeric(df_uso_recurso_dia['Cantidad'])
                        df_uso_recurso_dia['Fecha'] = pd.to_datetime(df_uso_recurso_dia['Fecha'], dayfirst=True).dt.date
                        df_uso_recurso_dia['Mes']=pd.to_numeric(df_uso_recurso_dia['Mes'])
                        mes_inicio= pd.to_numeric(mes_inicio)
                        mes_fin= pd.to_numeric(mes_fin)
                        df_filtrado_uso_dia = df_uso_recurso_dia[(df_uso_recurso_dia['Mes'] >= mes_inicio) & (df_uso_recurso_dia['Mes'] <= mes_fin)]
                        pivot_df_dia = df_filtrado_uso_dia.pivot_table(index=['Área', 'Partida', 'Recurso', 'Unidad'], columns='Fecha', values='Cantidad', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
                        formatted_pivot_df_dia = pivot_df_dia.applymap(lambda x: f'{x:,}')
                            
                        st.dataframe(formatted_pivot_df_dia, width=1100)

        else:
                st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
                st.warning(f'No existe costo en la obra {par4}')

#-------------------------------------------COSTOS FIN------------------------------------------------------------------------------------------


    if selected == 'Kardex':
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        #st.warning('Módulo no disponible')
        
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
        filtro_obra = filtered_data_obra['codObra'].unique()
        
        col1,col2,col3 = st.columns([1,2,0.7])
        with col1:
            par3=st.selectbox(label='Obra', options=[''] + list(filtro_obra), label_visibility='visible', placeholder='Obra')
        
        kardex4= ''
        kardex5='01/01/2023'
        kardex6='31/12/2024'            

        APIkardex = response_kardex(p1,p2,par3,kardex4,kardex5,kardex6)
        datos = APIkardex.json()['datos']
        selected_columns = [ 'obra', 'bodega', 'tipoMovimiento', 'nroMovmiento', 'proveedor', 'digita', 'codRecurso', 'recurso', 'unidad', 'fechaMov', 'entra', 'sale', 'precio', 'total', 'codClase', 'clase', 'tipoCosto', 'codigoArea', 'area', 'codPartida', 'partida', 'nombreRecibe', 'nombreObra', 'nroEquipo', 'nroOT']
        filtered_kardex = [{column: entry[column] for column in selected_columns} for entry in datos]
    
        kardex=pd.DataFrame(filtered_kardex)
        kardex['fechaMov']=pd.to_datetime(kardex['fechaMov'], dayfirst=True).dt.date
        kardex['entra'] = kardex['entra'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        kardex['sale'] = kardex['sale'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        kardex['entra']=pd.to_numeric(kardex['entra'])
        kardex['sale']=pd.to_numeric(kardex['sale'])
        kardex['precio'] = kardex['precio'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        kardex['precio']=pd.to_numeric(kardex['precio'])
        

        kardex['valor_ingreso'] = kardex['entra'] * kardex['precio']
        
        total_valor_ingreso_recurso = kardex.groupby('codRecurso')['valor_ingreso'].sum().reset_index()
        total_valor_ingreso_recurso.columns = ['codRecurso', 'total_valor_ingreso_recurso']
        total_cantidad_ingreso_recurso = kardex.groupby('codRecurso')['entra'].sum().reset_index()
        total_cantidad_ingreso_recurso.columns = ['codRecurso', 'total_cantidad_ingreso_recurso']
        total_cantidad_salidas_recurso = kardex.groupby('codRecurso')['sale'].sum().reset_index()
        total_cantidad_salidas_recurso.columns = ['codRecurso', 'total_cantidad_salidas_recurso']
        recurso = kardex.groupby('codRecurso')['recurso'].first().reset_index()
        recurso.columns = ['codRecurso', 'recurso']
        df_intermediate = pd.merge(total_valor_ingreso_recurso, total_cantidad_ingreso_recurso, on='codRecurso')
        df_intermediate2= pd.merge(df_intermediate, recurso, on='codRecurso')
        precio_promedio_ponderado = pd.merge(df_intermediate2, total_cantidad_salidas_recurso, on='codRecurso')
        precio_promedio_ponderado['Precio Promedio Ponderado'] = precio_promedio_ponderado['total_valor_ingreso_recurso'] / precio_promedio_ponderado['total_cantidad_ingreso_recurso']
        precio_promedio_ponderado['stock'] = precio_promedio_ponderado['total_cantidad_ingreso_recurso'] - precio_promedio_ponderado['total_cantidad_salidas_recurso']
        precio_promedio_ponderado['Stock Valorizado'] = precio_promedio_ponderado['Precio Promedio Ponderado'] * precio_promedio_ponderado['stock']
        con_stock_df = precio_promedio_ponderado[['recurso', 'total_cantidad_ingreso_recurso', 'total_cantidad_salidas_recurso', 'stock']]
        sin_stock_df = precio_promedio_ponderado[['recurso', 'total_cantidad_ingreso_recurso', 'total_cantidad_salidas_recurso', 'stock']]
        stock_valorizado_df = precio_promedio_ponderado[['recurso', 'stock', 'Precio Promedio Ponderado', 'Stock Valorizado']]
        total_stock_valorizado = stock_valorizado_df['Stock Valorizado'].sum()

        with col3:
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
            #st.metric(label= 'Total Inventario', value=f"{valor_total_inventario:,.0f}")         
        st.markdown(
            """
            <style>
            .custom-margin {
                margin-top: 80px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        col1,col2 = st.columns([1,3])
        with col1:
            #selected_recurso = st.selectbox('Recurso:', kardex['recurso'].unique())
            #filtered_stock_valorizado = stock_valorizado_df[stock_valorizado_df['codRecurso'] == selected_recurso]
            filtered_stock_valorizado_total = stock_valorizado_df['Stock Valorizado'].sum()

        col1,col2 = st.columns([1,3])
        with col1:
            selected = option_menu(menu_title=None, options=['Con Stock', 'Sin Stock', 'Stock Crítico', 'Todo', 'Stock Valorizado'], icons=['box-seam', 'x-octagon', 'exclamation-octagon', 'journals', 'coin']) 
        with col2:
            if selected == 'Con Stock':
                con_stock = con_stock_df[con_stock_df['stock'] > 0]
                st.dataframe(con_stock, width=1000)

            if selected == 'Sin Stock':
                sin_stock = sin_stock_df[sin_stock_df['stock'] == 0]
                st.dataframe(sin_stock, width=1000)

            if selected == 'Stock Crítico':
                stock_critico = con_stock_df[con_stock_df['stock'] < 4 & (con_stock_df['stock'] > 0)]
                st.dataframe(stock_critico, width=1000)
            
            if selected == 'Todo':
                st.dataframe(con_stock_df, width=1000)

            if selected == 'Stock Valorizado':
                total_stock_valorizado = stock_valorizado_df['Stock Valorizado'].sum()
                stock_valorizado = stock_valorizado_df[stock_valorizado_df['stock'] > 0 ]
                stock_valorizado = stock_valorizado.sort_values(by='Stock Valorizado', ascending=False)
                st.dataframe(stock_valorizado, width=1000)
                col1,col2 = st.columns([3,1])
                with col3:
                    st.metric(label= 'Stock Valorizado', value=f"{total_stock_valorizado:,.0f}")



    if selected == 'Maquinaria':
        st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
        st.warning('Módulo no disponible')



       











# Inicializar el estado de la sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_login" not in st.session_state:
    st.session_state.show_login = False

        # Comprobación del estado de la sesión y mostrar la interfaz correspondiente
if st.session_state.logged_in:
            main_interface()
else:
            show_login_form()
