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
