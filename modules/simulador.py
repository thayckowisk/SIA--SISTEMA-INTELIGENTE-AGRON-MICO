"""
Simulador de Produtividade Agrícola com Random Forest
Carrega dados, treina modelo e faz predições
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

@st.cache_data
def carregar_dados(dataset_path):
    """Carrega dataset de crop_yield.csv"""
    if dataset_path.exists():
        try:
            df = pd.read_csv(dataset_path)
            if len(df) > 40000:
                df = df.sample(n=40000, random_state=42)
            return df.dropna()
        except Exception as e:
            st.error(f"❌ Erro ao carregar dataset: {e}")
            st.stop()
    
    st.error("❌ Dataset crop_yield.csv não encontrado!")
    st.stop()

class ModeloML:
    """Modelo Random Forest para predição de produtividade"""
    
    def __init__(self, df):
        self.df = df
        self.model = RandomForestRegressor(n_estimators=30, max_depth=8, n_jobs=-1, random_state=42)
        self.encoders = {}
        self.trained = False
        
    def preparar(self):
        """Prepara dados para treinamento"""
        cat_cols = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition']
        num_cols = ['Rainfall_mm', 'Temperature_Celsius', 'Days_to_Harvest']
        bool_cols = ['Fertilizer_Used', 'Irrigation_Used']
        
        X = self.df[cat_cols + num_cols + bool_cols].copy()
        y = self.df['Yield_tons_per_hectare']
        
        for col in cat_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.encoders[col] = le
        
        for col in bool_cols:
            X[col] = X[col].astype(int)
        
        return X, y
    
    def treinar(self):
        """Treina o modelo"""
        X, y = self.preparar()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        self.trained = True
        return {'mae': mean_absolute_error(y_test, y_pred), 'r2': r2_score(y_test, y_pred)}
    
    def predizer(self, dados):
        """Faz predição com os dados fornecidos"""
        if not self.trained:
            return {"error": "Modelo não treinado"}
        
        try:
            cats = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition']
            for col in cats:
                if col in dados:
                    dados[col] = self.encoders[col].transform([dados[col]])[0]
            
            df_input = pd.DataFrame([dados])
            pred = self.model.predict(df_input)[0]
            
            all_preds = self.model.predict(self.preparar()[0])
            percentil = (np.sum(all_preds <= pred) / len(all_preds)) * 100
            
            return {'prediction': pred, 'percentile': percentil}
            
        except Exception as e:
            return {"error": f"Erro: {str(e)}"}

# ==================== TRADUÇÕES ====================
MAPA = {
    # Culturas
    'Rice': 'Arroz', 'Wheat': 'Trigo', 'Corn': 'Milho', 'Barley': 'Cevada',
    'Soybeans': 'Soja', 'Cotton': 'Algodão', 'Soybean': 'Soja', 'Maize': 'Milho',
    # Regiões
    'North': 'Norte', 'South': 'Sul', 'East': 'Leste', 'West': 'Oeste',
    # Solos
    'Clay': 'Argiloso', 'Sandy': 'Arenoso', 'Loam': 'Areno-Argiloso', 'Silt': 'Siltoso',
    # Clima
    'Sunny': 'Ensolarado', 'Rainy': 'Chuvoso', 'Cloudy': 'Nublado'
}

MAPA_REVERSO = {v: k for k, v in MAPA.items()}

def traduzir(itens):
    """Traduz lista de itens do inglês para português"""
    return [MAPA.get(item, item) for item in itens]

def original(item_pt):
    """Retorna nome original em inglês"""
    return MAPA_REVERSO.get(item_pt, item_pt)
