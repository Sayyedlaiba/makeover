import streamlit as st

# Set up page configuration
st.set_page_config(page_title="✨ Doll Glow-Up Salon ✨", layout="centered")

# Initialize game state variables if they don't exist
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "washed_percentage" not in st.session_state:
    st.session_state.washed_percentage = 0
if "makeup_applied" not in st.session_state:
    st.session_state.makeup_applied = {"Lipstick": False, "Blush": False, "Eyeshadow": False}

# Title and Styling
st.title("✨ Doll Glow-Up Salon ✨")
st.markdown("---")

# ---------------- STAGE 1: INTRO ----------------
if st.session_state.stage == "intro":
    st.subheader("Welcome to the Glamour Salon!")
    st.write("Our doll needs a massive transformation. Let's start with a refreshing face wash!")
    
    # Placeholder for initial doll image
    st.info("📸 [Imagine a messy/muddy doll face here]")
    
    if st.button("Start Makeover 🧴"):
        st.session_state.stage = "wash"
        st.rerun()

# ---------------- STAGE 2: WASH FACE ----------------
elif st.session_state.stage == "wash":
    st.subheader("Step 1: Clean the Doll's Face")
    st.write("Click the scrub button to wash away the dirt!")
    
    # Progress bar simulates washing
    progress = st.session_state.washed_percentage
    st.progress(progress / 100)
    st.write(f"Cleanliness: {progress}%")
    
    # Visual feedback based on progress
    if progress < 50:
        st.warning("🧼 Scrubbing in progress... still a bit dirty!")
    elif progress < 100:
        st.info("✨ Getting cleaner! Almost there.")
    else:
        st.success("💖 Perfectly clean! Ready for makeup.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Scrub Face 🧽", disabled=(progress >= 100)):
            st.session_state.washed_percentage += 25
            st.rerun()
            
    with col2:
        if st.button("Proceed to Makeup 💄", disabled=(progress < 100)):
            st.session_state.stage = "makeup"
            st.rerun()

# ---------------- STAGE 3: MAKEUP ----------------
elif st.session_state.stage == "makeup":
    st.subheader("Step 2: Time for Glamour!")
    st.write("Select the cosmetics to apply to the doll's face:")

    # Checkboxes or buttons for makeup elements
    lip = st.checkbox("Apply Pink Lipstick 💄", value=st.session_state.makeup_applied["Lipstick"])
    blush = st.checkbox("Apply Rosy Blush 🎨", value=st.session_state.makeup_applied["Blush"])
    eye = st.checkbox("Apply Sparkly Eyeshadow 👀", value=st.session_state.makeup_applied["Eyeshadow"])
    
    # Update state based on user input
    st.session_state.makeup_applied["Lipstick"] = lip
    st.session_state.makeup_applied["Blush"] = blush
    st.session_state.makeup_applied["Eyeshadow"] = eye

    # Dynamic image text simulation
    applied_features = [k for k, v in st.session_state.makeup_applied.items() if v]
    st.info(f"📸 Current Doll Face Status: Clean + {', '.join(applied_features) if applied_features else 'No Makeup Yet'}")

    if st.button("Reveal Final Look 🎉"):
        st.session_state.stage = "reveal"
        st.rerun()

# ---------------- STAGE 4: REVEAL ----------------
elif st.session_state.stage == "reveal":
    st.subheader("👑 The Final Glow-Up! 👑")
    st.write("You did an amazing job! Look at that transformation!")
    
    # Final state display
    st.balloons()
    st.success("🌟 Stunning! 🌟")
    st.info("📸 [Imagine a beautiful, glowing doll face here with all your selected makeup!]")
    
    if st.button("Play Again 🔄"):
        # Reset everything
        st.session_state.stage = "intro"
        st.session_state.washed_percentage = 0
        st.session_state.makeup_applied = {"Lipstick": False, "Blush": False, "Eyeshadow": False}
        st.rerun()
