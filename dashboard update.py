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
st.markdown("""
    <div style="text-align: center;">
        <img src="thalasea-logo.png" width="220">
    </div>
""", unsafe_allow_html=True)

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

# ============= OVERVIEW METRICS =============
st.markdown('<div class="section-header">📊 SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
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
        <h4 class="text-white-high-contrast">WATER TEMP</h4>
        <h1 style="color: #00d4ff; font-size: 36px; margin: 5px 0;">{buoy_data['temperature']}°C</h1>
        <p class="text-white-high-contrast">Current</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col4:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">CAMERA</h4>
        <h1 style="color: #ffbe0b; font-size: 36px; margin: 5px 0;">●</h1>
        <p class="text-white-high-contrast">{buoy_data['camera_status']}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col5:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">GPS STATUS</h4>
        <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">📡</h1>
        <p class="text-white-high-contrast">Tracking</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
st.markdown("---")

# ============= GPS TRACKING SECTION =============
st.markdown('<div class="section-header">📡 GPS TRACKING & LOCATION</div>', unsafe_allow_html=True)
gps_status_html = f"""
<div class="buoy-card">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 20px;">
        <div>
            <p class="text-white-high-contrast"><strong>Current Position:</strong></p>
            <p style="color: #00d4ff; font-size: 16px; font-weight: bold;">{buoy_data['lat']:.6f}, {buoy_data['lng']:.6f}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Movement:</strong></p>
            <p class="status-online">🌊 Drifting</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Signal:</strong></p>
            <p style="color: #00ff88; font-size: 16px; font-weight: bold;">Excellent</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Last Update:</strong></p>
            <p style="color: #ffbe0b; font-size: 14px;">{datetime.now().strftime('%H:%M:%S')}</p>
        </div>
    </div>
</div>
"""
st.markdown(gps_status_html, unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    if st.session_state.gps_history:
        df_map = pd.DataFrame([{'lat': buoy_data['lat'], 'lon': buoy_data['lng']}])
        st.map(df_map, zoom=13)
with col2:
    if len(st.session_state.gps_history) > 1:
        first_pos = st.session_state.gps_history[0]
        last_pos = st.session_state.gps_history[-1]
        lat_diff = abs(last_pos['lat'] - first_pos['lat'])
        lng_diff = abs(last_pos['lng'] - first_pos['lng'])
        approx_distance = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
        stats_html = f"""
        <div class="camera-feed-container">
            <h4 style="color: #00d4ff; text-align: center;">Movement Stats</h4>
            <div style="padding: 15px;">
                <div style="margin-bottom: 15px;">
                    <p style="color: #888; font-size: 12px; margin: 0;">Total Distance</p>
                    <p style="color: #00ff88; font-size: 24px; font-weight: bold; margin: 5px 0;">{approx_distance:.2f} km</p>
                </div>
                <div style="margin-bottom: 15px;">
                    <p style="color: #888; font-size: 12px; margin: 0;">Data Points</p>
                    <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 5px 0;">{len(st.session_state.gps_history)}</p>
                </div>
                <div>
                    <p style="color: #888; font-size: 12px; margin: 0;">Avg Speed</p>
                    <p style="color: #ff6b35; font-size: 24px; font-weight: bold; margin: 5px 0;">{random.uniform(0.5, 1.5):.2f} km/h</p>
                </div>
            </div>
        </div>
        """
        st.markdown(stats_html, unsafe_allow_html=True)
st.markdown("---")

# ============= WATER QUALITY SECTION =============
st.markdown('<div class="section-header">💧 WATER QUALITY MONITORING</div>', unsafe_allow_html=True)
buoy_info_html = f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">Water Quality Station</h4>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px;">
        <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
        <p class="text-white-high-contrast"><strong>Battery:</strong> <span style="color: #00ff88;">{buoy_data['battery']}%</span></p>
        <p class="text-white-high-contrast"><strong>Update Interval:</strong> 10 minutes</p>
    </div>
</div>
"""
st.markdown(buoy_info_html, unsafe_allow_html=True)
gauges_data = [
    {'name': 'pH', 'value': buoy_data['ph'], 'range': [0, 14], 'optimal': [6.5, 8.5], 'unit': ''},
    {'name': 'SALINITY', 'value': buoy_data['salinity'], 'range': [0, 50], 'optimal': [30, 35], 'unit': 'ppt'},
    {'name': 'TURBIDITY', 'value': buoy_data['turbidity'], 'range': [0, 300], 'optimal': [0, 200], 'unit': 'NTU'},
    {'name': 'TEMPERATURE', 'value': buoy_data['temperature'], 'range': [0, 40], 'optimal': [25, 30], 'unit': '°C'}
]
fig_gauges = go.Figure()
positions = [
    (0, 0.23, 0, 1), (0.27, 0.5, 0, 1), (0.53, 0.76, 0, 1), (0.79, 1, 0, 1)
]
for gauge_data, pos in zip(gauges_data, positions):
    value = gauge_data['value']
    optimal = gauge_data['optimal']
    if optimal[0] <= value <= optimal[1]:
        color = '#00ff88'
    elif value < optimal[0] * 0.8 or value > optimal[1] * 1.2:
        color = '#ff6b35'
    else:
        color = '#ffbe0b'
    fig_gauges.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [pos[0], pos[1]], 'y': [pos[2], pos[3]]},
        title={'text': f"<b>{gauge_data['name']}</b>", 'font': {'color': 'white', 'size': 14}},
        number={'suffix': f" {gauge_data['unit']}", 'font': {'color': 'white', 'size': 16}},
        gauge={
            'axis': {'range': [None, gauge_data['range'][1]], 'tickcolor': 'white', 'tickfont': {'color': 'white', 'size': 10}},
            'bar': {'color': color, 'thickness': 0.7},
            'bgcolor': "rgba(26, 35, 50, 0.8)",
            'borderwidth': 2,
            'bordercolor': "#00d4ff",
            'steps': [
                {'range': [gauge_data['range'][0], gauge_data['optimal'][0]], 'color': "rgba(255, 107, 53, 0.3)"},
                {'range': [gauge_data['optimal'][0], gauge_data['optimal'][1]], 'color': "rgba(0, 255, 136, 0.3)"},
                {'range': [gauge_data['optimal'][1], gauge_data['range'][1]], 'color': "rgba(255, 107, 53, 0.3)"}
            ]
        }
    ))
fig_gauges.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    font={'color': "white"},
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False
)
st.plotly_chart(fig_gauges, use_container_width=True)
st.markdown("---")

# ============= DEBRIS DETECTION SECTION =============
st.markdown('<div class="section-header">🎥 MARINE DEBRIS DETECTION</div>', unsafe_allow_html=True)
camera_status_html = f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">AI-Powered Camera System</h4>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 10px;">
        <div>
            <p class="text-white-high-contrast"><strong>Status:</strong></p>
            <p class="status-online">● {buoy_data['camera_status']}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Detections Today:</strong></p>
            <p style="color: #ff6b35; font-size: 20px; font-weight: bold;">{len(buoy_data['detections'])}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>AI Confidence:</strong></p>
            <p style="color: #00ff88; font-size: 20px; font-weight: bold;">88%</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Resolution:</strong></p>
            <p style="color: #00d4ff; font-size: 16px;">1080p HD</p>
        </div>
    </div>
</div>
"""
st.markdown(camera_status_html, unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("**Recent Detections:**")
    for detection in buoy_data['detections']:
        detection_html = f"""
        <div class="detection-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #00d4ff; font-size: 16px;">{detection['type']}</strong>
                <span style="color: #00ff88; font-weight: bold;">Confidence: {detection['confidence']}</span>
            </div>
            <div style="margin: 8px 0;">
                <span style="color: #ffffff;">⏰ {detection['time']}</span>
                <span style="color: #ffffff; margin-left: 20px;">📍 {detection['distance']}</span>
            </div>
        </div>
        """
        st.markdown(detection_html, unsafe_allow_html=True)
with col2:
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    detections = np.random.poisson(3, len(dates))
    fig_detections = go.Figure()
    fig_detections.add_trace(go.Bar(
        x=dates,
        y=detections,
        marker_color='#ff6b35',
        name='Daily Detections'
    ))
    fig_detections.update_layout(
        title=dict(text="7-Day Detection Trend", font=dict(color='#00d4ff', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white', size=10),
        xaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title=""),
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Items"),
        height=300,
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_detections, use_container_width=True)
st.markdown("---")

# ============= ANALYTICS SECTION =============
st.markdown('<div class="section-header">📈 ANALYTICS & TRENDS</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    detection_types = {'Plastic': 45, 'Fishing Gear': 25, 'Food Containers': 20, 'Other': 10}
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(detection_types.keys()),
        values=list(detection_types.values()),
        hole=0.4,
        marker=dict(colors=['#ff6b35', '#00d4ff', '#ffbe0b', '#00ff88'])
    )])
    fig_pie.update_layout(
        title=dict(text="Debris Type Distribution", x=0.5, font=dict(color='#00d4ff', size=18)),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=350,
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=dates, y=[7 + np.random.normal(0, 0.2) for _ in range(7)],
        mode='lines+markers', name='pH', line=dict(color='#00d4ff', width=2)
    ))
    fig_trends.add_trace(go.Scatter(
        x=dates, y=[32 + np.random.normal(0, 1) for _ in range(7)],
        mode='lines+markers', name='Salinity', line=dict(color='#ff6b35', width=2)
    ))
    fig_trends.add_trace(go.Scatter(
        x=dates, y=[26 + np.random.normal(0, 0.5) for _ in range(7)],
        mode='lines+markers', name='Temp', line=dict(color='#ffbe0b', width=2)
    ))
    fig_trends.update_layout(
        title=dict(text="7-Day Water Quality Trends", x=0.5, font=dict(color='#00d4ff', size=18)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)'),
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)'),
        height=350
    )
    st.plotly_chart(fig_trends, use_container_width=True)
st.markdown("---")

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
