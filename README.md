# 🌾 SIA - Sistema Inteligente Agronômico

Sistema completo de predição e análise agronômica com Inteligência Artificial, integrando Machine Learning, Séries Temporais e Visão Computacional.

## 🎯 Sobre o Projeto

O SIA foi desenvolvido para auxiliar produtores rurais na tomada de decisões com base em dados reais e análises inteligentes. O sistema oferece:

- 🌾 **Predição de Produtividade**: Estima a produção de culturas com Random Forest
- 💰 **Análise de ROI**: Calcula retorno sobre investimento e viabilidade financeira
- 🥛 **Previsão de Leite**: Modelo SARIMAX para séries temporais de produção leiteira
- 🐄 **Detecção de Gado**: YOLO para contagem automática de animais em vídeos
- 💬 **Chat Inteligente**: Assistente IA que responde perguntas sobre as análises

## 📁 Estrutura do Projeto

```
SIA_FINAL/
│
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências Python
├── packages.txt               # Pacotes do sistema (Linux)
│
├── modules/                   # Módulos do sistema
│   ├── agente_roi.py         # Análise financeira e ROI
│   ├── agente_chat.py        # Chat com IA (Groq)
│   ├── simulador.py          # Predição com Random Forest
│   ├── predicao_leite.py     # Séries temporais (SARIMAX)
│   └── deteccao_gado.py      # Visão computacional (YOLO)
│
├── data/                      # Datasets
│   └── crop_yield.csv        # 40k registros de culturas
│
├── models/                    # Modelos treinados
│   └── best.pt               # YOLO para detecção de gado
│
└── config/                    # Configurações
    └── .env                  # API keys (criar manualmente)
```

---

## 🚀 Como Usar

### **Passo 1: Clonar o Repositório**
```bash
git clone https://github.com/thayckowisk/SIA--SISTEMA-INTELIGENTE-AGRON-MICO.git
cd SIA--SISTEMA-INTELIGENTE-AGRON-MICO
```

### **Passo 2: Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **Passo 3: Configurar API Key (Opcional)**
Para usar o chat inteligente, crie o arquivo `config/.env`:
```
GROQ_API_KEY=gsk_sua_chave_aqui
```
> 💡 Obtenha sua chave gratuita em: https://console.groq.com

### **Passo 4: Executar o Sistema**
```bash
streamlit run app.py
```

### **Passo 5: Acessar**
Abra seu navegador em: **http://localhost:8501**

---

## 📱 Como Usar Cada Funcionalidade

### 🌾 **Simulador de Produtividade**
1. Selecione a cultura (Soja, Milho, Arroz, etc.)
2. Configure região, tipo de solo e clima
3. Ajuste temperatura, chuva e dias até colheita
4. Marque se usa fertilizante e irrigação
5. Clique em **"Simular Produtividade"**
6. Veja a produção estimada (t/ha) e análise de ROI

### 🥛 **Predição de Leite**
1. Prepare um CSV com dados mensais de produção
2. Faça upload do arquivo
3. Selecione a data inicial
4. Escolha quantos meses deseja prever (1-48)
5. Clique em **"Processar"**
6. Analise gráficos de tendência e baixe a previsão

### 🐄 **Detecção de Gado**
1. Grave ou obtenha um vídeo do seu rebanho (MP4, AVI, MOV)
2. Faça upload do vídeo
3. Clique em **"Processar"**
4. Aguarde a análise (pode levar alguns minutos)
5. Baixe o vídeo com detecções marcadas
6. Baixe a planilha Excel com estatísticas

### 💬 **Chat Inteligente**
1. Execute qualquer análise acima
2. Abra o chat na sidebar (clique na seta)
3. Faça perguntas como:
   - "Qual o ROI da simulação?"
   - "Vale a pena investir?"
   - "Como está a produção de leite?"
   - "Quantas vacas foram detectadas?"
4. O assistente responde com base nos seus dados

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|------------|---------|
| **Python 3.13** | Linguagem principal |
| **Streamlit** | Interface web interativa |
| **Scikit-learn** | Random Forest para predição |
| **Statsmodels** | SARIMAX para séries temporais |
| **Ultralytics YOLO** | Detecção de objetos em vídeo |
| **OpenCV** | Processamento de vídeo |
| **Groq API** | LLM para chat inteligente |
| **LangChain** | Framework para IA conversacional |
| **Pandas** | Manipulação de dados |
| **Matplotlib** | Visualização de gráficos |

---

## 📂 Estrutura de Arquivos

```
SIA_FINAL/
│
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências
├── packages.txt               # Pacotes sistema (Streamlit Cloud)
│
├── modules/                   # Módulos do sistema
│   ├── agente_roi.py         # Análise financeira
│   ├── agente_chat.py        # Chat com IA
│   ├── simulador.py          # Predição de produtividade
│   ├── predicao_leite.py     # Previsão de leite
│   └── deteccao_gado.py      # Detecção em vídeo
│
├── data/                      # Datasets
│   └── crop_yield.csv        # 40k registros de culturas
│
├── models/                    # Modelos treinados
│   └── best.pt               # YOLO para gado
│
└── config/                    # Configurações
    └── .env                  # API keys (não versionado)
```

---

## 💰 Análise de ROI - Preços Reais

O sistema usa **preços atualizados do mercado brasileiro (2024/2025)**:

### **Preços por Tonelada (CEPEA/CONAB/B3)**
- Arroz: R$ 1.800/ton
- Soja: R$ 1.400/ton (saca R$ 140)
- Milho: R$ 650/ton (saca R$ 65)
- Algodão: R$ 7.500/ton (arroba R$ 500)
- Trigo: R$ 1.200/ton
- Cevada: R$ 1.100/ton

### **Custos por Hectare**
- Custo Base: R$ 3.200 (sementes + defensivos + mão de obra + maquinário)
- Fertilizante: R$ 2.500 (NPK + micronutrientes)
- Irrigação: R$ 1.800 (energia + manutenção)

### **Interpretação do ROI**
- **ROI > 80%**: 🌟 Excelente - Investimento altamente lucrativo
- **ROI > 40%**: ✅ Bom - Retorno acima da média
- **ROI > 15%**: ⚠️ Modesto - Comum na agricultura
- **ROI > 0%**: ⚡ Baixo - Considere otimizações
- **ROI < 0%**: ❌ Prejuízo - Revise estratégia

---

## 🎓 Sobre o Desenvolvimento

Este projeto foi desenvolvido como trabalho de conclusão em Inteligência Artificial aplicada à agricultura. O objetivo é demonstrar a integração de múltiplas técnicas de IA em uma aplicação prática e funcional.

### **Decisões Técnicas**

**Por que Random Forest?**
- Ideal para dados tabulares
- Não requer normalização complexa
- Interpretável e rápido

**Por que SARIMAX?**
- Captura sazonalidade em dados mensais
- Validado cientificamente para agricultura

**Por que YOLO?**
- Estado da arte em detecção em tempo real
- Modelo pré-treinado para animais

**Por que Groq?**
- 10x mais rápido que OpenAI
- Gratuito (6000 tokens/min)
- Respostas em < 1 segundo

---

## 🔒 Licença

Este projeto é de código aberto e está disponível para uso educacional e comercial.

---

## 👨‍💻 Autor

Desenvolvido por **Thayckowisk**

📧 Contato: [thayckowisk@discente.ufg.br]
🔗 GitHub: [@thayckowisk](https://github.com/thayckowisk)

---

## 🙏 Agradecimentos

- Dataset de culturas: Kaggle
- Modelo YOLO: Ultralytics
- API LLM: Groq
- Framework: Streamlit

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**

**Estrutura é simples**:
- 1 módulo = 1 função
- app.py = coordenador
- Contexto JSON = comunicação entre módulos

---

Desenvolvido com ❤️ para facilitar análises agronômicas com IA.
