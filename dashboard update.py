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
st.markdown(, unsafe_allow_html=True)
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
    """, unsafe_allow_html=True)
    
    # Start button
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
    
    # Initialize view details state for each drone if not exists
    for drone_name in st.session_state.drone_data.keys():
        if f'view_details_{drone_name}' not in st.session_state:
            st.session_state[f'view_details_{drone_name}'] = False
    
    for drone_name, data in st.session_state.drone_data.items():
        status_class = "status-online" if data['status'] == 'Active' else "status-warning"
        
        # Enhanced drone card with better layout
        st.markdown(f"""
        <div class="drone-card">
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
        
        # View Details Button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button(f"View Details", key=f"details_{drone_name}", use_container_width=True):
                st.session_state[f'view_details_{drone_name}'] = not st.session_state[f'view_details_{drone_name}']
        
        # Show details if button was clicked
        if st.session_state[f'view_details_{drone_name}']:
            # For drone 1 with detections, show enhanced details
            if drone_name == 'drone_1' and data['detections']:
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
                    
                    # Create columns for different image detections
                    img_col1, img_col2, img_col3 = st.columns(3)
                    
                    with img_col1:
                        img_detection = data['image_detections'][0]
                        st.markdown(f"""
                        <div class="image-detection-container">
                            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                        </div>
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
                    
                    with img_col2:
                        img_detection = data['image_detections'][1]
                        st.markdown(f"""
                        <div class="image-detection-container">
                            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                        </div>
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
                    
                    with img_col3:
                        img_detection = data['image_detections'][2]
                        st.markdown(f"""
                        <div class="image-detection-container">
                            <h5 style="color: #00d4ff; text-align: center; margin-bottom: 10px;">{img_detection['title']}</h5>
                        </div>
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

            # For other drones, show simple status when details are viewed
            else:
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
                
                # Show placeholder for no detections
                if drone_name != 'drone_1':
                    st.markdown("**Recent Activity:**")
                    st.info("No recent detections - Area clear of pollution")
        
        st.markdown("---")

# MARBIN PAGE
elif st.session_state.current_page == 'marbin':
    st.markdown('<div class="section-header">MARBIN MONITORING</div>', unsafe_allow_html=True)
    
    if not st.session_state.marbin_data:
        update_live_data()
    
    # Location radar
    fig_location = go.Figure()
    
    # Add circular grid
    theta = np.linspace(0, 2*np.pi, 100)
    for r in [0.3, 0.6, 1.0]:
        fig_location.add_trace(go.Scatterpolar(
            r=[r]*len(theta),
            theta=theta*180/np.pi,
            mode='lines',
            line=dict(color='rgba(0, 212, 255, 0.4)', width=2),
            showlegend=False
        ))
    
    # Add MarBin positions
    positions = [
        {'name': 'MarBin 1', 'r': 0.8, 'theta': 45, 'status': 'Normal'},
        {'name': 'MarBin 2', 'r': 0.6, 'theta': 180, 'status': 'Warning'},
        {'name': 'MarBin 3', 'r': 0.9, 'theta': 300, 'status': 'Normal'}
    ]
    
    for pos in positions:
        color = '#00ff88' if pos['status'] == 'Normal' else '#ff6b35'
        fig_location.add_trace(go.Scatterpolar(
            r=[pos['r']],
            theta=[pos['theta']],
            mode='markers+text',
            marker=dict(size=20, color=color),
            text=[pos['name']],
            textposition="top center",
            name=pos['name'],
            textfont=dict(size=14, color='white')
        ))
    
    fig_location.update_layout(
        polar=dict(
            bgcolor='rgba(26, 35, 50, 0.8)',
            radialaxis=dict(visible=False, range=[0, 1]),
            angularaxis=dict(visible=False)
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        title=dict(text="MarBin Locations", x=0.5, font=dict(color='#00d4ff', size=20))
    )
    
    st.plotly_chart(fig_location, use_container_width=True)
    
    # MarBin status cards
    for i, (marbin_name, data) in enumerate(st.session_state.marbin_data.items(), 1):
        status_class = "status-online" if data['status'] == 'Normal' else "status-critical"
        
        st.markdown(f"""
        <div class="marbin-card">
            <h3 class="text-white-high-contrast">MarBin {i}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                <div>
                    <p class="text-white-high-contrast"><strong>Oil Spill Detection:</strong></p>
                    <p style="color: #ff6b35; font-size: 24px; font-weight: bold;">{data['oil_spill']}%</p>
                    <p class="text-white-high-contrast"><strong>Trash Collected:</strong></p>
                    <p style="color: #00ff88; font-size: 24px; font-weight: bold;">{data['trash_collected']}%</p>
                </div>
                <div>
                    <p class="text-white-high-contrast"><strong>Battery Level:</strong></p>
                    <p style="color: #00d4ff; font-size: 24px; font-weight: bold;">{data['battery']}%</p>
                    <p class="text-white-high-contrast"><strong>Status:</strong></p>
                    <p class="{status_class}">{data['status']}</p>
                </div>
            </div>
            <small style="color: #888;">Last Update: {data['last_update']}</small>
        </div>
        """, unsafe_allow_html=True)

# SMART BUOY PAGE
elif st.session_state.current_page == 'buoy':
    st.markdown('<div class="section-header">SMART BUOY MONITORING</div>', unsafe_allow_html=True)
    
    if not st.session_state.buoy_data:
        update_live_data()
    
    buoy_data = st.session_state.buoy_data['buoy_1']
    
    st.markdown(f"""
    <div class="buoy-card">
        <h3 class="text-white-high-contrast">Smart Buoy 1</h3>
        <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
        <p class="text-white-high-contrast"><strong>Battery Level:</strong> <span style="color: #00ff88; font-size: 20px;">{buoy_data['battery']}%</span></p>
        <small style="color: #888;">Updates every 10 minutes</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Create gauge meters using Plotly
    st.markdown("### Water Quality Parameters", unsafe_allow_html=True)
    
    # Define gauge parameters
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
    
    # Create 4x2 grid of gauges
    fig_gauges = go.Figure()
    
    # Define positions for 4x2 grid
    positions = [
        (0, 0.23, 0.5, 1),      # Top row, column 1
        (0.27, 0.5, 0.5, 1),    # Top row, column 2
        (0.53, 0.76, 0.5, 1),   # Top row, column 3
        (0.79, 1, 0.5, 1),      # Top row, column 4
        (0, 0.23, 0, 0.5),      # Bottom row, column 1
        (0.27, 0.5, 0, 0.5),    # Bottom row, column 2
        (0.53, 0.76, 0, 0.5),   # Bottom row, column 3
        (0.79, 1, 0, 0.5)       # Bottom row, column 4
    ]
    
    for i, (gauge_data, pos) in enumerate(zip(gauges_data, positions)):
        # Determine color based on optimal range
        value = gauge_data['value']
        optimal = gauge_data['optimal']
        
        if optimal[0] <= value <= optimal[1]:
            color = '#00ff88'  # Green for optimal
        elif value < optimal[0] * 0.8 or value > optimal[1] * 1.2:
            color = '#ff6b35'  # Red for critical
        else:
            color = '#ffbe0b'  # Yellow for warning
        
        fig_gauges.add_trace(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [pos[0], pos[1]], 'y': [pos[2], pos[3]]},
            title = {'text': f"<b>{gauge_data['name']}</b>", 'font': {'color': 'white', 'size': 14}},
            number = {'suffix': f" {gauge_data['unit']}", 'font': {'color': 'white', 'size': 16}},
            gauge = {
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
        font={'color': "white", 'family': "Arial"},
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_gauges, use_container_width=True)
    
    # Historical Trends section
    st.markdown("### Historical Trends")
    
    # Generate sample historical data for the past 7 days
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    
    fig_trends = go.Figure()
    
    # Add trend lines for key parameters
    trend_params = ['pH', 'Salinity', 'Temperature', 'DO Levels']
    trend_colors = ['#00d4ff', '#ff6b35', '#ffbe0b', '#00ff88']
    
    for param, color in zip(trend_params, trend_colors):
        # Generate realistic trend data
        base_values = {'pH': 7, 'Salinity': 32, 'Temperature': 26, 'DO Levels': 7}
        base = base_values[param]
        
        values = []
        for i in range(len(dates)):
            noise = np.random.normal(0, base * 0.05)  # 5% noise
            values.append(base + noise)
        
        fig_trends.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=param,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate=f'<b>{param}</b><br>Date: %{{x}}<br>Value: %{{y:.2f}}<extra></extra>'
        ))
    
    fig_trends.update_layout(
        title=dict(
            text="7-Day Parameter Trends",
            x=0.5,
            font=dict(color='#00d4ff', size=20)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white', size=14),
        xaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Date",
            title_font=dict(color='#00d4ff', size=14)
        ),
        yaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.2)',
            title="Parameter Values",
            title_font=dict(color='#00d4ff', size=14)
        ),
        legend=dict(
            bgcolor='rgba(26, 35, 50, 0.8)',
            bordercolor='#00d4ff',
            borderwidth=2,
            font=dict(size=12, color='white')
        ),
        height=400
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

# AUTHORITIES PAGE
elif st.session_state.current_page == 'authorities':
    st.markdown('<div class="section-header">REPORT TO AUTHORITIES</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">Report Incident / Complaint</h3>
            <p class="text-white-high-contrast">Please provide detailed information about the incident</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Report form
        report_text = st.text_area("Write your report here:", height=200, placeholder="Describe the incident or complaint in detail...")
        
        col_form1, col_form2 = st.columns([1, 1])
        with col_form1:
            uploaded_file = st.file_uploader("Add Media Evidence", type=['jpg', 'png', 'mp4', 'pdf'])
        with col_form2:
            report_type = st.selectbox("Report Type", ["Marine Pollution", "Equipment Malfunction", "Emergency", "General Complaint"])
        
        if st.button("SUBMIT REPORT", use_container_width=True):
            if report_text:
                st.success("Report submitted successfully!")
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, #1e2936 0%, #2a3441 100%); padding: 25px; border-radius: 15px; border: 2px solid #00ff88; margin-top: 20px;">
                    <h3 style="color: #00ff88; text-align: center;">Thank You for Your Report</h3>
                    <p class="text-white-high-contrast" style="text-align: center;">We will review your report and take appropriate action.</p>
                    <p class="text-white-high-contrast" style="text-align: center;">Your contribution helps us protect our marine environment.</p>
                    <div style="text-align: center; font-size: 48px; margin: 20px 0;">
                        Marine Protection
                    </div>
                    <div style="background: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #00d4ff;">
                        <h4 style="color: #00d4ff; text-align: center;">Report ID: MR-{datetime.now().strftime("%Y%m%d%H%M%S")}</h4>
                        <p class="text-white-high-contrast" style="text-align: center;">Reference this ID for follow-up inquiries</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please enter your report before submitting.")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">Emergency Contacts</h3>
            <div style="margin: 20px 0;">
                <h4 style="color: #ff6b35;">Emergency Hotline</h4>
                <p class="text-white-high-contrast" style="font-size: 24px; font-weight: bold;">999</p>
            </div>
            <div style="margin: 20px 0;">
                <h4 style="color: #00d4ff;">Marine Department</h4>
                <p class="text-white-high-contrast">+60-3-8000-8000</p>
            </div>
            <div style="margin: 20px 0;">
                <h4 style="color: #00ff88;">Local Authorities</h4>
                <p class="text-white-high-contrast">+60-7-2XX-XXXX</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3 class="text-white-high-contrast">Reporting Guidelines</h3>
            <ul class="text-white-high-contrast">
                <li>Include location coordinates if possible</li>
                <li>Add photos or videos as evidence</li>
                <li>Describe the severity of the incident</li>
                <li>Mention any immediate dangers</li>
                <li>Provide your contact information</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 25px; background: linear-gradient(145deg, #1a2332 0%, #243040 100%); border-radius: 15px; border: 1px solid #00d4ff;">
    <h3 style="color: #00d4ff;">MAREYE Marine Pollution Detection System</h3>
    <p class="text-white-high-contrast">Protecting our oceans with advanced monitoring technology</p>
    <div style="display: flex; justify-content: center; gap: 30px; margin: 15px 0;">
        <span class="text-white-high-contrast">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        <span>Status: <span style="color: #00ff88; font-weight: bold;">ONLINE</span></span>
        <span class="text-white-high-contrast">Current Page: {st.session_state.current_page.title()}</span>
    </div>
</div>
"""
