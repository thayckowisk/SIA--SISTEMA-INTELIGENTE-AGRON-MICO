"""
Módulo de Predição de Leite com SARIMAX
Análise de séries temporais e previsão
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import date
from io import StringIO

def show_milk_prediction():
    """Interface de predição de produção de leite"""
    
    st.header("🥛 Predição de Produção de Leite")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📁 Configurações")
        
        uploaded_file = st.file_uploader("Upload CSV:", type=['csv'])
        
        if uploaded_file is not None:
            start_date = st.date_input("Período Inicial:", value=date(2011, 1, 1))
            forecast_period = st.number_input("Meses para Previsão:", min_value=1, max_value=48, value=12)
            process_button = st.button("🚀 Processar", type="primary", use_container_width=True)
        else:
            st.info("👆 Faça upload de um CSV")
            process_button = False
    
    with col2:
        if uploaded_file is not None and process_button:
            try:
                string_io = StringIO(uploaded_file.getvalue().decode("utf-8"))
                data = pd.read_csv(string_io, header=None)
                
                ts_data = pd.Series(
                    data.iloc[:,0].values, 
                    index=pd.date_range(start=start_date, periods=len(data), freq='M')
                )
                
                st.subheader("📈 Resultados")
                
                with st.spinner("Analisando..."):
                    decompose = seasonal_decompose(ts_data, model='additive')
                    pic_decompose = decompose.plot()
                    pic_decompose.set_size_inches(10, 8)
                    
                    model = SARIMAX(ts_data, order=(2, 0, 0), seasonal_order=(0, 1, 1, 12))
                    model_fit = model.fit(disp=False)
                    forecast = model_fit.forecast(steps=forecast_period)
                
                pic_forecast, ax = plt.subplots(figsize=(10, 5))
                ts_data.plot(ax=ax, label='Histórico', color='#2196F3')
                forecast.plot(ax=ax, style='r--', label='Previsão', color='#FF5722')
                ax.set_xlabel('Período')
                ax.set_ylabel('Produção')
                ax.set_title('Série Temporal e Previsão')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                tab1, tab2, tab3 = st.tabs(["📊 Previsão", "📉 Decomposição", "📋 Dados"])
                
                with tab1:
                    st.pyplot(pic_forecast)
                    
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Média Histórica", f"{ts_data.mean():.2f}")
                    with col_m2:
                        st.metric("Média Prevista", f"{forecast.mean():.2f}")
                    with col_m3:
                        variacao = ((forecast.mean() - ts_data.mean()) / ts_data.mean()) * 100
                        st.metric("Variação", f"{variacao:+.2f}%")
                
                with tab2:
                    st.pyplot(pic_decompose)
                
                with tab3:
                    forecast_df = pd.DataFrame({
                        'Período': forecast.index.strftime('%Y-%m'),
                        'Previsão': forecast.values.round(2)
                    })
                    st.dataframe(forecast_df, use_container_width=True)
                    
                    csv = forecast_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"previsao_leite_{forecast_period}meses.csv",
                        mime="text/csv"
                    )
                
                st.success(f"✅ Previsão gerada para {forecast_period} meses!")
                
                # Salvar contexto
                if 'contexto_json' not in st.session_state:
                    st.session_state.contexto_json = {}
                
                st.session_state.contexto_json['predicao_leite'] = {
                    'total_meses': len(ts_data),
                    'media_historica': float(ts_data.mean()),
                    'media_prevista': float(forecast.mean()),
                    'meses_previsao': forecast_period,
                    'variacao_percentual': float(((forecast.mean() - ts_data.mean()) / ts_data.mean()) * 100),
                    'ultimo_valor': float(ts_data.iloc[-1]),
                    'primeiro_valor_previsto': float(forecast.iloc[0])
                }
                
            except Exception as ex:
                st.error(f"❌ Erro: {ex}")
        
        elif not uploaded_file:
            st.info("📊 Os gráficos aparecerão aqui após o upload")
