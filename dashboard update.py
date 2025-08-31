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

# Custom CSS for dark theme with better contrast
st.markdown("""
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
    
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-image {
        width: 120px;
        height: 120px;
        border: 3px solid #00d4ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        background: rgba(0, 212, 255, 0.15);
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
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
    
    .drone-card {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00ff88;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        border: 1px solid #00ff88;
    }
    
    .drone-card-enhanced {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00ff88;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        border: 1px solid #00ff88;
        min-height: 400px;
    }
    
    .detection-box {
        background: linear-gradient(145deg, #2a1f2e 0%, #3d2a40 100%);
        border: 2px solid #ff6b35;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
    }
    
    .image-detection-container {
        background: linear-gradient(145deg, #1e2332 0%, #2a2f40 100%);
        border: 2px solid #00d4ff;
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0, 212, 255, 0.2);
    }
    
    .capture-image {
        border: 2px solid #00d4ff;
        border-radius: 8px;
        width: 100%;
        height: auto;
        box-shadow: 0 4px 8px rgba(0, 212, 255, 0.3);
    }
    
    .marbin-card {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff6b35;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        border: 1px solid #ff6b35;
    }
    
    .buoy-card {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffbe0b;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: #ffffff;
        border: 1px solid #ffbe0b;
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
    
    .neon-text {
        text-shadow: 0 0 15px #00d4ff, 0 0 25px #00d4ff;
        color: #ffffff;
        font-weight: bold;
    }
    
    .section-header {
        background: linear-gradient(90deg, #00ff88, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
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
    
    .water-quality-metric {
        background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 15px;
        border-radius: 12px;
        margin: 8px 0;
        border: 1px solid #00d4ff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        color: #ffffff;
    }
    
    .meter-container {
        position: relative;
        width: 100%;
        height: 20px;
        background: #1a2332;
        border-radius: 10px;
        border: 1px solid #00d4ff;
        margin: 8px 0;
    }
    
    .meter-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
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
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'drone_data' not in st.session_state:
    st.session_state.drone_data = {}
if 'marbin_data' not in st.session_state:
    st.session_state.marbin_data = {}
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}

# Function to generate random live data
def update_live_data():
    current_time = datetime.now()
    
    # Drone data with enhanced detection information
    st.session_state.drone_data = {
        'drone_1': {
            'status': 'Active',
            'battery': random.randint(65, 85),
            'area_covered': round(random.uniform(35, 40), 1),
            'lat': random.uniform(1.2, 1.6),
            'lng': random.uniform(103.6, 104.0),
            'detections': [
                {'type': 'Plastic', 'time': '14:39:32', 'severity': 'High', 'confidence': '94%', 'location': '1.414, 103.732'},
                {'type': 'Oil', 'time': '12:52:50', 'severity': 'Medium', 'confidence': '87%', 'location': '1.412, 103.729'},
                {'type': 'Plastic', 'time': '16:14:20', 'severity': 'High', 'confidence': '91%', 'location': '1.416, 103.735'},
                {'type': 'Oil', 'time': '10:30:05', 'severity': 'Low', 'confidence': '78%', 'location': '1.410, 103.728'}
            ],
            'image_detections': [
                {'title': 'Marine Debris Detection', 'image': 'picture 1 drone capture.jpeg', 'objects': ['Plastic bottles', 'Food containers', 'Fishing nets']},
                {'title': 'Oil Spill Monitoring', 'image': 'picture 2 drone capture.jpeg', 'objects': ['Oil slick', 'Surface contamination']},
                {'title': 'Waste Accumulation', 'image': 'picture 3 drone capture.jpeg', 'objects': ['Floating debris', 'Microplastics']}
            ]
        },
        'drone_2': {
            'status': 'Active',
            'battery': random.randint(70, 90),
            'area_covered': round(random.uniform(28, 35), 1),
            'lat': random.uniform(1.1, 1.5),
            'lng': random.uniform(103.5, 103.9),
            'detections': [],
            'image_detections': []
        },
        'drone_3': {
            'status': 'Returning',
            'battery': random.randint(15, 25),
            'area_covered': round(random.uniform(42, 48), 1),
            'lat': random.uniform(1.3, 1.7),
            'lng': random.uniform(103.7, 104.1),
            'detections': [],
            'image_detections': []
        }
    }
    
    # MarBin data
    st.session_state.marbin_data = {
        'marbin_1': {
            'oil_spill': random.randint(15, 25),
            'trash_collected': random.randint(65, 85),
            'battery': random.randint(90, 100),
            'status': 'Normal',
            'last_update': current_time.strftime("%H:%M:%S")
        },
        'marbin_2': {
            'oil_spill': random.randint(5, 15),
            'trash_collected': random.randint(85, 95),
            'battery': random.randint(25, 35),
            'status': 'Warning - Trash Full',
            'last_update': current_time.strftime("%H:%M:%S")
        },
        'marbin_3': {
            'oil_spill': random.randint(30, 45),
            'trash_collected': random.randint(40, 60),
            'battery': random.randint(75, 85),
            'status': 'Normal',
            'last_update': current_time.strftime("%H:%M:%S")
        }
    }
    
    # Buoy data
    st.session_state.buoy_data = {
        'buoy_1': {
            'ph': round(random.uniform(6.5, 7.5), 1),
            'salinity': round(random.uniform(28, 35), 1),
            'turbidity': round(random.uniform(100, 150), 0),
            'calcium': round(random.uniform(90, 110), 0),
            'magnesium': round(random.uniform(140, 160), 0),
            'do_levels': round(random.uniform(6, 8), 1),
            'ammonia': round(random.uniform(0.005, 0.015), 3),
            'temperature': round(random.uniform(24, 28), 1),
            'battery': random.randint(55, 65),
            'last_reading': current_time.strftime("%d-%m-%Y at %H:%M:%S")
        }
    }

# Function to create water quality meter
def create_water_quality_meter(parameter, value, min_val, max_val, optimal_range, unit):
    # Calculate percentage for the meter
    percentage = ((value - min_val) / (max_val - min_val)) * 100
    
    # Determine color based on optimal range
    if optimal_range[0] <= value <= optimal_range[1]:
        color = '#00ff88'  # Green for optimal
        status = 'Optimal'
    elif value < optimal_range[0] * 0.8 or value > optimal_range[1] * 1.2:
        color = '#ff6b35'  # Red for critical
        status = 'Critical'
    else:
        color = '#ffbe0b'  # Yellow for warning
        status = 'Warning'
    
    return f"""
    <div class="water-quality-metric">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h6 style="margin: 0; color: #00d4ff; font-weight: bold; font-size: 16px;">{parameter}</h6>
            <span style="color: {color}; font-weight: bold; font-size: 14px;">{status}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px 0;">
            <span style="font-size: 20px; font-weight: bold; color: #ffffff;">{value} {unit}</span>
        </div>
        <div class="meter-container">
            <div class="meter-fill" style="width: {percentage}%; background: linear-gradient(90deg, {color}, {color}80);"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888;">
            <span>{min_val} {unit}</span>
            <span>Optimal: {optimal_range[0]}-{optimal_range[1]} {unit}</span>
            <span>{max_val} {unit}</span>
        </div>
    </div>
    """

# Navigation
st.markdown("""
<div class="page-nav">
    <h3 style="color: #ffffff; margin: 0;">MAREYE Marine Monitoring System</h3>
</div>
""", unsafe_allow_html=True)

# Page navigation buttons
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("DASHBOARD", use_container_width=True):
        st.session_state.current_page = 'dashboard'
with col2:
    if st.button("DRONES", use_container_width=True):
        st.session_state.current_page = 'drones'
with col3:
    if st.button("MARBIN", use_container_width=True):
        st.session_state.current_page = 'marbin'
with col4:
    if st.button("SMART BUOY", use_container_width=True):
        st.session_state.current_page = 'buoy'
with col5:
    if st.button("AUTHORITIES", use_container_width=True):
        st.session_state.current_page = 'authorities'

# Auto-refresh data
if st.button("Refresh Data", use_container_width=True) or (datetime.now() - st.session_state.last_update).seconds > 10:
    update_live_data()
    st.session_state.last_update = datetime.now()
    st.rerun()

# DASHBOARD PAGE - Version 1 Simple
if st.session_state.current_page == 'dashboard':
    # Center everything
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Centered logo
        try:
            st.image("thalasea-logo.png", use_container_width=True)
        except:
            # Fallback centered text logo
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                           border-radius: 20px; padding: 3rem; margin-bottom: 2rem;">
                    <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 2rem;">
                        <h1 style="font-size: 4rem; color: #00BCD4; margin: 0; text-shadow: 2px 2px 10px rgba(0,0,0,0.3);">👁️</h1>
                        <h2 style="color: white; margin: 1rem 0 0 0; font-size: 1.5rem; letter-spacing: 3px;">MAREYE</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    
    # Dashboard title
    st.markdown("""
    <div style="text-align: center; margin-top: 15px;">
        <h1 style="font-size: 32px; color: #4CAF50; font-weight: bold;">
            MAREYE DASHBOARD
        </h1>
    </div>
    """, unsafe_allow_html=True)    # Start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START MONITORING", use_container_width=True, key="start_monitoring"):
            st.success("Monitoring System Activated!")
            update_live_data()

    st.markdown("---")

    # Overview cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">DRONES ACTIVE</h3>
            <h1 style="color: #00ff88; font-size: 48px; margin: 10px 0;">3</h1>
            <p class="text-white-high-contrast">All systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">MARBIN UNITS</h3>
            <h1 style="color: #ff6b35; font-size: 48px; margin: 10px 0;">3</h1>
            <p class="text-white-high-contrast">1 warning status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">SMART BUOYS</h3>
            <h1 style="color: #ffbe0b; font-size: 48px; margin: 10px 0;">1</h1>
            <p class="text-white-high-contrast">Monitoring water quality</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick status overview
    st.markdown('<div class="section-header">SYSTEM STATUS</div>', unsafe_allow_html=True)
    
    # Generate sample time series data for dashboard
    dates = pd.date_range(start='2024-08-21', end='2024-09-14', freq='D')
    detections = np.random.poisson(3, len(dates))  # Average 3 detections per day
    
    fig_overview = go.Figure()
    fig_overview.add_trace(go.Scatter(
        x=dates,
        y=detections,
        mode='lines+markers',
        name='Daily Detections',
        line=dict(color='#ff6b35', width=3),
        marker=dict(size=8, color='#ff6b35'),
        fill='tonexty',
        fillcolor='rgba(255, 107, 53, 0.2)'
    ))
    
    fig_overview.update_layout(
        title=dict(
            text="Marine Pollution Detections - Last 30 Days",
            x=0.5,
            font=dict(color='#00d4ff', size=24)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white', size=14),
        xaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Date",
            title_font=dict(color='#00d4ff', size=16)
        ),
        yaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Number of Detections",
            title_font=dict(color='#00d4ff', size=16)
        ),
        height=400
    )
    
    st.plotly_chart(fig_overview, use_container_width=True)

    # Statistics for dashboard
    st.markdown("---")
    st.markdown('<div class="section-header">DETAILED STATISTICS</div>', unsafe_allow_html=True)

    # Generate sample time series data
    dates = pd.date_range(start='2024-08-21', end='2024-09-14', freq='D')
    parameters = ['pH', 'Salinity', 'Turbidity', 'DO Levels', 'Ammonia', 'Calcium', 'Magnesium', 'Temperature']
    colors = ['#00d4ff', '#ff6b35', '#ffbe0b', '#00ff88', '#ff006e', '#8338ec', '#3a86ff', '#06ffa5']

    fig_stats = go.Figure()

    for param, color in zip(parameters, colors):
        # Generate realistic trend data
        base_values = {
            'pH': 7, 'Salinity': 32, 'Turbidity': 120, 'DO Levels': 7,
            'Ammonia': 0.01, 'Calcium': 100, 'Magnesium': 150, 'Temperature': 26
        }
        
        values = []
        base = base_values[param]
        for i in range(len(dates)):
            noise = np.random.normal(0, base * 0.1)  # 10% noise
            values.append(base + noise)
        
        fig_stats.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=param,
            line=dict(color=color, width=3),
            marker=dict(size=6),
            hovertemplate=f'<b>{param}</b><br>Date: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>'
        ))

    fig_stats.update_layout(
        title=dict(
            text="Water Quality Parameters - 30 Day Trend",
            x=0.5,
            font=dict(color='#00d4ff', size=24)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white', size=14),
        xaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Date",
            title_font=dict(color='#00d4ff', size=16)
        ),
        yaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Parameter Values",
            title_font=dict(color='#00d4ff', size=16)
        ),
        legend=dict(
            bgcolor='rgba(26, 35, 50, 0.8)',
            bordercolor='#00d4ff',
            borderwidth=2,
            font=dict(size=12, color='white')
        ),
        height=500
    )

    st.plotly_chart(fig_stats, use_container_width=True)

# ENHANCED DRONES PAGE
elif st.session_state.current_page == 'drones':
    st.markdown('<div class="section-header">DRONE MONITORING</div>', unsafe_allow_html=True)
    
    if not st.session_state.drone_data:
        update_live_data()
    
    for drone_name, data in st.session_state.drone_data.items():
        status_class = "status-online" if data['status'] == 'Active' else "status-warning"
        
        # Enhanced drone card with better layout
        st.markdown(f"""
        <div class="drone-card-enhanced">
            <h3 class="text-white-high-contrast">{drone_name.replace('_', ' ').title()}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div>
                    <p class="text-white-high-contrast"><strong>Status:</strong></p>
                    <p class="{status_class}">● {data['status']}</p>
                </div>
                <div>
                    <p class="text-white-high-contrast"><strong>Battery:</strong></p>
                    <p style="color: #00ff88; font-size: 20px; font-weight: bold;">{data['battery']}%</p>
                </div>
                <div>
                    <p class="text-white-high-contrast"><strong>Area Covered:</strong></p>
                    <p style="color: #00d4ff; font-size: 20px; font-weight: bold;">{data['area_covered']} km²</p>
                </div>
            </div>
            <p class="text-white-high-contrast"><strong>Location:</strong> {data['lat']:.3f}, {data['lng']:.3f}</p>
            <small style="color: #888;">Updates every 10 seconds</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced detections section for drone 1 with image detection details
        if drone_name == 'drone_1' and data['detections']:
            # Recent Detections with detailed information
            st.markdown("### Recent Detections")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Detection Log:**")
                for detection in data['detections'][:4]:
                    severity_color = {"High": "#ff6b35", "Medium": "#ffbe0b", "Low": "#00ff88"}
                    st.markdown(f"""
                    <div class="detection-box">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #00d4ff;">{detection['type']} Detected</strong>
                            <span style="color: {severity_color[detection['severity']]}; font-weight: bold;">{detection['severity']}</span>
                        </div>
                        <div style="margin: 8px 0;">
                            <span style="color: #ffffff;">Time: {detection['time']}</span><br>
                            <span style="color: #ffffff;">Confidence: {detection['confidence']}</span><br>
                            <span style="color: #ffffff;">Location: {detection['location']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Object Detection Summary:**")
                total_detections = len(data['detections'])
                plastic_count = len([d for d in data['detections'] if d['type'] == 'Plastic'])
                oil_count = len([d for d in data['detections'] if d['type'] == 'Oil'])
                
                st.markdown(f"""
                <div class="image-detection-container">
                    <div style="text-align: center;">
                        <h4 style="color: #00ff88; margin: 0;">Detection Statistics</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0;">
                            <div>
                                <p style="color: #ff6b35; font-size: 24px; font-weight: bold; margin: 5px 0;">{plastic_count}</p>
                                <p style="color: #ffffff; font-size: 14px;">Plastic Items</p>
                            </div>
                            <div>
                                <p style="color: #ffbe0b; font-size: 24px; font-weight: bold; margin: 5px 0;">{oil_count}</p>
                                <p style="color: #ffffff; font-size: 14px;">Oil Spills</p>
                            </div>
                        </div>
                        <div style="border-top: 1px solid #00d4ff; padding-top: 10px; margin-top: 10px;">
                            <p style="color: #00d4ff; font-size: 18px; font-weight: bold;">Total: {total_detections} Detections</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Image Detection Section with actual drone captures
            if data['image_detections']:
                st.markdown("### Live Drone Captures with AI Detection")
                
                # Create tabs or columns for different image detections
                img_col1, img_col2, img_col3 = st.columns(3)
                
                with img_col1:
                    img_detection = data['image_detections'][0]
                    st.markdown(f"""
                    <div class="image-detection-container">
                        <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.image(img_detection['image'], caption="Drone Capture 1", use_container_width=True)
                    except:
                        st.markdown("""
                        <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 40px; text-align: center; color: #00d4ff;">
                            📷 Drone Capture 1<br>
                            <small style="color: #888;">Image: picture 1 drone capture.jpeg</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("**Detected Objects:**")
                    for obj in img_detection['objects']:
                        st.markdown(f"• <span style='color: #ff6b35;'>{obj}</span>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with img_col2:
                    img_detection = data['image_detections'][1]
                    st.markdown(f"""
                    <div class="image-detection-container">
                        <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.image(img_detection['image'], caption="Drone Capture 2", use_container_width=True)
                    except:
                        st.markdown("""
                        <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 40px; text-align: center; color: #00d4ff;">
                            📷 Drone Capture 2<br>
                            <small style="color: #888;">Image: picture 2 drone capture.jpeg</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("**Detected Objects:**")
                    for obj in img_detection['objects']:
                        st.markdown(f"• <span style='color: #ff6b35;'>{obj}</span>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with img_col3:
                    img_detection = data['image_detections'][2]
                    st.markdown(f"""
                    <div class="image-detection-container">
                        <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.image(img_detection['image'], caption="Drone Capture 3", use_container_width=True)
                    except:
                        st.markdown("""
                        <div style="background: #1a2332; border: 2px solid #00d4ff; border-radius: 8px; padding: 40px; text-align: center; color: #00d4ff;">
                            📷 Drone Capture 3<br>
                            <small style="color: #888;">Image: picture 3 drone capture.jpeg</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("**Detected Objects:**")
                    for obj in img_detection['objects']:
                        st.markdown(f"• <span style='color: #ff6b35;'>{obj}</span>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

        # For other drones, show simple status
        elif drone_name != 'drone_1':
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Status:**")
                if data['status'] == 'Active':
                    st.success("✅ Patrol Mode - Scanning for marine pollution")
                else:
                    st.warning("🔋 Returning to base for battery recharge")
            
            with col2:
                st.markdown("**Coverage Area:**")
                st.info(f"📍 Currently monitoring {data['area_covered']} km² of marine area")

# MARBIN PAGE
elif st.session_state.current_page == 'marbin':