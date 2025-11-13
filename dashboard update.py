import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- PAGE CONFIG & CUSTOM STYLE ---
st.set_page_config(
    page_title="MAREYE Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
custom_css = """
<style>
    .main {background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);}
    .stApp {background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);}
    .metric-card {background: linear-gradient(145deg, #1e2a3a 0%, #2a3441 100%);
        padding: 25px;border-radius: 15px;border: 2px solid #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.25);margin-bottom: 20px;color: #ffffff;}
    .buoy-card {background: linear-gradient(145deg, #1a2332 0%, #243040 100%);
        padding: 20px;border-radius: 15px;border-left: 5px solid #00ff88;margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);color: #ffffff;border: 1px solid #00ff88;}
    .status-online {color: #00ff88;font-weight: bold;font-size: 18px;}
    .section-header {background: linear-gradient(90deg, #00ff88, #00d4ff);-webkit-background-clip: text;
        -webkit-text-fill-color: transparent;font-size: 28px;font-weight: bold;
        margin: 30px 0 20px 0;}
    .text-white-high-contrast {color: #ffffff !important;text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);font-weight: 600;}
    .stButton button {background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
        border: 2px solid #00d4ff;color: #ffffff;font-weight: bold;box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;}
    .stButton button:hover {box-shadow: 0 0 25px rgba(0, 212, 255, 0.5);transform: translateY(-2px);}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- HEADER LOGO + TITLE ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("image.jpg", width=110)  # Use your logo if preferred

st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 32px; color: #4CAF50; font-weight: bold;">
        SMART BUOY MONITORING SYSTEM
    </h1>
    <p style="color: #00d4ff; font-size: 18px;">
        Real-time Marine Monitoring • AI Debris Detection • GPS Tracking • Water Quality
    </p>
</div>
""", unsafe_allow_html=True)

# --- STATE / DATA SIMULATION & MODAL STATE ---
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}
if 'gps_history' not in st.session_state:
    st.session_state.gps_history = []
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False
if 'modal_index' not in st.session_state:
    st.session_state.modal_index = None

def random_gps():
    base_lat, base_lng = 5.9552, 116.0400
    return round(base_lat + random.uniform(-0.002, 0.002), 6), round(base_lng + random.uniform(-0.002, 0.002), 6)

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
        'lat': lat,'lng': lng,'timestamp': current_time
    })
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    detections = [
        {'type':'Plastic Bottle','time':'14:39:32','confidence':'94%','distance':'2.3m'},
        {'type':'Food Container','time':'12:52:50','confidence':'87%','distance':'1.8m'},
        {'type':'Fishing Net','time':'16:14:20','confidence':'91%','distance':'3.1m'},
        {'type':'Plastic Bag','time':'10:30:05','confidence':'78%','distance':'1.5m'}
    ]
    for d in detections:
        d['lat'], d['lng'] = random_gps()
        d['img'] = "image.jpg"
    st.session_state.buoy_data = {
        'buoy_1': {
            'status':'Active',
            'battery': random.randint(75, 95),
            'lat': lat,'lng': lng,
            'ph': round(random.uniform(7.8, 8.4), 2),
            'tds': random.randint(32000, 38000),
            'turbidity': round(random.uniform(5, 25), 1),
            'temperature': round(random.uniform(28, 31), 1),
            'last_reading': current_time.strftime("%d-%m-%Y at %H:%M:%S"),
            'camera_status': 'Recording',
            'detections': detections
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


# ============= OVERVIEW METRICS =============
st.markdown('<div class="section-header">📊 SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">BUOY STATUS</h4>
    <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">ACTIVE</h1></div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">DEBRIS DETECTED</h4>
    <h1 style="color: #ff6b35; font-size: 36px; margin: 5px 0;">{len(buoy_data['detections'])}</h1>
    <p class="text-white-high-contrast">Today's count</p></div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">CAMERA</h4>
    <h1 style="color: #ffbe0b; font-size: 36px; margin: 5px 0;">●</h1>
    <p class="text-white-high-contrast">{buoy_data['camera_status']}</p></div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">GPS STATUS</h4>
    <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">📡</h1>
    <p class="text-white-high-contrast">Tracking</p></div>
    """, unsafe_allow_html=True)
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
        st.map(df_map, zoom=14)
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
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 10px;">
        <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
        <p class="text-white-high-contrast"><strong>Update Interval:</strong> 10 minutes</p>
    </div>
</div>
"""
st.markdown(buoy_info_html, unsafe_allow_html=True)
gauges_data = [
    {'name': 'pH', 'value': buoy_data['ph'], 'range': [0, 14], 'optimal': [7.8, 8.5], 'unit': ''},
    {'name': 'TDS', 'value': buoy_data['tds'], 'range': [0, 50000], 'optimal': [30000, 40000], 'unit': 'ppm'},
    {'name': 'TURBIDITY', 'value': buoy_data['turbidity'], 'range': [0, 100], 'optimal': [0, 50], 'unit': 'NTU'},
    {'name': 'TEMPERATURE', 'value': buoy_data['temperature'], 'range': [0, 40], 'optimal': [27, 31], 'unit': '°C'}
]
fig_gauges = go.Figure()
positions = [(0, 0.23, 0, 1), (0.27, 0.5, 0, 1), (0.53, 0.76, 0, 1), (0.79, 1, 0, 1)]
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
    paper_bgcolor='rgba(0,0,0,0)',font={'color': "white"}, height=300,
    margin=dict(l=20, r=20, t=20, b=20), showlegend=False
)
st.plotly_chart(fig_gauges, use_container_width=True)
st.markdown("---")

# ============= RECENT DETECTIONS with MODAL & GPS =============
st.markdown("""<h4 style="margin-bottom: 1rem; color: #cccccc;">Recent Detections:</h4>""", unsafe_allow_html=True)
for idx, detection in enumerate(buoy_data['detections']):
    colA, colB, colC = st.columns([2.2, 1.0, 1.4])
    with colA:
        st.markdown(
            f"<div style='font-weight:bold;color:#00d4ff;font-size:17px'>{detection['type']}</div>"
            f"<span style='color:#bbbbbb;'>🕒 {detection['time']} &nbsp; | &nbsp; 📍 {detection['distance']} &nbsp; | &nbsp;"
            f"🌐 {detection['lat']}, {detection['lng']}</span>",
            unsafe_allow_html=True,
        )
    with colB:
        st.image(detection['img'], width=65)
        view_btn = st.button("View", key=f"view{idx}")
        if view_btn:
            st.session_state['show_modal'] = True
            st.session_state['modal_index'] = idx

    with colC:
        st.markdown(
            f"<span style='font-weight:800;color:#00ff88;font-size:18px;margin-top:6px;'>Confidence: {detection['confidence']}</span>",
            unsafe_allow_html=True,
        )
    st.markdown('<hr style="border:1px solid #ff6b35; margin-top:0.5em; margin-bottom:0.8em;"/>', unsafe_allow_html=True)

if st.session_state['show_modal'] and st.session_state['modal_index'] is not None:
    idx = st.session_state['modal_index']
    detection = buoy_data['detections'][idx]
    st.markdown(
        f"""
        <div style='position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(22,24,35,0.85); z-index:9000; display:flex; align-items:center; justify-content:center;'>
          <div style='background:#22202a; border-radius:14px; box-shadow:0 2px 15px #000b; padding:36px 38px; min-width:350px; max-width:98vw; text-align:center;'>
            <img src="{detection['img']}" style="max-width:340px; border-radius:12px; margin-bottom:1.2em;"/>
            <div style='font-weight:bold; color:#00d4ff; font-size:22px; margin-bottom:10px;'>{detection['type']}</div>
            <div style='color:#bbbbbb; margin-bottom:12px;'>
                <span style='margin-right:18px;'>🕒 {detection['time']}</span>
                <span style='margin-right:18px;'>Confidence: <span style="color:#00ff88;">{detection['confidence']}</span></span>
                <br>
                <span style='margin-right:12px;'>📍 {detection['distance']}</span>
                <span>🌐 {detection['lat']}, {detection['lng']}</span>
            </div>
            <form method="post">
              <button style='background:#ff6b35; color:#fff; font-weight:600; border:none; border-radius:6px; padding:7px 26px; margin-top:12px; cursor:pointer; font-size:15px;' name='close-modal' type='submit'>Close</button>
            </form>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Close", key="close_modal_btn"):
        st.session_state['show_modal'] = False
        st.session_state['modal_index'] = None
else:
    st.session_state['show_modal'] = False
    st.session_state['modal_index'] = None

# ============= ANALYTICS & TRENDS =============
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
    fig_trends.add_trace(go.Scatter(
        x=dates, y=[29 + np.random.normal(0, 0.5) for _ in range(7)],
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
