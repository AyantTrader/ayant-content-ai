import streamlit as st
import requests
import json
import re

st.set_page_config(
    page_title="AYANT Content AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AYANT Content AI")
st.caption(
    "Story → Continuity Lock → Scenes → Image Prompts → "
    "Image-to-Video Prompts → Google Flow"
)

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
# OPENROUTER REQUEST
# =========================================================

def openrouter_request(prompt):

    api_key = st.secrets.get("OPENROUTER_API_KEY")

    if not api_key:
        return None, "OPENROUTER_API_KEY नहीं मिला। Streamlit Secrets check करो।"

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
                "temperature": 0.7,
            },
            timeout=120
        )

        if response.status_code != 200:

            try:
                error_data = response.json()

                error_message = error_data.get(
                    "error",
                    {}
                ).get(
                    "message",
                    response.text
                )

            except Exception:
                error_message = response.text

            return None, f"OpenRouter Error: {error_message}"

        data = response.json()

        result = data["choices"][0]["message"]["content"]

        return result.strip(), None

    except requests.exceptions.Timeout:

        return None, "AI response में बहुत समय लग रहा है। फिर से try करो।"

    except Exception as e:

        return None, f"Connection Error: {str(e)}"


# =========================================================
# AI STORY
# =========================================================

def generate_ai_story(idea, duration, style, character):

    prompt = f"""
तुम AYANT Content AI के professional Hindi cinematic story writer हो।

USER VIDEO IDEA:
{idea}

VIDEO DURATION:
{duration}

VISUAL STYLE:
{style}

CHARACTER:
{character}

एक engaging Hindi short-video story लिखो।

RULES:

- पूरी कहानी हिंदी में हो।
- शुरुआत में strong hook हो।
- कहानी cinematic और visual हो।
- suspense और curiosity जहाँ suitable हो वहाँ रखो।
- Main character की identity और appearance बिल्कुल Character Lock के अनुसार रखो।
- कहानी duration के हिसाब से concise रखो।
- अनावश्यक characters या locations मत जोड़ो।
- केवल final story दो।
- Scene prompts मत दो।
- Image prompts मत दो।
- Video prompts मत दो।
"""

    return openrouter_request(prompt)


# =========================================================
# STORY CONTINUITY + SCENE BREAKDOWN
# =========================================================

def generate_continuity_and_scenes(
    story,
    duration,
    style,
    aspect_ratio,
    character
):

    prompt = f"""
तुम AYANT Content AI के strict cinematic continuity director हो।

STORY:
{story}

VIDEO DURATION:
{duration}

VISUAL STYLE:
{style}

FORMAT:
{aspect_ratio}

USER CHARACTER LOCK:
{character}

अब इस कहानी को production-ready scenes में break करो।

========================
STRICT CONTINUITY RULES
========================

CHARACTER LOCK:
Character का face, skin tone, age, body proportions, hairstyle,
beard/moustache, clothing, shoes और accessories हर relevant scene
में बिल्कुल same रहने चाहिए।

LOCATION LOCK:
एक बार location establish होने के बाद वही environment, architecture,
landscape, background, weather और lighting continuity maintain करो।
Location केवल तभी बदले जब कहानी में explicitly location change हो।

OBJECT LOCK:
Important objects की appearance, size, position और orientation
consistent रहनी चाहिए।

POSITION LOCK:
अगले scene में previous scene की अंतिम position, pose,
body orientation, hand/leg placement, expression और gaze को
natural continuation के रूप में carry forward करो।

MOVEMENT LOCK:
सिर्फ वही action/movement करो जो current scene में explicitly
लिखा है।

AI अपनी तरफ से:
- नया character
- नया object
- नया location
- extra movement
- extra action
- random camera movement

नहीं जोड़ेगा।

VISUAL STYLE LOCK:
पूरी story में {style} maintain करो।

FORMAT:
{aspect_ratio}

========================
OUTPUT
========================

पहले:

### STORY CONTINUITY LOCK

CHARACTERS:
...

LOCATION:
...

IMPORTANT OBJECTS:
...

TIME / WEATHER / LIGHTING:
...

VISUAL STYLE:
...

CONTINUITY RULE:
...

फिर हर scene:

### SCENE 1

DURATION:
...

ACTION:
...

CHARACTER POSITION:
...

EXPRESSION / GAZE:
...

LOCATION:
...

CAMERA:
...

IMAGE PROMPT:
...

IMAGE-TO-VIDEO PROMPT:
...

CONTINUITY FROM PREVIOUS SCENE:
...

फिर Scene 2 और आगे के सभी scenes इसी format में।

हर scene के IMAGE PROMPT और IMAGE-TO-VIDEO PROMPT में
locked character और location details maintain करो।
"""


    return openrouter_request(prompt)


# =========================================================
# COPYABLE SCENE PROMPTS
# =========================================================

def generate_copyable_scene_prompts(
    story,
    continuity_output,
    duration,
    style,
    aspect_ratio,
    character
):

    prompt = f"""
तुम AYANT Content AI के professional Google Flow prompt director हो।

STORY:
{story}

CONTINUITY + SCENE BREAKDOWN:
{continuity_output}

CHARACTER LOCK:
{character}

STYLE:
{style}

FORMAT:
{aspect_ratio}

तुम्हारा काम है ऊपर दिए गए scenes को final production prompts
में convert करना।

========================
STRICT RULES
========================

1. हर scene previous scene का natural continuation होना चाहिए।

2. Character की exact identity और appearance हर relevant scene में
same रखो।

3. Location और environment locked रहेंगे जब तक story explicitly
location change न करे।

4. Important objects locked रहेंगे।

5. Previous scene की अंतिम:
- position
- pose
- body orientation
- hand placement
- leg placement
- facial expression
- gaze direction

अगले scene में natural continuity के साथ carry forward होगी।

6. Current scene में केवल वही movement/action होगा जो story और
scene breakdown में explicitly दिया गया है।

7. अपनी तरफ से कोई:
- नया character
- नया object
- नया location
- extra movement
- extra action
- random event
- random camera movement

मत जोड़ो।

8. IMAGE PROMPT में image बनाने के लिए complete visual description दो।

9. IMAGE-TO-VIDEO PROMPT में केवल existing image को animate करो।
नई चीजें add मत करो।

10. Image-to-video prompt में character का appearance बदलना,
face बदलना, clothing बदलना, body morphing या object morphing
सख्त मना है।

11. Google Flow के लिए prompts English में लिखो।

========================
EXACT OUTPUT FORMAT
========================

हर scene के लिए EXACTLY:

SCENE_START

SCENE_NUMBER: 1

DURATION:
[duration]

IMAGE_PROMPT:
[complete English image prompt]

IMAGE_TO_VIDEO_PROMPT:
[complete English image-to-video prompt]

SCENE_END

फिर अगला scene:

SCENE_START

SCENE_NUMBER: 2

DURATION:
[duration]

IMAGE_PROMPT:
...

IMAGE_TO_VIDEO_PROMPT:
...

SCENE_END

इसी तरह सभी scenes दो।

कोई extra explanation मत दो।
"""


    return openrouter_request(prompt)


# =========================================================
# PARSE SCENES
# =========================================================

def parse_scenes(text):

    scenes = []

    blocks = re.findall(
        r"SCENE_START(.*?)SCENE_END",
        text,
        re.DOTALL
    )

    for block in blocks:

        number_match = re.search(
            r"SCENE_NUMBER:\s*(.*)",
            block
        )

        duration_match = re.search(
            r"DURATION:\s*(.*)",
            block
        )

        image_match = re.search(
            r"IMAGE_PROMPT:\s*(.*?)(?=\nIMAGE_TO_VIDEO_PROMPT:)",
            block,
            re.DOTALL
        )

        video_match = re.search(
            r"IMAGE_TO_VIDEO_PROMPT:\s*(.*)",
            block,
            re.DOTALL
        )

        if image_match and video_match:

            scenes.append({
                "number": (
                    number_match.group(1).strip()
                    if number_match else str(len(scenes) + 1)
                ),
                "duration": (
                    duration_match.group(1).strip()
                    if duration_match else ""
                ),
                "image_prompt": image_match.group(1).strip(),
                "video_prompt": video_match.group(1).strip()
            })

    return scenes


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
        # STORY
        # =================================================

        with st.spinner("🤖 AI तुम्हारी कहानी लिख रहा है..."):

            generated_story, story_error = generate_ai_story(
                idea,
                duration,
                style,
                character
            )


        if story_error:

            st.error(story_error)

        else:

            st.markdown("## 📖 AI GENERATED STORY")

            st.write(generated_story)


            # =================================================
            # CONTINUITY
            # =================================================

            with st.spinner(
                "🔒 Character, Location और Scene Continuity तैयार हो रही है..."
            ):

                continuity_output, continuity_error = (
                    generate_continuity_and_scenes(
                        generated_story,
                        duration,
                        style,
                        aspect_ratio,
                        character
                    )
                )


            if continuity_error:

                st.error(continuity_error)

            else:

                st.markdown(
                    "## 🔒 STORY CONTINUITY + SCENE BREAKDOWN"
                )

                st.write(continuity_output)


                # =================================================
                # COPYABLE GOOGLE FLOW PROMPTS
                # =================================================

                with st.spinner(
                    "🎨 हर scene के final Google Flow prompts बनाए जा रहे हैं..."
                ):

                    scene_output, scene_error = (
                        generate_copyable_scene_prompts(
                            generated_story,
                            continuity_output,
                            duration,
                            style,
                            aspect_ratio,
                            character
                        )
                    )


                if scene_error:

                    st.error(scene_error)

                else:

                    scenes = parse_scenes(scene_output)

                    st.markdown(
                        "## 🎬 GOOGLE FLOW — COPYABLE SCENE PROMPTS"
                    )

                    if not scenes:

                        st.warning(
                            "Scenes generate हुए लेकिन उनका format "
                            "read नहीं हो पाया। फिर से STORY WORKFLOW START करो।"
                        )

                    else:

                        st.success(
                            f"✅ {len(scenes)} scenes के prompts तैयार हैं।"
                        )

                        for scene in scenes:

                            st.markdown(
                                f"## 🎬 SCENE {scene['number']}"
                            )

                            if scene["duration"]:
                                st.caption(
                                    f"Duration: {scene['duration']}"
                                )

                            st.markdown("### 🎨 IMAGE PROMPT")

                            st.code(
                                scene["image_prompt"],
                                language="text"
                            )

                            st.markdown(
                                "### 🎥 IMAGE-TO-VIDEO PROMPT"
                            )

                            st.code(
                                scene["video_prompt"],
                                language="text"
                            )

                            st.divider()

                        st.success(
                            "🎉 सभी scene prompts Google Flow में "
                            "copy-paste करने के लिए तैयार हैं।"
                        )
