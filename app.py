import streamlit as st
import requests
import re
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AYANT Content AI",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# HINDI UI FONT
# =========================================================

st.markdown(
    """
    <style>
    .hindi-story,
    .hindi-story * {
        font-family: "Noto Sans Devanagari",
                     "Nirmala UI",
                     "Mangal",
                     sans-serif !important;
        line-height: 1.8 !important;
    }

    .hindi-story {
        font-size: 18px;
        white-space: normal;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# APP HEADER
# =========================================================

st.title("🎬 AYANT Content AI")

st.caption(
    "Story → Continuity Lock → Scenes → Start/End Frames → "
    "Image Prompts → Image-to-Video Prompts → Google Flow"
)

st.divider()


# =========================================================
# VIDEO INPUT
# =========================================================

st.subheader("📝 अपनी कहानी या वीडियो आइडिया लिखो")

idea = st.text_area(
    "Video idea",
    placeholder="उदाहरण: Ayant 5000 साल पीछे Dwapar Yuga में चला जाता है...",
    height=180
)


# =========================================================
# VIDEO SETTINGS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    duration = st.selectbox(
        "वीडियो duration",
        [
            "30 सेकंड",
            "60 सेकंड",
            "90 सेकंड",
            "2 मिनट"
        ]
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
        [
            "9:16 Vertical",
            "16:9 Horizontal",
            "1:1 Square"
        ]
    )


# =========================================================
# EXACT CLIP / IMAGE COUNT
# =========================================================

DURATION_CONFIG = {

    "30 सेकंड": {
        "clips": 4,
        "images": 8
    },

    "60 सेकंड": {
        "clips": 8,
        "images": 16
    },

    "90 सेकंड": {
        "clips": 12,
        "images": 24
    },

    "2 मिनट": {
        "clips": 15,
        "images": 30
    }
}


expected_clips = DURATION_CONFIG[duration]["clips"]
expected_images = DURATION_CONFIG[duration]["images"]


st.info(
    f"🎬 {duration} → {expected_clips} clips → "
    f"{expected_images} images → हर clip exactly 8 seconds"
)


# =========================================================
# FIXED AYANT CHARACTER LOCK
# =========================================================

FIXED_AYANT_CLOTHING = """
AYANT CLOTHING IS PERMANENTLY LOCKED.

Ayant must always wear exactly:

- black T-shirt
- the word "AYANT" clearly written in white letters on the FRONT
- the word "AYANT" clearly written in white letters on the BACK
- black pants
- clean white shoes

These details MUST remain identical in every scene and every frame.

Do NOT change:
- shirt color
- shirt design
- shirt text
- pants color
- shoes
- clothing style
- wardrobe
- accessories

No wardrobe change.
No clothing variation.
No clothing morphing.
No outfit redesign.
No added clothing.
No removed clothing.
"""


# =========================================================
# CHARACTER LOCK INPUT
# =========================================================

st.subheader("🔒 Character Lock")

character = st.text_area(
    "अगर कोई मुख्य character है तो उसकी fixed appearance यहाँ लिखो",
    value=(
        "Ayant: young Indian male, wheatish skin, brown eyes, "
        "short trimmed beard and moustache, black hair tied in a high "
        "man-bun/top-knot, consistent face, body proportions and "
        "appearance across all scenes."
    ),
    height=120
)


st.info(
    "🔒 Character + Clothing Lock | "
    "📍 Location Lock | "
    "🧱 Object Lock | "
    "🔄 Pose/Position Continuity | "
    f"🎬 {expected_clips} clips | "
    f"🖼️ {expected_images} images | "
    "⏱️ Every clip exactly 8 seconds"
)


# =========================================================
# OPENROUTER REQUEST
# =========================================================

def openrouter_request(prompt):

    api_key = st.secrets.get("OPENROUTER_API_KEY")

    if not api_key:

        return (
            None,
            "OPENROUTER_API_KEY नहीं मिला। Streamlit Secrets check करो।"
        )

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

                error_message = (
                    error_data
                    .get("error", {})
                    .get("message", response.text)
                )

            except Exception:

                error_message = response.text


            return (
                None,
                f"OpenRouter Error: {error_message}"
            )


        data = response.json()

        result = data["choices"][0]["message"]["content"]

        return result.strip(), None


    except requests.exceptions.Timeout:

        return (
            None,
            "AI response में बहुत समय लग रहा है। फिर से try करो।"
        )


    except Exception as e:

        return (
            None,
            f"Connection Error: {str(e)}"
        )


# =========================================================
# AI STORY
# =========================================================

def generate_ai_story(
    idea,
    duration,
    style,
    character,
    expected_clips
):

    prompt = f"""
तुम AYANT Content AI के professional Hindi cinematic story writer हो।

USER VIDEO IDEA:
{idea}

VIDEO DURATION:
{duration}

EXACT CLIP COUNT:
{expected_clips}

IMPORTANT:

इस project में:

- 1 clip = exactly 8 seconds
- हर clip के लिए 2 images होंगी
- Image 1 = Start Frame
- Image 2 = End Frame
- दोनों images से 1 video clip बनेगी

इसलिए इस कहानी को EXACTLY {expected_clips} sequential
8-second clips के लिए design करो।

VISUAL STYLE:
{style}

FORMAT:
{aspect_ratio}

USER CHARACTER LOCK:
{character}

PERMANENT AYANT CLOTHING LOCK:
{FIXED_AYANT_CLOTHING}

STORY RULES:

- पूरी कहानी साफ़ और natural Hindi में लिखो।
- Hindi sentences के लिए standard Unicode Devanagari इस्तेमाल करो।
- Chinese, Japanese या random decorative Unicode characters मत इस्तेमाल करो।
- Strong hook से शुरुआत करो।
- कहानी cinematic और visual हो।
- कहानी एक continuous story हो।
- हर अगला भाग पिछले भाग से naturally continue हो।
- कहानी को EXACTLY {expected_clips} sequential clips में divide
  करने योग्य बनाओ।
- हर clip में केवल वही action हो जो 8 seconds में naturally हो सके।
- अनावश्यक characters मत जोड़ो।
- अनावश्यक locations मत बदलो।
- Main character की identity और appearance consistent रखो।
- अगर Ayant story में है तो उसका fixed clothing lock हर scene में लागू होगा।
- कहानी में अचानक wardrobe change मत करो।
- कहानी में अचानक environment change मत करो।
- random events मत जोड़ो।

IMPORTANT VISUAL TEXT RULE:

Generated images और videos में कोई unnecessary written text नहीं होना चाहिए।

No:
- subtitles
- captions
- random letters
- random words
- labels
- posters
- banners
- watermarks
- typography
- random logos
- signs containing readable text

EXCEPTION:
Ayant के black T-shirt पर explicitly requested white "AYANT"
text allowed और permanently locked है।

केवल final story दो।
Scene prompts मत दो।
Image prompts मत दो।
Video prompts मत दो।
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
    character,
    expected_clips
):

    prompt = f"""
तुम AYANT Content AI के STRICT cinematic continuity director हो।

STORY:
{story}

VIDEO DURATION:
{duration}

EXACT REQUIRED CLIP COUNT:
{expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS

VISUAL STYLE:
{style}

FORMAT:
{aspect_ratio}

USER CHARACTER LOCK:
{character}

PERMANENT AYANT CLOTHING LOCK:
{FIXED_AYANT_CLOTHING}


==================================================
ABSOLUTE SCENE COUNT RULE
==================================================

GENERATE EXACTLY {expected_clips} CLIPS/SCENES.

NOT 3.
NOT {expected_clips - 1}.
NOT {expected_clips + 1}.

EXACTLY {expected_clips} scenes only.


==================================================
CHARACTER LOCK
==================================================

हर character का:

- face
- identity
- age
- skin tone
- body proportions
- height/proportions
- hairstyle
- beard/moustache
- clothing
- clothing colors
- clothing design
- shoes
- accessories

LOCKED रहेगा।

जब कोई character पहली बार दिखाई देता है,
उसका complete visual identity और outfit establish करो।

उसके बाद उस character के सभी later scenes में वही exact
appearance और wardrobe maintain करो।

Character का look केवल तभी बदल सकता है जब USER STORY
explicitly clothing/look change मांगती हो।

AI अपनी तरफ से कोई wardrobe change नहीं करेगा।


==================================================
AYANT LOCK
==================================================

अगर Ayant scene में मौजूद है तो:

- same face
- same skin tone
- same body proportions
- same hairstyle
- same beard/moustache
- black T-shirt
- white "AYANT" front text
- white "AYANT" back text
- black pants
- white shoes

हर scene और हर frame में exactly same रहेंगे।


==================================================
LOCATION LOCK
==================================================

हर location का canonical environment establish करो।

Location में बिना explicit story change के कोई बदलाव नहीं होगा।

Lock:

- architecture
- landscape
- trees
- buildings
- roads
- ground
- background
- weather
- atmosphere
- time of day
- lighting conditions

AI अपनी तरफ से नया location नहीं बनाएगा।


==================================================
OBJECT LOCK
==================================================

Important objects का:

- appearance
- size
- shape
- color
- position
- orientation

consistent रहेगा।

AI अपनी तरफ से नया important object add नहीं करेगा।


==================================================
POSITION / POSE LOCK
==================================================

हर scene पिछले scene के END STATE से continue होगा।

Carry forward:

- character position
- body orientation
- pose
- hand placement
- leg placement
- facial expression
- gaze direction
- object positions
- ongoing action state


==================================================
MOVEMENT LOCK
==================================================

Current scene में केवल वही movement/action होगा
जो story में required है।

AI अपनी तरफ से:

- extra movement
- extra action
- random event
- random camera movement
- random character reaction

नहीं जोड़ेगा।


==================================================
START FRAME / END FRAME SYSTEM
==================================================

हर scene/clip में EXACTLY 2 images होंगी:

1. START FRAME
2. END FRAME

इन दोनों images के बीच 1 video clip बनेगी।

Scene N का END FRAME,
Scene N+1 के START FRAME का exact continuity reference होगा।

इसलिए:

Scene 1 End
↓
Scene 2 Start

Scene 2 End
↓
Scene 3 Start

और इसी तरह पूरी story में continuity maintain करो।


==================================================
8 SECOND LOCK
==================================================

हर clip EXACTLY 8 SECONDS की होगी।

हर scene का action 8-second timeline में naturally fit होना चाहिए।


==================================================
VISUAL TEXT RULE
==================================================

Images/videos में कोई unnecessary text generate मत करो।

Do not add:

- subtitles
- captions
- random letters
- random words
- labels
- posters
- banners
- watermarks
- typography
- random logos
- readable signs

EXCEPTION:

Ayant के T-shirt पर explicitly requested white "AYANT"
text allowed है।


==================================================
VISUAL STYLE LOCK
==================================================

पूरी story में:

{style}

maintain करो।

FORMAT:

{aspect_ratio}


==================================================
OUTPUT
==================================================

पहले:

### STORY CONTINUITY LOCK

CHARACTERS:
...

AYANT CLOTHING LOCK:
...

OTHER CHARACTER CLOTHING LOCK:
...

LOCATIONS:
...

IMPORTANT OBJECTS:
...

TIME / WEATHER / LIGHTING:
...

VISUAL STYLE:
...

CLIP COUNT:
Exactly {expected_clips}

CLIP DURATION:
Exactly 8 seconds each

FRAME SYSTEM:
Start Frame + End Frame per clip

CONTINUITY RULE:
...

फिर EXACTLY {expected_clips} scenes दो।

हर scene:

### SCENE 1

DURATION:
EXACTLY 8 SECONDS

ACTION:
...

START FRAME:
...

END FRAME:
...

CHARACTER POSITION:
...

EXPRESSION / GAZE:
...

LOCATION:
...

OBJECTS:
...

CAMERA:
...

CONTINUITY FROM PREVIOUS SCENE:
...

फिर Scene 2...

और इसी तरह EXACTLY {expected_clips} scenes।

कोई extra scene मत बनाओ।
"""


    return openrouter_request(prompt)


# =========================================================
# FINAL GOOGLE FLOW PROMPTS
# =========================================================

def generate_copyable_scene_prompts(
    story,
    continuity_output,
    duration,
    style,
    aspect_ratio,
    character,
    expected_clips
):

    prompt = f"""
तुम AYANT Content AI के professional Google Flow prompt director हो।

STORY:
{story}

CONTINUITY + SCENE BREAKDOWN:
{continuity_output}

CHARACTER LOCK:
{character}

PERMANENT AYANT CLOTHING LOCK:
{FIXED_AYANT_CLOTHING}

STYLE:
{style}

FORMAT:
{aspect_ratio}

REQUIRED CLIPS:
EXACTLY {expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS


==================================================
ABSOLUTE COUNT RULE
==================================================

Generate EXACTLY {expected_clips} scenes.

Each scene = one video clip.

Each scene MUST contain:

1. START FRAME IMAGE PROMPT
2. END FRAME IMAGE PROMPT
3. ONE IMAGE-TO-VIDEO PROMPT

Therefore total output must contain:

{expected_clips} Start Frame image prompts
+
{expected_clips} End Frame image prompts
+
{expected_clips} video prompts.


==================================================
CRITICAL CONTINUITY
==================================================

Scene 1 establishes the initial visual state.

For every next scene:

Scene N START FRAME must naturally continue
from Scene N-1 END FRAME.

Do not reset the character.
Do not reset the location.
Do not reset objects.
Do not reset pose.
Do not reset clothing.

The next scene must feel like the exact next moment
of the previous scene.


==================================================
CHARACTER LOCK
==================================================

Every character must maintain:

- same face
- same identity
- same age
- same skin tone
- same body proportions
- same hairstyle
- same beard/moustache
- same clothing
- same clothing colors
- same clothing design
- same shoes
- same accessories

No character redesign.

No face morphing.

No body morphing.

No hairstyle change.

No wardrobe change unless explicitly required by the user story.


==================================================
AYANT CLOTHING LOCK
==================================================

Whenever Ayant appears:

BLACK T-SHIRT
WHITE "AYANT" TEXT ON FRONT
WHITE "AYANT" TEXT ON BACK
BLACK PANTS
WHITE SHOES

These details MUST remain exactly identical
in every Start Frame, End Frame and video clip.

No clothing variation.
No wardrobe change.
No color change.
No redesign.


==================================================
LOCATION LOCK
==================================================

Maintain exact:

- environment
- architecture
- landscape
- background
- weather
- time of day
- lighting
- atmosphere

unless story explicitly changes location.

No random location changes.


==================================================
OBJECT LOCK
==================================================

Important objects must retain:

- same appearance
- same size
- same color
- same shape
- same position
- same orientation

unless the story explicitly moves them.


==================================================
POSITION / POSE / GAZE CONTINUITY
==================================================

Carry forward the previous End Frame state:

- position
- pose
- body orientation
- hand placement
- leg placement
- facial expression
- gaze direction
- object positions
- ongoing movement state

Only change what the current action explicitly requires.


==================================================
MOVEMENT LOCK
==================================================

Do not add:

- new movement
- new action
- random reaction
- random event
- random camera movement
- new character
- new object
- new location


==================================================
IMAGE PROMPT RULE
==================================================

Each image prompt must describe the COMPLETE visual state
required for that frame.

The Start Frame and End Frame must look like two
consistent moments of the SAME scene.

Do not create unrelated images.


==================================================
IMAGE-TO-VIDEO RULE
==================================================

Animate ONLY the existing Start Frame toward the End Frame.

Do not introduce anything that is not already established.

No:

- character morphing
- face changing
- clothing changing
- body changing
- object morphing
- location changing
- random new elements
- random camera movement


==================================================
VISUAL TEXT RULE
==================================================

Do NOT generate:

- subtitles
- captions
- random text
- random letters
- random words
- labels
- posters
- banners
- watermarks
- typography
- random logos
- readable signs

EXCEPTION:

Ayant's explicitly requested white "AYANT" T-shirt text
is allowed and must remain locked.


==================================================
GOOGLE FLOW
==================================================

All IMAGE PROMPTS and IMAGE-TO-VIDEO PROMPTS
must be written in English.

Every video prompt MUST explicitly contain:

Duration: exactly 8 seconds.


==================================================
EXACT OUTPUT FORMAT
==================================================

SCENE_START

SCENE_NUMBER: 1

DURATION:
EXACTLY 8 SECONDS

START_FRAME_IMAGE_PROMPT:
[complete English prompt]

END_FRAME_IMAGE_PROMPT:
[complete English prompt]

IMAGE_TO_VIDEO_PROMPT:
[complete English prompt]

SCENE_END


Then Scene 2.

Continue until exactly {expected_clips} scenes.

DO NOT generate fewer scenes.
DO NOT generate more scenes.
DO NOT add explanations.
"""


    return openrouter_request(prompt)


# =========================================================
# PARSE FINAL SCENES
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

        start_match = re.search(
            r"START_FRAME_IMAGE_PROMPT:\s*(.*?)(?=\nEND_FRAME_IMAGE_PROMPT:)",
            block,
            re.DOTALL
        )

        end_match = re.search(
            r"END_FRAME_IMAGE_PROMPT:\s*(.*?)(?=\nIMAGE_TO_VIDEO_PROMPT:)",
            block,
            re.DOTALL
        )

        video_match = re.search(
            r"IMAGE_TO_VIDEO_PROMPT:\s*(.*)",
            block,
            re.DOTALL
        )

        if start_match and end_match and video_match:

            scenes.append(
                {
                    "number": (
                        number_match.group(1).strip()
                        if number_match
                        else str(len(scenes) + 1)
                    ),

                    "duration": "EXACTLY 8 SECONDS",

                    "start_frame_prompt": (
                        start_match.group(1).strip()
                    ),

                    "end_frame_prompt": (
                        end_match.group(1).strip()
                    ),

                    "video_prompt": (
                        video_match.group(1).strip()
                    )
                }
            )

    return scenes


# =========================================================
# MAIN WORKFLOW
# =========================================================

if st.button(
    "🚀 STORY WORKFLOW START",
    type="primary"
):

    if not idea.strip():

        st.warning(
            "पहले अपनी story या video idea लिखो।"
        )

    else:

        st.success(
            "Content workflow शुरू हो गया!"
        )


        # =================================================
        # VIDEO PLAN
        # =================================================

        st.markdown(
            "## 🎬 VIDEO PLAN"
        )

        st.write(
            f"**Selected Duration:** {duration}"
        )

        st.write(
            f"**Clips:** {expected_clips}"
        )

        st.write(
            f"**Images:** {expected_images}"
        )

        st.write(
            "**Images per Clip:** 2 "
            "(Start Frame + End Frame)"
        )

        st.write(
            "**Clip Duration:** EXACTLY 8 SECONDS"
        )

        st.write(
            f"**Style:** {style}"
        )

        st.write(
            f"**Format:** {aspect_ratio}"
        )


        # =================================================
        # STORY
        # =================================================

        with st.spinner(
            "🤖 AI तुम्हारी कहानी लिख रहा है..."
        ):

            generated_story, story_error = (
                generate_ai_story(
                    idea,
                    duration,
                    style,
                    character,
                    expected_clips
                )
            )


        if story_error:

            st.error(
                story_error
            )

        else:

            st.markdown(
                "## 📖 AI GENERATED STORY"
            )

            safe_story = html.escape(
                generated_story
            ).replace(
                "\n",
                "<br>"
            )

            st.markdown(
                f"""
                <div class="hindi-story">
                    {safe_story}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # CONTINUITY
            # =================================================

            with st.spinner(
                "🔒 Characters, Clothing, Location, Objects और "
                "Scene Continuity तैयार हो रही है..."
            ):

                continuity_output, continuity_error = (
                    generate_continuity_and_scenes(
                        generated_story,
                        duration,
                        style,
                        aspect_ratio,
                        character,
                        expected_clips
                    )
                )


            if continuity_error:

                st.error(
                    continuity_error
                )

            else:

                st.markdown(
                    "## 🔒 STORY CONTINUITY + SCENE BREAKDOWN"
                )

                st.write(
                    continuity_output
                )


                # =================================================
                # FINAL PROMPTS
                # =================================================

                with st.spinner(
                    "🎨 Start Frame, End Frame और "
                    "Image-to-Video prompts बनाए जा रहे हैं..."
                ):

                    scene_output, scene_error = (
                        generate_copyable_scene_prompts(
                            generated_story,
                            continuity_output,
                            duration,
                            style,
                            aspect_ratio,
                            character,
                            expected_clips
                        )
                    )


                if scene_error:

                    st.error(
                        scene_error
                    )

                else:

                    scenes = parse_scenes(
                        scene_output
                    )


                    st.markdown(
                        "## 🎬 GOOGLE FLOW — COPYABLE PROMPTS"
                    )


                    # =================================================
                    # COUNT VALIDATION
                    # =================================================

                    if len(scenes) != expected_clips:

                        st.warning(
                            f"⚠️ AI ने {expected_clips} scenes की जगह "
                            f"{len(scenes)} scenes read किए। "
                            f"Workflow को दोबारा START करना बेहतर रहेगा।"
                        )


                    else:

                        st.success(
                            f"✅ EXACTLY {expected_clips} clips तैयार हैं | "
                            f"🖼️ EXACTLY {expected_images} images के prompts | "
                            f"🎥 {expected_clips} video prompts"
                        )


                    # =================================================
                    # DISPLAY EACH SCENE
                    # =================================================

                    for scene in scenes:

                        st.markdown(
                            f"## 🎬 CLIP / SCENE {scene['number']}"
                        )

                        st.caption(
                            "Duration: EXACTLY 8 SECONDS | "
                            "2 Images: Start Frame + End Frame"
                        )


                        # ---------------------------------------------
                        # START FRAME
                        # ---------------------------------------------

                        st.markdown(
                            "### 🟢 START FRAME — IMAGE PROMPT"
                        )

                        st.code(
                            scene["start_frame_prompt"],
                            language="text"
                        )


                        # ---------------------------------------------
                        # END FRAME
                        # ---------------------------------------------

                        st.markdown(
                            "### 🔴 END FRAME — IMAGE PROMPT"
                        )

                        st.code(
                            scene["end_frame_prompt"],
                            language="text"
                        )


                        # ---------------------------------------------
                        # VIDEO
                        # ---------------------------------------------

                        st.markdown(
                            "### 🎥 IMAGE-TO-VIDEO PROMPT"
                        )

                        st.code(
                            scene["video_prompt"],
                            language="text"
                        )


                        st.divider()


                    # =================================================
                    # FINAL SUMMARY
                    # =================================================

                    if len(scenes) == expected_clips:

                        st.success(
                            "🎉 Workflow complete! "
                            f"{expected_clips} clips × 2 images = "
                            f"{expected_images} images और "
                            f"{expected_clips} Image-to-Video prompts "
                            "Google Flow के लिए तैयार हैं।"
                        )
