import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# ---- CONFIGURATION & STYLES ----
st.set_page_config(
    page_title="MAREYE Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

css_styles = """
<style>
/* ... (same styles provided above, unchanged for brevity) ... */
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# ---- CONSTANTS ----
REFRESH_INTERVAL = 10   # seconds between auto-refresh
LOW_BATTERY_THRESHOLD = 20

base_lat, base_lng = 5.9552, 116.0400

# ---- HELPERS ----
def simulate_buoy_data(last_pos):
    """
    Simulate realistic tropical seawater buoy data for Tanjung Aru.
    """
    now = datetime.now()
    if last_pos is None:
        lat, lng = base_lat, base_lng
    else:
        lat = last_pos['lat'] + random.uniform(-0.0005, 0.0005)
        lng = last_pos['lng'] + random.uniform(-0.0005, 0.0005)
    return {
        'status': 'Active',
        'battery': random.randint(13, 98),
        'lat': lat,
        'lng': lng,
        'ph': round(random.uniform(7.8, 8.4), 2),
        'tds': random.randint(32000, 38000),  # realistic Tanjung Aru
        'turbidity': round(random.uniform(3, 13), 1),  # slightly turbid
        'temperature': round(random.uniform(28, 31), 1),
        'last_reading': now.strftime("%d-%m-%Y at %H:%M:%S"),
        'camera_status': 'Recording',
        # Simulated detection set
        'detections': [
            {'Type': 'Plastic Bottle',   'Time': '14:39:32', 'Confidence': 94, 'Distance': 2.3},
            {'Type': 'Food Container',   'Time': '12:52:50', 'Confidence': 87, 'Distance': 1.8},
            {'Type': 'Fishing Net',      'Time': '16:14:20', 'Confidence': 91, 'Distance': 3.1},
            {'Type': 'Plastic Bag',      'Time': '10:30:05', 'Confidence': 78, 'Distance': 1.5}
        ]
    }, lat, lng

def battery_alert(battery):
    """
    Show warning if battery falls below threshold.
    """
    if battery < LOW_BATTERY_THRESHOLD:
        st.warning(
            f"⚠️ Battery low ({battery}%) — consider maintenance soon.",
            icon="🔋"
        )

def water_quality_tooltip(sensor):
    """
    Info text for each water quality sensor for user guidance.
    """
    return {
        'pH': "pH should be 7.8–8.5 for healthy tropical seawater.",
        'TDS': "TDS (ppm) for seawater: 32,000–38,000 near Tanjung Aru.",
        'TURBIDITY': "Turbidity (NTU) <15 is normal for open tropical sea.",
        'TEMPERATURE': "Temperature 28–31°C typical for tropical coastal waters."
    }[sensor]

def create_gauges_panel(bdata):
    """
    Create Plotly gauge indicators for water quality.
    """
    gauges = [
        {'name': 'pH', 'value': bdata['ph'], 'range': [0,14], 'optimal': [7.8,8.5], 'unit': ''},
        {'name': 'TDS', 'value': bdata['tds'], 'range': [0,50000], 'optimal': [32000,38000], 'unit': 'ppm'},
        {'name': 'TURBIDITY', 'value': bdata['turbidity'], 'range': [0,50], 'optimal': [0,15], 'unit': 'NTU'},
        {'name': 'TEMPERATURE', 'value': bdata['temperature'], 'range': [26,34], 'optimal': [28,31], 'unit': '°C'}
    ]
    fig = go.Figure()
    positions = [(0,0.23,0,1), (0.27,0.5,0,1), (0.53,0.76,0,1), (0.79,1,0,1)]
    for g,pos in zip(gauges, positions):
        color = (
            '#00ff88' if g['optimal'][0] <= g['value'] <= g['optimal'][1]
            else ('#ffbe0b' if g['optimal'][0]*.8 <= g['value'] <= g['optimal'][1]*1.2 else '#ff6b35')
        )
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=float(g['value']),
            domain={'x': [pos[0], pos[1]], 'y': [pos[2], pos[3]]},
            title={'text': f"<b>{g['name']}</b>", 'font': {'color': 'white', 'size': 14}},
            number={'suffix': f" {g['unit']}", 'font': {'color': 'white', 'size': 16}},
            gauge={
                'axis': {'range': [g['range'][0], g['range'][1]], 'tickcolor': 'white', 'tickfont': {'color': 'white', 'size': 10}},
                'bar': {'color': color, 'thickness': 0.7},
                'bgcolor': "rgba(26, 35, 50, 0.8)",
                'borderwidth': 2,
                'bordercolor': "#00d4ff",
                'steps': [
                    {'range': [g['range'][0], g['optimal'][0]], 'color': "rgba(255, 107, 53, 0.32)"},
                    {'range': [g['optimal'][0], g['optimal'][1]], 'color': "rgba(0, 255, 136, 0.22)"},
                    {'range': [g['optimal'][1], g['range'][1]], 'color': "rgba(255, 107, 53, 0.32)"}
                ]
            }
        ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"},
        height=290, margin=dict(l=20,r=20,t=20,b=20), showlegend=False
    )
    return fig

def detection_table(detections):
    """
    Show detections as formatted dataframe rather than as boxes.
    """
    df = pd.DataFrame(detections)
    df['Time'] = pd.to_datetime(
        df['Time'], format='%H:%M:%S', errors='coerce'
    ).dt.time.astype(str)
    # Color-highlight confident detections
    def color_row(row):
        color = 'background-color: #ff6b35;' if row['Confidence'] >= 90 else (
            'background-color: #00ff88;' if row['Confidence'] >= 80 else '')
        return [color] * len(row)
    st.dataframe(
        df.style.apply(color_row, axis=1),
        height=220,
        use_container_width=True,
        hide_index=True
    )

def progress_bar(seconds):
    """
    Show a countdown progress bar for the auto-refresh.
    """
    ph = st.empty()
    for i in range(seconds, 0, -1):
        ph.info(f"⏳ Auto-refresh in {i} seconds...", icon="🔄")
        time.sleep(1)
    ph.empty()

# ---- STATE INITIALIZATION ----
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'buoy_data' not in st.session_state:
    st.session_state.buoy_data = {}
if 'gps_history' not in st.session_state:
    st.session_state.gps_history = []

# ---- HEADER & LOGO ----
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("thalasea-logo.png", width=320)
st.markdown("""
<div style="text-align:center;margin-bottom:20px;">
    <h1 style="font-size:32px;color:#4CAF50;font-weight:bold;">SMART BUOY MONITORING SYSTEM</h1>
    <p style="color:#00d4ff;font-size:18px;">Real-time Marine Monitoring • AI Debris Detection • GPS Tracking • Water Quality</p>
</div>
""", unsafe_allow_html=True)

# ---- DATA UPDATE / REFRESH ----
manual_refresh = st.button("🔄 Refresh Data", use_container_width=True, disabled=False)
now = datetime.now()
refresh_due = (now - st.session_state.last_update).seconds >= REFRESH_INTERVAL

# Only update data if:
if manual_refresh or refresh_due or not st.session_state.buoy_data:
    last_gps = st.session_state.gps_history[-1] if st.session_state.gps_history else None
    buoy_data, lat, lng = simulate_buoy_data(last_gps)
    # Update/rebuild GPS history
    st.session_state.gps_history.append({'lat': lat,'lng': lng,'timestamp': now})
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    st.session_state.last_update = now
    st.session_state.buoy_data = buoy_data
else:
    # If not updating, show progress bar
    progress_bar(REFRESH_INTERVAL - (now - st.session_state.last_update).seconds)
buoy_data = st.session_state.buoy_data

# ---- METRIC CARDS ----
st.markdown('<div class="section-header">📊 SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card"> <h4 class="text-white-high-contrast">BUOY STATUS</h4>
    <h1 style="color:#00ff88;font-size:36px;margin:5px 0;">ACTIVE</h1>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card"><h4 class="text-white-high-contrast">DEBRIS DETECTED</h4>
    <h1 style="color:#ff6b35;font-size:36px;margin:5px 0;">{len(buoy_data['detections'])}</h1>
    <p class="text-white-high-contrast">Today's count</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">CAMERA</h4>
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

battery_alert(buoy_data['battery'])

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
        stats_html = f"""
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
        """
        st.markdown(stats_html, unsafe_allow_html=True)
st.markdown("---")

# ---- WATER QUALITY GAUGES ----
st.markdown('<div class="section-header">💧 WATER QUALITY MONITORING</div>', unsafe_allow_html=True)
with st.expander("ℹ️ Water Quality Sensor Info", expanded=False):
    for key in ['pH', 'TDS', 'TURBIDITY', 'TEMPERATURE']:
        st.info(f"{key}: {water_quality_tooltip(key)}", icon="💡")
st.markdown(f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">Water Quality Station</h4>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:15px;margin-top:10px;">
    <p class="text-white-high-contrast"><strong>Last Reading:</strong> {buoy_data['last_reading']}</p>
    <p class="text-white-high-contrast"><strong>Update Interval:</strong> {REFRESH_INTERVAL} seconds</p></div>
</div>
""", unsafe_allow_html=True)
st.plotly_chart(create_gauges_panel(buoy_data), use_container_width=True)
st.markdown("---")

# ---- DEBRIS DETECTION ----
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
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("**Recent Detections:**")
    detection_table(buoy_data['detections'])
with col2:
    # Plot detection trend (last 7 days)
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    detections = np.random.poisson(3, len(dates))
    fig_detections = go.Figure()
    fig_detections.add_trace(go.Bar(
        x=dates.strftime('%d-%b'),
        y=detections,
        marker_color='#ff6b35',
        name='Daily Detections'
    ))
    fig_detections.update_layout(
        title=dict(text="7-Day Detection Trend", font=dict(color='#00d4ff', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white', size=10),
        height=250,
        margin=dict(l=30, r=10, t=40, b=40)
    )
    st.plotly_chart(fig_detections, use_container_width=True)
st.markdown("---")

# ---- ANALYTICS ----
st.markdown('<div class="section-header">📈 ANALYTICS & TRENDS</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    detection_types = {'Plastic': 45, 'Fishing Gear': 25, 'Food Containers': 20, 'Other': 10}
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(detection_types.keys()),
        values=list(detection_types.values()),
        hole=0.5,
        marker=dict(colors=['#ff6b35', '#00d4ff', '#ffbe0b', '#00ff88'])
    )])
    fig_pie.update_layout(
        title=dict(text="Debris Type Distribution", x=0.5, font=dict(color='#00d4ff', size=18)),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300, showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    # Simulate trends for analytics
    pH_trend = [7.8 + np.random.normal(0,0.1) for _ in range(7)]
    tds_trend = [34000 + np.random.normal(0,400) for _ in range(7)]
    temp_trend = [29 + np.random.normal(0,0.5) for _ in range(7)]
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=dates.strftime('%d-%b'), y=pH_trend, mode='lines+markers', name='pH', line=dict(color='#00d4ff',width=2)))
    fig_trends.add_trace(go.Scatter(
        x=dates.strftime('%d-%b'), y=tds_trend, mode='lines+markers', name='TDS', line=dict(color='#ff6b35',width=2)))
    fig_trends.add_trace(go.Scatter(
        x=dates.strftime('%d-%b'), y=temp_trend, mode='lines+markers', name='Temp', line=dict(color='#ffbe0b',width=2)))
    fig_trends.update_layout(
        title=dict(text="7-Day Water Quality Trends", x=0.5, font=dict(color='#00d4ff', size=18)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26, 35, 50, 0.8)',
        font=dict(color='white'),
        height=300
    )
    st.plotly_chart(fig_trends, use_container_width=True)
st.markdown("---")

# ---- FOOTER ----
footer_html = f"""
<div style="text-align:center;padding:20px;background:linear-gradient(145deg,#1a2332 0%,#243040 100%);border-radius:15px; border:1px solid #00d4ff;">
    <h3 style="color:#00d4ff;margin-bottom:10px;">MAREYE Smart Buoy Monitoring System</h3>
    <p class="text-white-high-contrast">Real-time Marine Monitoring • AI Detection • GPS Tracking • Water Quality Analysis</p>
    <div style="display:flex;justify-content:center;gap:30px;margin:15px 0;flex-wrap:wrap;">
        <span class="text-white-high-contrast">Last Updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}</span>
        <span>System: <span style="color:#00ff88;font-weight:bold;">ONLINE</span></span>
    </div>
    <p style="color:#888;font-size:12px;margin-top:10px;">🌊 Protecting our oceans through advanced technology</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
