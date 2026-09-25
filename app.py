import streamlit as st
import requests

st.set_page_config(
    page_title="AYANT Content AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AYANT Content AI")
st.caption("Story → Continuity Lock → Scenes → Image Prompts → Image-to-Video Prompts")

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

नीचे एक पूरी कहानी दी गई है।

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

सबसे महत्वपूर्ण नियम:

========================
🔒 CONTINUITY RULES
========================

1. CHARACTER LOCK:
जो character शुरुआत में establish होता है, उसकी:
- face
- skin tone
- age
- body proportions
- hairstyle
- beard/moustache
- clothing
- shoes
- accessories

हर relevant scene में बिल्कुल same रहने चाहिए।

2. LOCATION LOCK:
Story में जो मुख्य location establish होती है, उसका:
- environment
- architecture
- landscape
- trees
- buildings
- background
- weather
- time-of-day

बिना कहानी में बदलाव के नहीं बदलना चाहिए।

3. OBJECT LOCK:
जो important objects पहले establish होते हैं, उनकी:
- appearance
- size
- position
- orientation

consistent रहनी चाहिए।

4. POSITION CONTINUITY:
हर अगला scene पिछले scene का natural continuation होना चाहिए।

Character की:
- exact position
- body orientation
- hand position
- leg position
- pose
- facial expression
- gaze direction

जहाँ तक story अनुमति देती है, carry forward करो।

5. MOVEMENT RULE:
हर scene में केवल वही movement/action होगा जो उस scene में explicitly लिखा गया है।

AI अपनी तरफ से:
- extra walking
- extra running
- extra hand movement
- extra characters
- extra objects
- extra actions
- random camera movement

नहीं जोड़ेगा।

6. NO RANDOM ADDITIONS:
Story में जो establish नहीं हुआ है, उसे अपनी तरफ से add मत करो।

7. NATURAL CONTINUATION:
Scene 2 को Scene 1 के अंतिम moment से naturally continue होना चाहिए।
Scene 3 को Scene 2 के अंतिम moment से continue होना चाहिए।

8. VISUAL STYLE LOCK:
पूरी story में वही visual style maintain करो:
{style}

9. FORMAT:
हर scene {aspect_ratio} के लिए बनाया जाएगा।

========================
OUTPUT FORMAT
========================

पहले:

### STORY CONTINUITY LOCK

CHARACTERS:
[सभी characters की exact fixed appearance]

LOCATION:
[मुख्य location की exact fixed description]

IMPORTANT OBJECTS:
[सभी important objects]

TIME / WEATHER / LIGHTING:
[fixed details]

VISUAL STYLE:
{style}

CONTINUITY RULE:
[एक strict continuity paragraph]

फिर scenes दो।

हर scene exactly इस format में:

### SCENE 1

DURATION:
[scene duration]

ACTION:
[सिर्फ इस scene में होने वाला exact action]

CHARACTER POSITION:
[character की exact position और body orientation]

EXPRESSION / GAZE:
[exact expression और gaze]

LOCATION:
[locked location को maintain करते हुए]

CAMERA:
[इस scene के लिए camera]

IMAGE PROMPT:
[पूरा detailed image-generation prompt]

IMAGE-TO-VIDEO PROMPT:
[सिर्फ established image को animate करने वाला prompt]

CONTINUITY FROM PREVIOUS SCENE:
[पहले scene में: N/A
अगले scenes में पिछले scene के अंतिम state से exact continuation]

IMPORTANT:
हर scene के IMAGE PROMPT में CHARACTER LOCK और LOCATION LOCK की आवश्यक details automatically repeat करो।

हर scene के IMAGE-TO-VIDEO PROMPT में भी वही continuity rules repeat करो।

कोई नया character, location, object या movement अपने आप मत जोड़ो।
"""


    return openrouter_request(prompt)


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
        # STORY GENERATION
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
            # CONTINUITY + SCENES
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

                st.success(
                    "✅ Story, Character Lock, Location Lock और "
                    "Scene Continuity तैयार हो गई।"
                )

                st.info(
                    "अगले module में इसी structure को अलग-अलग "
                    "copyable Scene 1, Scene 2, Scene 3 prompts "
                    "और Google Flow workflow में convert किया जा सकता है।"
                )
