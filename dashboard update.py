import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
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
    
    .status-warning {
        color: #ffbe0b;
        font-weight: bold;
        font-size: 18px;
    }
    
    .status-critical {
        color: #ff6b35;
        font-weight: bold;
        font-size: 18px;
    }
    
    .section-header {
        background: linear-gradient(90deg, #00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    
    .page-nav {
        background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
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

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}
if 'gps_history' not in st.session_state:
    st.session_state.gps_history = []

# Function to generate random live data
def update_live_data():
    current_time = datetime.now()
    
    # Simulate GPS movement (drift with current)
    if not st.session_state.gps_history:
        # Initial position
        base_lat = 1.4
        base_lng = 103.7
    else:
        # Drift from last position
        last_pos = st.session_state.gps_history[-1]
        base_lat = last_pos['lat'] + random.uniform(-0.001, 0.001)
        base_lng = last_pos['lng'] + random.uniform(-0.001, 0.001)
    
    # Add to history
    st.session_state.gps_history.append({
        'lat': base_lat,
        'lng': base_lng,
        'timestamp': current_time
    })
    
    # Keep only last 50 positions
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    
    # Buoy data with water quality and camera detections
    st.session_state.buoy_data = {
        'buoy_1': {
            'status': 'Active',
            'battery': random.randint(75, 95),
            'lat': base_lat,
            'lng': base_lng,
            'ph': round(random.uniform(6.5, 7.5), 1),
            'salinity': round(random.uniform(28, 35), 1),
            'turbidity': round(random.uniform(100, 150), 0),
            'calcium': round(random.uniform(90, 110), 0),
            'magnesium': round(random.uniform(140, 160), 0),
            'do_levels': round(random.uniform(6, 8), 1),
            'ammonia': round(random.uniform(0.005, 0.015), 3),
            'temperature': round(random.uniform(24, 28), 1),
            'last_reading': current_time.strftime("%d-%m-%Y at %H:%M:%S"),
            'camera_status': 'Recording',
            'detections': [
                {'type': 'Plastic Bottle', 'time': '14:39:32', 'confidence': '94%', 'distance': '2.3m'},
                {'type': 'Food Container', 'time': '12:52:50', 'confidence': '87%', 'distance': '1.8m'},
                {'type': 'Fishing Net', 'time': '16:14:20', 'confidence': '91%', 'distance': '3.1m'},
                {'type': 'Plastic Bag', 'time': '10:30:05', 'confidence': '78%', 'distance': '1.5m'}
            ],
            'camera_captures': [
                {
                    'title': 'Marine Debris Detection',
                    'image': 'picture 1 drone capture.jpeg',
                    'objects': ['Plastic bottles', 'Food containers', 'Beverage cans'],
                    'count': 8,
                    'time': '14:39:32'
                },
                {
                    'title': 'Floating Waste',
                    'image': 'picture 2 drone capture.jpeg',
                    'objects': ['Fishing nets', 'Rope fragments', 'Styrofoam'],
                    'count': 5,
                    'time': '12:52:50'
                },
                {
                    'title': 'Microplastic Accumulation',
                    'image': 'picture 3 drone capture.jpeg',
                    'objects': ['Plastic fragments', 'Food wrappers', 'Bottle caps'],
                    'count': 12,
                    'time': '16:14:20'
                }
            ]
        }
    }

# Navigation
nav_html = """
<div class="page-nav">
    <h3 style="color: #ffffff; margin: 0;">MAREYE Smart Buoy Monitoring System</h3>
</div>
"""
st.markdown(nav_html, unsafe_allow_html=True)

# Page navigation buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("DASHBOARD", use_container_width=True):
        st.session_state.current_page = 'dashboard'
with col2:
    if st.button("WATER QUALITY", use_container_width=True):
        st.session_state.current_page = 'water_quality'
with col3:
    if st.button("DEBRIS DETECTION", use_container_width=True):
        st.session_state.current_page = 'debris'
with col4:
    if st.button("GPS TRACKING", use_container_width=True):
        st.session_state.current_page = 'gps'

# Auto-refresh data
if st.button("Refresh Data", use_container_width=True) or (datetime.now() - st.session_state.last_update).seconds > 10:
    update_live_data()
    st.session_state.last_update = datetime.now()
    st.rerun()

# DASHBOARD PAGE
if st.session_state.current_page == 'dashboard':
    # Logo section
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        try:
            st.image("thalasea-logo.png", use_container_width=True)
        except:
            logo_html = """
            <div style="text-align: center; padding: 2rem;">
                <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                           border-radius: 20px; padding: 3rem; margin-bottom: 2rem;">
                    <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 2rem;">
                        <h1 style="font-size: 4rem; color: #00BCD4; margin: 0;">🌊</h1>
                        <h2 style="color: white; margin: 1rem 0 0 0; font-size: 1.5rem; letter-spacing: 3px;">MAREYE</h2>
                    </div>
                </div>
            </div>
            """
            st.markdown(logo_html, unsafe_allow_html=True)
    
    # Dashboard title
    title_html = """
    <div style="text-align: center; margin-top: 15px;">
        <h1 style="font-size: 32px; color: #4CAF50; font-weight: bold;">
            SMART BUOY DASHBOARD
        </h1>
        <p style="color: #00d4ff; font-size: 18px;">Real-time Marine Monitoring with AI-Powered Debris Detection</p>
    </div>
    """
    st.markdown(title_html, unsafe_allow_html=True)
    
    # Start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START MONITORING", use_container_width=True, key="start_monitoring"):
            st.success("Smart Buoy System Activated!")
            update_live_data()

    st.markdown("---")

    if not st.session_state.buoy_data:
        update_live_data()
    
    buoy_data = st.session_state.buoy_data['buoy_1']

    # Overview cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        card1_html = f"""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">BUOY STATUS</h3>
            <h1 style="color: #00ff88; font-size: 48px; margin: 10px 0;">ACTIVE</h1>
            <p class="text-white-high-contrast">Battery: {buoy_data['battery']}%</p>
        </div>
        """
        st.markdown(card1_html, unsafe_allow_html=True)
    
    with col2:
        total_detections = len(buoy_data['detections'])
        card2_html = f"""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">DEBRIS DETECTED</h3>
            <h1 style="color: #ff6b35; font-size: 48px; margin: 10px 0;">{total_detections}</h1>
            <p class="text-white-high-contrast">Today's detections</p>
        </div>
        """
        st.markdown(card2_html, unsafe_allow_html=True)
    
    with col3:
        card3_html = f"""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">WATER TEMP</h3>
            <h1 style="color: #00d4ff; font-size: 48px; margin: 10px 0;">{buoy_data['temperature']}°C</h1>
            <p class="text-white-high-contrast">Current reading</p>
        </div>
        """
        st.markdown(card3_html, unsafe_allow_html=True)
    
    with col4:
        card4_html = f"""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">CAMERA STATUS</h3>
            <h1 style="color: #ffbe0b; font-size: 48px; margin: 10px 0;">●</h1>
            <p class="text-white-high-contrast">{buoy_data['camera_status']}</p>
        </div>
        """
        st.markdown(card4_html, unsafe_allow_html=True)
    
    # Quick map view
    st.markdown('<div class="section-header">CURRENT LOCATION</div>', unsafe_allow_html=True)
    
    if st.session_state.gps_history:
        # Create map with buoy position and trail
        df_map = pd.DataFrame([
            {'lat': buoy_data['lat'], 'lon': buoy_data['lng']}
        ])
        st.map(df_map, zoom=13)
    
    # Recent detections summary
    st.markdown('<div class="section-header">RECENT DETECTIONS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Detection timeline
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        detections = np.random.poisson(3, len(dates))
        
        fig_detections = go.Figure()
        fig_detections.add_trace(go.Scatter(
            x=dates,
            y=detections,
            mode='lines+markers',
            name='Daily Detections',
            line=dict(color='#ff6b35', width=3),
            marker=dict(size=8, color='#ff6b35'),
            fill='tonexty',
            fillcolor='rgba(255, 107, 53, 0.2)'
        ))
        
        fig_detections.update_layout(
            title=dict(
                text="Marine Debris Detection - Last 30 Days",
                x=0.5,
                font=dict(color='#00d4ff', size=20)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26, 35, 50, 0.8)',
            font=dict(color='white', size=12),
            xaxis=dict(
                gridcolor='rgba(0, 212, 255, 0.2)',
                title="Date"
            ),
            yaxis=dict(
                gridcolor='rgba(0, 212, 255, 0.2)',
                title="Number of Items"
            ),
            height=300
        )
        
        st.plotly_chart(fig_detections, use_container_width=True)
    
    with col2:
        # Detection type breakdown
        detection_types = {
            'Plastic': 45,
            'Fishing Gear': 25,
            'Food Containers': 20,
            'Other': 10
        }
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(detection_types.keys()),
            values=list(detection_types.values()),
            hole=0.4,
            marker=dict(colors=['#ff6b35', '#00d4ff', '#ffbe0b', '#00ff88'])
        )])
        
        fig_pie.update_layout(
            title=dict(
                text="Debris Types",
                x=0.5,
                font=dict(color='#00d4ff', size=18)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

# WATER QUALITY PAGE
elif st.session_state.current_page == 'water_quality':
    st.markdown('<div class="section-header">WATER QUALITY MONITORING</div>', unsafe_allow_html=True)
    
    if not st.session_state.buoy_data:
        update_live_data()
    
    buoy_data = st.session_state.buoy_data['buoy_1']
    
    buoy_card_html = f"""
    <div class="buoy-card">
        <h3 class="text-white-high-contrast">Smart Buoy - Water Quality Station</h3>
        <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
        <p class="text-white-high-contrast"><strong>Battery Level:</strong> <span style="color: #00ff88; font-size: 20px;">{buoy_data['battery']}%</span></p>
        <p class="text-white-high-contrast"><strong>Location:</strong> {buoy_data['lat']:.4f}, {buoy_data['lng']:.4f}</p>
        <small style="color: #888;">Updates every 10 minutes</small>
    </div>
    """
    st.markdown(buoy_card_html, unsafe_allow_html=True)
    
    # Create gauge meters
    st.markdown("### Water Quality Parameters", unsafe_allow_html=True)
    
    gauges_data = [
        {'name': 'pH', 'value': buoy_data['ph'], 'range': [0, 14], 'optimal': [6.5, 8.5], 'unit': ''},
        {'name': 'SALINITY', 'value': buoy_data['salinity'], 'range': [0, 50], 'optimal': [30, 35], 'unit': 'ppt'},
        {'name': 'TURBIDITY', 'value': buoy_data['turbidity'], 'range': [0, 300], 'optimal': [0, 200], 'unit': 'NTU'},
        {'name': 'CALCIUM', 'value': buoy_data['calcium'], 'range': [0, 300], 'optimal': [100, 200], 'unit': 'mg/L'},
        {'name': 'MAGNESIUM', 'value': buoy_data['magnesium'], 'range': [0, 200], 'optimal': [140, 160], 'unit': 'mg/L'},
        {'name': 'DO LEVELS', 'value': buoy_data['do_levels'], 'range': [0, 15], 'optimal': [6, 14], 'unit': 'mg/L'},
        {'name': 'AMMONIA', 'value': buoy_data['ammonia'], 'range': [0, 0.05], 'optimal': [0, 0.02], 'unit': 'mg/L'},
        {'name': 'TEMPERATURE', 'value': buoy_data['temperature'], 'range': [0, 40], 'optimal': [25, 30], 'unit': '°C'}
    ]
    
    fig_gauges = go.Figure()
    
    positions = [
        (0, 0.23, 0.5, 1), (0.27, 0.5, 0.5, 1), (0.53, 0.76, 0.5, 1), (0.79, 1, 0.5, 1),
        (0, 0.23, 0, 0.5), (0.27, 0.5, 0, 0.5), (0.53, 0.76, 0, 0.5), (0.79, 1, 0, 0.5)
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
                'bar': {'color': color, 'thickness': 0.8},
                'bgcolor': "rgba(26, 35, 50, 0.8)",
                'borderwidth': 2,
                'bordercolor': "#00d4ff",
                'steps': [
                    {'range': [gauge_data['range'][0], gauge_data['optimal'][0]], 'color': "rgba(255, 107, 53, 0.3)"},
                    {'range': [gauge_data['optimal'][0], gauge_data['optimal'][1]], 'color': "rgba(0, 255, 136, 0.3)"},
                    {'range': [gauge_data['optimal'][1], gauge_data['range'][1]], 'color': "rgba(255, 107, 53, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
    
    fig_gauges.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_gauges, use_container_width=True)
    
    # Historical trends
    st.markdown("### 7-Day Parameter Trends")
    
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    
    fig_trends = go.Figure()
    
    trend_params = ['pH', 'Salinity', 'Temperature', 'DO Levels']
    trend_colors = ['#00d4ff', '#ff6b35', '#ffbe0b', '#00ff88']
    
    for param, color in zip(trend_params, trend_colors):
        base_values = {'pH': 7, 'Salinity': 32, 'Temperature': 26, 'DO Levels': 7}
        base = base_values[param]
        
        values = [base + np.random.normal(0, base * 0.05) for _ in range(len(dates))]
        
        fig_trends.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=param,
            line=dict(color=color, width=3),
            marker=dict(size=8)
        ))
    
    fig_trends.update_layout(
        title=dict(text="Water Quality Trends", x=0.5, font=dict(color='#00d4ff', size=20)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Date"),
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Values"),
        legend=dict(bgcolor='rgba(26, 35, 50, 0.8)', bordercolor='#00d4ff', borderwidth=2),
        height=400
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

# DEBRIS DETECTION PAGE
elif st.session_state.current_page == 'debris':
    st.markdown('<div class="section-header">MARINE DEBRIS DETECTION</div>', unsafe_allow_html=True)
    
    if not st.session_state.buoy_data:
        update_live_data()
    
    buoy_data = st.session_state.buoy_data['buoy_1']
    
    # Camera status card
    camera_status_html = f"""
    <div class="buoy-card">
        <h3 class="text-white-high-contrast">🎥 CCTV Camera System</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
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
        </div>
    </div>
    """
    st.markdown(camera_status_html, unsafe_allow_html=True)
    
    # Detection Log
    st.markdown("### Real-Time Detection Log")
    
    col1, col2 = st.columns([1, 1])
    
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
                    <span style="color: #ffffff;">⏰ Time: {detection['time']}</span><br>
                    <span style="color: #ffffff;">📍 Distance: {detection['distance']}</span>
                </div>
            </div>
            """
            st.markdown(detection_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Detection Statistics:**")
        
        total_items = sum([cap['count'] for cap in buoy_data['camera_captures']])
        
        stats_html = f"""
        <div class="camera-feed-container">
            <div style="text-align: center;">
                <h4 style="color: #00ff88; margin: 0;">Today's Summary</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                    <div>
                        <p style="color: #00d4ff; font-size: 28px; font-weight: bold; margin: 5px 0;">{total_items}</p>
                        <p style="color: #ffffff; font-size: 14px;">Total Items</p>
                    </div>
                </div>
                <div style="border-top: 1px solid #00d4ff; padding-top: 10px; margin-top: 10px;">
                    <p style="color: #ffbe0b; font-size: 16px;">Average Confidence: 87.5%</p>
                </div>
            </div>
        </div>
        """
        st.markdown(stats_html, unsafe_allow_html=True)
    
    # Camera Captures with AI Detection
    st.markdown("### Live Camera Captures - AI Object Detection")
    
    img_col1, img_col2, img_col3 = st.columns(3)
    
    with img_col1:
        capture = buoy_data['camera_captures'][0]
        container_html = f"""
        <div class="camera-feed-container">
            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{capture['title']}</h5>
            <p style="color: #888; text-align: center; font-size: 12px;">Captured: {capture['time']}</p>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        try:
            st.image(capture['image'], caption=f"Camera Feed - {capture['time']}", use_container_width=True)
        except:
            placeholder_html = """
            <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 60px; text-align: center; color: #00d4ff;">
                📹 Live Camera Feed<br>
                <small style="color: #888;">Buoy CCTV Capture</small>
            </div>
            """
            st.markdown(placeholder_html, unsafe_allow_html=True)
        
        st.markdown(f"**🎯 Detected Objects ({capture['count']} items):**")
        for obj in capture['objects']:
            st.markdown(f"• <span style='color: #ff6b35; font-weight: bold;'>{obj}</span>", unsafe_allow_html=True)
    
    with img_col2:
        capture = buoy_data['camera_captures'][1]
        container_html = f"""
        <div class="camera-feed-container">
            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{capture['title']}</h5>
            <p style="color: #888; text-align: center; font-size: 12px;">Captured: {capture['time']}</p>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        try:
            st.image(capture['image'], caption=f"Camera Feed - {capture['time']}", use_container_width=True)
        except:
            placeholder_html = """
            <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 60px; text-align: center; color: #00d4ff;">
                📹 Live Camera Feed<br>
                <small style="color: #888;">Buoy CCTV Capture</small>
            </div>
            """
            st.markdown(placeholder_html, unsafe_allow_html=True)
        
        st.markdown(f"**🎯 Detected Objects ({capture['count']} items):**")
        for obj in capture['objects']:
            st.markdown(f"• <span style='color: #ff6b35; font-weight: bold;'>{obj}</span>", unsafe_allow_html=True)
    
    with img_col3:
        capture = buoy_data['camera_captures'][2]
        container_html = f"""
        <div class="camera-feed-container">
            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{capture['title']}</h5>
            <p style="color: #888; text-align: center; font-size: 12px;">Captured: {capture['time']}</p>
        </div>
        """
        st.markdown(container_html, unsafe_allow_html=True)
        
        try:
            st.image(capture['image'], caption=f"Camera Feed - {capture['time']}", use_container_width=True)
        except:
            placeholder_html = """
            <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 60px; text-align: center; color: #00d4ff;">
                📹 Live Camera Feed<br>
                <small style="color: #888;">Buoy CCTV Capture</small>
            </div>
            """
            st.markdown(placeholder_html, unsafe_allow_html=True)
        
        st.markdown(f"**🎯 Detected Objects ({capture['count']} items):**")
        for obj in capture['objects']:
            st.markdown(f"• <span style='color: #ff6b35; font-weight: bold;'>{obj}</span>", unsafe_allow_html=True)
    
    # Detection trends
    st.markdown("---")
    st.markdown("### Detection Trends - Last 30 Days")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    plastic_detections = np.random.poisson(2, len(dates))
    fishing_detections = np.random.poisson(1, len(dates))
    other_detections = np.random.poisson(1, len(dates))
    
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Bar(
        x=dates,
        y=plastic_detections,
        name='Plastic Items',
        marker_color='#ff6b35'
    ))
    
    fig_trends.add_trace(go.Bar(
        x=dates,
        y=fishing_detections,
        name='Fishing Gear',
        marker_color='#00d4ff'
    ))
    
    fig_trends.add_trace(go.Bar(
        x=dates,
        y=other_detections,
        name='Other Debris',
        marker_color='#ffbe0b'
    ))
    
    fig_trends.update_layout(
        title=dict(text="Daily Debris Detection by Type", x=0.5, font=dict(color='#00d4ff', size=20)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Date"),
        yaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Number of Items"),
        barmode='stack',
        legend=dict(bgcolor='rgba(26, 35, 50, 0.8)', bordercolor='#00d4ff', borderwidth=2),
        height=400
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

# GPS TRACKING PAGE
elif st.session_state.current_page == 'gps':
    st.markdown('<div class="section-header">GPS TRACKING & MOVEMENT</div>', unsafe_allow_html=True)
    
    if not st.session_state.buoy_data:
        update_live_data()
    
    buoy_data = st.session_state.buoy_data['buoy_1']
    
    # GPS status card
    gps_status_html = f"""
    <div class="buoy-card">
        <h3 class="text-white-high-contrast">📡 GPS Tracking System (SIM-Enabled)</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
            <div>
                <p class="text-white-high-contrast"><strong>Current Position:</strong></p>
                <p style="color: #00d4ff; font-size: 16px; font-weight: bold;">{buoy_data['lat']:.6f}, {buoy_data['lng']:.6f}</p>
            </div>
            <div>
                <p class="text-white-high-contrast"><strong>Movement Status:</strong></p>
                <p class="status-online">🌊 Drifting with Current</p>
            </div>
            <div>
                <p class="text-white-high-contrast"><strong>Signal Strength:</strong></p>
                <p style="color: #00ff88; font-size: 20px; font-weight: bold;">Excellent</p>
            </div>
        </div>
        <small style="color: #888;">GPS updates every 5 minutes via cellular network</small>
    </div>
    """
    st.markdown(gps_status_html, unsafe_allow_html=True)
    
    # Current location map
    st.markdown("### Real-Time Location")
    
    if st.session_state.gps_history:
        df_map = pd.DataFrame([
            {'lat': buoy_data['lat'], 'lon': buoy_data['lng']}
        ])
        st.map(df_map, zoom=14)
    
    st.markdown("---")
    
    # Movement history
    st.markdown("### Movement History & Drift Pattern")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(st.session_state.gps_history) > 1:
            # Create path plot
            lats = [pos['lat'] for pos in st.session_state.gps_history]
            lngs = [pos['lng'] for pos in st.session_state.gps_history]
            times = [pos['timestamp'].strftime('%H:%M:%S') for pos in st.session_state.gps_history]
            
            fig_path = go.Figure()
            
            # Add path line
            fig_path.add_trace(go.Scattergl(
                x=lngs,
                y=lats,
                mode='lines+markers',
                name='Buoy Path',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=8, color='#00d4ff'),
                text=times,
                hovertemplate='<b>Position</b><br>Lat: %{y:.6f}<br>Lng: %{x:.6f}<br>Time: %{text}<extra></extra>'
            ))
            
            # Mark current position
            fig_path.add_trace(go.Scattergl(
                x=[lngs[-1]],
                y=[lats[-1]],
                mode='markers+text',
                name='Current Position',
                marker=dict(size=20, color='#00ff88', symbol='star'),
                text=['NOW'],
                textposition='top center',
                textfont=dict(size=14, color='#00ff88')
            ))
            
            # Mark starting position
            fig_path.add_trace(go.Scattergl(
                x=[lngs[0]],
                y=[lats[0]],
                mode='markers+text',
                name='Start Position',
                marker=dict(size=15, color='#ff6b35', symbol='circle'),
                text=['START'],
                textposition='bottom center',
                textfont=dict(size=12, color='#ff6b35')
            ))
            
            fig_path.update_layout(
                title=dict(text="Buoy Drift Path", x=0.5, font=dict(color='#00d4ff', size=20)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26, 35, 50, 0.8)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Longitude"),
                yaxis=dict(gridcolor='rgba(0, 212, 255, 0.2)', title="Latitude"),
                showlegend=True,
                legend=dict(bgcolor='rgba(26, 35, 50, 0.8)', bordercolor='#00d4ff', borderwidth=2),
                height=500
            )
            
            st.plotly_chart(fig_path, use_container_width=True)
        else:
            st.info("Collecting GPS data... Movement history will appear after multiple readings.")
    
    with col2:
        st.markdown("**Movement Statistics:**")
        
        if len(st.session_state.gps_history) > 1:
            # Calculate approximate distance
            first_pos = st.session_state.gps_history[0]
            last_pos = st.session_state.gps_history[-1]
            
            lat_diff = abs(last_pos['lat'] - first_pos['lat'])
            lng_diff = abs(last_pos['lng'] - first_pos['lng'])
            approx_distance = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111  # Rough km conversion
            
            stats_html = f"""
            <div class="camera-feed-container">
                <div style="padding: 15px;">
                    <div style="margin-bottom: 15px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">Total Distance</p>
                        <p style="color: #00ff88; font-size: 24px; font-weight: bold; margin: 5px 0;">{approx_distance:.2f} km</p>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">Data Points</p>
                        <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 5px 0;">{len(st.session_state.gps_history)}</p>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">Current Direction</p>
                        <p style="color: #ffbe0b; font-size: 20px; font-weight: bold; margin: 5px 0;">{'Northeast' if lat_diff > 0 and lng_diff > 0 else 'Southeast' if lat_diff < 0 and lng_diff > 0 else 'Northwest' if lat_diff > 0 else 'Southwest'}</p>
                    </div>
                    <div style="border-top: 1px solid #00d4ff; padding-top: 10px;">
                        <p style="color: #888; font-size: 12px; margin: 0;">Average Speed</p>
                        <p style="color: #ff6b35; font-size: 18px; font-weight: bold; margin: 5px 0;">{random.uniform(0.5, 1.5):.2f} km/h</p>
                    </div>
                </div>
            </div>
            """
            st.markdown(stats_html, unsafe_allow_html=True)
        else:
            st.info("Movement statistics will be calculated once buoy starts drifting.")
        
        st.markdown("**Coverage Area:**")
        area_html = """
        <div class="detection-box">
            <p style="color: #ffffff; text-align: center; margin: 0;">
                <strong>Monitoring Radius:</strong><br>
                <span style="color: #00d4ff; font-size: 28px; font-weight: bold;">500m</span><br>
                <span style="color: #888; font-size: 12px;">from buoy position</span>
            </p>
        </div>
        """
        st.markdown(area_html, unsafe_allow_html=True)
    
    # Position history table
    st.markdown("### Recent Position History")
    
    if st.session_state.gps_history:
        recent_positions = st.session_state.gps_history[-10:]  # Last 10 positions
        
        df_history = pd.DataFrame([
            {
                'Timestamp': pos['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'Latitude': f"{pos['lat']:.6f}",
                'Longitude': f"{pos['lng']:.6f}"
            }
            for pos in reversed(recent_positions)
        ])
        
        st.dataframe(df_history, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
footer_html = f"""
<div style="text-align: center; padding: 25px; background: linear-gradient(145deg, #1a2332 0%, #243040 100%); border-radius: 15px; border: 1px solid #00d4ff;">
    <h3 style="color: #00d4ff;">MAREYE Smart Buoy System</h3>
    <p class="text-white-high-contrast">Real-time Marine Monitoring with AI-Powered Detection & GPS Tracking</p>
    <div style="display: flex; justify-content: center; gap: 30px; margin: 15px 0; flex-wrap: wrap;">
        <span class="text-white-high-contrast">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        <span>System: <span style="color: #00ff88; font-weight: bold;">ONLINE</span></span>
        <span class="text-white-high-contrast">Page: {st.session_state.current_page.replace('_', ' ').title()}</span>
    </div>
    <p style="color: #888; font-size: 12px; margin-top: 10px;">
        🌊 Protecting our oceans • 📹 AI Detection • 📡 GPS Tracking • 💧 Water Quality Monitoring
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
                        <p style="color: #ff6b35; font-size: 28px; font-weight: bold; margin: 5px 0;">{len(buoy_data['detections'])}</p>
                        <p style="color: #ffffff; font-size: 14px;">Unique Detections</p>
                    </div>
                    <div>
