"""
Agente Chat com Groq API
Responde perguntas sobre simulador, leite e gado usando contexto JSON
"""

import os
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class AgenteChat:
    """Agente de chat com Groq - Contexto JSON completo de TODAS as análises"""
    
    def __init__(self, groq_api_key, groq_model="llama-3.3-70b-versatile"):
        """Inicializa agente com Groq API"""
        if not groq_api_key or groq_api_key == "your_groq_api_key_here":
            self.llm = None
        else:
            self.llm = ChatGroq(model=groq_model, temperature=0.7, api_key=groq_api_key)
        
        self.template = PromptTemplate(
            input_variables=["contexto", "pergunta"],
            template="""Você é um especialista em agricultura, pecuária e análise de dados.

DADOS DISPONÍVEIS (JSON):
{contexto}

PERGUNTA: {pergunta}

Responda de forma técnica, clara e objetiva em português. Use os dados JSON para fundamentar sua resposta."""
        )
        
        if self.llm:
            self.chain = self.template | self.llm | StrOutputParser()
    
    def responder(self, mensagem, contexto_json=None):
        """Responde usando contexto JSON de simulador, leite e gado"""
        
        if not contexto_json or not any(contexto_json.values()):
            if not self.llm:
                return "⚠️ Configure GROQ_API_KEY no arquivo config/.env"
            try:
                return self.chain.invoke({"contexto": "Nenhuma análise disponível", "pergunta": mensagem})
            except:
                return "❌ Erro ao conectar com Groq API"
        
        msg_lower = mensagem.lower()
        
        # ==================== 1. SIMULADOR DE PRODUTIVIDADE ====================
        if 'simulacao' in contexto_json:
            sim = contexto_json['simulacao']
            roi = contexto_json.get('roi', {}).get('financeiro', {})
            
            if any(w in msg_lower for w in ['roi', 'lucro', 'retorno', 'vale']):
                roi_val = roi.get('roi_percentual', 0)
                return f"💰 **ROI:** {roi_val:.1f}%\n💵 **Lucro:** R$ {roi.get('lucro_liquido',0):,.0f}/ha\n🌾 **Cultura:** {sim.get('cultura')}\n{'✅ Investimento rentável!' if roi_val>30 else '⚠️ Revise custos'}"
            
            if 'fertilizante' in msg_lower:
                return f"🧪 **Fertilizante:** {'✅ Sim (R$ 800/ha)' if sim.get('fertilizante') else '❌ Não - ADICIONE para +25% produção!'}"
            
            if any(w in msg_lower for w in ['irrigação', 'irrigacao', 'água']):
                chuva_mm = sim.get('chuva', 0)
                status_irrigacao = '✅ Sim (R$ 1.200/ha)' if sim.get('irrigacao') else f'❌ Não - Com {chuva_mm}mm, RECOMENDADO!'
                return f"💧 **Irrigação:** {status_irrigacao}"
            
            if any(w in msg_lower for w in ['melhorar', 'otimizar', 'aumentar']):
                dicas = []
                if not sim.get('fertilizante'): dicas.append("🧪 Fertilizante (+25%)")
                if not sim.get('irrigacao'): dicas.append("💧 Irrigação (+20%)")
                return "💡 **Sugestões:**\n" + ("\n".join(dicas) if dicas else "✅ Já otimizado!")
        
        # ==================== 2. PREDIÇÃO DE LEITE ====================
        if 'predicao_leite' in contexto_json:
            leite = contexto_json['predicao_leite']
            
            if any(w in msg_lower for w in ['leite', 'produção', 'previsão', 'litros']):
                var = leite.get('variacao_percentual', 0)
                return f"🥛 **Produção de Leite:**\n📊 Média histórica: {leite.get('media_historica'):.1f}L\n🔮 Previsão ({leite.get('meses_previsao')}m): {leite.get('media_prevista'):.1f}L\n📈 Variação: {var:+.1f}%\n{'✅ Tendência positiva!' if var>0 else '⚠️ Queda prevista'}"
        
        # ==================== 3. DETECÇÃO DE GADO ====================
        if 'deteccao_gado' in contexto_json:
            gado = contexto_json['deteccao_gado']
            
            if any(w in msg_lower for w in ['gado', 'vaca', 'animal', 'rebanho']):
                return f"🐄 **Análise de Rebanho:**\n🎬 Frames: {gado.get('frames_processados')}\n📊 Média: {gado.get('media_vacas'):.1f} vacas\n📈 Máximo: {gado.get('maximo_vacas')} vacas\n⚡ FPS: {gado.get('fps_medio'):.1f}"
        
        # ==================== 4. RESUMO GERAL ====================
        if any(w in msg_lower for w in ['resumo', 'tudo', 'geral', 'status']):
            resumo = "📊 **RESUMO GERAL:**\n\n"
            
            if 'simulacao' in contexto_json:
                s = contexto_json['simulacao']
                r = contexto_json.get('roi', {}).get('financeiro', {})
                resumo += f"🌾 **Produtividade:** {s.get('producao_tha')}t/ha (ROI {r.get('roi_percentual',0):.1f}%)\n"
            
            if 'predicao_leite' in contexto_json:
                l = contexto_json['predicao_leite']
                resumo += f"🥛 **Leite:** {l.get('media_prevista'):.1f}L ({l.get('variacao_percentual'):+.1f}%)\n"
            
            if 'deteccao_gado' in contexto_json:
                g = contexto_json['deteccao_gado']
                resumo += f"🐄 **Gado:** {g.get('media_vacas'):.1f} vacas (máx {g.get('maximo_vacas')})\n"
            
            return resumo if len(resumo) > 50 else "ℹ️ Faça análises nas abas primeiro!"
        
        # ==================== 5. GROQ PARA PERGUNTAS COMPLEXAS ====================
        if not self.llm:
            return "⚠️ Configure GROQ_API_KEY para perguntas avançadas"
        
        try:
            # Converter contexto JSON para texto
            contexto_str = json.dumps(contexto_json, indent=2, ensure_ascii=False)
            return self.chain.invoke({"contexto": contexto_str, "pergunta": mensagem})
        except Exception as e:
            return f"❌ Erro: {str(e)[:100]}"
