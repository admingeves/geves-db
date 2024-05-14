import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from APIbodega import response
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

# CONFIG PAGINA
st.set_page_config(page_icon='📊', layout='wide', page_title='Dashboard')

# Función para la pantalla de inicio de sesión
def show_login_form():
    with st.form(key='login_form'):
        username = st.text_input("Usuario", key='username')
        password = st.text_input("Contraseña", type="password", key='password')
        submit_button = st.form_submit_button(label='Login')
        if submit_button:
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Usuario/Contraseña incorrecto")

# Función para cerrar sesión
def logout():
    st.session_state.logged_in = False

# Función para la interfaz principal
def main_interface():
    # SIDEBAR
    with st.sidebar:
        st.image('assets/Incoprovil.png')
        if st.button("Logout"):
            logout()
        
        # MENU DEL SIDEBAR
        selected = option_menu(menu_title=None, options=['Bodega', 'Costos', 'Seguimiento'], icons=['boxes', 'coin', 'list-task'])
    
    # CLICK BODEGA SIDEBAR
    if selected == 'Bodega':
        st.title('EPP')
        st.text('Parámetros')
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
        with col1:
            p1 = st.selectbox('Cliente', options=['INCOPROV'] + ['INCOPROV'])
        with col2:
            p2 = st.selectbox('Empresa', options=['HGM'] + ['INCOPROV', 'HGM'])
        with col3:    
            mes_seleccionado = st.selectbox(label='Mes inicio mov bodega (2024)', options=['Enero'] + list(meses_dict.keys()))
            fecha_inicio = meses_dict[mes_seleccionado]
            st.container() 
            p4 = st.text_input(label='Mes Inicio API', value=(fecha_inicio), label_visibility='hidden')
        with col4:
            mes_seleccionado = st.selectbox(label='Me fin mov bodega (2024)', options=['Diciembre'] + list(meses_dict_fin.keys()))
            fecha_fin = meses_dict_fin[mes_seleccionado]
            p5 = st.text_input(label='Mes Fin API', value=(fecha_fin), label_visibility='hidden')
    
        # LLAMADA API DESDE APIbodega.py
        API = response(p1, p2, p4, p5)
        data = API.json()['datos']
        # Columnas que voy a llamar de 'datos'
        selected_columns = ['obra', 'recibe', 'nombreRecurso', 'undRecurso', 'cantidad', 'precio', 'subTotal', 'clase', 'nombreClase', 'fecha']
        # Armar un nuevo DF para mostrar las columnas seleccionadas
        filtered_data = [{column: entry[column] for column in selected_columns} for entry in data]
    
        # TITULO PARA DATOS
        st.text('DATA')
        st.divider()
    
        # FILTRO DATOS API CLASE, OBRA, RECURSO y RECIBE
        filtered_data_clases = pd.DataFrame(filtered_data)
    
        # COLUMNAS PARA FILTROS
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
            recursos = (filtered_data_clase['nombreRecurso'].unique())
            recurso_seleccionado = st.selectbox(label='Recurso', options=[''] + list(recursos), placeholder='Recursos')
            filtered_data_recurso = filtered_data_obra[filtered_data_obra['nombreRecurso'] == recurso_seleccionado] if recurso_seleccionado else filtered_data_obra
    
        with col4:
            recibe = (filtered_data_clase['recibe'].unique())
            trabajador_seleccionado = st.selectbox(label='Trabajador', options=[''] + list(recibe), placeholder='Nombre Trabajador')
            filtered_data_trabajador = filtered_data_obra[filtered_data_obra['recibe'] == trabajador_seleccionado] if trabajador_seleccionado else filtered_data_recurso
    
        # MENU RESUMEN, FLUJO ECONOMICO, USO RECURSO
        st.divider()
        selected = option_menu(menu_title=None, options=['Cantidad', 'Monto', 'Ver Datos'], icons=['123', 'cash-coin', 'database'], orientation='horizontal')
    
        # CLICK MENU CANTIDAD, MONTO, DATOS
        if selected == 'Cantidad':
            # TOTAL CANTIDAD
            total_cantidad = int(filtered_data_trabajador['cantidad'].sum())
            st.metric(label='Total Cantidad', value=total_cantidad)
    
            # GRAFICO CANTIDAD    
            graficoCantidad = st.bar_chart(filtered_data_trabajador, x='fecha', y='cantidad', width=0, height=0, use_container_width=True)
    
            # GRAFICOS OBRA, RECURSO, RECIBE
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObra = st.bar_chart(filtered_data, x='obra', y='cantidad', width=0, height=0, use_container_width=True)
            with col2:
                graficoRecibe = st.bar_chart(filtered_data, x='recibe', y='cantidad', width=0, height=0, use_container_width=True)
            with col3:
                graficoRecurso = st.bar_chart(filtered_data, x='nombreRecurso', y='cantidad', width=0, height=0, use_container_width=True)
    
        if selected == 'Monto':
            # TOTAL MONTO
            total_monto = int(filtered_data_trabajador['subTotal'].sum())
            st.metric(label='Total Monto', value=total_monto)
    
            # GRAFICO MONTO    
            graficoMonto = st.bar_chart(filtered_data_trabajador, x='fecha', y='subTotal', width=0, height=0, use_container_width=True)
    
            # GRAFICOS OBRA, RECURSO, RECIBE MONTO
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                graficoObraMonto = st.bar_chart(filtered_data, x='obra', y='subTotal', width=0, height=0, use_container_width=True)
                obra_monto = px.scatter(filtered_data_trabajador, x="obra", y="subTotal")
                st.plotly_chart(obra_monto, theme="streamlit", use_container_width=True)
    
            with col2:
                graficoRecibeMonto = st.bar_chart(filtered_data, x='recibe', y='subTotal', width=0, height=0, use_container_width=True)
            with col3:
                graficoRecursoMonto = st.bar_chart(filtered_data, x='nombreRecurso', y='subTotal', width=0, height=0, use_container_width=True)
    
        if selected == 'Ver Datos':
            # TABLA CANTIDAD
            with st.container(height=600):
                st.table(filtered_data_trabajador)
    
    if selected == 'Costos':
        st.title('Costos')
    
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
    if st.button('Iniciar Sesión'):
        st.session_state.show_login = True

    if st.session_state.show_login:
        show_login_form()
