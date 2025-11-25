"""
Agente ROI - Análise Financeira
Calcula ROI, custos e receitas de produção agrícola
"""

class AgenteROI:
    """Agente especializado em calcular ROI e análise financeira"""
    
    # Preços médios por tonelada (R$) - Valores reais mercado brasileiro 2024/2025
    # Fonte: CEPEA, CONAB, B3
    PRECOS_CULTURAS = {
        'Rice': 1800,      # Arroz: R$ 1.800/ton (alta recente)
        'Wheat': 1200,     # Trigo: R$ 1.200/ton
        'Corn': 650,       # Milho: R$ 650/ton (saca R$ 65)
        'Barley': 1100,    # Cevada: R$ 1.100/ton
        'Soybeans': 1400,  # Soja: R$ 1.400/ton (saca R$ 140)
        'Cotton': 7500,    # Algodão: R$ 7.500/ton (arroba R$ 500)
        'Soybean': 1400,   # Soja alternativo
        'Maize': 650       # Milho alternativo
    }
    
    # Custos REAIS por hectare (R$) - Média Brasil 2024/2025
    CUSTO_FERTILIZANTE = 2500   # NPK + micronutrientes (aumentou muito)
    CUSTO_IRRIGACAO = 1800      # Energia + manutenção
    CUSTO_BASE = 3200           # Sementes (R$ 800) + Defensivos (R$ 1.200) + Mão de obra (R$ 800) + Maquinário (R$ 400)
    
    @staticmethod
    def calcular_roi(predicao_data):
        """
        Calcula ROI completo baseado na predição
        
        Args:
            predicao_data: dict com 'crop', 'prediction', 'fertilizer', 'irrigation'
        
        Returns:
            dict com análise financeira completa em JSON
        """
        crop = predicao_data.get('crop')
        producao_tha = predicao_data.get('prediction', 0)
        usa_fertilizante = predicao_data.get('fertilizer', False)
        usa_irrigacao = predicao_data.get('irrigation', False)
        
        # Receita Bruta
        preco_tonelada = AgenteROI.PRECOS_CULTURAS.get(crop, 1000)
        receita_bruta = producao_tha * preco_tonelada
        
        # Custos
        custo_total = AgenteROI.CUSTO_BASE
        if usa_fertilizante:
            custo_total += AgenteROI.CUSTO_FERTILIZANTE
        if usa_irrigacao:
            custo_total += AgenteROI.CUSTO_IRRIGACAO
        
        # Lucro e ROI
        lucro_liquido = receita_bruta - custo_total
        roi_percentual = (lucro_liquido / custo_total) * 100 if custo_total > 0 else 0
        
        # Payback (meses)
        payback_meses = (custo_total / receita_bruta) * 12 if receita_bruta > 0 else 999
        
        # Retornar JSON estruturado
        return {
            "financeiro": {
                "receita_bruta": round(receita_bruta, 2),
                "custo_total": round(custo_total, 2),
                "lucro_liquido": round(lucro_liquido, 2),
                "roi_percentual": round(roi_percentual, 2),
                "payback_meses": round(payback_meses, 1)
            },
            "detalhes_custo": {
                "custo_base": AgenteROI.CUSTO_BASE,
                "fertilizante": AgenteROI.CUSTO_FERTILIZANTE if usa_fertilizante else 0,
                "irrigacao": AgenteROI.CUSTO_IRRIGACAO if usa_irrigacao else 0
            },
            "mercado": {
                "preco_tonelada": preco_tonelada,
                "producao_tha": round(producao_tha, 2),
                "cultura": crop
            },
            "status": "lucrativo" if lucro_liquido > 0 else "prejuizo",
            "recomendacao": AgenteROI._gerar_recomendacao(roi_percentual, lucro_liquido)
        }
    
    @staticmethod
    def _gerar_recomendacao(roi, lucro):
        """Gera recomendação baseada no ROI - Padrões agricultura brasileira"""
        if roi > 80:
            return "🌟 Excelente! ROI acima de 80%. Investimento altamente lucrativo."
        elif roi > 40:
            return "✅ Bom ROI. Investimento viável com retorno sólido acima da média."
        elif roi > 15:
            return "⚠️ ROI modesto (~15-40%). Comum na agricultura, mas avalie melhorias."
        elif roi > 0:
            return "⚡ ROI positivo mas baixo. Considere otimizar insumos ou trocar cultura."
        else:
            return "❌ Prejuízo. Revise custos, clima ou considere outra cultura/região."
