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

    .reference-box {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.35);
        margin-bottom: 12px;
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
    "Story → Master Reference → Continuity Chain → "
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


# =========================================================
# REFERENCE WORKFLOW INFO
# =========================================================

st.info(
    "🔗 REAL REFERENCE CHAIN: "
    "Master Reference → Clip 1 Start → Clip 1 End → "
    "Clip 2 Start → Clip 2 End → Clip 3 Start → ... | "
    "हर अगला frame पिछले actual generated frame को reference बनाएगा।"
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
    aspect_ratio,
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

Write ONE continuous cinematic Hindi story designed for EXACTLY
{expected_clips} sequential 8-second clips.

IMPORTANT:

1. Use clean, natural STANDARD HINDI.
2. Use standard Unicode Devanagari only for Hindi.
3. Never use Chinese, Japanese, Arabic, Persian or random Unicode.
4. Dialogue, if required, must be natural spoken Hindi.
5. Never randomly add dialogue.
6. Never randomly change language.
7. The story must be one continuous sequence.
8. Every clip must naturally continue from the previous clip.
9. Every scene must be physically possible as the next moment.
10. Do not randomly change location.
11. Do not randomly change weather.
12. Do not randomly change time of day.
13. Do not randomly change clothing.
14. Do not randomly change objects.
15. Avoid unnecessary characters.
16. Avoid unnecessary locations.
17. Every clip must contain a simple action that can happen within 8 seconds.
18. Do not describe image prompts.
19. Do not describe video prompts.
20. Do not add production instructions.

VISUAL TEXT RULE:

Generated visuals must contain NO written text unless explicitly
requested by the story.

EXCEPTION:

Ayant's white "AYANT" clothing text is explicitly required.

Return ONLY the final Hindi story.
"""

    return openrouter_request(prompt)


# =========================================================
# MASTER CONTINUITY + ACTUAL REFERENCE CHAIN PLAN
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
You are AYANT Content AI's STRICT CONTINUITY ARCHITECT.

Your job is to create a MASTER CONTINUITY BIBLE and a REAL
REFERENCE-CHAIN PLAN.

The most important rule:

A later frame must NOT be treated as an independent image.

Every frame must inherit its visual identity from the actual
previous generated frame.

==================================================
STORY
==================================================

{story}

==================================================
SETTINGS
==================================================

DURATION:
{duration}

EXACT CLIPS:
{expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS

STYLE:
{style}

FORMAT:
{aspect_ratio}

CHARACTER:
{character}

AYANT CLOTHING:
{FIXED_AYANT_CLOTHING}


==================================================
MASTER REFERENCE
==================================================

Before Clip 1, establish ONE MASTER REFERENCE IMAGE.

The Master Reference defines:

- Ayant's exact face
- skin tone
- body proportions
- hairstyle
- beard
- moustache
- clothing
- shoes
- accessories
- primary location
- background
- environment
- lighting
- visual style
- important objects

The Master Reference is the permanent visual identity source.

Do NOT redesign these elements later.


==================================================
CHARACTER BIBLE
==================================================

For every recurring character lock:

- face
- facial features
- eyes
- eyebrows
- nose
- lips
- skin
- age
- height
- body proportions
- hair
- beard
- moustache
- clothing
- clothing color
- clothing design
- shoes
- accessories

Once established, NEVER redesign them.


==================================================
AYANT LOCK
==================================================

Ayant MUST remain:

{character}

AND:

{FIXED_AYANT_CLOTHING}

No variation.


==================================================
LOCATION BIBLE
==================================================

For every location establish a canonical physical environment.

Lock:

- architecture
- walls
- doors
- windows
- floor
- road
- trees
- plants
- buildings
- mountains
- furniture
- landscape
- horizon
- foreground
- background
- weather
- atmosphere
- season
- time of day
- lighting direction
- shadows

Do not summarize this as "same background".

Give exact visual details.

A location may change ONLY when the story explicitly moves
to another location.


==================================================
OBJECT BIBLE
==================================================

For every important object lock:

- type
- shape
- color
- material
- size
- visible details
- orientation
- owner
- hand
- exact position

Never replace an established object with another object.

Never randomly remove an object.

Never invent another copy.


==================================================
REAL FRAME CHAIN
==================================================

This is the most important system.

Create this exact dependency:

MASTER_REFERENCE
↓
CLIP_1_START
↓
CLIP_1_END
↓
CLIP_2_START
↓
CLIP_2_END
↓
CLIP_3_START
↓
CLIP_3_END
↓
continue until final clip


RULE:

Clip N Start Frame MUST use the ACTUAL generated Clip N-1
End Frame as its PRIMARY visual reference.

Clip N End Frame MUST use the ACTUAL generated Clip N Start
Frame as its PRIMARY visual reference.

Only the explicitly required action may change.

Everything else remains visually inherited.


==================================================
POSE / STATE TRANSFER
==================================================

The End State of each frame must define:

- exact character position
- body orientation
- head direction
- gaze
- facial expression
- torso orientation
- left hand
- right hand
- left leg
- right leg
- object position
- object orientation
- movement state

The next frame inherits this state.


==================================================
NO RANDOM CHANGES
==================================================

Never add:

- new characters
- new objects
- new locations
- new buildings
- new trees
- new animals
- new events
- random actions
- random dialogue
- random camera movement
- random lighting change
- random weather change


==================================================
VISUAL TEXT
==================================================

Do NOT generate:

- subtitles
- captions
- random letters
- random words
- signs
- labels
- banners
- logos
- watermarks
- typography

EXCEPTION:

Ayant's explicitly required white "AYANT" shirt text.


==================================================
DIALOGUE
==================================================

If dialogue exists:

- standard Hindi
- Devanagari
- natural spoken Hindi
- no other language
- no gibberish

If there is no dialogue:

DIALOGUE = NONE


==================================================
OUTPUT
==================================================

FIRST:

### MASTER CONTINUITY BIBLE

CHARACTER BIBLE:
...

AYANT LOCK:
...

LOCATION BIBLE:
...

BACKGROUND FINGERPRINT:
...

OBJECT BIBLE:
...

MASTER REFERENCE DESCRIPTION:
...

VISUAL STYLE:
...

FORMAT:
...

CLIP COUNT:
Exactly {expected_clips}

CLIP DURATION:
Exactly 8 seconds


THEN FOR EACH SCENE:

### SCENE 1

ACTION:
...

REFERENCE_SOURCE:
MASTER_REFERENCE

START_STATE:
...

END_STATE:
...

CHARACTER_STATE:
...

LOCATION_STATE:
...

BACKGROUND_STATE:
...

OBJECT_STATE:
...

DIALOGUE:
...

CONTINUITY_RULE:
...

### SCENE 2

REFERENCE_SOURCE:
CLIP_1_END_FRAME

START_STATE:
...

END_STATE:
...

Continue until EXACTLY {expected_clips} scenes.

For every scene explicitly state its reference source.

NO EXTRA SCENES.
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
You are AYANT Content AI's FINAL GOOGLE FLOW CONTINUITY
PROMPT DIRECTOR.

Your output will be manually used in Google Flow.

The critical objective is NOT merely to describe continuity.

The objective is to force a HUMAN OPERATOR + IMAGE GENERATOR
workflow where every next image uses the PREVIOUS ACTUAL IMAGE
as its visual reference.

==================================================
STORY
==================================================

{story}

==================================================
MASTER CONTINUITY
==================================================

{continuity_output}

==================================================
CHARACTER
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

EXACT CLIPS:
{expected_clips}

EVERY CLIP:
EXACTLY 8 SECONDS


==================================================
ABSOLUTE REFERENCE RULE
==================================================

NEVER describe a later frame as a completely new generation.

The actual previous generated frame is the PRIMARY visual
reference.

The text prompt describes ONLY what must remain identical and
what small action/state change must happen.


==================================================
REFERENCE CHAIN
==================================================

For Scene 1:

START FRAME REFERENCE:
MASTER REFERENCE IMAGE

END FRAME REFERENCE:
ACTUAL SCENE 1 START FRAME

For Scene 2:

START FRAME REFERENCE:
ACTUAL SCENE 1 END FRAME

END FRAME REFERENCE:
ACTUAL SCENE 2 START FRAME

For Scene 3:

START FRAME REFERENCE:
ACTUAL SCENE 2 END FRAME

END FRAME REFERENCE:
ACTUAL SCENE 3 START FRAME

Continue exactly like this.

This reference chain MUST be explicitly written inside every
prompt.


==================================================
REFERENCE IMAGE INSTRUCTION
==================================================

Every image prompt MUST begin with a clear instruction such as:

"REFERENCE IMAGE: Use the specified previous generated frame
as the PRIMARY visual reference. Preserve the exact identity,
geometry, appearance, environment, object placement, lighting,
camera perspective and composition from that reference."

Then specify ONLY the required change.

Never ask the image model to redesign the scene.


==================================================
CHARACTER LOCK
==================================================

Preserve exactly:

- face
- skin tone
- eyes
- hair
- beard
- moustache
- age
- body proportions
- height
- clothes
- shoes
- accessories

No morphing.
No face redesign.
No body redesign.
No wardrobe change.


==================================================
AYANT LOCK
==================================================

Whenever Ayant appears:

- same exact face
- same exact skin tone
- same exact body proportions
- same exact hairstyle
- same exact beard and moustache
- black T-shirt
- white "AYANT" front text
- white "AYANT" back text
- black pants
- white shoes

No variation.


==================================================
LOCATION LOCK
==================================================

Preserve the exact physical environment from the reference:

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

Do NOT create a new interpretation of the location.


==================================================
OBJECT LOCK
==================================================

Preserve every important object exactly:

- same object
- same material
- same color
- same shape
- same size
- same details
- same orientation
- same hand
- same position

Only explicitly required object movement is allowed.


==================================================
POSE LOCK
==================================================

Carry forward:

- character position
- body orientation
- head orientation
- gaze
- facial expression
- hand positions
- leg positions
- object positions

Only the current scene's explicitly required action can change.


==================================================
NO VISUAL TEXT
==================================================

Do NOT create:

- subtitles
- captions
- random letters
- random words
- signs
- labels
- posters
- banners
- logos
- watermarks
- typography

EXCEPTION:

The explicitly required "AYANT" text on Ayant's T-shirt.


==================================================
NO AI IMPROVISATION
==================================================

Do NOT add:

- characters
- objects
- locations
- animals
- buildings
- trees
- events
- actions
- dialogue
- camera movements

unless explicitly required.


==================================================
START FRAME
==================================================

The Start Frame is NOT a fresh scene.

It MUST use the specified reference image.

The prompt must say:

1. Which actual image is the reference.
2. What must remain identical.
3. What exact state is required.
4. What tiny change, if any, is required.


==================================================
END FRAME
==================================================

The End Frame MUST use the actual Start Frame as its reference.

It represents the exact next visual state after the defined
8-second action.

Do not redesign anything.


==================================================
IMAGE TO VIDEO
==================================================

The video uses:

START FRAME = actual generated Start Frame
END FRAME = actual generated End Frame

Animate ONLY the transition between them.

Do NOT regenerate the character.
Do NOT redesign the environment.
Do NOT change clothing.
Do NOT change objects.
Do NOT add characters.
Do NOT add objects.
Do NOT add events.
Do NOT add random camera movements.

Duration: exactly 8 seconds.

If dialogue exists:

"Any spoken dialogue must be natural standard Hindi only,
with accurate Hindi pronunciation. No other language and no
gibberish speech."


==================================================
EXACT OUTPUT FORMAT
==================================================

SCENE_START

SCENE_NUMBER: 1

REFERENCE_CHAIN:
START_FRAME_REFERENCE: MASTER REFERENCE IMAGE
END_FRAME_REFERENCE: ACTUAL SCENE 1 START FRAME

DURATION:
EXACTLY 8 SECONDS

START_FRAME_IMAGE_PROMPT:
[complete English prompt]

END_FRAME_IMAGE_PROMPT:
[complete English prompt]

IMAGE_TO_VIDEO_PROMPT:
[complete English prompt]

SCENE_END


SCENE_START

SCENE_NUMBER: 2

REFERENCE_CHAIN:
START_FRAME_REFERENCE: ACTUAL SCENE 1 END FRAME
END_FRAME_REFERENCE: ACTUAL SCENE 2 START FRAME

DURATION:
EXACTLY 8 SECONDS

START_FRAME_IMAGE_PROMPT:
[complete English prompt]

END_FRAME_IMAGE_PROMPT:
[complete English prompt]

IMAGE_TO_VIDEO_PROMPT:
[complete English prompt]

SCENE_END

Continue exactly until Scene {expected_clips}.

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

        reference_match = re.search(
            r"REFERENCE_CHAIN:\s*(.*?)(?=\nDURATION:)",
            block,
            re.DOTALL
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

                    "reference_chain": (
                        reference_match.group(1).strip()
                        if reference_match
                        else ""
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
            "**Continuity:** Actual Previous Frame → Next Frame"
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
            "🤖 AI तुम्हारी continuous Hindi story लिख रहा है..."
        ):

            generated_story, story_error = (
                generate_ai_story(
                    idea,
                    duration,
                    style,
                    aspect_ratio,
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
                "🔒 Master Reference + Character + Location + "
                "Object + State Chain तैयार हो रही है..."
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
                    "## 🔒 MASTER CONTINUITY + REFERENCE CHAIN"
                )

                st.write(
                    continuity_output
                )


                # =================================================
                # FINAL PROMPTS
                # =================================================

                with st.spinner(
                    "🎨 Actual Reference Chain आधारित Google Flow "
                    "prompts बनाए जा रहे हैं..."
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
                        "## 🎬 GOOGLE FLOW — REAL REFERENCE CHAIN"
                    )


                    # =================================================
                    # IMPORTANT USER INSTRUCTION
                    # =================================================

                    st.warning(
                        "⚠️ IMPORTANT: अब हर अगली image को नई independent "
                        "image की तरह generate मत करना। जिस frame को "
                        "REFERENCE IMAGE लिखा है, उसी actual generated "
                        "image को Google Flow में reference के रूप में "
                        "देना है। यही visual continuity का मुख्य हिस्सा है।"
                    )


                    # =================================================
                    # MASTER REFERENCE
                    # =================================================

                    st.markdown(
                        "## 🧬 STEP 0 — MASTER REFERENCE IMAGE"
                    )

                    st.write(
                        "सबसे पहले Master Reference Image generate करो। "
                        "यही Ayant + location + objects की visual identity "
                        "का base होगा।"
                    )

                    st.info(
                        "Master Reference को save करके रखो। "
                        "Clip 1 Start Frame बनाते समय यही reference रहेगा।"
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
                            "🔗 Real Reference Chain Ready"
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
                            "Actual Reference → Start Frame → End Frame → Video"
                        )


                        # ---------------------------------------------
                        # REFERENCE CHAIN
                        # ---------------------------------------------

                        st.markdown(
                            "### 🔗 REFERENCE CHAIN"
                        )

                        st.code(
                            scene["reference_chain"],
                            language="text"
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
                            "Reference Chain: "
                            "Previous Actual Frame → Next Frame."
                        )
