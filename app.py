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

        selected = option_menu(menu_title=None, options=['EPP', 'Costos', 'Kardex'], icons=['person-badge-fill', 'coin'])
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
            
            data_bodega['cantidad'] = data_bodega['cantidad'].astype(int)
            
            suma_data_bodega=data_bodega.groupby('fecha')['cantidad'].sum().reset_index()
            suma_obra_bodega=data_bodega.groupby('obra')['cantidad'].sum().reset_index()
            suma_recibe_bodega=data_bodega.groupby('recibe')['cantidad'].sum().reset_index()
            suma_recurso_bodega=data_bodega.groupby('nombreRecurso')['cantidad'].sum().reset_index()            

            total_cantidad = data_bodega['cantidad'].sum()
            
            col1,col2,col3 = st.columns([1,2,1])
            with col3:
                with st.container(border=True, height=110):
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
            total_monto = data_bodega['subTotal'].sum()
            col1,col2,col3 = st.columns([1,1,1])
            with col3:
                with st.container(border=True, height=110):
                    st.metric(label='Total Monto', value=f"{total_monto:,}")
    
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

#-------------------------------------------BODEGA (MONTO FIN)------------------------------------------------------------------------------------------

#-------------------------------------------BODEGA (VER DATOS INICIO)------------------------------------------------------------------------------------------

        if selected == 'Ver Datos':
    #TABLA DATOS

            with st.container(height=600):
                st.table(filtered_data_trabajador)

#-------------------------------------------BODEGA (VER DATOS FIN)------------------------------------------------------------------------------------------


#-------------------------------------------BODEGA FIN------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS INICIO------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS (LLAMADA APIS INICIO)------------------------------------------------------------------------------------------

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
        col1,col2,col3,col4,col5,col6 = st.columns([1,1,1,1,1,2])
        with col1:
            par3=st.selectbox(label='Periodo', options=['2024','2023'], label_visibility='visible')
            filtro_obra = (filtered_data_obra['codObra'].unique())
        with col2:
            par4=st.selectbox(label='Obra', options=[''] + list(filtro_obra), label_visibility='visible', placeholder='Obra')

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
             
        suma_data_consumo['fecha'] = pd.to_datetime(suma_data_consumo['fecha'], format='%d/%m/%Y')

        hoy = datetime.now().date()
        ayer = hoy - timedelta(days=1)
        antes_ayer = hoy - timedelta(days=2)
        hoy_menos3 = hoy - timedelta(days=3)
        
        df_hoy = suma_data_consumo[suma_data_consumo['fecha'] == hoy]
        df_ayer = suma_data_consumo[suma_data_consumo['fecha'] == ayer]
        df_antes_ayer = suma_data_consumo[suma_data_consumo['fecha'] == antes_ayer]
        df_hoy_menos3 = suma_data_consumo[suma_data_consumo['fecha'] == hoy_menos3]
        
        suma_total_hoy = df_hoy['total'].sum()
        suma_total_ayer = df_ayer['total'].sum()
        suma_total_antes_ayer = df_antes_ayer['total'].sum()
        suma_total_hoy_menos3 = df_hoy_menos3['total'].sum()

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        #with col1:
         #   st.text(hoy)
          #  st.table(suma_data_consumo == '2024-02-10')
           # st.text(df_hoy)

        #with col2:
            #st.metric(label='Total Costo ayer', value=suma_total_ayer)

        #with col3:
            #st.metric(label='Total Costo hoy', value=suma_total_hoy)

        with col4:
            total_suma_consumo = suma_data_consumo['total'].sum()
            total_promedio_consumo = suma_data_consumo['total']
            total_consumo= suma_data_consumo['total'].sum()
            

#-------------------------------------------COSTOS (INDICADORES FIN)------------------------------------------------------------------------------------------

#-------------------------------------------COSTOS (GRAFICOS)------------------------------------------------------------------------------------------

#----GRAFICO CONSUMOS---

#-------------------------------------------COSTOS (RESUMEN INICIO)------------------------------------------------------------------------------------------

        if selected == '':
        
            col1,col2,col3 = st.columns([1,1,1])   
            with col3:     
             with st.container(border=True, height=110):
                st.metric(label= 'Total Consumos', value=f"{total_suma_consumo:,}")
            
            tabla_total = data_consumo[['codigoArea', 'total', 'fecha']]
            tabla_total = tabla_total.rename(columns={'codigoArea': 'Área', 'total': 'Total', 'fecha':'Fecha'})
            
            df_tabla_total= pd.DataFrame(tabla_total)
            df_tabla_total['Total']=pd.to_numeric(df_tabla_total['Total'])
            df_tabla_total['Fecha']=pd.to_datetime(df_tabla_total['Fecha']).dt.date
            
            pivot_df_total = df_tabla_total.pivot_table(index='Área', columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)
            st.dataframe(pivot_df_total, width=1100)

            df_tabla_total_suma=df_tabla_total['Total'].sum()
            
            grafico_consumos= st.bar_chart(df_tabla_total, x='Fecha', y='Total')
        
            #grafico_costo= px.scatter(suma_data_consumo.set_index('fecha'))
            #st.plotly_chart(grafico_costo, theme=None, use_container_width=True, )


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

            col1,col2,col3= st.columns([1,1,1])

            with col3:
                with st.container(border=True, height=110):
                    st.metric(label= 'Total Consumos', value=f"{total_suma_consumo:,}")


            with st.container(border=False, height=600):
                st.dataframe(tabla_resumen, width=1100)

        if selected == 'Flujo Económico':

            tabla_flujo_economico = data_consumo[['codigoArea', 'nombrePartida', 'total', 'fecha']]
            tabla_flujo_economico = tabla_flujo_economico.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida', 'total': 'Total', 'fecha':'Fecha'})
            #tabla_flujo_economico['Total'] = tabla_flujo_economico['Total'].apply(lambda x: f"{x:,}")

            col1,col2,col3= st.columns([1,1,1])

            with col3:
                with st.container(border=True, height=110):
                    st.metric(label= 'Total Consumos', value=f"{total_suma_consumo:,}")
            
           
            df_flujo_economico= pd.DataFrame(tabla_flujo_economico)
            df_flujo_economico['Total']=pd.to_numeric(df_flujo_economico['Total'])
            df_flujo_economico['Fecha']=pd.to_datetime(df_flujo_economico['Fecha']).dt.date

               # Crear la pivot table
            pivot_df_fe = df_flujo_economico.pivot_table(index=['Área', 'Partida'], columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)

            formatted_pivot_df_fe = pivot_df_fe.applymap(lambda x: f'{x:,}')

                # Mostrar la pivot table
                
            st.dataframe(formatted_pivot_df_fe, width=1100)            
            

        if selected == 'Uso Recursos':

            tabla_uso_recurso = data_consumo[['codigoArea', 'nombrePartida', 'nombreRecurso', 'unidad', 'total','fecha']]
            tabla_uso_recurso = tabla_uso_recurso.rename(columns={'codigoArea': 'Área','nombrePartida': 'Partida','nombreRecurso': 'Recurso', 'unidad':'Unidad', 'total': 'Total', 'fecha':'Fecha'})
            #tabla_uso_recurso['Total'] = tabla_uso_recurso['Total'].apply(lambda x: f"{x:,}")
            
            col1,col2,col3= st.columns([1,1,1])

            with col3:
                with st.container(border=True, height=110):
                    st.metric(label= 'Total Consumos', value=f"{total_suma_consumo:,}")
            
           
            df_uso_recurso= pd.DataFrame(tabla_uso_recurso)
            df_uso_recurso['Total']=pd.to_numeric(df_uso_recurso['Total'])
            df_uso_recurso['Fecha']=pd.to_datetime(df_uso_recurso['Fecha']).dt.date
               # st.write(df_uso_recurso.dtypes)

               # Crear la pivot table
            pivot_df = df_uso_recurso.pivot_table(index=['Área', 'Partida', 'Recurso', 'Unidad'], columns='Fecha', values='Total', aggfunc='sum', margins=True, margins_name='Total').fillna(0).astype(int)

            formatted_pivot_df = pivot_df.applymap(lambda x: f'{x:,}')

                # Mostrar la pivot table
                
            st.dataframe(formatted_pivot_df, width=1100)



#-------------------------------------------COSTOS FIN------------------------------------------------------------------------------------------


    if selected == 'kardex':


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
