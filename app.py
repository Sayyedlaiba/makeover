# --- CONTROL AREA (RIGHT COLUMN) ---
with col2:
    st.subheader("Salon Controls")

    # CONTROLS: WELCOME
    if st.session_state.game_stage == "welcome":
        st.write("A new client has arrived, and she's a mess! Time to get to work.")
        if st.button("Begin Deep Clean ✨"):
            st.session_state.game_stage = "washing"
            st.rerun()

    # CONTROLS: WASHING
    elif st.session_state.game_stage == "washing":
        st.write("Click below to scrub the dirt away!")
        
        # Progress visualizer
        current_clean = st.session_state.clean_progress
        st.progress(current_clean / 100)
        st.write(f"Dirt Removed: {current_clean}%")

        if st.button("Scrub Face 🧽", disabled=(current_clean >= 100)):
            # Dynamic Step update
            st.session_state.clean_progress += 25 
            if st.session_state.clean_progress >= 100:
                st.session_state.clean_progress = 100
            st.rerun()

        if current_clean == 100:
            st.success("Face is perfectly clean!")
            if st.button("Proceed to Makeup 💄"):
                st.session_state.game_stage = "makeup"
                st.rerun()

    # CONTROLS: MAKEUP
    elif st.session_state.game_stage == "makeup":
        st.write("The canvas is clean. Apply the final touches!")
        
        lipstick_check = st.checkbox("Apply Pink Lipstick 💄", value=st.session_state.lipstick_on)
        eyeshadow_check = st.checkbox("Apply Sparkly Eyeshadow 👀", value=st.session_state.eyeshadow_on)
        
        st.session_state.lipstick_on = lipstick_check
        st.session_state.eyeshadow_on = eyeshadow_check

        applied = []
        if st.session_state.lipstick_on: applied.append("Pink Lipstick")
        if st.session_state.eyeshadow_on: applied.append("Blue Eyeshadow")
        
        st.write(f"Current Look: **{' + '.join(applied) if applied else 'Clean Face'}**")

        col_refresh, col_finish = st.columns(2)
        with col_refresh:
            if st.button("Update Mirror 🪞"):
                st.rerun()
        with col_finish:
            if st.button("Finish Makeover 🎉"):
                st.session_state.game_stage = "reveal"
                st.rerun()

    # CONTROLS: REVEAL
    elif st.session_state.game_stage == "reveal":
        st.success("What a stunning transformation!")
        st.balloons()
        
        if st.button("Start New Appointment 🔄"):
            # RESET STATE
            st.session_state.game_stage = "welcome"
            st.session_state.clean_progress = 0
            st.session_state.lipstick_on = False
            st.session_state.eyeshadow_on = False
            st.rerun()

st.markdown("---")
st.caption("A dynamic Streamlit experiment by [Your Name/Github]")
