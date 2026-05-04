import streamlit as st
import requests
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="CRM Analytics Projects",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de la API
API_BASE_URL = "http://localhost:8000/api/v1"

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def get_data(endpoint):
    """Obtener datos de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return []


def post_data(endpoint, data):
    """Enviar datos a la API"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al enviar datos: {e}")
        return None


def delete_data(endpoint, id):
    """Eliminar datos de la API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/{endpoint}/{id}")
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Error al eliminar: {e}")
        return False


def dashboard_home():
    """Dashboard principal con métricas y visualizaciones"""
    st.markdown('<div class="main-header">📊 CRM Analytics Projects</div>', unsafe_allow_html=True)

    # Obtener datos
    clientes = get_data("clientes")
    proyectos = get_data("proyectos")
    tareas = get_data("tareas")
    entregables = get_data("entregables")

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Clientes", len(clientes), delta=None)

    with col2:
        proyectos_activos = len([p for p in proyectos if p.get('estado') == 'en_progreso'])
        st.metric("Proyectos Activos", proyectos_activos, delta=None)

    with col3:
        tareas_pendientes = len([t for t in tareas if t.get('estado') == 'pendiente'])
        st.metric("Tareas Pendientes", tareas_pendientes, delta=None)

    with col4:
        presupuesto_total = sum([p.get('presupuesto', 0) or 0 for p in proyectos])
        st.metric("Presupuesto Total", f"${presupuesto_total:,.0f}", delta=None)

    st.divider()

    # Visualizaciones
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Proyectos por Estado")
        if proyectos:
            df_proyectos = pd.DataFrame(proyectos)
            estado_counts = df_proyectos['estado'].value_counts()
            fig = px.pie(
                values=estado_counts.values,
                names=estado_counts.index,
                title="Distribución de Estados de Proyectos"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay proyectos para mostrar")

    with col2:
        st.subheader("📊 Proyectos por Tipo")
        if proyectos:
            df_proyectos = pd.DataFrame(proyectos)
            tipo_counts = df_proyectos['tipo_proyecto'].value_counts()
            fig = px.bar(
                x=tipo_counts.index,
                y=tipo_counts.values,
                title="Cantidad de Proyectos por Tipo",
                labels={'x': 'Tipo de Proyecto', 'y': 'Cantidad'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay proyectos para mostrar")

    # Tabla de proyectos recientes
    st.subheader("🗂️ Proyectos Recientes")
    if proyectos:
        df_proyectos = pd.DataFrame(proyectos)
        df_display = df_proyectos[['nombre', 'estado', 'tipo_proyecto', 'presupuesto']].head(10)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No hay proyectos registrados")


def gestionar_clientes():
    """Gestión de clientes"""
    st.header("👥 Gestión de Clientes")

    tab1, tab2 = st.tabs(["📋 Lista de Clientes", "➕ Nuevo Cliente"])

    with tab1:
        clientes = get_data("clientes")

        if clientes:
            # Convertir a DataFrame
            df = pd.DataFrame(clientes)
            df_display = df[['id', 'nombre', 'empresa', 'email', 'industria', 'telefono']]

            # Mostrar tabla con opción de eliminar
            for idx, row in df_display.iterrows():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"**{row['nombre']}** - {row['empresa']} ({row['email']})")
                    st.caption(f"Industria: {row['industria']} | Tel: {row['telefono']}")
                with col2:
                    if st.button("🗑️", key=f"del_cliente_{row['id']}"):
                        if delete_data("clientes", row['id']):
                            st.success("Cliente eliminado")
                            st.rerun()
                st.divider()
        else:
            st.info("No hay clientes registrados")

    with tab2:
        with st.form("nuevo_cliente"):
            st.subheader("Registrar Nuevo Cliente")

            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input("Nombre Completo*")
                empresa = st.text_input("Empresa*")
                email = st.text_input("Email*")

            with col2:
                telefono = st.text_input("Teléfono")
                industria = st.selectbox("Industria", [
                    "tecnologia", "finanzas", "retail", "salud",
                    "manufactura", "energia", "telecomunicaciones", "otros"
                ])
                direccion = st.text_area("Dirección")

            notas = st.text_area("Notas")

            submitted = st.form_submit_button("Registrar Cliente")

            if submitted:
                if nombre and empresa and email:
                    data = {
                        "nombre": nombre,
                        "empresa": empresa,
                        "email": email,
                        "telefono": telefono,
                        "industria": industria,
                        "direccion": direccion,
                        "notas": notas
                    }
                    result = post_data("clientes", data)
                    if result:
                        st.success("Cliente registrado exitosamente")
                        st.rerun()
                else:
                    st.error("Por favor completa los campos obligatorios")


def gestionar_proyectos():
    """Gestión de proyectos"""
    st.header("📁 Gestión de Proyectos")

    tab1, tab2 = st.tabs(["📋 Lista de Proyectos", "➕ Nuevo Proyecto"])

    with tab1:
        proyectos = get_data("proyectos")
        clientes = get_data("clientes")

        # Crear diccionario de clientes para lookup
        clientes_dict = {c['id']: c['nombre'] for c in clientes}

        if proyectos:
            for proyecto in proyectos:
                with st.expander(f"**{proyecto['nombre']}** - {proyecto['estado']}"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(f"**Cliente:** {clientes_dict.get(proyecto['cliente_id'], 'N/A')}")
                        st.write(f"**Tipo:** {proyecto['tipo_proyecto']}")
                        st.write(f"**Estado:** {proyecto['estado']}")

                    with col2:
                        st.write(f"**Presupuesto:** ${proyecto.get('presupuesto', 0):,.2f}")
                        st.write(f"**Costo Actual:** ${proyecto.get('costo_actual', 0):,.2f}")
                        if proyecto.get('fecha_inicio'):
                            st.write(f"**Inicio:** {proyecto['fecha_inicio']}")

                    with col3:
                        if proyecto.get('fecha_fin_estimada'):
                            st.write(f"**Fin Estimado:** {proyecto['fecha_fin_estimada']}")
                        if st.button("🗑️ Eliminar", key=f"del_proy_{proyecto['id']}"):
                            if delete_data("proyectos", proyecto['id']):
                                st.success("Proyecto eliminado")
                                st.rerun()

                    if proyecto.get('descripcion'):
                        st.write(f"**Descripción:** {proyecto['descripcion']}")
        else:
            st.info("No hay proyectos registrados")

    with tab2:
        clientes = get_data("clientes")

        if not clientes:
            st.warning("Primero debes registrar al menos un cliente")
        else:
            with st.form("nuevo_proyecto"):
                st.subheader("Crear Nuevo Proyecto")

                col1, col2 = st.columns(2)

                with col1:
                    nombre = st.text_input("Nombre del Proyecto*")
                    cliente_id = st.selectbox(
                        "Cliente*",
                        options=[c['id'] for c in clientes],
                        format_func=lambda x: next(c['nombre'] for c in clientes if c['id'] == x)
                    )
                    tipo_proyecto = st.selectbox("Tipo de Proyecto*", [
                        "exploratorio", "predictivo", "prescriptivo", "dashboard",
                        "etl_pipeline", "machine_learning", "business_intelligence"
                    ])
                    estado = st.selectbox("Estado*", [
                        "propuesta", "en_progreso", "en_pausa", "completado", "cancelado"
                    ])

                with col2:
                    presupuesto = st.number_input("Presupuesto ($)", min_value=0.0, value=0.0, step=1000.0)
                    fecha_inicio = st.date_input("Fecha de Inicio")
                    fecha_fin_estimada = st.date_input("Fecha Fin Estimada")

                descripcion = st.text_area("Descripción del Proyecto")

                submitted = st.form_submit_button("Crear Proyecto")

                if submitted:
                    if nombre and cliente_id and tipo_proyecto:
                        data = {
                            "nombre": nombre,
                            "descripcion": descripcion,
                            "tipo_proyecto": tipo_proyecto,
                            "estado": estado,
                            "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
                            "fecha_fin_estimada": fecha_fin_estimada.isoformat() if fecha_fin_estimada else None,
                            "presupuesto": presupuesto,
                            "costo_actual": 0.0,
                            "cliente_id": cliente_id
                        }
                        result = post_data("proyectos", data)
                        if result:
                            st.success("Proyecto creado exitosamente")
                            st.rerun()
                    else:
                        st.error("Por favor completa los campos obligatorios")


def gestionar_tareas():
    """Gestión de tareas"""
    st.header("✅ Gestión de Tareas")

    proyectos = get_data("proyectos")
    tareas = get_data("tareas")

    # Filtrar por proyecto
    proyecto_filter = st.selectbox(
        "Filtrar por Proyecto",
        options=[None] + [p['id'] for p in proyectos],
        format_func=lambda x: "Todos" if x is None else next((p['nombre'] for p in proyectos if p['id'] == x), "N/A")
    )

    if proyecto_filter:
        tareas = [t for t in tareas if t['proyecto_id'] == proyecto_filter]

    # Mostrar tareas
    if tareas:
        st.subheader(f"📝 {len(tareas)} Tarea(s)")

        for tarea in tareas:
            proyecto_nombre = next((p['nombre'] for p in proyectos if p['id'] == tarea['proyecto_id']), 'N/A')

            color = {
                'pendiente': '🔴',
                'en_progreso': '🟡',
                'revision': '🟠',
                'completada': '🟢',
                'bloqueada': '⚫'
            }.get(tarea['estado'], '⚪')

            st.markdown(f"{color} **{tarea['titulo']}** - {tarea['estado']} ({proyecto_nombre})")
            if tarea.get('descripcion'):
                st.caption(tarea['descripcion'])
            st.caption(f"Prioridad: {tarea['prioridad']} | Vencimiento: {tarea.get('fecha_vencimiento', 'Sin fecha')}")
            st.divider()
    else:
        st.info("No hay tareas registradas")


def main():
    """Función principal"""

    # Sidebar
    st.sidebar.title("🎯 Navegación")
    page = st.sidebar.radio(
        "Selecciona una opción:",
        ["🏠 Dashboard", "👥 Clientes", "📁 Proyectos", "✅ Tareas"]
    )

    st.sidebar.divider()
    st.sidebar.info(
        "**CRM Analytics Projects**\n\n"
        "Sistema de gestión para proyectos de análisis de datos"
    )

    # Routing
    if page == "🏠 Dashboard":
        dashboard_home()
    elif page == "👥 Clientes":
        gestionar_clientes()
    elif page == "📁 Proyectos":
        gestionar_proyectos()
    elif page == "✅ Tareas":
        gestionar_tareas()


if __name__ == "__main__":
    main()
