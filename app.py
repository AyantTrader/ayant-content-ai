import streamlit as st

st.set_page_config(
    page_title="AYANT Content AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AYANT Content AI")
st.caption("Story → Scenes → Image Prompts → Image-to-Video Prompts")

st.divider()

st.subheader("📝 अपनी कहानी या वीडियो आइडिया लिखो")

idea = st.text_area(
    "Video idea",
    placeholder="उदाहरण: Ayant 5000 साल पीछे Dwapar Yuga में चला जाता है...",
    height=180
)

col1, col2, col3 = st.columns(3)

with col1:
    duration = st.selectbox(
        "वीडियो duration",
        ["30 सेकंड", "60 सेकंड", "90 सेकंड", "2 मिनट"]
    )

with col2:
    style = st.selectbox(
        "Visual Style",
        [
            "Cinematic Semi-Realistic 3D",
            "Realistic Cinematic",
            "3D Animated",
            "Epic Historical"
        ]
    )

with col3:
    aspect_ratio = st.selectbox(
        "Format",
        ["9:16 Vertical", "16:9 Horizontal", "1:1 Square"]
    )

st.subheader("🔒 Character Lock")

character = st.text_area(
    "अगर कोई मुख्य character है तो उसकी fixed appearance यहाँ लिखो",
    value=(
        "Ayant: young Indian male, wheatish skin, brown eyes, "
        "short trimmed beard and moustache, black hair tied in a high "
        "man-bun/top-knot, consistent face, body and clothing across "
        "all scenes."
    ),
    height=120
)

if st.button("🚀 STORY WORKFLOW START", type="primary"):

    if not idea.strip():
        st.warning("पहले अपनी story या video idea लिखो।")
    else:

        st.success("Content workflow तैयार है!")

        st.markdown("## 🎬 VIDEO PLAN")

        st.write(f"**Duration:** {duration}")
        st.write(f"**Style:** {style}")
        st.write(f"**Format:** {aspect_ratio}")

        st.markdown("## 📖 STORY IDEA")
        st.write(idea)

        st.markdown("## 🔒 CHARACTER LOCK")
        st.code(character)

        st.markdown("## 🎨 IMAGE GENERATION MASTER PROMPT")

        image_prompt = f"""
Create a cinematic {style} scene for a {aspect_ratio} video.

Story:
{idea}

Character continuity:
{character}

Important:
- Keep the main character's face identical in every scene.
- Keep hairstyle identical.
- Keep body proportions identical.
- Keep clothing identical unless the story explicitly requires a change.
- Maintain the same cinematic visual language.
- High detail.
- Strong cinematic lighting.
- Realistic environment.
- Consistent character design.
"""

        st.code(image_prompt, language="text")

        st.markdown("## 🎥 IMAGE-TO-VIDEO MASTER PROMPT")

        video_prompt = f"""
Animate this image into a cinematic video.

Story context:
{idea}

Character continuity:
{character}

Animation instructions:
- Preserve the exact character appearance.
- Do not change face, hairstyle, clothing or body proportions.
- Natural body movement.
- Natural facial expressions.
- Cinematic camera movement.
- Realistic environmental motion.
- No random new characters.
- No object morphing.
- No character deformation.
- Keep the original composition consistent.
"""

        st.code(video_prompt, language="text")

        st.info(
            "यह पहला base version है। अगले modules में AI story writing, "
            "automatic scene breakdown, अलग-अलग scene prompts, "
            "character locking और Google Flow workflow जोड़ा जाएगा."
        )
