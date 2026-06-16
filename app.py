import streamlit as st
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Dynamic Doll Glow-Up", layout="wide")

# --- UTILITY: Dynamic Image Loading ---
def get_image_base64(path):
    """Encodes a local image to base64 for embedding in HTML."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_dynamic_stage(base_path, overlay_path, base_opacity, overlay_opacity):
    """
    Renders two images stacked dynamically using CSS.
    Requires base_messy.png, base_clean.png, 
    lipstick_layer.png, and eyeshadow_layer.png in the same directory.
    """
    base_data = get_image_base64(base_path)
    overlay_data = get_image_base64(overlay_path)

    if not base_data:
        st.error(f"Missing required base image: {base_path}")
        return

    # Base HTML structure
    html_content = f"""
    <div class="glowup-container" style="position: relative; width: 100%; max-width: 600px; margin: auto;">
        <img src="data:image/png;base64,{base_data}" 
             class="doll-base" 
             style="width: 100%; height: auto; display: block; 
                    opacity: {base_opacity}; transition: opacity 0.5s ease;">
    """

    # Add Dynamic Overlay Layer (if available)
    if overlay_data:
        html_content += f"""
        <img src="data:image/png;base64,{overlay_data}" 
             class="doll-overlay" 
             style="position: absolute; top: 0; left: 0; width: 100%; height: auto; 
                    opacity: {overlay_opacity}; transition: opacity 0.5s ease; pointer-events: none;">
        """
    
    html_content += "</div>"
    st.components.v1.html(html_content, height=650)


# --- INITIALIZE STATE ---
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "welcome"
if "clean_progress" not in st.session_state:
    st.session_state.clean_progress = 0
if "lipstick_on" not in st.session_state:
    st.session_state.lipstick_on = False
if "eyeshadow_on" not in st.session_state:
    st.session_state.eyeshadow_on = False


# --- TITLE & MAIN INTERFACE ---
st.title("💖 Dynamic Doll Salon: The Glow-Up 💖")
st.write("Washing and Makeup: Dynamic Edition!")
st.markdown("---")

col1, col2 = st.columns([1, 1])

# --- DISPLAY AREA (LEFT COLUMN) ---
with col1:
    st.subheader("Your Doll")

    # STAGE: WELCOME/MESSY
    if st.session_state.game_stage == "welcome":
        render_dynamic_stage("base_messy.png", None, 1.0, 0.0)
    
    # STAGE: WASHING (Opacity Blend)
    elif st.session_state.game_stage == "washing":
        # Dynamic Opacity: As progress increases, clean face shows more, messy face shows less.
        clean_opacity = st.session_state.clean_progress / 100.0
        messy_opacity = 1.0 - clean_opacity
        render_dynamic_stage("base_clean.png", "base_messy.png", clean_opacity, messy_opacity)
        
    # STAGE: MAKEUP (Overlay Blend)
    elif st.session_state.game_stage == "makeup":
        # We start with the clean face as the base.
        # Then, we decide which makeup layer to dynamically display based on state.
        
        selected_layer = None
        layer_opacity = 0.0

        if st.session_state.lipstick_on:
            selected_layer = "lipstick_layer.png"
            layer_opacity = 1.0
        elif st.session_state.eyeshadow_on:
            selected_layer = "eyeshadow_layer.png"
            layer_opacity = 1.0
            
        render_dynamic_stage("base_clean.png", selected_layer, 1.0, layer_opacity)
        
    # STAGE: REVEAL (Final Clean State)
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
        
        # Note: We are only showing one makeup option at a time in this simple dynamic version.
        
        st.info("Dynamic Lip Option:")
        if st.checkbox("Apply Pink Lipstick 💄", value=st.session_state.lipstick_on):
            st.session_state.lipstick_on = True
            st.session_state.eyeshadow_on = False # Single select for demonstration
            st.rerun()
        else:
            if st.session_state.lipstick_on: # If was true and user unchecked
                st.session_state.lipstick_on = False
                st.rerun()

        st.info("Dynamic Eye Option:")
        if st.checkbox("Apply Sparkly Eyeshadow 👀", value=st.session_state.eyeshadow_on):
            st.session_state.eyeshadow_on = True
            st.session_state.lipstick_on = False # Single select for demonstration
            st.rerun()
        else:
            if st.session_state.eyeshadow_on: # If was true and user unchecked
                st.session_state.eyeshadow_on = False
                st.rerun()

        # Update text dynamically
        applied = []
        if st.session_state.lipstick_on: applied.append("Pink Lipstick")
        if st.session_state.eyeshadow_on: applied.append("Blue Eyeshadow")
        
        st.write(f"Current Look: **{' + '.join(applied) if applied else 'Clean Face'}**")

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
