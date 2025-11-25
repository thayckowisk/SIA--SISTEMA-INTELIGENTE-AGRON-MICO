"""
SIA - Sistema Inteligente Agrícola
Aplicação modular com predição de produtividade, leite e detecção de gado
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Imports dos módulos
from modules.agente_roi import AgenteROI
from modules.agente_chat import AgenteChat
from modules.simulador import carregar_dados, ModeloML, traduzir, original, MAPA
from modules.predicao_leite import show_milk_prediction
from modules.deteccao_gado import show_cattle_detection

# ==================== CONFIGURAÇÃO ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
CONFIG_DIR = BASE_DIR / "config"

load_dotenv(CONFIG_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

DATASET_PATH = DATA_DIR / "crop_yield.csv"
YOLO_MODEL_PATH = MODELS_DIR / "best.pt"

# ==================== CONFIGURAÇÃO DA PÁGINA ====================
st.set_page_config(
    page_title="SIA - Sistema Inteligente Agronômico,
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CSS LIMPO ====================
st.markdown("""
<style>
    /* Remover padding do topo */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* Título principal */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-title h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
    }
    
    .main-title p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cartões de resultado */
    .result-card {
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .result-value {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
    }
    
    .result-label {
        font-size: 1.3rem;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    /* Métricas */
    .metric-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    /* Chat sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNÇÃO PRINCIPAL ====================
def main():
    """Aplicação principal"""
    
    # Título visível
    st.markdown("""
    <div class="main-title">
        <h1>🌾 SIA - Sistema Inteligente Agrícola</h1>
        <p>Predição de Produtividade com Inteligência Artificial</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = carregar_dados(DATASET_PATH)
    
    # Treinar modelo (silencioso)
    if 'modelo_ml' not in st.session_state:
        st.session_state.modelo_ml = ModeloML(df)
        st.session_state.modelo_ml.treinar()
    
    simulador = st.session_state.modelo_ml
    
    # Inicializar agente chat
    if 'agente_chat' not in st.session_state:
        st.session_state.agente_chat = AgenteChat(GROQ_API_KEY, GROQ_MODEL)
    
    agente = st.session_state.agente_chat
    
    # ==================== SIDEBAR: CHAT ====================
    with st.sidebar:
        st.markdown("### 💬 Chat IA")
        
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            st.warning("⚠️ Configure GROQ_API_KEY")
        else:
            # Mostrar dados disponíveis
            if 'contexto_json' in st.session_state and st.session_state.contexto_json:
                ctx = st.session_state.contexto_json
                
                dados_disponiveis = []
                if 'simulacao' in ctx:
                    dados_disponiveis.append("🌾 Simulador")
                if 'predicao_leite' in ctx:
                    dados_disponiveis.append("🥛 Leite")
                if 'deteccao_gado' in ctx:
                    dados_disponiveis.append("🐄 Gado")
                
                if dados_disponiveis:
                    st.success("✅ Dados: " + " | ".join(dados_disponiveis))
            
            # Histórico
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            chat_container = st.container(height=400)
            
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            # Input
            if prompt := st.chat_input("Pergunte..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                contexto = st.session_state.get('contexto_json', None)
                
                with st.spinner("⚡ Processando..."):
                    resposta = agente.responder(prompt, contexto)
                
                st.session_state.chat_history.append({"role": "assistant", "content": resposta})
                st.rerun()
            
            if st.button("🗑️ Limpar", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    # ==================== ABAS PRINCIPAIS ====================
    tab1, tab2, tab3 = st.tabs([
        "🌾 Simulador de Produtividade", 
        "🥛 Predição de Leite",
        "🐄 Detecção de Gado"
    ])
    
    # ==================== ABA 1: SIMULADOR ====================
    with tab1:
        with st.form("form_simulador"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🌍 Localização e Solo")
                opcoes_regiao = traduzir(df['Region'].unique())
                region_selecionada = st.selectbox("Região:", opcoes_regiao)
                region = original(region_selecionada)
                
                opcoes_solo = traduzir(df['Soil_Type'].unique())
                solo_selecionado = st.selectbox("Tipo de Solo:", opcoes_solo)
                soil_type = original(solo_selecionado)
                
                opcoes_clima = traduzir(df['Weather_Condition'].unique())
                clima_selecionado = st.selectbox("Condição Climática:", opcoes_clima)
                weather = original(clima_selecionado)
            
            with col2:
                st.markdown("#### 🌾 Cultura e Ambiente")
                opcoes_cultura = traduzir(df['Crop'].unique())
                cultura_selecionada = st.selectbox("Cultura:", opcoes_cultura)
                crop = original(cultura_selecionada)
                
                rainfall = st.slider("Precipitação (mm):", int(df['Rainfall_mm'].min()), int(df['Rainfall_mm'].max()), int(df['Rainfall_mm'].mean()))
                temperature = st.slider("Temperatura (°C):", int(df['Temperature_Celsius'].min()), int(df['Temperature_Celsius'].max()), int(df['Temperature_Celsius'].mean()))
            
            with col3:
                st.markdown("#### ⏱️ Práticas Agrícolas")
                days_harvest = st.slider("Dias até Colheita:", int(df['Days_to_Harvest'].min()), int(df['Days_to_Harvest'].max()), int(df['Days_to_Harvest'].mean()))
                
                col_fert, col_irrig = st.columns(2)
                with col_fert:
                    fertilizer = st.checkbox("🧪 Fertilizante", value=True)
                with col_irrig:
                    irrigation = st.checkbox("💧 Irrigação", value=True)
            
            predict_button = st.form_submit_button("🔮 Simular Produtividade", type="primary", use_container_width=True)
        
        if predict_button:
            input_data = {
                'Region': region, 'Soil_Type': soil_type, 'Crop': crop, 'Weather_Condition': weather,
                'Rainfall_mm': rainfall, 'Temperature_Celsius': temperature, 'Days_to_Harvest': days_harvest,
                'Fertilizer_Used': fertilizer, 'Irrigation_Used': irrigation
            }
            
            resultado = simulador.predizer(input_data)
            
            if 'error' in resultado:
                st.error(f"❌ {resultado['error']}")
            else:
                # Calcular ROI
                roi_input = {
                    'crop': crop,
                    'prediction': resultado['prediction'],
                    'fertilizer': fertilizer,
                    'irrigation': irrigation
                }
                roi_analise = AgenteROI.calcular_roi(roi_input)
                
                # Salvar contexto
                st.session_state.contexto_json = {
                    'simulacao': {
                        'cultura': cultura_selecionada,
                        'regiao': region_selecionada,
                        'solo': solo_selecionado,
                        'clima': clima_selecionado,
                        'temperatura': temperature,
                        'chuva': rainfall,
                        'producao_tha': round(resultado['prediction'], 2),
                        'fertilizante': fertilizer,
                        'irrigacao': irrigation
                    },
                    'roi': roi_analise
                }
                
                prediction = resultado['prediction']
                percentile = resultado['percentile']
                
                # Status visual
                if percentile < 25:
                    status, color, bg = "🔴 Baixo", "#D32F2F", "linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%)"
                elif percentile < 50:
                    status, color, bg = "🟠 Moderado", "#F57C00", "linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%)"
                elif percentile < 75:
                    status, color, bg = "🟡 Bom", "#FBC02D", "linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%)"
                else:
                    status, color, bg = "🟢 Excelente", "#388E3C", "linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%)"
                
                st.markdown(f"""
                <div class="result-card" style="background: {bg}; border: 3px solid {color};">
                    <p class="result-value" style="color: {color};">🎯 {prediction:.2f} t/ha</p>
                    <p class="result-label" style="color: {color};">{status} - Percentil {percentile:.0f}º</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas ROI
                st.markdown("---")
                st.markdown("### 💰 Análise Financeira")
                
                fin = roi_analise['financeiro']
                
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("💵 Receita", f"R$ {fin['receita_bruta']:,.0f}")
                with col_b:
                    st.metric("💸 Custo", f"R$ {fin['custo_total']:,.0f}")
                with col_c:
                    st.metric("💚 Lucro", f"R$ {fin['lucro_liquido']:,.0f}")
                with col_d:
                    st.metric("📊 ROI", f"{fin['roi_percentual']:.1f}%")
                
                # Recomendação
                rec_color = "#C8E6C9" if fin['roi_percentual'] > 0 else "#FFCDD2"
                st.markdown(f"""
                <div style="background: {rec_color}; padding: 15px; border-radius: 10px; margin-top: 15px;">
                    <h4 style="margin: 0 0 10px 0;">🤖 Recomendação:</h4>
                    <p style="margin: 0; color: #333;">{roi_analise['recomendacao']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== ABA 2: LEITE ====================
    with tab2:
        show_milk_prediction()
    
    # ==================== ABA 3: GADO ====================
    with tab3:
        show_cattle_detection(YOLO_MODEL_PATH)

if __name__ == "__main__":
    main()
