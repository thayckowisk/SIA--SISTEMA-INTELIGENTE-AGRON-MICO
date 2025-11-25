# 🌾 SIA - Sistema Inteligente Agrícola

Sistema modular de predição agrícola com IA, desenvolvido com Streamlit e Groq.

## 📁 Estrutura do Projeto

```
SIA_FINAL/
│
├── app.py                      # Aplicação principal (código limpo e simples)
├── requirements.txt            # Dependências Python
│
├── modules/                    # Módulos organizados
│   ├── __init__.py
│   ├── agente_roi.py          # Cálculo de ROI e análise financeira
│   ├── agente_chat.py         # Chat IA com Groq API
│   ├── simulador.py           # Random Forest + carregamento de dados
│   ├── predicao_leite.py      # SARIMAX para séries temporais
│   └── deteccao_gado.py       # YOLO para detecção em vídeos
│
├── data/                       # Dados de treinamento
│   └── crop_yield.csv         # Dataset agrícola (40k registros)
│
├── models/                     # Modelos treinados
│   └── best.pt                # Modelo YOLO para gado
│
└── config/                     # Configurações
    └── .env                   # GROQ_API_KEY
```

## 🔧 Como Funciona Cada Módulo

### 1. **app.py** - Aplicação Principal
- **Responsabilidade**: Orquestrar a interface e integrar os módulos
- **O que faz**:
  - Configura a página Streamlit
  - Carrega os módulos (agente_roi, agente_chat, simulador, etc.)
  - Cria as 3 abas: Simulador, Leite, Gado
  - Gerencia o chat na sidebar
  - Coordena o fluxo de dados entre módulos

**Por que é simples agora?**
- Todo código complexo foi movido para os módulos
- app.py apenas IMPORTA e COORDENA
- Fácil de entender e manter

---

### 2. **modules/agente_roi.py** - Agente Financeiro
- **Responsabilidade**: Cálculos de ROI, custos e receitas
- **Entradas**: 
  - Cultura (crop)
  - Produção prevista (prediction)
  - Fertilizante usado (fertilizer)
  - Irrigação usada (irrigation)
- **Saídas**: 
  ```python
  {
    "financeiro": {
      "receita_bruta": 15000.00,
      "custo_total": 4500.00,
      "lucro_liquido": 10500.00,
      "roi_percentual": 233.33,
      "payback_meses": 3.6
    },
    "status": "lucrativo",
    "recomendacao": "Excelente! ROI acima de 100%..."
  }
  ```

**Principais Funções**:
- `calcular_roi(predicao_data)` - Calcula ROI completo
- `_gerar_recomendacao(roi, lucro)` - Gera texto de recomendação

---

### 3. **modules/agente_chat.py** - Chat IA
- **Responsabilidade**: Responder perguntas usando contexto JSON
- **Como funciona**:
  1. Recebe mensagem do usuário
  2. Busca no contexto JSON (simulacao, predicao_leite, deteccao_gado)
  3. Se encontrar resposta rápida, retorna diretamente
  4. Se não, envia para Groq API com contexto completo

**Exemplos de Perguntas**:
- "Qual o ROI?" → Busca em `contexto_json['roi']`
- "Como está o leite?" → Busca em `contexto_json['predicao_leite']`
- "Quantas vacas?" → Busca em `contexto_json['deteccao_gado']`
- "Me dê um resumo geral" → Combina TODOS os dados

**Principais Funções**:
- `responder(mensagem, contexto_json)` - Processa pergunta

---

### 4. **modules/simulador.py** - Machine Learning
- **Responsabilidade**: Treinar Random Forest e fazer predições
- **Componentes**:
  - `carregar_dados(dataset_path)` - Carrega CSV e faz amostragem
  - `ModeloML` - Classe com Random Forest
    - `treinar()` - Treina modelo com 40k registros
    - `predizer(dados)` - Faz predição de produtividade

**Fluxo**:
1. Usuário preenche formulário (região, solo, cultura...)
2. `ModeloML.predizer()` processa os dados
3. Retorna: `{'prediction': 5.23, 'percentile': 78.5}`
4. app.py chama `AgenteROI.calcular_roi()` para calcular finanças

---

### 5. **modules/predicao_leite.py** - Séries Temporais
- **Responsabilidade**: Previsão de produção de leite com SARIMAX
- **Como funciona**:
  1. Usuário faz upload de CSV com dados mensais
  2. Escolhe período inicial e meses para previsão
  3. SARIMAX analisa sazonalidade e tendência
  4. Gera previsão e gráficos

**Principais Funções**:
- `show_milk_prediction()` - Interface completa da aba

**Contexto Salvo**:
```python
st.session_state.contexto_json['predicao_leite'] = {
  'media_historica': 1523.45,
  'media_prevista': 1678.90,
  'variacao_percentual': +10.2,
  'meses_previsao': 12
}
```

---

### 6. **modules/deteccao_gado.py** - Visão Computacional
- **Responsabilidade**: Detectar e contar gado em vídeos com YOLO
- **Fluxo**:
  1. Usuário faz upload de vídeo MP4
  2. YOLO processa frame por frame
  3. Detecta vacas (confiança > 0.5)
  4. Desenha caixas verdes e conta
  5. Gera vídeo processado + Excel com métricas

**Principais Funções**:
- `show_cattle_detection(yolo_model_path)` - Interface completa

**Contexto Salvo**:
```python
st.session_state.contexto_json['deteccao_gado'] = {
  'frames_processados': 1250,
  'media_vacas': 47.3,
  'maximo_vacas': 53,
  'fps_medio': 12.5
}
```

---

## 🚀 Como Executar

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Configurar Groq API**:
Crie `config/.env`:
```
GROQ_API_KEY=gsk_sua_chave_aqui
```

3. **Executar**:
```bash
streamlit run app.py
```

4. **Acessar**:
http://localhost:8501

---

## 💡 Por Que Modularizar?

### **Antes** (1093 linhas em um arquivo):
- ❌ Difícil de entender
- ❌ Difícil de manter
- ❌ Difícil de explicar
- ❌ Difícil de testar partes individualmente

### **Depois** (módulos separados):
- ✅ Cada módulo tem 1 responsabilidade clara
- ✅ Fácil de entender o que cada parte faz
- ✅ Fácil de modificar sem quebrar outras partes
- ✅ Fácil de testar módulos individualmente
- ✅ Fácil de explicar em apresentações

---

## 📊 Fluxo de Dados Completo

### Aba 1 - Simulador:
```
Usuário preenche formulário
    ↓
modules/simulador.py (ModeloML.predizer)
    ↓
modules/agente_roi.py (calcular_roi)
    ↓
st.session_state.contexto_json['simulacao'] + ['roi']
    ↓
Chat pode usar esses dados!
```

### Aba 2 - Leite:
```
Upload CSV
    ↓
modules/predicao_leite.py (SARIMAX)
    ↓
st.session_state.contexto_json['predicao_leite']
    ↓
Chat pode responder sobre leite!
```

### Aba 3 - Gado:
```
Upload vídeo
    ↓
modules/deteccao_gado.py (YOLO)
    ↓
st.session_state.contexto_json['deteccao_gado']
    ↓
Chat pode responder sobre gado!
```

### Chat Sidebar:
```
Usuário pergunta "Qual o ROI?"
    ↓
modules/agente_chat.py
    ↓
Busca em contexto_json['simulacao'] e ['roi']
    ↓
Resposta rápida ou Groq API se complexo
```

---

## 🎯 Melhorias Implementadas

### Layout:
- ✅ Título grande e visível no topo
- ✅ CSS gradiente moderno
- ✅ Sidebar começa FECHADA (`initial_sidebar_state="collapsed"`)
- ✅ Chat sem descrição longa, direto ao ponto
- ✅ Métricas visuais com cards coloridos

### Código:
- ✅ app.py com apenas **329 linhas** (antes: 1093!)
- ✅ 6 módulos organizados por função
- ✅ Cada módulo é independente e reutilizável
- ✅ Imports claros no início

### Pastas:
- ✅ Removidas pastas antigas (03.WEB_SIMULADOR, 04.LEITE, etc.)
- ✅ Apenas SIA_FINAL/ com estrutura profissional
- ✅ Tudo organizado: data/, models/, config/, modules/

---

## 📚 Tecnologias Usadas

- **Streamlit**: Interface web
- **Groq API**: LLM ultra-rápido (Llama 3.3 70B)
- **LangChain**: Framework para LLM
- **Random Forest**: ML para produtividade
- **SARIMAX**: Séries temporais
- **YOLO (ultralytics)**: Detecção de objetos
- **OpenCV**: Processamento de vídeo
- **Pandas**: Manipulação de dados
- **Matplotlib**: Gráficos

---

## 🤝 Contribuindo

Se quiser adicionar novos módulos:

1. Crie arquivo em `modules/novo_modulo.py`
2. Importe no `app.py`
3. Adicione uma nova aba se necessário
4. Salve contexto em `st.session_state.contexto_json`

**Exemplo**:
```python
# modules/analise_solo.py
def analisar_solo(dados_solo):
    # Sua lógica aqui
    return resultado

# app.py
from modules.analise_solo import analisar_solo

# Adicionar em nova aba
with tab4:
    resultado = analisar_solo(dados)
```

---

## 📞 Suporte

Para dúvidas sobre cada módulo, veja o código comentado em `modules/`.

**Estrutura é simples**:
- 1 módulo = 1 função
- app.py = coordenador
- Contexto JSON = comunicação entre módulos

---

Desenvolvido com ❤️ para facilitar análises agrícolas com IA.
