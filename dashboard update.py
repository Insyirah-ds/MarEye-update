# --- This block REPLACES your previous for detection in buoy_data['detections']: block ---

st.markdown("""
    <h4 style="margin-bottom: 1rem; color: #cccccc;">Recent Detections:</h4>
""", unsafe_allow_html=True)
for detection in buoy_data['detections']:
    st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: space-between; background: #28203a; border: 2px solid #ff6b35; border-radius: 10px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 8px rgba(255, 107, 53, 0.12);">

    <div style="flex: 3;">
        <div style="font-weight: bold; color: #00d4ff; font-size: 16px; margin-bottom: 4px;">{detection['type']}</div>
        <div style="color: #bbbbbb;">
            <span style="margin-right:18px;">🕒 {detection['time']}</span>
            <span style="margin-right:18px;">📍 {detection['distance']}</span>
            <span style="margin-right:18px;">🌐 {buoy_data['lat']:.5f}, {buoy_data['lng']:.5f}</span>
        </div>
    </div>

    <div style="flex: 1; text-align: center;">
        <img src="image.jpg" alt="Detection Image" style="width:70px; height:70px; border-radius:10px; object-fit:cover; border:2px solid #333333; box-shadow: 0 2px 8px #003f57ad;" />
        <br/>
        <a href="image.jpg" target="_blank" style="background:#00d4ff; color:white; font-weight:500; padding:3px 12px; border-radius:8px; margin-top:7px; display:inline-block; text-decoration:none; font-size:13px;">View</a>
    </div>

    <div style="flex: 0.8; text-align: right;">
        <span style="font-weight: 800; color: #00ff88; font-size:18px; margin-top:6px; display:inline-block;">Confidence: {detection['confidence']}</span>
    </div>
</div>
""", unsafe_allow_html=True)
