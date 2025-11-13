import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import random
import os

# ---- PAGE CONFIG & STYLES ----
st.set_page_config(
    page_title="MAREYE Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
css_styles = """
/* Enter your original CSS styles here for consistent formatting */
"""
st.markdown(css_styles, unsafe_allow_html=True)

# ---- LOGO IMAGE ----
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("thalasea-logo.png", width=320)

st.markdown("""
<div style="text-align:center;margin-bottom:20px;">
    <h1 style="font-size:32px;color:#4CAF50;font-weight:bold;">SMART BUOY MONITORING SYSTEM</h1>
    <p style="color:#00d4ff;font-size:18px;">Real-time Marine Monitoring • AI Debris Detection • GPS Tracking • Water Quality</p>
</div>
""", unsafe_allow_html=True)

# ---- IMAGE DISCOVERY ----
def get_image_files():
    exts = ['.jpg', '.jpeg']
    files = [f for f in os.listdir() if any(f.lower().endswith(ext) for ext in exts)]
    if not files:
        files = ["image.jpg"]
    return files
available_images = get_image_files()

# ---- DASHBOARD STATE ----
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}
if 'gps_history' not in st.session_state:
    st.session_state.gps_history = []

def update_live_data():
    current_time = datetime.now()
    base_lat = 5.9552
    base_lng = 116.0400
    if not st.session_state.gps_history:
        lat, lng = base_lat, base_lng
    else:
        last_pos = st.session_state.gps_history[-1]
        lat = last_pos['lat'] + random.uniform(-0.0005, 0.0005)
        lng = last_pos['lng'] + random.uniform(-0.0005, 0.0005)
    st.session_state.gps_history.append({
        'lat': lat,
        'lng': lng,
        'timestamp': current_time
    })
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    detections_list = [
        {'type': 'Plastic Bottle', 'time': '14:39:32', 'confidence': '94%', 'distance': '2.3m'},
        {'type': 'Food Container', 'time': '12:52:50', 'confidence': '87%', 'distance': '1.8m'},
        {'type': 'Fishing Net', 'time': '16:14:20', 'confidence': '91%', 'distance': '3.1m'},
        {'type': 'Plastic Bag', 'time': '10:30:05', 'confidence': '78%', 'distance': '1.5m'}
    ]
    for d in detections_list:
        d['image'] = random.choice(available_images) if available_images else None
        d['longitude'] = round(lng, 6)
        d['latitude'] = round(lat, 6)
    st.session_state.buoy_data = {
        'buoy_1': {
            'status': 'Active',
            'battery': random.randint(75, 95),
            'lat': lat,
            'lng': lng,
            'ph': round(random.uniform(7.8, 8.4), 2),
            'tds': random.randint(32000, 38000),
            'turbidity': round(random.uniform(5, 25), 1),
            'last_reading': current_time.strftime("%d-%m-%Y at %H:%M:%S"),
            'camera_status': 'Recording',
            'detections': detections_list
        }
    }

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

# ---- METRIC CARDS ----
st.markdown('<div class="section-header">📊 SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card"><h4 class="text-white-high-contrast">BUOY STATUS</h4>
    <h1 style="color:#00ff88;font-size:36px;margin:5px 0;">ACTIVE</h1></div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">DEBRIS DETECTED</h4>
    <h1 style="color:#ff6b35;font-size:36px;margin:5px 0;">{len(buoy_data['detections'])}</h1>
    <p class="text-white-high-contrast">Today's count</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">CAMERA</h4>
    <h1 style="color:#ffbe0b;font-size:36px;margin:5px 0;">●</h1>
    <p class="text-white-high-contrast">{buoy_data['camera_status']}</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card"><h4 class="text-white-high-contrast">GPS STATUS</h4>
    <h1 style="color:#00ff88;font-size:36px;margin:5px 0;">📡</h1>
    <p class="text-white-high-contrast">Tracking</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# ---- GPS SECTION ----
st.markdown('<div class="section-header">📡 GPS TRACKING & LOCATION</div>', unsafe_allow_html=True)
gps_status_html = f"""
<div class="buoy-card">
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
        <div><p class="text-white-high-contrast"><strong>Current Position:</strong></p><p style="color:#00d4ff;font-size:16px;font-weight:bold;">{buoy_data['lat']:.6f}, {buoy_data['lng']:.6f}</p></div>
        <div><p class="text-white-high-contrast"><strong>Movement:</strong></p><p class="status-online">🌊 Drifting</p></div>
        <div><p class="text-white-high-contrast"><strong>Signal:</strong></p><p style="color:#00ff88;font-size:16px;font-weight:bold;">Excellent</p></div>
        <div><p class="text-white-high-contrast"><strong>Last Update:</strong></p><p style="color:#ffbe0b;font-size:14px;">{datetime.now().strftime('%H:%M:%S')}</p></div>
    </div>
</div>
"""
st.markdown(gps_status_html, unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    if st.session_state.gps_history:
        df_map = pd.DataFrame([{'lat': buoy_data['lat'], 'lon': buoy_data['lng']}])
        st.map(df_map, zoom=14)
with col2:
    if len(st.session_state.gps_history) > 1:
        first_pos = st.session_state.gps_history[0]
        last_pos = st.session_state.gps_history[-1]
        lat_diff = abs(last_pos['lat'] - first_pos['lat'])
        lng_diff = abs(last_pos['lng'] - first_pos['lng'])
        approx_distance = ((lat_diff**2 + lng_diff**2) ** 0.5) * 111
        st.markdown(f"""
        <div class="camera-feed-container">
            <h4 style="color:#00d4ff;">Movement Stats</h4>
            <div><p style="color:#888;font-size:12px;">Total Distance</p>
            <p style="color:#00ff88;font-size:24px;font-weight:bold;">{approx_distance:.2f} km</p></div>
            <div><p style="color:#888;font-size:12px;">Data Points</p>
            <p style="color:#00d4ff;font-size:24px;font-weight:bold;">{len(st.session_state.gps_history)}</p></div>
            <div><p style="color:#888;font-size:12px;">Avg Speed</p>
            <p style="color:#ff6b35;font-size:24px;font-weight:bold;">{random.uniform(0.5,1.5):.2f} km/h</p></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("---")

# ---- WATER QUALITY GAUGES ----
st.markdown('<div class="section-header">💧 WATER QUALITY MONITORING</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">Water Quality Station</h4>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:15px;margin-top:10px;">
    <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
    <p class="text-white-high-contrast"><strong>Update Interval:</strong> 10 minutes</p></div>
</div>
""", unsafe_allow_html=True)
gauges_data = [
    {'name': 'pH', 'value': buoy_data['ph'], 'range': [0, 14], 'optimal': [7.8, 8.5], 'unit': ''},
    {'name': 'TDS', 'value': buoy_data['tds'], 'range': [0, 50000], 'optimal': [30000, 40000], 'unit': 'ppm'},
    {'name': 'TURBIDITY', 'value': buoy_data['turbidity'], 'range': [0, 100], 'optimal': [0, 50], 'unit': 'NTU'},
]
fig_gauges = go.Figure()
positions = [(0, 0.3, 0, 1), (0.35, 0.65, 0, 1), (0.7, 1, 0, 1)]
for gauge_data, pos in zip(gauges_data, positions):
    value = gauge_data['value']
    optimal = gauge_data['optimal']
    title = f"<b>{gauge_data['name']}</b>"
    if gauge_data['name'] == 'TDS':
        number_display = {'valueformat': 'd', 'suffix': ' ppm', 'font': {'color': 'white', 'size': 16}}
    else:
        number_display = {'suffix': f" {gauge_data['unit']}", 'font': {'color': 'white', 'size': 16}}
    if optimal[0] <= float(value) <= optimal[1]:
        color = '#00ff88'
    elif float(value) < optimal[0] * 0.8 or float(value) > optimal[1] * 1.2:
        color = '#ff6b35'
    else:
        color = '#ffbe0b'
    fig_gauges.add_trace(go.Indicator(
        mode="gauge+number",
        value=float(value),
        domain={'x': [pos[0], pos[1]], 'y': [pos[2], pos[3]]},
        title={'text': title, 'font': {'color': 'white', 'size': 14}},
        number=number_display,
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

# ---- DEBRIS DETECTION SECTION [UPDATED] ----
st.markdown('<div class="section-header">🎥 MARINE DEBRIS DETECTION</div>', unsafe_allow_html=True)
camera_status_html = f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">AI-Powered Camera System</h4>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:10px;">
        <div><p class="text-white-high-contrast"><strong>Status:</strong></p><p class="status-online">● {buoy_data['camera_status']}</p></div>
        <div><p class="text-white-high-contrast"><strong>Detections Today:</strong></p><p style="color:#ff6b35;font-size:20px;font-weight:bold;">{len(buoy_data['detections'])}</p></div>
        <div><p class="text-white-high-contrast"><strong>AI Confidence:</strong></p><p style="color:#00ff88;font-size:20px;font-weight:bold;">88%</p></div>
        <div><p class="text-white-high-contrast"><strong>Resolution:</strong></p><p style="color:#00d4ff;font-size:16px;">1080p HD</p></div>
    </div>
</div>
"""
st.markdown(camera_status_html, unsafe_allow_html=True)

st.markdown("**Recent Detections:**")
for i, detection in enumerate(buoy_data['detections']):
    card_key = f"view_{i}"
    st.markdown(
        f"""
        <div style='border:2px solid #ff6b35; border-radius:14px; margin-bottom:16px; padding:18px; background:rgba(20,10,30,0.8); position:relative;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-weight:bold; font-size:18px; color:#00d4ff;'>{detection['type']}</span>
                <span style='color:#00ff88; font-weight:bold; font-size:18px;'>Confidence: {detection['confidence']}</span>
            </div>
            <div style='display:flex; flex-wrap:wrap; align-items:center; margin-top:8px; gap:28px;'>
              <div>
                <span style='color:#ffbe0b;'>⏰</span> {detection['time']}<br>
                <span style='color:#ffbe0b;'>📍</span> {detection['distance']}<br>
                <span style='color:#ffbe0b;'>🌐</span> Latitude: {detection['latitude']}<br>
                <span style='color:#ffbe0b;'>🌐</span> Longitude: {detection['longitude']}
              </div>
              <div>
                {f"<img src='data:image/jpeg;base64,{open(detection['image'],'rb').read().hex()}' width='90' style='border-radius:8px;border:2px solid #00d4ff;box-shadow:0 2px 8px #0ff2;'/>" if detection['image'] and os.path.exists(detection['image']) else "<span style='color:#888;'>No image available.</span>"}
                <br>
                <form action='#'><button name='{card_key}' type='submit'>View</button></form>
              </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.session_state.get(card_key):
        if detection['image'] and os.path.exists(detection['image']):
            st.image(detection['image'], caption=detection['type'], use_column_width=True)
        else:
            st.write("No image found for this detection.")
st.markdown("---")

# ---- ANALYTICS SECTION ----
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
        x=dates, y=[7.8 + np.random.normal(0, 0.1) for _ in range(7)],
        mode='lines+markers', name='pH', line=dict(color='#00d4ff', width=2)
    ))
    fig_trends.add_trace(go.Scatter(
        x=dates, y=[35000 + np.random.normal(0, 400) for _ in range(7)],
        mode='lines+markers', name='TDS', line=dict(color='#ff6b35', width=2)
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

footer_html = f"""
<div style="text-align:center;padding:20px;background:linear-gradient(145deg,#1a2332 0%,#243040 100%);border-radius:15px; border:1px solid #00d4ff;">
    <h3 style="color:#00d4ff;margin-bottom:10px;">MAREYE Smart Buoy Monitoring System</h3>
    <p class="text-white-high-contrast">Real-time Marine Monitoring • AI Detection • GPS Tracking • Water Quality Analysis</p>
    <div style="display:flex;justify-content:center;gap:30px;margin:15px 0;flex-wrap:wrap;">
        <span class="text-white-high-contrast">Last Updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}</span>
        <span>System: <span style="color:#00ff88;font-weight:bold;">ONLINE</span></span>
        <span class="text-white-high-contrast">Battery: {buoy_data['battery']}%</span>
    </div>
    <p style="color:#888;font-size:12px;margin-top:10px;">🌊 Protecting our oceans through advanced technology</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
