import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from APIbodega import response
from APIconsumos import response_consumo
from APIobras import response_obras
import plotly.express as px



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

#CONFIG PAGINA
st.set_page_config(page_icon='📊', layout='wide', page_title='Dashboard')

#FUNCION PARA PANTALLA DE INICIO DE SESIÓN
def show_login_form():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form(key='login_form'):
            username = st.text_input(label="Usuario", key='username', label_visibility='hidden', placeholder='Usuario')
            password = st.text_input("Contraseña", type="password", key='password', label_visibility='hidden', placeholder='Contraseña')
            submit_button = st.form_submit_button(label='Iniciar Sesión')
            if submit_button:
                if username == "admin" and password == "1111":
                    st.session_state.logged_in = True
                #st.session_state.username = username
                else:
                    st.error("Usuario/Contraseña incorrecto")

#FUNCION PARA CERRAR SESIÓN
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

        selected = option_menu(menu_title=None, options=['Bodega', 'Costos', 'Seguimiento'], icons=['boxes', 'coin', 'list-task'])
        p1 = st.selectbox(label='Cliente', options=['INCOPROV'], label_visibility='hidden', placeholder='Cliente')
        p2 = st.selectbox(label='Empresa', options=['INCOPROV', 'HGM'], label_visibility='hidden', placeholder='Empresa')
        
        
        
#CLICK BODEGA SIDEBAR

    if selected == 'Bodega':
        st.title('EPP')
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
        with col1:    
            mes_inicio,mes_fin=st.select_slider(label='Rango Fecha Bodega', options=list(meses_dict.keys()), value=['Enero','Diciembre'], label_visibility='hidden', )
            fecha_inicio = meses_dict[mes_inicio]
            fecha_fin = meses_dict_fin[mes_fin]
        
        
        with col2:
            p4 = st.text_input(label='Mes Inicio API', value=(fecha_inicio), label_visibility='hidden', disabled=True)
        
        with col3:
            p5 = st.text_input(label='Mes Fin API', value=(fecha_fin), label_visibility='hidden', disabled=True, )
    
# LLAMADA APIbodega.py

        APIbodega = response(p1, p2, p4, p5)
        data = APIbodega.json()['datos']
        # Columnas que voy a llamar de 'datos'
        selected_columns = ['obra', 'recibe', 'nombreRecurso', 'undRecurso', 'cantidad', 'precio', 'subTotal', 'clase', 'nombreClase', 'fecha']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_data = [{column: entry[column] for column in selected_columns} for entry in data]

    
#RESULTADO APIbodega.py (DATOS)
        
        st.divider()
    
    #FILTRO DATOS API CLASE, OBRA, RECURSO y RECIBE

        filtered_data_clases = pd.DataFrame(filtered_data)
    
        col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
        with col1:
            clases = (filtered_data_clases['nombreClase'].unique())
            clase_a_excluir = 'Combustibles'
            clases_sin_excluir = [nombreClase for nombreClase in clases if nombreClase != clase_a_excluir]
            clase_seleccionada = st.selectbox(label='Clase', options=[''] + list(clases_sin_excluir), placeholder='Tipos de EPP')
            filtered_data_clase = filtered_data_clases[filtered_data_clases['nombreClase'] == clase_seleccionada] if clase_seleccionada else filtered_data_clases
    
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
    
    #MENU RESUMEN, FLUJO ECONOMICO, USO RECURSO
        
        selected = option_menu(menu_title=None, options=['Cantidad', 'Monto', 'Ver Datos'], icons=['123', 'cash-coin', 'database'], orientation='horizontal')
    
        #CLICK MENU CANTIDAD, MONTO, DATOS
        if selected == 'Cantidad':
            #TOTAL CANTIDAD
            data_bodega=pd.DataFrame(filtered_data_trabajador)
            suma_data_bodega=data_bodega.groupby('fecha')['cantidad'].sum().reset_index()
            suma_obra_bodega=data_bodega.groupby('obra')['cantidad'].sum().reset_index()
            suma_recibe_bodega=data_bodega.groupby('recibe')['cantidad'].sum().reset_index()
            suma_recurso_bodega=data_bodega.groupby('nombreRecurso')['cantidad'].sum().reset_index()
            



            total_cantidad = int(filtered_data_trabajador['cantidad'].sum())
        
            st.metric(label='Total Cantidad', value=total_cantidad)
        
            #GRAFICO CANTIDAD 
            graficoCantidad=st.bar_chart(suma_data_bodega.set_index('fecha'))
            #graficoCantidad = st.bar_chart(filtered_data_trabajador, x='fecha', y='cantidad', width=0, height=0, use_container_width=True)
    
            #GRAFICOS OBRA, RECURSO, RECIBE

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObra = st.bar_chart(suma_obra_bodega.set_index('obra'))
            with col2:
                graficoRecibe = st.bar_chart(suma_recibe_bodega.set_index('recibe'))
            with col3:
                graficoRecurso = st.bar_chart(suma_recurso_bodega.set_index('nombreRecurso'))
    
        if selected == 'Monto':
            #TOTAL MONTO

            total_monto = int(filtered_data_trabajador['subTotal'].sum())
            st.metric(label='Total Monto', value=total_monto)
    
            #GRAFICO MONTO    
            
            graficoMonto = st.bar_chart(filtered_data_trabajador, x='fecha', y='subTotal', width=0, height=0, use_container_width=True)
    
            #GRAFICOS OBRA, RECURSO, RECIBE MONTO
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObraMonto = st.bar_chart(filtered_data_trabajador, x='obra', y='subTotal', width=0, height=0, use_container_width=True)
                obra_monto = px.scatter(filtered_data_trabajador, x="obra", y="subTotal")
                st.plotly_chart(obra_monto, theme=None, use_container_width=True)
    
            with col2:
                graficoRecibeMonto = st.bar_chart(filtered_data_trabajador, x='recibe', y='subTotal', width=0, height=0, use_container_width=True)
            with col3:
                graficoRecursoMonto = st.bar_chart(filtered_data_trabajador, x='nombreRecurso', y='subTotal', width=0, height=0, use_container_width=True)
    
        if selected == 'Ver Datos':
            #TABLA DATOS

            with st.container(height=600):
                st.table(filtered_data_trabajador)
    
#CLICK SIDEBAR COSTOS

    if selected == 'Costos':

#LLAMADA APIobras
        
        APIobras = response_obras(p1, p2)
        datos_obra = APIobras.json()['datos']
        # Columnas que voy a llamar de 'datos'
        columns_obra = ['codObra']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_obra = [{column: entry[column] for column in columns_obra} for entry in datos_obra]
        filtered_data_obra = pd.DataFrame(filtered_obra)
        
        st.title('Costos')
        col1,col2= st.columns([1,3])
        
        with col1:
            par3=st.selectbox(label='Año', options=['2024','2023'], label_visibility='hidden')
            filtro_obra = (filtered_data_obra['codObra'].unique())
            par4=st.selectbox(label='Obra', options=[''] + list(filtro_obra), label_visibility='hidden')

#LLAMADA APIconsumos
        
            APIconsumos = response_consumo(p1, p2, par3, par4)
            datos = APIconsumos.json()['datos']
        # Columnas que voy a llamar de 'datos'
            columns = ['obra', 'cantidad', 'tipoCosto', 'codigoArea', 'nombrePartida', 'nombreRecurso', 'fecha']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
            filtered = [{column: entry[column] for column in columns} for entry in datos]

            filtered_data_consumos = pd.DataFrame(filtered)

            t_costo=(filtered_data_consumos['tipoCosto'].unique())
            t_costo_seleccionado=st.selectbox(label='Tipo Costo', options=[''] + list(t_costo), placeholder='Tipo de Costos', label_visibility='hidden' )
            filtered_t_costo = filtered_data_consumos[filtered_data_consumos['tipoCosto'] == t_costo_seleccionado] if t_costo_seleccionado else filtered_data_consumos

            area_consumo= (filtered_t_costo['codigoArea'].unique())
            area_consumo_seleccionada=st.selectbox(label='Área', options=[''] + list(area_consumo), placeholder='Nombre Área', label_visibility='hidden')
            filtered_area_consumo = filtered_t_costo[filtered_t_costo['codigoArea'] == area_consumo_seleccionada] if area_consumo_seleccionada else filtered_t_costo

            partida_consumo= (filtered_area_consumo['nombrePartida'].unique())
            partida_consumo_seleccionada=st.selectbox(label='Partida', options=[''] + list(partida_consumo), placeholder='Nombre Partida', label_visibility='hidden')
            filtered_partida_consumo = filtered_area_consumo[filtered_area_consumo['nombrePartida'] == partida_consumo_seleccionada] if partida_consumo_seleccionada else filtered_area_consumo

            recurso_consumo= (filtered_partida_consumo['nombreRecurso'].unique())
            recurso_consumo_seleccionada=st.selectbox(label='Recurso', options=[''] + list(recurso_consumo), placeholder='Nombre Recurso', label_visibility='hidden')
            filtered_recurso_consumo = filtered_partida_consumo[filtered_partida_consumo['nombreRecurso'] == recurso_consumo_seleccionada] if recurso_consumo_seleccionada else filtered_partida_consumo

        with col2:
            with st.container(height=400):
                data_consumo=pd.DataFrame(filtered_recurso_consumo)
                suma_data_consumo=data_consumo.groupby('fecha')['cantidad'].sum().reset_index()
                st.bar_chart(suma_data_consumo.set_index('fecha'))
        
                #st.table(filtered_recurso_consumo)

    
    if selected == 'Seguimiento':
        st.title('Seguimiento')

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
