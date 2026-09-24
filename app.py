import streamlit as st
import requests

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


# =========================================================
# OPENROUTER AI STORY GENERATOR
# =========================================================

def generate_ai_story(idea, duration, style, character):

    api_key = st.secrets.get("OPENROUTER_API_KEY")

    if not api_key:
        return None, "OPENROUTER_API_KEY नहीं मिला। Streamlit Secrets check करो।"

    prompt = f"""
तुम AYANT Content AI के professional Hindi story writer हो।

यूज़र का वीडियो आइडिया:
{idea}

वीडियो duration:
{duration}

Visual style:
{style}

Character Lock:
{character}

इस idea पर एक engaging Hindi short-video story लिखो।

Rules:
- कहानी पूरी तरह हिंदी में हो।
- शुरुआत में strong hook हो।
- कहानी cinematic और visual हो।
- कहानी में suspense, emotion और curiosity हो जहाँ suitable हो।
- Main character की personality और appearance Character Lock के अनुसार रखो।
- कहानी duration के हिसाब से concise रखो।
- अनावश्यक explanation मत दो।
- केवल final story दो।
- Scene numbers मत दो।
- Image prompts मत दो।
- Image-to-video prompts मत दो।
- कहानी ऐसी हो जिसे बाद में अलग-अलग scenes में आसानी से तोड़ा जा सके।
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8,
            },
            timeout=120
        )

        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get(
                    "message",
                    response.text
                )
            except Exception:
                error_message = response.text

            return None, f"OpenRouter Error: {error_message}"

        data = response.json()

        story = data["choices"][0]["message"]["content"]

        return story.strip(), None

    except requests.exceptions.Timeout:
        return None, "AI response में बहुत समय लग रहा है। थोड़ी देर बाद फिर try करो।"

    except Exception as e:
        return None, f"Connection Error: {str(e)}"


# =========================================================
# MAIN WORKFLOW
# =========================================================

if st.button("🚀 STORY WORKFLOW START", type="primary"):

    if not idea.strip():
        st.warning("पहले अपनी story या video idea लिखो।")

    else:

        st.success("Content workflow शुरू हो गया!")

        st.markdown("## 🎬 VIDEO PLAN")

        st.write(f"**Duration:** {duration}")
        st.write(f"**Style:** {style}")
        st.write(f"**Format:** {aspect_ratio}")

        # =================================================
        # AI STORY GENERATION
        # =================================================

        with st.spinner("🤖 AI तुम्हारी कहानी लिख रहा है..."):

            generated_story, error = generate_ai_story(
                idea,
                duration,
                style,
                character
            )

        if error:

            st.error(error)

        else:

            st.markdown("## 📖 AI GENERATED STORY")

            st.write(generated_story)

            st.markdown("## 🔒 CHARACTER LOCK")

            st.code(character)

            # =================================================
            # IMAGE GENERATION MASTER PROMPT
            # =================================================

            st.markdown("## 🎨 IMAGE GENERATION MASTER PROMPT")

            image_prompt = f"""
Create a cinematic {style} scene for a {aspect_ratio} video.

Story:
{generated_story}

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

            # =================================================
            # IMAGE TO VIDEO MASTER PROMPT
            # =================================================

            st.markdown("## 🎥 IMAGE-TO-VIDEO MASTER PROMPT")

            video_prompt = f"""
Animate this image into a cinematic video.

Story context:
{generated_story}

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
                "AI Story Generation module successfully connected. "
                "अगले module में इसी generated story को automatic scenes "
                "में break करके हर scene के अलग image prompts और "
                "image-to-video prompts बनाए जा सकते हैं."
            )
