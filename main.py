import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Comptech · Consultoría Integral Cloud, On-Premise, Ciberseguridad, Datos & IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()
MODEL_ID = "gemini-2.5-flash"

# ==========================================
# 1. TARIFARIO MULTI-CAPA DE LISTA (USD)
# ==========================================
PRECIOS_LISTA_MULTI_CAPA = {
    "GCP": {
        "Almacenamiento_DataWarehouse_TB_mes": 25.0,
        "Procesamiento_Compute_mes": 110.0,
        "Conectividad_Hibrida_VPN_mes": 115.0,
        "IAM_ZeroTrust_Identidades_mes": 65.0,
        "Ciberseguridad_DLP_WAF_mes": 120.0,
        "IA_LLM_Input_1M_tokens": 0.15,
        "IA_LLM_Output_1M_tokens": 0.60,
        "Vector_DB_RAG_mes": 140.0
    },
    "AWS": {
        "Almacenamiento_DataWarehouse_TB_mes": 30.0,
        "Procesamiento_Compute_mes": 120.0,
        "Conectividad_Hibrida_VPN_mes": 130.0,
        "IAM_ZeroTrust_Identidades_mes": 70.0,
        "Ciberseguridad_DLP_WAF_mes": 135.0,
        "IA_LLM_Input_1M_tokens": 0.25,
        "IA_LLM_Output_1M_tokens": 1.25,
        "Vector_DB_RAG_mes": 165.0
    },
    "Azure": {
        "Almacenamiento_DataWarehouse_TB_mes": 28.0,
        "Procesamiento_Compute_mes": 115.0,
        "Conectividad_Hibrida_VPN_mes": 120.0,
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
    escenario_competitivo: str = "08 Equipo interno, CoE o no hacer nada"
    modalidad_comptech: str = "Híbrido Comptech + VTO Cliente (Transferencia de conocimiento)"
    horizonte_boost: str = "Versión Acelerada BOOST (~4 meses: M1-M4)"
    servicios_comptech: List[ServicioConsultoriaComptech]

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
    supuestos_y_datos_por_validar: List[str] = Field(description="Lista de datos técnicos que quedaron sin confirmar en el levantamiento y supuestos aplicados para cotizar")
    diagrama_arquitectura_mermaid: str
    diagrama_flujo_trabajo_mermaid: str
    arquitectura_multi_capa: List[ComponenteMultiCapa]
    marcos_y_politicas_entregables: List[PoliticaYMarcoTecnico]
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

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=config
    )
    return response.text

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

    pendientes_txt = ", ".join(req.datos_pendientes_levantar) if req.datos_pendientes_levantar else "Ninguno; todos los datos críticos fueron confirmados."

    contexto = f"""
    FIRMA DE CONSULTORÍA: Comptech (Certificada ISO 9001 e ISO 27001; Marcos de referencia TOGAF e ISO 42001; Metodología BOOST)
    ESCENARIO DE PROYECTO SELECCIONADO: {req.tipo_escenario}
    MÓDULOS ACOPLADOS ACTIVOS: {', '.join(req.modulos_acoplados)}
    NUBE BASE PREFERIDA: {req.nube_preferida}
    ESCENARIO COMPETITIVO: {req.escenario_competitivo}
    MODALIDAD Y HORIZONTE: {req.modalidad_comptech} | {req.horizonte_boost}

    DATOS LEVANTADOS POR MÓDULO:
    {req.informacion_cliente_libre}

    DATOS TÉCNICOS MARCADOS COMO PENDIENTES DE VALIDAR CON EL CLIENTE:
    {pendientes_txt}

    SERVICIOS DE CONSULTORÍA Y PLATAFORMA COMPTECH (RESPETAR PRECIOS EXACTOS):
    {servicios_txt}

    TARIFARIO REFERENCIAL DE LISTA POR CAPA CLOUD (USD):
    {json.dumps(PRECIOS_LISTA_MULTI_CAPA, indent=2)}
    """

    try:
        ingenieria_integral = ejecutar_agente(
            """Eres Principal Enterprise Architect especialista en Migraciones Cloud, Infraestructura Híbrida On-Premise, 
            Almacenamiento de Datos, Ciberseguridad, IAM y Sistemas Agénticos de IA.
            Acopla ÚNICAMENTE los módulos marcados en 'modulos_acoplados' bajo el escenario seleccionado. 
            Si hay datos marcados como pendientes de validar, establece supuestos técnicos conservadores para poder cotizar.""",
            f"Diseña la arquitectura integral, licenciamiento y políticas:\n{contexto}"
        )

        sys_consolidacion = """Eres el Director de Consultoría Integral y Project Management en Comptech.
        Consolida el informe técnico, financiero y de gobierno en JSON.
        REGLAS ESTRICTAS:
        1. Enfoca el diseño y los diagramas estrictamente en el 'tipo_escenario' y 'modulos_acoplados' seleccionados.
        2. Documenta en 'supuestos_y_datos_por_validar' qué datos faltan por confirmar en la próxima sesión de levantamiento y qué supuesto se usó para costear.
        3. En 'diagrama_arquitectura_mermaid' usa 'flowchart TB' con subgraphs limpios según los módulos activos. Prohibido usar paréntesis () o caracteres especiales dentro de etiquetas de nodos.
        4. En 'diagrama_flujo_trabajo_mermaid' usa 'sequenceDiagram' mostrando el flujo operativo acorde a los módulos activos.
        5. Respeta exactamente los precios ingresados en 'servicios_comptech'."""

        resultado = ejecutar_agente(
            sys_consolidacion,
            f"Genera el informe integral de consultoría y arquitectura en JSON:\n\nCONTEXTO:\n{contexto}\n\nINGENIERÍA MULTI-CAPA:\n{ingenieria_integral}",
            schema=InformeConsultoriaIntegral
        )

        return json.loads(resultado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en motor de consultoría Comptech: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
