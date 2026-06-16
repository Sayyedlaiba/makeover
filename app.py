# CONTROLS: MAKEUP
    elif st.session_state.game_stage == "makeup":
        st.write("The canvas is clean. Apply the final touches!")
        
        # We read and update the states cleanly without immediate reruns
        lipstick_check = st.checkbox("Apply Pink Lipstick 💄", value=st.session_state.lipstick_on)
        eyeshadow_check = st.checkbox("Apply Sparkly Eyeshadow 👀", value=st.session_state.eyeshadow_on)
        
        # Sync the checkbox state to our session state
        st.session_state.lipstick_on = lipstick_check
        st.session_state.eyeshadow_on = eyeshadow_check

        # Display what's currently applied
        applied = []
        if st.session_state.lipstick_on: applied.append("Pink Lipstick")
        if st.session_state.eyeshadow_on: applied.append("Blue Eyeshadow")
        
        st.write(f"Current Look: **{' + '.join(applied) if applied else 'Clean Face'}**")

        # Let the user see their updates instantly when they hit the button
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
