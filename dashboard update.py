import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="MAREYE Dashboard", layout="wide", initial_sidebar_state="collapsed")

css_styles = """
<style>
.main {background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%); color: #ffffff;}
.stApp {background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);}
.metric-card {background: linear-gradient(145deg, #1e2a3a 0%, #2a3441 100%); padding: 25px; border-radius: 15px; border: 2px solid #00d4ff; box-shadow: 0 0 20px rgba(0, 212, 255, 0.25); margin-bottom: 20px; color: #ffffff;}
.buoy-card {background: linear-gradient(145deg, #1a2332 0%, #243040 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #00ff88; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.4); color: #ffffff; border: 1px solid #00ff88;}
.detection-box {background: linear-gradient(145deg, #2a1f2e 0%, #3d2a40 100%); border: 2px solid #ff6b35; border-radius: 10px; padding: 15px; margin: 10px 0; box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);}
.camera-feed-container {background: linear-gradient(145deg, #1e2332 0%, #2a2f40 100%); border: 2px solid #00d4ff; border-radius: 12px; padding: 15px; margin: 15px 0; box-shadow: 0 6px 12px rgba(0, 212, 255, 0.2);}
.status-online {color: #00ff88; font-weight: bold; font-size: 18px;}
.section-header {background: linear-gradient(90deg, #00ff88, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 28px; font-weight: bold; margin: 30px 0 20px 0;}
.text-white-high-contrast {color: #ffffff !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); font-weight: 600;}
.stButton > button {background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%); border: 2px solid #00d4ff; color: #ffffff; font-weight: bold; box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);}
.stButton > button:hover {box-shadow: 0 0 25px rgba(0, 212, 255, 0.5); transform: translateY(-2px);}
.image-thumb {height: 90px; width: auto; border-radius: 8px; box-shadow: 0 1px 8px rgba(0,0,0,0.45);}
.image-full {max-width: 100%; max-height: 420px; border-radius: 8px; box-shadow: 0 2px 20px rgba(0,0,0,0.45);}
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# Title/logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("thalasea-logo.png", width=320)
title_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 32px; color: #4CAF50; font-weight: bold;">SMART BUOY MONITORING SYSTEM</h1>
    <p style="color: #00d4ff; font-size: 18px;">Real-time Marine Monitoring | AI Debris Detection | GPS Tracking | Water Quality</p>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()
if "buoy_data" not in st.session_state:
    st.session_state.buoy_data = {}
if "gps_history" not in st.session_state:
    st.session_state.gps_history = []

def update_live_data():
    current_time = datetime.now()
    base_lat = 5.9552
    base_lng = 116.0400
    if not st.session_state.gps_history:
        lat, lng = base_lat, base_lng
    else:
        lastpos = st.session_state.gps_history[-1]
        lat = lastpos["lat"] + random.uniform(-0.0005, 0.0005)
        lng = lastpos["lng"] + random.uniform(-0.0005, 0.0005)
    st.session_state.gps_history.append({"lat": lat, "lng": lng, "timestamp": current_time})
    if len(st.session_state.gps_history) > 50:
        st.session_state.gps_history = st.session_state.gps_history[-50:]
    detection_types = ["Plastic Bottle", "Food Container", "Fishing Net", "Plastic Bag", "Styrofoam", "Rope", "Metal Can"]
    detections = []
    for i in range(25):
        det_lat = lat + random.uniform(-0.002, 0.002)
        det_lng = lng + random.uniform(-0.002, 0.002)
        detections.append({
            "type": random.choice(detection_types),
            "time": (datetime.now() - timedelta(minutes=random.randint(0, 600))).strftime("%H:%M:%S"),
            "confidence": random.randint(75, 99),
            "latitude": det_lat,
            "longitude": det_lng,
        })
    st.session_state.buoy_data = {
        "buoy1": {
            "status": "Active",
            "battery": random.randint(75, 95),
            "lat": lat,
            "lng": lng,
            "ph": round(random.uniform(7.8, 8.4), 2),
            "tds": random.randint(32000, 38000),
            "turbidity": round(random.uniform(5, 25), 1),
            "lastreading": current_time.strftime("%d-%m-%Y at %H:%M:%S"),
            "camera_status": "Recording",
            "detections": detections
        }
    }

col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("Refresh Data", use_container_width=True):
        update_live_data()
        st.session_state.last_update = datetime.now()
        st.rerun()

if (datetime.now() - st.session_state.last_update).seconds > 10:
    update_live_data()
    st.session_state.last_update = datetime.now()
    st.rerun()

if not st.session_state.buoy_data:
    update_live_data()

buoy_data = st.session_state.buoy_data["buoy1"]

st.markdown("---")

# SYSTEM OVERVIEW
st.markdown('<div class="section-header">SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    card_html = """
    <div class="metric-card">
        <h4 class="text-white-high-contrast">BUOY STATUS</h4>
        <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">ACTIVE</h1>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col2:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">DEBRIS DETECTED</h4>
        <h1 style="color: #ff6b35; font-size: 36px; margin: 5px 0;">{len(buoy_data["detections"])}</h1>
        <p class="text-white-high-contrast">Today's count</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col3:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">CAMERA</h4>
        <h1 style="color: #ffbe0b; font-size: 36px; margin: 5px 0;">●</h1>
        <p class="text-white-high-contrast">{buoy_data["camera_status"]}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col4:
    card_html = """
    <div class="metric-card">
        <h4 class="text-white-high-contrast">GPS STATUS</h4>
        <h1 style="color: #00ff88; font-size: 36px; margin: 5px 0;">📡</h1>
        <p class="text-white-high-contrast">Tracking</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
with col5:
    card_html = f"""
    <div class="metric-card">
        <h4 class="text-white-high-contrast">BATTERY LEVEL</h4>
        <h1 style="color: #00d4ff; font-size: 36px; margin: 5px 0;">{buoy_data["battery"]}%</h1>
        <p class="text-white-high-contrast">Remaining</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# GPS TRACKING SECTION
st.markdown('<div class="section-header">GPS TRACKING LOCATION</div>', unsafe_allow_html=True)
gpsstatushtml = f"""
<div class="buoy-card">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 20px;">
        <div>
            <p class="text-white-high-contrast"><strong>Current Position</strong></p>
            <p style="color: #00d4ff; font-size: 16px; font-weight: bold;">{buoy_data['lat']:.6f}, {buoy_data['lng']:.6f}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Movement</strong></p>
            <p class="status-online">Drifting</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Signal</strong></p>
            <p style="color: #00ff88; font-size: 16px; font-weight: bold;">Excellent</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Last Update</strong></p>
            <p style="color: #ffbe0b; font-size: 14px;">{datetime.now().strftime('%H:%M:%S')}</p>
        </div>
    </div>
</div>
"""
st.markdown(gpsstatushtml, unsafe_allow_html=True)
col1, col2 = st.columns([2,1])
with col1:
    if st.session_state.gps_history:
        dfmap = pd.DataFrame({"lat": [buoy_data["lat"]], "lon": [buoy_data["lng"]]})
        st.map(dfmap, zoom=14)
with col2:
    if len(st.session_state.gps_history) > 1:
        firstpos = st.session_state.gps_history[0]
        lastpos = st.session_state.gps_history[-1]
        lat_diff = abs(lastpos["lat"] - firstpos["lat"])
        lng_diff = abs(lastpos["lng"] - firstpos["lng"])
        approx_distance = ((lat_diff**2 + lng_diff**2)**0.5) * 111
        stats_html = f"""
        <div class="camera-feed-container">
            <h4 style="color: #00d4ff; text-align: center;">Movement Stats</h4>
            <div style="padding: 15px;">
                <div style="margin-bottom: 15px;">
                    <p style="color: #888; font-size: 12px; margin: 0;">Total Distance</p>
                    <p style="color: #00ff88; font-size: 24px; font-weight: bold; margin: 5px 0;">{approx_distance:.2f} km</p>
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

# WATER QUALITY SECTION
st.markdown('<div class="section-header">WATER QUALITY MONITORING</div>', unsafe_allow_html=True)
buoyinfohtml = f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">Water Quality Station</h4>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px;">
        <p class="text-white-high-contrast"><strong>Last Reading</strong> {buoy_data['lastreading']}</p>
        <p class="text-white-high-contrast"><strong>Update Interval</strong> 10 minutes</p>
    </div>
</div>
"""
st.markdown(buoyinfohtml, unsafe_allow_html=True)
gauges_data = [
    {"name": "pH", "value": buoy_data["ph"], "range": (0, 14), "optimal": (7.8, 8.5), "unit": ""},
    {"name": "TDS", "value": buoy_data["tds"], "range": (0, 50000), "optimal": (32000, 38000), "unit": "ppm"},
    {"name": "TURBIDITY", "value": buoy_data["turbidity"], "range": (0, 100), "optimal": (5, 25), "unit": "NTU"}
]
fig_gauges = go.Figure()
positions = [(0, 0.32, 0, 1), (0.34, 0.67, 0, 1), (0.68, 1, 0, 1)]
for gauge_data, pos in zip(gauges_data, positions):
    value = gauge_data["value"]
    optimal = gauge_data["optimal"]
    title = f"{gauge_data['name']}"
    if gauge_data["name"] == "TDS":
        number_display = dict(valueformat="d", suffix=" ppm", font=dict(color="white", size=16))
    else:
        number_display = dict(suffix=f" {gauge_data['unit']}", font=dict(color="white", size=16))
    if optimal[0] <= float(value) <= optimal[1]:
        color = "#00ff88"
    elif optimal[0]*0.8 <= float(value) <= optimal[1]*1.2:
        color = "#ff6b35"
    else:
        color = "#ffbe0b"
    fig_gauges.add_trace(go.Indicator(
        mode="gauge+number",
        value=float(value),
        domain={"x": [pos[0], pos[1]], "y": [pos[2], pos[3]]},
        title={"text": title, "font": {"color": "white", "size": 14}},
        number=number_display,
        gauge={
            "axis": {"range": [None, gauge_data["range"][1]], "tickcolor": "white", "tickfont": {"color": "white", "size": 10}},
            "bar": {"color": color, "thickness": 0.7},
            "bgcolor": "rgba(26, 35, 50, 0.8)",
            "borderwidth": 2,
            "bordercolor": "#00d4ff",
            "steps": [
                {"range": [gauge_data["range"][0], optimal[0]], "color": "rgba(255, 107, 53, 0.3)"},
                {"range": [optimal[0], optimal[1]], "color": "rgba(0, 255, 136, 0.3)"},
                {"range": [optimal[1], gauge_data["range"][1]], "color": "rgba(255, 107, 53, 0.3)"}
            ]
        }
    ))
fig_gauges.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    height=300,
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False
)
st.plotly_chart(fig_gauges, use_container_width=True)

st.markdown("---")

# DEBRIS DETECTION SECTION (with IMAGES and LOCATION)
st.markdown('<div class="section-header">MARINE DEBRIS DETECTION</div>', unsafe_allow_html=True)
camerastatushtml = f"""
<div class="buoy-card">
    <h4 class="text-white-high-contrast">AI-Powered Camera System</h4>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 10px;">
        <div>
            <p class="text-white-high-contrast"><strong>Status</strong></p>
            <p class="status-online">{buoy_data["camera_status"]}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Detections Today</strong></p>
            <p style="color: #ff6b35; font-size: 20px; font-weight: bold;">{len(buoy_data["detections"])}</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>AI Confidence</strong></p>
            <p style="color: #00ff88; font-size: 20px; font-weight: bold;">88</p>
        </div>
        <div>
            <p class="text-white-high-contrast"><strong>Resolution</strong></p>
            <p style="color: #00d4ff; font-size: 16px;">1080p HD</p>
        </div>
    </div>
</div>
"""
st.markdown(camerastatushtml, unsafe_allow_html=True)

img_files = ["plastic image for cctv.jpg", "plastic image for cctv 2.jpg"]
if "view_img_idx" not in st.session_state:
    st.session_state.view_img_idx = None

col1, col2 = st.columns([3,2])
with col1:
    st.markdown("#### Recent Detections")
    for idx, detection in enumerate(buoy_data["detections"]):
        show_image = (idx < 2)
        img_path = img_files[idx] if show_image and idx < len(img_files) else None

        detectionhtml = f"""
        <div class="detection-box" style="display: flex; flex-direction: row; align-items: center;">
            <div style="flex: 2;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #00d4ff; font-size: 16px;">{detection["type"]}</strong>
                    <span style="color: #00ff88; font-weight: bold;">Confidence {detection["confidence"]}</span>
                </div>
                <div style="margin: 8px 0;">
                    <span style="color: #ffffff;">{detection["time"]}</span>
                    <span style="color: #00d4ff; margin-left: 20px;">
                        Location Detected: {detection["latitude"]:.5f}, {detection["longitude"]:.5f}
                    </span>
                </div>
            </div>
            <div style="flex: 1; text-align: center;">
        """
        detectionhtml_end = "</div></div>"

        st.markdown(detectionhtml, unsafe_allow_html=True)
        if show_image and img_path:
            st.image(img_path, use_column_width=False, width=90)
            if st.button(f"View (Detection {idx+1})", key=f"view_img_{idx}", help="Click to expand image"):
                st.session_state.view_img_idx = idx
        else:
            st.markdown('<div style="height:90px;"></div>', unsafe_allow_html=True)
        st.markdown(detectionhtml_end, unsafe_allow_html=True)

    if st.session_state.view_img_idx is not None:
        st.markdown("---")
        expanded_path = img_files[st.session_state.view_img_idx]
        st.markdown(f"**Expanded Detection Image:**", unsafe_allow_html=True)
        st.image(expanded_path, use_column_width=True)

with col2:
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    detections_trend = np.random.poisson(3, len(dates))
    fig_detections = go.Figure()
    fig_detections.add_trace(go.Bar(x=dates, y=detections_trend, marker_color="#ff6b35", name="Daily Detections"))
    fig_detections.update_layout(
        title=dict(text="7-Day Detection Trend", font=dict(color="#00d4ff", size=16)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26, 35, 50, 0.8)",
        font=dict(color="white", size=10),
        xaxis=dict(gridcolor="rgba(0,212,255,0.2)", title="Date"),
        yaxis=dict(gridcolor="rgba(0,212,255,0.2)", title="Items"),
        height=300,
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_detections, use_container_width=True)

st.markdown("---")

# ANALYTICS SECTION
st.markdown('<div class="section-header">ANALYTICS TRENDS</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    detection_types = {"Plastic": 45, "Fishing Gear": 25, "Food Containers": 20, "Other": 10}
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(detection_types.keys()),
        values=list(detection_types.values()),
        hole=0.4,
        marker=dict(colors=["#ff6b35", "#00d4ff", "#ffbe0b", "#00ff88"]),
        textinfo='percent+label',
        insidetextorientation="auto",
        textfont=dict(color="white", size=18),
        pull=[0.04, 0.04, 0.04, 0.04]
    )])
    fig_pie.update_layout(
        title=dict(text="Debris Type Distribution", x=0.5, font=dict(color="#00d4ff", size=20)),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(
            orientation="v",
            font=dict(color="white", size=18),
            bgcolor="rgba(34,40,55,0.8)",
            bordercolor="#00d4ff",
            borderwidth=1,
            x=1.02
        ),
        height=350,
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    dates = pd.date_range(end=datetime.now(), periods=7, freq='D')
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(x=dates, y=[7.8 + np.random.normal(0, 0.1) for _ in range(7)], mode="lines+markers", name="pH", line=dict(color="#00d4ff", width=2)))
    fig_trends.add_trace(go.Scatter(x=dates, y=[35000 + np.random.normal(0, 400) for _ in range(7)], mode="lines+markers", name="TDS", line=dict(color="#ff6b35", width=2)))
    fig
