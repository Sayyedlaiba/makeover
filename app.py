import streamlit as st
import base64
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Dynamic Doll Glow-Up", layout="wide")

# --- 2. UTILITY: Dynamic Image Loading & Overlaying ---
def get_image_base64(path):
    """Encodes a local image to base64 for embedding in HTML."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_dynamic_stage(base_path, overlay_path, base_opacity, overlay_opacity):
    """Renders two images stacked dynamically using custom HTML/CSS."""
    base_data = get_image_base64(base_path)
    overlay_data = get_image_base64(overlay_path)

    if not base_data:
        st.error(f"Missing required base image: {base_path}")
        return

    # HTML & CSS structure to overlay images directly on top of each other
    html_content = f"""
    <div class="glowup-container" style="position: relative; width: 100%; max-width: 500px; margin: auto;">
        <img src="data:image/png;base64,{base_data}" 
             style="width: 100%; height: auto; display: block; 
                    opacity: {base_opacity}; transition: opacity 0.5s ease;">
    """

    # Add Overlay Image Layer (if present)
    if overlay_data:
        html_content += f"""
        <img src="data:image/png;base64,{overlay_data}" 
             style="position: absolute; top: 0; left: 0; width: 100%; height: auto; 
                    opacity: {overlay_opacity}; transition: opacity 0.5s ease; pointer-events: none;">
        """
    
    html_content += "</div>"
    st.components.v1.html(html_content, height=520)


# --- 3. INITIALIZE SESSION STATE ---
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "welcome"
if "clean_progress" not in st.session_state:
    st.session_state.clean_progress = 0
if "lipstick_on" not in st.session_state:
    st.session_state.lipstick_on = False
if "eyeshadow_on" not in st.session_state:
    st.session_state.eyeshadow_on = False


# --- 4. MAIN INTERFACE ---
st.title("💖 Dynamic Doll Salon: The Glow-Up 💖")
st.write("Washing and Makeup: Dynamic Edition!")
st.markdown("---")

# Define the columns so Streamlit knows where col1 and col2 are!
col1, col2 = st.columns([1, 1])

# --- DISPLAY AREA (LEFT COLUMN) ---
with col1:
    st.subheader("Your Doll")

    # STAGE: WELCOME
    if st.session_state.game_stage == "welcome":
        render_dynamic_stage("base_messy.png", None, 1.0, 0.0)
    
    # STAGE: WASHING (Fades out messy face, fades in clean face)
    elif st.session_state.game_stage == "washing":
        clean_opacity = st.session_state.clean_progress / 100.0
        messy_opacity = 1.0 - clean_opacity
        render_dynamic_stage("base_clean.png", "base_messy.png", clean_opacity, messy_opacity)
        
    # STAGE: MAKEUP (Overlays chosen cosmetics)
    elif st.session_state.game_stage == "makeup":
        selected_layer = None
        layer_opacity = 0.0

        if st.session_state.lipstick_on:
            selected_layer = "lipstick_layer.png"
            layer_opacity = 1.0
        elif st.session_state.eyeshadow_on:
            selected_layer = "eyeshadow_layer.png"
            layer_opacity = 1.0
            
        render_dynamic_stage("base_clean.png", selected_layer, 1.0, layer_opacity)
        
    # STAGE: REVEAL
    elif st.session_state.game_stage == "reveal":
        render_dynamic_stage("base_clean.png", None, 1.0, 0.0)


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
        
        current_clean = st.session_state.clean_progress
        st.progress(current_clean / 100)
        st.write(f"Dirt Removed: {current_clean}%")

        if st.button("Scrub Face 🧽", disabled=(current_clean >= 100)):
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
            st.session_state.game_stage = "welcome"
            st.session_state.clean_progress = 0
            st.session_state.lipstick_on = False
            st
