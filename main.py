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
        "Almacenamiento_DataWarehouse_TB_mes": 25.0,   # BigQuery + Cloud Storage
        "Procesamiento_Compute_mes": 110.0,            # Cloud Run / GKE Autopilot
        "Conectividad_Hibrida_VPN_mes": 115.0,         # Cloud VPN / Interconnect
        "IAM_ZeroTrust_Identidades_mes": 65.0,         # Cloud IAM + Identity Platform
        "Ciberseguridad_DLP_WAF_mes": 120.0,           # Cloud Armor + Sensitive Data Protection
        "IA_LLM_Input_1M_tokens": 0.15,                # Vertex AI / Gemini
        "IA_LLM_Output_1M_tokens": 0.60,
        "Vector_DB_RAG_mes": 140.0
    },
    "AWS": {
        "Almacenamiento_DataWarehouse_TB_mes": 30.0,   # S3 + Redshift Serverless
        "Procesamiento_Compute_mes": 120.0,            # ECS Fargate / EKS
        "Conectividad_Hibrida_VPN_mes": 130.0,         # AWS Site-to-Site VPN / Direct Connect
        "IAM_ZeroTrust_Identidades_mes": 70.0,         # IAM Identity Center + Secrets Manager
        "Ciberseguridad_DLP_WAF_mes": 135.0,           # AWS WAF + Macie + GuardDuty
        "IA_LLM_Input_1M_tokens": 0.25,                # Amazon Bedrock
        "IA_LLM_Output_1M_tokens": 1.25,
        "Vector_DB_RAG_mes": 165.0
    },
    "Azure": {
        "Almacenamiento_DataWarehouse_TB_mes": 28.0,   # Azure Data Lake + Microsoft Fabric
        "Procesamiento_Compute_mes": 115.0,            # Azure Container Apps / AKS
        "Conectividad_Hibrida_VPN_mes": 120.0,         # Azure VPN Gateway / ExpressRoute
        "IAM_ZeroTrust_Identidades_mes": 68.0,         # Microsoft Entra ID P2 + Key Vault
        "Ciberseguridad_DLP_WAF_mes": 130.0,           # Microsoft Purview + Defender for Cloud
        "IA_LLM_Input_1M_tokens": 0.20,                # Azure OpenAI
        "IA_LLM_Output_1M_tokens": 0.80,
        "Vector_DB_RAG_mes": 155.0
    }
}

# ==========================================
# 2. ESQUEMAS DE DATOS (PYDANTIC)
# ==========================================

class ServicioConsultoriaComptech(BaseModel):
    nombre: str
    categoria: str          # Consultoría Marco/Políticas, Ingeniería Cloud/Datos, Ciberseguridad/IAM, Plataforma AIVO/MCP, Operación HIL
    unidad: str             # Mes, Hora, Entregable Único
    precio_unitario_usd: float
    cantidad: float

class ProyectoConsultoriaRequest(BaseModel):
    informacion_cliente_libre: str
    modulos_acoplados: List[str] = Field(
        description="Lista de capas activadas: Almacenamiento y Datos, Procesamiento e Infraestructura, Conectividad On-Premise, Ciberseguridad y DLP, Arquitectura IAM, Licenciamiento Multi-Capa, Agentes IA y MCP, Marcos Técnicos y Políticas"
    )
    nube_preferida: str = "GCP"
    estrategia_infraestructura: str = "Híbrida (Convivencia On-Premise + Migración Cloud)"
    escenario_competitivo: str = "08 Equipo interno / CoE / No hacer nada"
    modalidad_comptech: str = "Híbrido Comptech + VTO Cliente (Transferencia de conocimiento)"
    horizonte_boost: str = "Versión Acelerada BOOST (~4 meses: M1-M4)"
    servicios_comptech: List[ServicioConsultoriaComptech]

class ComponenteMultiCapa(BaseModel):
    capa_arquitectura: str = Field(
        description="Almacenamiento y Datos | Procesamiento e Infraestructura | Conectividad On-Premise | Ciberseguridad | IAM y Control de Acceso | Licenciamiento | Orquestación Agéntica IA | Marcos y Gobierno"
    )
    proveedor_o_origen: str
    nombre_componente: str
    referencia_funcional: str = Field(description="Qué hace exactamente en la arquitectura, cómo se acopla con las demás capas y qué problema resuelve")
    detalle_licenciamiento_o_metrica: str = Field(description="Modelo de licenciamiento: por consumo, por usuario, vCPU/TB, suscripción o servicio de consultoría")
    origen_tarifa: str = Field(description="Precio Lista Nube | Consultoría/Servicio Comptech | Existente On-Premise")
    costo_implementacion_usd: float
    costo_mensual_usd: float

class PoliticaYMarcoTecnico(BaseModel):
    dominio: str = Field(description="Marco Técnico de Arquitectura (TOGAF/Cloud) | Política de Gobierno de IA (ISO 42001) | Política de IAM (Humanos y Agentes) | Política de Seguridad y Datos (ISO 27001/DLP)")
    nombre_entregable: str
    alcance_y_controles: str
    modalidad_entrega: str = Field(description="Consultoría como Servicio Comptech (Entregable + Traspaso)")

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
    diagrama_arquitectura_mermaid: str = Field(
        description="Código válido Mermaid 'flowchart TB' con subgraphs para las capas acopladas (OnPremise, Conectividad_IAM, Datos_Storage, Procesamiento_Cloud, Seguridad_Gobierno, Agentes_IA). Sin paréntesis ni caracteres especiales dentro de etiquetas."
    )
    diagrama_flujo_trabajo_mermaid: str = Field(
        description="Código válido Mermaid 'sequenceDiagram' mostrando el flujo completo con validación IAM, acceso a datos On-Premise/Cloud, procesamiento IA, controles DLP y auditoría."
    )
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

    contexto = f"""
    FIRMA DE CONSULTORÍA: Comptech (Certificada ISO 9001 e ISO 27001; Marcos de referencia TOGAF e ISO 42001; Metodología BOOST: Build, Outcome, Optimize, Scale, Time)
    MÓDULOS ACOPLADOS REQUERIDOS POR EL CLIENTE: {', '.join(req.modulos_acoplados)}
    ESTRATEGIA INFRAESTRUCTURA: {req.estrategia_infraestructura}
    NUBE BASE PREFERIDA: {req.nube_preferida}
    ESCENARIO COMPETITIVO DETECTADO: {req.escenario_competitivo}
    MODALIDAD Y HORIZONTE: {req.modalidad_comptech} | {req.horizonte_boost}

    LEVANTAMIENTO / INFORMACIÓN CRUDA DEL CLIENTE:
    {req.informacion_cliente_libre}

    SERVICIOS DE CONSULTORÍA Y PLATAFORMA COMPTECH (RESPETAR PRECIOS EXACTOS):
    {servicios_txt}

    TARIFARIO REFERENCIAL DE LISTA POR CAPA CLOUD (USD):
    {json.dumps(PRECIOS_LISTA_MULTI_CAPA, indent=2)}
    """

    try:
        # AGENTE 1: Arquitecto Principal Multi-Capa (Infraestructura, Datos, Redes On-Prem, IAM, Ciberseguridad y Licenciamiento)
        ingenieria_integral = ejecutar_agente(
            """Eres Principal Enterprise Architect especialista en infraestructura On-Premise y Cloud (GCP, AWS, Azure), 
            Almacenamiento de Datos (Data Lakes/Warehouses), Procesamiento/Cómputo, Ciberseguridad (DLP, WAF, cifrado), 
            IAM (Zero-Trust, RBAC/ABAC para usuarios y agentes de IA) y modelos de licenciamiento empresarial.
            Acopla ÚNICAMENTE los módulos solicitados en 'modulos_acoplados', dimensiona cada capa con precios de lista reales 
            e integra los servicios de consultoría de Comptech.""",
            f"Diseña la arquitectura integral multi-capa, licenciamiento y políticas:\n{contexto}"
        )

        # AGENTE 2: Director de Consultoría, Gobierno IA, FinOps y Preventa Competitiva Comptech
        sys_consolidacion = """Eres el Director de Consultoría Integral y Project Management en Comptech.
        Consolida el informe técnico, financiero y de gobierno en JSON.
        REGLAS ESTRICTAS:
        1. Acopla los módulos seleccionados cubriendo Almacenamiento, Procesamiento, Conectividad On-Premise, Ciberseguridad, IAM, Licenciamiento de todas las capas, IA y Marcos Técnicos.
        2. En 'marcos_y_politicas_entregables', define los entregables formales de consultoría como servicio:
           - Marco Técnico de Arquitectura (basado en TOGAF y mejores prácticas Cloud/Híbridas)
           - Política de Gobierno de IA (basada en ISO 42001, inventario, comité y evaluación de riesgos)
           - Política de IAM y Control de Identidades (principio de mínimo privilegio para humanos, servidores MCP y agentes IA)
           - Política de Ciberseguridad y Clasificación de Datos (ISO 27001, cifrado, DLP).
        3. En 'diagrama_arquitectura_mermaid' usa 'flowchart TB' con subgraphs limpios según los módulos acoplados. Prohibido usar paréntesis () o caracteres especiales dentro de etiquetas de nodos.
        4. En 'diagrama_flujo_trabajo_mermaid' usa 'sequenceDiagram' incluyendo explícitamente la validación IAM y controles de seguridad/datos en el flujo.
        5. En 'inteligencia_competitiva', responde según el 'escenario_competitivo' con el diferenciador de Comptech y su pregunta trampa clave para el cliente.
        6. Respeta exactamente los precios ingresados en 'servicios_comptech'."""

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
