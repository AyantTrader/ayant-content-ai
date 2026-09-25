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
    "Story → Master Continuity Bible → Scene State Lock → "
    "Start/End Frames → Image Prompts → Image-to-Video Prompts → Google Flow"
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
    "🔒 Character Lock | "
    "🏞️ Background Lock | "
    "🧱 Object Lock | "
    "🔄 End→Start Continuity | "
    "🗣️ Hindi Dialogue Lock | "
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
You are AYANT Content AI, a professional cinematic Hindi story writer.

USER VIDEO IDEA:
{idea}

VIDEO DURATION:
{duration}

EXACT CLIP COUNT:
{expected_clips}

VISUAL STYLE:
{style}

FORMAT:
{aspect_ratio}

CHARACTER:
{character}

PERMANENT AYANT CLOTHING:
{FIXED_AYANT_CLOTHING}

Write one continuous cinematic Hindi story designed for EXACTLY
{expected_clips} sequential video clips.

IMPORTANT STORY RULES:

1. The story must be written in clean, natural STANDARD HINDI.
2. Use ONLY standard Unicode Devanagari for Hindi text.
3. Do NOT use Chinese, Japanese, Arabic, Persian, random symbols,
   decorative Unicode or fake-looking characters.
4. If characters speak dialogue, their dialogue must be natural
   spoken Hindi in Devanagari.
5. NEVER invent a different language for character dialogue.
6. If the story does not require dialogue, characters must NOT
   randomly speak.
7. Do not add random dialogue just to fill the scene.
8. The story must be one continuous sequence of events.
9. Every clip must naturally continue from the previous clip.
10. Do not randomly change location, environment, weather or time.
11. Do not randomly change character clothing.
12. Do not randomly change important objects.
13. Avoid unnecessary characters.
14. Avoid unnecessary locations.
15. Every clip must contain an action that can naturally happen
    within exactly 8 seconds.
16. Do not describe image prompts or video prompts.
17. Do not add production instructions.

VISUAL CONTINUITY:

The same environment should remain visually consistent unless
the story explicitly requires a location change.

Important objects introduced in the story must remain the same
objects throughout the story unless the story explicitly changes them.

Only explicitly required changes are allowed.

Return ONLY the final Hindi story.
"""

    return openrouter_request(prompt)


# =========================================================
# MASTER CONTINUITY + SCENE STATE
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
You are AYANT Content AI's STRICT MASTER CONTINUITY DIRECTOR.

Your job is NOT simply to divide the story into scenes.

Your job is to create a MASTER CONTINUITY BIBLE and a precise
scene-to-scene STATE TRANSFER system so that every generated
image looks like the next moment of the SAME world.

==================================================
STORY
==================================================

{story}

==================================================
VIDEO SETTINGS
==================================================

DURATION:
{duration}

EXACT CLIP COUNT:
{expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS

STYLE:
{style}

FORMAT:
{aspect_ratio}

USER CHARACTER LOCK:
{character}

PERMANENT AYANT CLOTHING:
{FIXED_AYANT_CLOTHING}


==================================================
ABSOLUTE COUNT
==================================================

Generate EXACTLY {expected_clips} scenes.

No fewer.
No more.

Exactly {expected_clips}.


==================================================
MASTER CHARACTER BIBLE
==================================================

For EVERY recurring character establish a permanent identity.

Lock:

- face shape
- facial features
- eye shape
- eye color
- eyebrows
- nose
- lips
- skin tone
- age
- height
- body proportions
- hairstyle
- beard
- moustache
- clothing
- clothing colors
- clothing design
- shoes
- accessories

Once established, these details MUST be repeated consistently.

Never redesign a character between scenes.

Never randomly change:

- face
- hair
- beard
- body
- clothes
- shoes
- accessories


==================================================
AYANT MASTER LOCK
==================================================

Ayant MUST remain exactly:

{character}

AND:

{FIXED_AYANT_CLOTHING}

This applies to EVERY Start Frame, End Frame and video.

No variation.


==================================================
MASTER LOCATION / BACKGROUND BIBLE
==================================================

For every location create an exact canonical environment description.

Lock:

- architecture
- walls
- doors
- windows
- floor
- road
- trees
- plants
- mountains
- buildings
- furniture
- landscape
- horizon
- background structures
- foreground structures
- weather
- atmosphere
- season
- time of day
- lighting direction
- lighting intensity
- shadows
- color mood

IMPORTANT:

Do NOT merely write "same background".

Describe the exact background elements.

Every later scene in the same location MUST use the SAME
canonical background description.

Do not replace trees.
Do not replace buildings.
Do not redesign architecture.
Do not move the environment.
Do not change weather.
Do not change time of day.
Do not change lighting.

A location may change ONLY when the story explicitly changes location.


==================================================
MASTER OBJECT BIBLE
==================================================

For EVERY important object establish:

- exact object identity
- type
- material
- color
- shape
- size
- visible details
- condition
- orientation
- current holder
- which hand
- exact hand position
- relationship to body
- relationship to environment

Example:

If Ayant holds a red smartphone in his right hand,
later scenes must explicitly describe THE SAME RED SMARTPHONE
with the same shape, color, size and position in Ayant's
right hand.

Do NOT replace it with another phone.

Do NOT change its color.

Do NOT change its size.

Do NOT make it disappear.

Do NOT invent a second object.

Objects can move ONLY when the story explicitly moves them.


==================================================
MASTER POSE / STATE BIBLE
==================================================

At the end of every scene record the exact state:

- character position
- body orientation
- head direction
- gaze direction
- facial expression
- torso orientation
- left hand position
- right hand position
- left leg position
- right leg position
- object position
- object orientation
- ongoing movement state

This END STATE becomes the next scene's START STATE.


==================================================
END → START HARD LINK
==================================================

This is ABSOLUTE.

SCENE 1 END STATE
MUST become
SCENE 2 START STATE.

SCENE 2 END STATE
MUST become
SCENE 3 START STATE.

Continue this for the entire story.

The next scene is NOT a fresh image.

It is the exact next moment of the previous scene.


==================================================
LANGUAGE / DIALOGUE LOCK
==================================================

If a character speaks:

- dialogue language = STANDARD HINDI
- writing system = Devanagari
- speech must sound like natural spoken Hindi
- do NOT use Chinese
- do NOT use Japanese
- do NOT use Arabic
- do NOT use random invented language
- do NOT use gibberish
- do NOT use fake words

If there is NO dialogue in the story:

The character must remain silent.

Never invent dialogue.

Dialogue must be explicitly specified in the scene.


==================================================
VISUAL TEXT LOCK
==================================================

Do NOT place written text inside generated visuals unless
explicitly required.

No:

- subtitles
- captions
- random letters
- random words
- posters
- banners
- labels
- watermarks
- typography
- random logos
- readable signs

EXCEPTION:

Ayant's white "AYANT" T-shirt text is explicitly required
and must remain locked.


==================================================
NO AI IMPROVISATION
==================================================

AI MUST NOT add:

- new characters
- new objects
- new locations
- new buildings
- new trees
- new animals
- new events
- new actions
- new dialogue
- random camera movements
- random environmental changes


==================================================
SCENE STRUCTURE
==================================================

For each scene define:

SCENE NUMBER

ACTION

START STATE

END STATE

CHARACTER STATE

LOCATION STATE

BACKGROUND STATE

OBJECT STATE

DIALOGUE

CAMERA

CONTINUITY FROM PREVIOUS SCENE

CONTINUITY TO NEXT SCENE


==================================================
OUTPUT FORMAT
==================================================

FIRST:

### MASTER CONTINUITY BIBLE

CHARACTER BIBLE:
...

AYANT LOCK:
...

OTHER CHARACTER CLOTHING:
...

LOCATION BIBLE:
...

BACKGROUND FINGERPRINT:
...

OBJECT BIBLE:
...

LANGUAGE / DIALOGUE LOCK:
...

VISUAL STYLE:
...

FORMAT:
...

CLIP COUNT:
Exactly {expected_clips}

CLIP DURATION:
Exactly 8 seconds


THEN:

### SCENE 1

DURATION:
EXACTLY 8 SECONDS

ACTION:
...

START STATE:
...

END STATE:
...

CHARACTER STATE:
...

LOCATION STATE:
...

BACKGROUND FINGERPRINT:
...

OBJECT STATE:
...

DIALOGUE:
...

CAMERA:
...

CONTINUITY TO NEXT SCENE:
...


Then Scene 2, Scene 3 and so on.

EXACTLY {expected_clips} scenes.

No extra scenes.
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
You are AYANT Content AI's FINAL GOOGLE FLOW PROMPT DIRECTOR.

Your job is to convert the Master Continuity Bible and scene
states into extremely strict image and image-to-video prompts.

==================================================
STORY
==================================================

{story}

==================================================
MASTER CONTINUITY BIBLE + SCENE STATES
==================================================

{continuity_output}

==================================================
USER CHARACTER
==================================================

{character}

==================================================
AYANT CLOTHING
==================================================

{FIXED_AYANT_CLOTHING}

==================================================
SETTINGS
==================================================

STYLE:
{style}

FORMAT:
{aspect_ratio}

EXACT CLIP COUNT:
{expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS


==================================================
ABSOLUTE CONTINUITY RULE
==================================================

EVERY IMAGE MUST BELONG TO THE SAME CONTINUOUS WORLD.

Never treat a new scene as a completely new generation.

Use the Master Continuity Bible as the permanent source of truth.


==================================================
BACKGROUND FINGERPRINT LOCK
==================================================

Whenever the story remains in the same location:

REPEAT THE SAME CANONICAL BACKGROUND DETAILS.

Do NOT summarize them as:

"same background"
"same environment"
"same location"

Instead explicitly describe the same:

- architecture
- walls
- doors
- windows
- roads
- trees
- buildings
- ground
- landscape
- horizon
- foreground
- background
- weather
- atmosphere
- time of day
- lighting
- shadows

The visual environment must remain recognizable as the exact
same physical place.

Only explicitly requested story changes can modify it.


==================================================
OBJECT FINGERPRINT LOCK
==================================================

Every recurring object must remain the SAME object.

Repeat:

- exact type
- shape
- color
- material
- size
- visible details
- orientation
- holder
- hand
- position

If an object is in the character's right hand at the previous
End Frame, the next Start Frame must contain that SAME object
in the same right hand unless the story explicitly moves it.

Never replace an object with a visually different version.

Never randomly remove an object.

Never invent another version of the object.


==================================================
CHARACTER FINGERPRINT LOCK
==================================================

Every recurring character must retain:

- exact face
- skin tone
- eyes
- hair
- beard
- moustache
- age
- body proportions
- height
- clothes
- clothing colors
- shoes
- accessories

No redesign.

No morphing.

No wardrobe change.

No facial change.


==================================================
AYANT LOCK
==================================================

Whenever Ayant appears:

- exact same face
- exact same skin tone
- exact same body proportions
- exact same hairstyle
- exact same beard and moustache
- black T-shirt
- white "AYANT" front text
- white "AYANT" back text
- black pants
- white shoes

These MUST remain identical in every image and video.


==================================================
END FRAME → NEXT START FRAME
==================================================

THIS IS A HARD RULE.

Scene N END FRAME and Scene N+1 START FRAME must represent
the SAME physical moment/state with only the minimum natural
transition between them.

The following MUST carry forward:

- character position
- body orientation
- head direction
- gaze
- facial expression
- hand placement
- leg placement
- object position
- object orientation
- background
- lighting
- weather
- environment

The next scene may change ONLY the action explicitly required
by the story.


==================================================
DIALOGUE / LANGUAGE LOCK
==================================================

If the scene contains dialogue:

The character MUST speak ONLY natural STANDARD HINDI.

Dialogue must be written in Devanagari.

No other language.

No invented language.

No gibberish.

No random syllables.

No Chinese/Japanese/Arabic/Persian text.

Do NOT invent dialogue if none exists.

The video prompt must explicitly state:

"Any spoken dialogue must be natural standard Hindi only,
with accurate Hindi pronunciation. No other language and no
gibberish speech."


==================================================
VISUAL TEXT LOCK
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

Ayant's explicitly requested white "AYANT" T-shirt text.


==================================================
NO IMPROVISATION
==================================================

Do NOT add:

- new characters
- new objects
- new locations
- new background elements
- new animals
- new events
- new actions
- new dialogue
- random camera movement

Only execute the explicitly defined scene action.


==================================================
START FRAME IMAGE PROMPT
==================================================

The Start Frame prompt must describe the COMPLETE visual state.

It must include:

- character identity
- exact appearance
- exact clothing
- exact pose
- exact position
- exact gaze
- exact expression
- exact objects
- exact object positions
- exact location
- exact background
- exact lighting
- exact weather
- exact style
- exact format

It must be a direct continuation of the previous End Frame.


==================================================
END FRAME IMAGE PROMPT
==================================================

The End Frame must be the natural next state after the scene's
explicit action.

Do NOT redesign anything.

Change ONLY what the action requires.

Everything else stays locked.


==================================================
IMAGE-TO-VIDEO
==================================================

Animate the Start Frame naturally toward the End Frame.

Do NOT regenerate the world.

Do NOT redesign the character.

Do NOT change clothing.

Do NOT change objects.

Do NOT change the background.

Do NOT add characters.

Do NOT add objects.

Do NOT add events.

Do NOT add random camera movement.

The animation must look like one continuous 8-second shot.

The prompt MUST contain:

Duration: exactly 8 seconds.

And:

Any spoken dialogue must be natural standard Hindi only,
with accurate Hindi pronunciation. No other language and no
gibberish speech.


==================================================
EXACT OUTPUT
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

Repeat until EXACTLY {expected_clips} scenes.

NO EXTRA EXPLANATION.
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
            # MASTER CONTINUITY
            # =================================================

            with st.spinner(
                "🔒 Master Continuity Bible + Character + Background + "
                "Objects + End→Start State तैयार हो रहा है..."
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
                    "## 🔒 MASTER CONTINUITY + SCENE STATE"
                )

                st.write(
                    continuity_output
                )


                # =================================================
                # FINAL PROMPTS
                # =================================================

                with st.spinner(
                    "🎨 Locked Start Frame, End Frame और "
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
                        "## 🎬 GOOGLE FLOW — LOCKED COPYABLE PROMPTS"
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
                            f"🖼️ EXACTLY {expected_images} images | "
                            f"🎥 {expected_clips} video prompts | "
                            "🔒 Continuity Lock Active"
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
                            "Start Frame → End Frame → Video | "
                            "🔒 Previous End State → Current Start State"
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
                            "Google Flow के लिए तैयार हैं। "
                            "Character, Background, Objects, Pose और "
                            "Hindi Dialogue continuity locks applied."
                        )
