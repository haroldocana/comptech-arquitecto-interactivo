import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Comptech · Enterprise Architecture, Cybersecurity, AI & PM Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()
PRIMARY_MODEL_ID = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACK_MODELS = [PRIMARY_MODEL_ID, "gemini-3.8-flash", "gemini-4-hydrogen", "gemini-3.6-flash"]

# ==========================================
# 1. TARIFARIO MULTI-CAPA DE LISTA (USD)
# ==========================================
PRECIOS_LISTA_MULTI_CAPA = {
    "GCP": {
        "Almacenamiento_DataWarehouse_TB_mes": 25.0,
        "Procesamiento_Compute_mes": 110.0,
        "Conectividad_VPN_HA_mes": 115.0,
        "Enlace_Dedicado_Interconnect_mes": 450.0,
        "IAM_ZeroTrust_Identidades_mes": 65.0,
        "Ciberseguridad_DLP_WAF_mes": 120.0,
        "IA_LLM_Input_1M_tokens": 0.15,
        "IA_LLM_Output_1M_tokens": 0.60,
        "Vector_DB_RAG_mes": 140.0
    },
    "AWS": {
        "Almacenamiento_DataWarehouse_TB_mes": 30.0,
        "Procesamiento_Compute_mes": 120.0,
        "Conectividad_VPN_HA_mes": 130.0,
        "Enlace_Dedicado_DirectConnect_mes": 480.0,
        "IAM_ZeroTrust_Identidades_mes": 70.0,
        "Ciberseguridad_DLP_WAF_mes": 135.0,
        "IA_LLM_Input_1M_tokens": 0.25,
        "IA_LLM_Output_1M_tokens": 1.25,
        "Vector_DB_RAG_mes": 165.0
    },
    "Azure": {
        "Almacenamiento_DataWarehouse_TB_mes": 28.0,
        "Procesamiento_Compute_mes": 115.0,
        "Conectividad_VPN_HA_mes": 120.0,
        "Enlace_Dedicado_ExpressRoute_mes": 460.0,
        "IAM_ZeroTrust_Identidades_mes": 68.0,
        "Ciberseguridad_DLP_WAF_mes": 130.0,
        "IA_LLM_Input_1M_tokens": 0.20,
        "IA_LLM_Output_1M_tokens": 0.80,
        "Vector_DB_RAG_mes": 155.0
    }
}

# ==========================================
# 2. ESQUEMAS DE DATOS (PYDANTIC)
# ==========================================

class ServicioConsultoriaComptech(BaseModel):
    nombre: str
    categoria: str
    unidad: str
    precio_unitario_usd: float
    cantidad: float

class ProyectoConsultoriaRequest(BaseModel):
    tipo_escenario: str = "Proyecto Combinado Integral"
    informacion_cliente_libre: str
    datos_pendientes_levantar: List[str] = []
    modulos_acoplados: List[str]
    nube_preferida: str = "GCP"
    metodo_conexion_principal: str = "VPN IPsec HA + Google Workspace / Office 365"
    escenario_competitivo: str = "08 Equipo interno, CoE o no hacer nada"
    modalidad_comptech: str = "Híbrido Comptech + VTO Cliente (Transferencia de conocimiento)"
    horizonte_boost: str = "Versión Acelerada BOOST (~4 meses: M1-M4)"
    servicios_comptech: List[ServicioConsultoriaComptech]

class DisenoAgenteIA(BaseModel):
    nombre_agente: str
    proposito_negocio: str = Field(description="Objetivo exacto de negocio, explicación sencilla para el cliente y problema que resuelve")
    modelo_ia_y_herramientas: str = Field(description="Tipo de modelo IA (Razonamiento Profundo, Baja Latencia o Multimodal), embeddings y conectores MCP/API/DB exactos")
    flujo_automatizacion_proceso: str = Field(description="Paso a paso de qué automatiza, disparadores, acciones y validación Human-in-the-loop")
    consumo_estimado_mes: str = Field(description="Dimensionamiento: ejecuciones/mes, tokens entrada/salida, latencia/SLA y costo mensual proyectado")
    nivel_riesgo_ia: str = Field(description="Bajo | Medio | Alto")

class PasoFundacionCloudIAM(BaseModel):
    orden: int
    dominio_fundacion: str = Field(description="1. Organización y Carpetas | 2. Proyectos (Dev/QA/Prod) | 3. Usuarios y Service Accounts | 4. Permisos RBAC y Políticas de Seguridad | 5. Conectividad (VPN / Workspace / Office 365 / Interconnect)")
    configuracion_tecnica: str
    politicas_seguridad_aplicadas: str
    tiempo_implementacion_dias: int

class ComponenteMultiCapa(BaseModel):
    capa_arquitectura: str
    proveedor_o_origen: str
    nombre_componente: str
    referencia_funcional: str
    detalle_licenciamiento_o_metrica: str
    origen_tarifa: str
    costo_implementacion_usd: float
    costo_mensual_usd: float

class PoliticaYMarcoTecnico(BaseModel):
    dominio: str
    nombre_entregable: str
    alcance_y_controles: str
    modalidad_entrega: str

class RiesgoProyectoPM(BaseModel):
    id_riesgo: str
    categoria: str = Field(description="Técnico / Conectividad | Seguridad / IAM | Datos / Migración | Adopción / Negocio")
    descripcion_riesgo: str
    probabilidad_impacto: str = Field(description="Ej: Probabilidad Media · Impacto Alto")
    plan_mitigacion_comptech: str

class AlcanceYTerminosPM(BaseModel):
    incluye_en_alcance: List[str]
    excluye_del_alcance: List[str]
    prerequisitos_cliente: List[str]
    terminos_despliegue_y_entrega: str
    sugerencias_estrategicas_consultor: List[str] = Field(description="Recomendaciones proactivas de arquitectura, modelos, conectores, dimensionamiento y optimización de costos")

class ComparativaProveedor(BaseModel):
    proveedor: str
    es_recomendado: bool
    justificacion_integral: str
    inversion_implementacion_usd: float
    costo_recurrente_mensual_usd: float
    tco_anual_usd: float

class EstrategiaCompetitivaComptech(BaseModel):
    arquetipo_competidor: str
    en_que_gana_comptech: str
    riesgo_a_vigilar: str
    frase_posicionamiento: str
    pregunta_trampa_clave: str

class FaseProjectManagement(BaseModel):
    fase_boost: str
    duracion: str
    entregables_multi_capa: List[str]
    hito_formal: str
    responsables_raci: str

class InformeConsultoriaIntegral(BaseModel):
    titulo_proyecto: str
    cliente_detectado: str
    resumen_ejecutivo_consultoria: str
    supuestos_y_datos_por_validar: List[str]
    diagrama_arquitectura_mermaid: str
    diagrama_flujo_trabajo_mermaid: str
    diseno_agentes_y_automatizacion: List[DisenoAgenteIA]
    fundacion_cloud_iam_y_conectividad: List[PasoFundacionCloudIAM]
    arquitectura_multi_capa: List[ComponenteMultiCapa]
    marcos_y_politicas_entregables: List[PoliticaYMarcoTecnico]
    alcance_terminos_y_sugerencias: AlcanceYTerminosPM
    matriz_riesgos_pm: List[RiesgoProyectoPM]
    comparativa_proveedores_cloud: List[ComparativaProveedor]
    inteligencia_competitiva: EstrategiaCompetitivaComptech
    cronograma_pm_boost: List[FaseProjectManagement]
    total_implementacion_usd: float
    total_mensual_usd: float
    tco_anual_usd: float

# ==========================================
# 3. ORQUESTACIÓN MULTI-AGENTE FULL-STACK
# ==========================================

def ejecutar_agente(system_instruction: str, prompt: str, schema=None):
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.15,
    )
    if schema:
        config.response_mime_type = "application/json"
        config.response_schema = schema

    last_err = None
    for model_name in dict.fromkeys(FALLBACK_MODELS):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as err:
            last_err = err
    raise last_err

@app.get("/api/tarifario-multi-capa")
async def obtener_tarifario():
    return PRECIOS_LISTA_MULTI_CAPA

@app.post("/api/generar-consultoria-integral", response_model=InformeConsultoriaIntegral)
async def generar_consultoria_integral(req: ProyectoConsultoriaRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Falta configurar GEMINI_API_KEY en Render.")

    servicios_txt = "\n".join([
        f"- {s.nombre} [{s.categoria}]: ${s.precio_unitario_usd} USD / {s.unidad} x {s.cantidad} = ${s.precio_unitario_usd * s.cantidad:.2f} USD"
        for s in req.servicios_comptech
    ])

    pendientes_txt = ", ".join(req.datos_pendientes_levantar) if req.datos_pendientes_levantar else "Ninguno; datos críticos confirmados."

    contexto = f"""
    FIRMA DE CONSULTORÍA: Comptech (Certificada ISO 9001 e ISO 27001; Marcos de referencia TOGAF e ISO 42001; Metodología BOOST)
    ESCENARIO DE PROYECTO: {req.tipo_escenario}
    MÓDULOS ACOPLADOS: {', '.join(req.modulos_acoplados)}
    NUBE PRINCIPAL: {req.nube_preferida}
    MÉTODO DE CONEXIÓN E IDENTIDAD SELECCIONADO: {req.metodo_conexion_principal}
    ESCENARIO COMPETITIVO: {req.escenario_competitivo}
    MODALIDAD Y HORIZONTE: {req.modalidad_comptech} | {req.horizonte_boost}

    DATOS TÉCNICOS LEVANTADOS:
    {req.informacion_cliente_libre}

    DATOS PENDIENTES POR VALIDAR:
    {pendientes_txt}

    SERVICIOS COMPTECH (RESPETAR PRECIOS EXACTOS):
    {servicios_txt}

    TARIFARIO LISTA POR CAPA CLOUD (USD):
    {json.dumps(PRECIOS_LISTA_MULTI_CAPA, indent=2)}
    """

    try:
        # AGENTE 1: Principal Cloud, Landing Zone (Org/Projects/IAM/Network) & AI Systems Engineer
        ingenieria_integral = ejecutar_agente(
            """Eres Principal Cloud & AI Systems Architect en Comptech.
            Explica en lenguaje claro para el negocio y con rigor técnico para ingeniería:
            1) La Landing Zone completa desde cero: creación de Organización Cloud, estructura de Carpetas y Proyectos (Dev, QA, Prod),
               Usuarios, Grupos, Service Accounts para agentes IA, Permisos RBAC/Zero-Trust, Políticas de Seguridad (Org Policies, KMS, DLP, VPC Service Controls)
               y el método exacto de conectividad seleccionado (VPN IPsec HA, integración con Google Workspace, Office 365 / Entra ID, o Enlace Dedicado Cloud Interconnect/Direct Connect).
            2) El diseño detallado de cada Agente de IA: propósito de negocio, tipos de modelos IA (razonamiento vs. baja latencia/multimodal), conectores MCP/API/DB exactos,
               flujo de automatización paso a paso, validación Human-in-the-loop y dimensionamiento (ejecuciones/mes, tokens, latencia y costo mensual).
            3) Dimensionamiento de costos y capacidad de todas las capas acopladas.""",
            f"Diseña la arquitectura desde fundación hasta agentes IA, modelos, conectores y dimensionamiento:\n{contexto}"
        )

        # AGENTE 2: Senior Project Manager (PMP/BOOST) & Director de Consultoría Comptech
        sys_pm_consolidacion = """Eres Senior Project Manager (PMP / Agile BOOST) y Director de Consultoría en Comptech.
        Consolida todo el informe en JSON siguiendo la ESTRUCTURA OBLIGATORIA DE 7 SECCIONES para cada negocio:
        1. 'diseno_agentes_y_automatizacion': propósito en lenguaje claro, tipos de modelos IA y conectores MCP/API exactos, flujo de automatización paso a paso, dimensionamiento mensual y nivel de riesgo. (Si el escenario no incluye IA, incluye al menos 1 propuesta sugerida como fase futura).
        2. 'fundacion_cloud_iam_y_conectividad': paso a paso en días: (1) Creación de Organización y jerarquía, (2) Proyectos separados por ambiente, (3) Usuarios y Service Accounts, (4) Políticas IAM y Seguridad, y (5) Conectividad específica (VPN / Workspace / Office 365 / Enlace Dedicado).
        3. 'diagrama_arquitectura_mermaid' en 'flowchart TB' limpio (sin paréntesis () ni caracteres raros dentro de etiquetas).
        4. 'diagrama_flujo_trabajo_mermaid' en 'sequenceDiagram' mostrando identidad, conectividad, conectores/modelos, automatización y auditoría.
        5. 'marcos_y_politicas_entregables': marcos técnicos y políticas de gobierno IA/IAM.
        6. 'arquitectura_multi_capa' y 'comparativa_proveedores_cloud': dimensionamiento de métricas/licenciamiento y costos respetando exactamente 'servicios_comptech'.
        7. 'alcance_terminos_y_sugerencias', 'matriz_riesgos_pm' y 'cronograma_pm_boost': alcance, exclusiones, prerrequisitos, términos de despliegue, sugerencias estratégicas, riesgos y fases BOOST."""

        resultado = ejecutar_agente(
            sys_pm_consolidacion,
            f"Genera el informe integral de Ingeniería y Project Management en JSON:\n\nCONTEXTO:\n{contexto}\n\nDISEÑO DE INGENIERÍA:\n{ingenieria_integral}",
            schema=InformeConsultoriaIntegral
        )

        return json.loads(resultado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en motor de consultoría Comptech: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
