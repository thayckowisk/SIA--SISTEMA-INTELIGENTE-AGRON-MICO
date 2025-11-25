"""
Agente ROI - Análise Financeira
Calcula ROI, custos e receitas de produção agrícola
"""

class AgenteROI:
    """Agente especializado em calcular ROI e análise financeira"""
    
    # Preços médios por tonelada (R$) - Valores de 2024
    PRECOS_CULTURAS = {
        'Rice': 1200, 'Wheat': 900, 'Corn': 850, 'Barley': 800,
        'Soybeans': 1500, 'Cotton': 3200, 'Soybean': 1500, 'Maize': 850
    }
    
    # Custos por hectare (R$)
    CUSTO_FERTILIZANTE = 800
    CUSTO_IRRIGACAO = 1200
    CUSTO_BASE = 2500  # Sementes, mão de obra, maquinário
    
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
        """Gera recomendação baseada no ROI"""
        if roi > 100:
            return "Excelente! ROI acima de 100%. Investimento altamente recomendado."
        elif roi > 50:
            return "Bom ROI. Investimento viável com retorno sólido."
        elif roi > 0:
            return "ROI positivo mas modesto. Considere otimizações."
        else:
            return "ROI negativo. Revise custos ou mude estratégia."
