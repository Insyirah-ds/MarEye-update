import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="MAREYE Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
css_styles = """
<style>
    .main {
        background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);
    }
    .dashboard-header {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 50%, #004d66 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
        border: 2px solid #00d4ff;
    }
    .metric-card {
        background: linear-gradient(145deg, #1e2a3a 0%, #2a3441 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.25);
        margin-bottom: 20px;
        color: #ffffff;
    }
    .buoy-card {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00ff88;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        border: 1px solid #00ff88;
    }
    .detection-box {
        background: linear-gradient(145deg, #2a1f2e 0%, #3d2a40 100%);
        border: 2px solid #ff6b35;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
    }
    .camera-feed-container {
        background: linear-gradient(145deg, #1e2332 0%, #2a2f40 100%);
        border: 2px solid #00d4ff;
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0, 212, 255, 0.2);
    }
    .status-online {
        color: #00ff88;
        font-weight: bold;
        font-size: 18px;
    }
    .section-header {
        background: linear-gradient(90deg, #00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: bold;
        margin: 30px 0 20px 0;
    }
    .text-white-high-contrast {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        font-weight: 600;
    }
    .stButton button {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        border: 2px solid #00d4ff;
        color: #ffffff;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# --- Centered, Large Logo ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("thalasea-logo.png", width=320)

title_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 32px; color: #4CAF50; font-weight: bold;">
        SMART BUOY MONITORING SYSTEM
    </h1>
    <p style="color: #00d4ff; font-size: 18px;">Real-time Marine Monitoring • AI Debris Detection • GPS Tracking • Water Quality</p>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}
if 'gps_history' not in st.session_state:
    st.session_state.gps_history = []

# Function to generate random live data
def update_live_data():
    current_time = datetime.now()
    if not st.session_state.gps_history:
        base_lat = 1.4
        base_lng = 103.7
    else:
        last_pos = st.session_state.gps_history[-1]
        base_lat = last_pos['lat'] + random.uniform(-0.001, 0.001)
        base_lng = last_pos['lng'] + random.uniform(-0.001, 0.001)
    st.session_state.gps_history.append({
        'lat': base_lat,
        'lng': base_lng,
        'timestamp': current_time
    })
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    st.session_state.buoy_data = {
        'buoy_1': {
            'status': 'Active',
            'battery': random.randint(75, 95),
            'lat': base_lat,
            'lng': base_lng,
            'ph': round(random.uniform(6.5, 7.5), 1),
            'salinity': round(random.uniform(28, 35), 1),
            'turbidity': round(random.uniform(100, 150), 0),
            'temperature': round(random.uniform(24, 28), 1),
            'last_reading': current_time.strftime("%d-%m-%Y at %H:%M:%S"),
            'camera_status': 'Recording',
            'detections': [
                {'type': 'Plastic Bottle', 'time': '14:39:32', 'confidence': '94%', 'distance': '2.3m'},
                {'type': 'Food Container', 'time': '12:52:50', 'confidence': '87%', 'distance': '1.8m'},
                {'type': 'Fishing Net', 'time': '16:14:20', 'confidence': '91%', 'distance': '3.1m'},
                {'type': 'Plastic Bag', 'time': '10:30:05', 'confidence': '78%', 'distance': '1.5m'}
            ]
        }
    }

# Auto-refresh and manual refresh
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        update_live_data()
        st.session_state.last_update = datetime.now()
        st.rerun()
if (datetime.now() - st.session_state.last_update).seconds > 10:
    update_live_data()
    st.session_state.last_update = datetime.now()
    st.rerun()
if not st.session_state.buoy_data:
    update_live_data()
buoy_data = st.session_state.buoy_data['buoy_1']
st.markdown("---")

# ============= OVERVIEW METRICS (No Water Temp) =============
st.markdown('<div class="section-header">📊 SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)  # Only 4 columns now

with col1:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">BUOY STATUS</h4>
        <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">ACTIVE</h1>
        <p class="text-white-high-contrast">Battery: {buoy_data['battery']}%</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

with col2:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">DEBRIS DETECTED</h4>
        <h1 style="color: #ff6b35; font-size: 36px; margin: 5px 0;">{len(buoy_data['detections'])}</h1>
        <p class="text-white-high-contrast">Today's count</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

with col3:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">CAMERA</h4>
        <h1 style="color: #ffbe0b; font-size: 36px; margin: 5px 0;">●</h1>
        <p class="text-white-high-contrast">{buoy_data['camera_status']}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

with col4:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">GPS STATUS</h4>
        <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">📡</h1>
        <p class="text-white-high-contrast">Tracking</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# [Continue all other code, everything else below remains untouched (GPS, debris, analytics, footer, etc.)]
# ...[REMAINDER OF CODE AS PREVIOUSLY PROVIDED]...

# Footer
footer_html = f"""
<div style="text-align: center; padding: 20px; background: linear-gradient(145deg, #1a2332 0%, #243040 100%); border-radius: 15px; border: 1px solid #00d4ff;">
    <h3 style="color: #00d4ff; margin-bottom: 10px;">MAREYE Smart Buoy Monitoring System</h3>
    <p class="text-white-high-contrast">Real-time Marine Monitoring • AI Detection • GPS Tracking • Water Quality Analysis</p>
    <div style="display: flex; justify-content: center; gap: 30px; margin: 15px 0; flex-wrap: wrap;">
        <span class="text-white-high-contrast">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        <span>System: <span style="color: #00ff88; font-weight: bold;">ONLINE</span></span>
        <span class="text-white-high-contrast">Battery: {buoy_data['battery']}%</span>
    </div>
    <p style="color: #888; font-size: 12px; margin-top: 10px;">
        🌊 Protecting our oceans through advanced technology
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
