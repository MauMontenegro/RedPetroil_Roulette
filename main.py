import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components
import time
import json

# Configuración de la página
st.set_page_config(page_title="Sorteo de Ganadores Red Petroil", page_icon="gota_red.png", layout="wide")

# Estilos CSS personalizados
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(45deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4);
    }
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
</style>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📁 Cargar archivo de participantes", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Load uploaded file
    df = pd.read_excel(uploaded_file)
    
    # Limpiar nombres de columnas (eliminar espacios)
    df.columns = df.columns.str.strip()
    
    # Validar que exista la columna requerida
    if 'Nombre' not in df.columns:
        st.error("❌ Falta la columna 'Nombre' en el archivo")
        st.warning("📋 El archivo debe contener la columna: 'Nombre'")
        st.stop()
    
    participants = df.to_dict(orient="records")
    st.success(f"✅ Archivo cargado: {len(participants)} participantes encontrados")
else:
    st.info("👆 Por favor carga un archivo Excel con los participantes")
    st.warning("📋 El archivo debe contener la columna: 'Nombre'")
    st.stop()  # Stop execution until file is uploaded

# Logo container with blue background
import base64

# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Logo container with blue background
logo_base64 = get_base64_image("logo_petroil.png")  # Make sure the filename is correct
gota_base64 = get_base64_image("gota_red.png")

st.markdown(f"""
<div style='background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 1rem;'>
    <img src='data:image/png;base64,{logo_base64}' 
         style='max-width: 300px; height: auto;'>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<h1 style='text-align: center; color: black; padding: 1rem;   
    border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 0px 0px rgba(0,0,0,0.3);'>
    SORTEO RED PETROIL
</h1>
""", unsafe_allow_html=True)

if len(participants) == 0:
    st.error("No hay participantes")
    st.stop()

# Estado
if 'winner_index' not in st.session_state:
    st.session_state.winner_index = None
    st.session_state.animation_running = False

# HTML para la animación de números
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        @import url('https://cdn.jsdelivr.net/gh/Gilroy-free/Gilroy-free@master/Gilroy-Light.css');
        @import url('https://cdn.jsdelivr.net/gh/Gilroy-free/Gilroy-free@master/Gilroy-ExtraBold.css');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Orbitron', monospace;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }}
        
        .container {{
            text-align: center;
            position: relative;
        }}
        
        .slot-machine {{
            background: linear-gradient(145deg, #0f0f23, #1a1a2e);
            border-radius: 30px;
            padding: 40px 60px;
            box-shadow: 
                0 20px 60px rgba(0,0,0,0.5),
                inset 0 -5px 10px rgba(0,0,0,0.3),
                inset 0 5px 10px rgba(255,255,255,0.1);
            position: relative;
            overflow: hidden;
            width: 600px; 
            margin: 0 auto;  
        }}
        
        .slot-machine::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                transparent, 
                rgba(255, 107, 107, 0.1),
                transparent 30%
            );
            animation: rotate 4s linear infinite;
        }}

        .slot-machine::after {{
            content: '';
            position: absolute;
            bottom: 10px;
            right: 10px;
            width: 50px;
            height: 50px;
            background-image: url('data:image/png;base64,{gota_base64}');
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.1;
            z-index: 0;
        }}
        
        @keyframes rotate {{
            100% {{ transform: rotate(360deg); }}
        }}
        
        .number-display {{
            font-size: 150px;
            font-weight: 900;
            line-height: 1;
            background: linear-gradient(45deg, #fbbf24, #f59e0b, #fbbf24);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
            position: relative;
            z-index: 1;
            text-shadow: 0 0 80px rgba(255, 107, 107, 0.5);
            min-width: 300px;
            display: inline-block;
        }}
        
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .rolling {{
            animation: roll 0.1s linear infinite;
        }}
        
        @keyframes roll {{
            0% {{ transform: translateY(0); opacity: 1; }}
            50% {{ transform: translateY(-2px); opacity: 0.8; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}
        
        .label {{
            font-size: 20px;
            color: #888;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }}
        
        .winner-info {{
            margin-top: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.5s ease;
        }}
        
        .winner-info.show {{
            opacity: 1;
            transform: translateY(0);
        }}
        
        .winner-name {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #fbbf24;
            text-shadow: 0 3px 6px rgba(0,0,0,0.5);
        }}
        
        .winner-details {{
            font-size: 18px;
            color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            font-family: 'Gilroy-Light', sans-serif;  /* or 'Gilroy-ExtraBold' */
        }}
        
        .particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 100;
        }}
        
        .particle {{
            position: absolute;
            width: 10px;
            height: 10px;
            background: #FFD93D;
            border-radius: 50%;
        }}
        
        .glow {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(255,107,107,0.3) 0%, transparent 70%);
            border-radius: 50%;
            opacity: 0;
            z-index: 0;
        }}
        
        .glow.active {{
            animation: pulse 2s ease-out infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 0; }}
            50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.5; }}
            100% {{ transform: translate(-50%, -50%) scale(1.5); opacity: 0; }}
        }}
        
        #startButton {{
            margin-top: 40px;
            padding: 15px 50px;
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(45deg, #fbbf24, #f59e0b);
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        }}
        
        #startButton:hover:not(:disabled) {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.5);
        }}
        
        #startButton:disabled {{
            background: #555;
            cursor: not-allowed;
            transform: scale(0.95);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="slot-machine">
                <div class="glow" id="glow"></div>
                <img src='data:image/png;base64,{logo_base64}' 
                    style='width: 120px; height: auto; margin-bottom: 20px; opacity: 0.8;'>
                <div class="label">Participante Número</div> 
                       
            <div class="number-display" id="numberDisplay">---</div>
        </div>
        
        <button id="startButton" onclick="startAnimation()">🎲 INICIAR SORTEO</button>
        
        <div class="winner-info" id="winnerInfo">
            <div class="winner-name" id="winnerName"></div>
            <div class="winner-details" id="winnerDetails"></div>
        </div>
    </div>
    
    <div class="particles" id="particles"></div>

    <script>
        const participants = {json.dumps(participants)};
        const totalParticipants = participants.length;
        let isAnimating = false;
        let animationId;
        let currentNumber = 1;
        let speed = 50;
        let targetNumber = null;
        
        function getRandomNumber() {{
            return Math.floor(Math.random() * totalParticipants) + 1;
        }}
        
        function updateDisplay(number) {{
            const display = document.getElementById('numberDisplay');
            display.textContent = String(number).padStart(3, '0');
        }}
        
        function createParticles() {{
            const container = document.getElementById('particles');
            container.innerHTML = '';
            
            const colors = ['#fbbf24', '#f59e0b', '#2563eb', '#3b82f6', '#60a5fa'];
            
            for (let i = 0; i < 100; i++) {{
                setTimeout(() => {{
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.left = '50%';
                    particle.style.top = '50%';
                    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                    
                    const angle = (Math.PI * 2 * i) / 50;
                    const velocity = 5 + Math.random() * 10;
                    const vx = Math.cos(angle) * velocity;
                    const vy = Math.sin(angle) * velocity;
                    
                    container.appendChild(particle);
                    
                    let x = 0;
                    let y = 0;
                    let opacity = 1;
                    
                    const moveParticle = () => {{
                        x += vx;
                        y += vy;
                        opacity -= 0.02;
                        
                        particle.style.transform = `translate(${{x}}px, ${{y}}px)`;
                        particle.style.opacity = opacity;
                        
                        if (opacity > 0) {{
                            requestAnimationFrame(moveParticle);
                        }} else {{
                            particle.remove();
                        }}
                    }};
                    
                    requestAnimationFrame(moveParticle);
                }}, i * 10);
            }}
        }}
        
        function startAnimation() {{
            if (isAnimating) return;
            
            isAnimating = true;
            document.getElementById('startButton').disabled = true;
            document.getElementById('numberDisplay').classList.add('rolling');
            document.getElementById('winnerInfo').classList.remove('show');
            document.getElementById('glow').classList.remove('active');
            
            // Seleccionar ganador aleatorio
            targetNumber = getRandomNumber();
            speed = 30;
            
            // Enviar el ganador a Streamlit
            window.parent.postMessage({{
                type: 'winner_selected',
                winnerIndex: targetNumber - 1
            }}, '*');
            
            animate();
        }}
        
        function animate() {{
            if (speed > 0) {{
                currentNumber = getRandomNumber();
                updateDisplay(currentNumber);
                
                // Desacelerar gradualmente
                if (speed > 10) {{
                    speed -= 1.5;
                }} else {{
                    speed -= 0.4;
                }}
                
                animationId = setTimeout(animate, 200 - speed);
            }} else {{
                // Mostrar el número ganador
                updateDisplay(targetNumber);
                document.getElementById('numberDisplay').classList.remove('rolling');
                document.getElementById('glow').classList.add('active');
                
                // Mostrar información del ganador
                setTimeout(() => {{
                    const winner = participants[targetNumber - 1];
                    document.getElementById('winnerName').textContent = '🏆 ' + winner.Nombre + ' 🏆';
                    document.getElementById('winnerDetails').textContent = 
                        '🎉 ¡Felicidades! 🎉';
                    document.getElementById('winnerInfo').classList.add('show');
                    
                    createParticles();
                    
                    // Reactivar botón después de 2 segundos
                    setTimeout(() => {{
                        document.getElementById('startButton').disabled = false;
                        isAnimating = false;
                    }}, 2000);
                }}, 500);
            }}
        }}
        
        // Inicializar display
        updateDisplay('---');
    </script>
</body>
</html>
"""

# Mostrar la máquina de números
components.html(html_code, height=700, scrolling=False)

# Información adicional en columnas
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,1,2])

with col1:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; 
                border-radius: 15px; text-align: center; backdrop-filter: blur(10px);'>
        <h3 style='color: #4ECDC4; margin: 0;'>📊 Total</h3>
        <p style='font-size: 36px; font-weight: bold; color: blue; margin: 10px 0;'>{}</p>
        <p style='color: #888; margin: 0;'>Participantes</p>
    </div>
    """.format(len(participants)), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; 
                border-radius: 15px; text-align: center; backdrop-filter: blur(10px);'>
        <h3 style='color: #FFD93D; margin: 0;'>🎲 Probabilidad</h3>
        <p style='font-size: 36px; font-weight: bold; color: blue; margin: 10px 0;'>{:.1f}%</p>
        <p style='color: #888; margin: 0;'>Por participante</p>
    </div>
    """.format(100/len(participants)), unsafe_allow_html=True)

# Lista de participantes
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📋 Ver lista completa de participantes", expanded=False):
    # Crear tabla estilizada
    for i, p in enumerate(participants):
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 15px; 
                    margin: 5px 0; border-radius: 10px; 
                    border-left: 4px solid {"#FFD93D" if i == st.session_state.winner_index else "#4ECDC4"};'>
            <div style='display: flex; align-items: center;'>
                <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                            width: 40px; height: 40px; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center;
                            font-weight: bold; margin-right: 15px;'>{i + 1}</div>
                <div style='flex: 1;'>
                    <strong style='font-size: 18px;'>{p['Nombre']}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 50px; padding: 25px; 
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); 
            border-radius: 20px; box-shadow: 0 5px 20px rgba(30, 58, 138, 0.2);'>
    <p style='color: #ffffff; margin: 0; font-weight: 500;'>
        🏆 Sistema de Sorteo Digital | Totalmente Aleatorio | 
        <span style='color: #fbbf24; font-weight: 600;'>Powered by Streamlit</span>
    </p>
</div>
""", unsafe_allow_html=True)