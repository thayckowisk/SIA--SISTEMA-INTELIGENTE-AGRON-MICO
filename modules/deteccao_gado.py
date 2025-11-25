"""
Módulo de Detecção de Gado com YOLO
Processa vídeos e conta animais
"""

import streamlit as st
import pandas as pd
import cv2
import tempfile
import os
import time
import matplotlib.pyplot as plt
from pathlib import Path

def show_cattle_detection(yolo_model_path):
    """Interface de detecção de gado"""
    
    st.header("🐄 Detecção e Contagem de Gado")
    
    if not yolo_model_path.exists():
        st.error(f"❌ Modelo YOLO não encontrado em: {yolo_model_path}")
        return
    
    try:
        from ultralytics import YOLO
    except ImportError:
        st.error("❌ Instale: pip install ultralytics opencv-python")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📤 Upload de Vídeo")
        uploaded_file = st.file_uploader("Escolha um vídeo", type=['mp4', 'avi', 'mov'])
        
        if uploaded_file is not None:
            st.success(f"✅ '{uploaded_file.name}' carregado!")
            processar = st.button("🚀 Processar", type="primary", use_container_width=True)
        else:
            processar = False
    
    with col2:
        st.markdown("#### ℹ️ Informações")
        st.info(f"""
        **Modelo:** YOLO
        **Status:** ✅ Pronto
        
        O sistema irá:
        - Detectar gado (confiança > 0.5)
        - Desenhar caixas verdes
        - Contar por frame
        - Gerar vídeo e Excel
        """)
    
    if uploaded_file is not None and processar:
        try:
            st.markdown("### 🎬 Processando...")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                input_video_path = os.path.join(temp_dir, "input.mp4")
                with open(input_video_path, "wb") as f:
                    f.write(uploaded_file.read())
                
                output_video_path = os.path.join(temp_dir, "output.mp4")
                metricas_path = os.path.join(temp_dir, "metricas.xlsx")
                
                with st.spinner("🔄 Carregando YOLO..."):
                    model = YOLO(yolo_model_path)
                
                video = cv2.VideoCapture(input_video_path)
                
                if not video.isOpened():
                    st.error("❌ Erro ao abrir vídeo")
                    return
                
                frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(video.get(cv2.CAP_PROP_FPS))
                total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
                
                metricas = []
                frame_count = 0
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                while True:
                    check, img = video.read()
                    if not check:
                        break
                    
                    frame_count += 1
                    inicio = time.time()
                    
                    results = model(img, verbose=False)[0]
                    nomes = results.names
                    
                    cow_count_frame = 0
                    
                    for box in results.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        cls = int(box.cls.item())
                        nomeClasse = nomes[cls]
                        conf = float(box.conf.item())
                        
                        if conf < 0.5:
                            continue
                        
                        if nomeClasse.lower() == "cow":
                            cow_count_frame += 1
                        
                        texto = f"{nomeClasse} - {conf:.2f}"
                        cv2.putText(img, texto, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (250, 250, 250), 2)
                        
                        cor = (0, 250, 0) if nomeClasse.lower() == "cow" else (0, 0, 255)
                        cv2.rectangle(img, (x1, y1), (x2, y2), cor, 3)
                    
                    cv2.putText(img, f"Contagem: {cow_count_frame}", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    
                    tempo_inferencia = time.time() - inicio
                    fps_atual = 1 / tempo_inferencia if tempo_inferencia > 0 else 0
                    
                    metricas.append({
                        "Frame": frame_count,
                        "Tempo_inferencia (s)": round(tempo_inferencia, 4),
                        "FPS": round(fps_atual, 2),
                        "Vacas no Frame": cow_count_frame
                    })
                    
                    output_video.write(img)
                    
                    progress = int((frame_count / total_frames) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"Frame {frame_count}/{total_frames} - Vacas: {cow_count_frame}")
                
                video.release()
                output_video.release()
                
                df_metricas = pd.DataFrame(metricas)
                df_metricas.to_excel(metricas_path, index=False)
                
                st.success("✅ Processamento concluído!")
                
                # Salvar contexto
                if 'contexto_json' not in st.session_state:
                    st.session_state.contexto_json = {}
                
                st.session_state.contexto_json['deteccao_gado'] = {
                    'frames_processados': int(frame_count),
                    'media_vacas': float(df_metricas["Vacas no Frame"].mean()),
                    'maximo_vacas': int(df_metricas["Vacas no Frame"].max()),
                    'fps_medio': float(df_metricas["FPS"].mean()),
                    'nome_arquivo': uploaded_file.name
                }
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Frames", frame_count)
                with col2:
                    st.metric("🐄 Média Vacas", f"{df_metricas['Vacas no Frame'].mean():.1f}")
                with col3:
                    st.metric("📈 Máximo", int(df_metricas["Vacas no Frame"].max()))
                with col4:
                    st.metric("⚡ FPS", f"{df_metricas['FPS'].mean():.1f}")
                
                st.markdown("### 📥 Downloads")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    with open(output_video_path, "rb") as video_file:
                        st.download_button(
                            label="⬇️ Vídeo Processado",
                            data=video_file,
                            file_name="video_deteccoes.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                
                with col_b:
                    with open(metricas_path, "rb") as excel_file:
                        st.download_button(
                            label="⬇️ Métricas Excel",
                            data=excel_file,
                            file_name="metricas.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                
                st.markdown("### 📊 Gráfico")
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(df_metricas["Frame"], df_metricas["Vacas no Frame"], color='green', linewidth=2)
                ax.fill_between(df_metricas["Frame"], df_metricas["Vacas no Frame"], alpha=0.3, color='green')
                ax.set_xlabel("Frame")
                ax.set_ylabel("Vacas")
                ax.set_title("Contagem por Frame")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
