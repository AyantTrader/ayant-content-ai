import streamlit as st
import requests
import re
import html
import json
import os
import uuid
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AYANTVERSE.01 Content AI",
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

    .channel-box {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.35);
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PERSISTENT WORKFLOW STORAGE
# =========================================================

WORKFLOW_DIR = "workflow_data"
os.makedirs(WORKFLOW_DIR, exist_ok=True)


def get_workflow_id():

    workflow_id = st.query_params.get("workflow")

    if workflow_id:
        return workflow_id

    workflow_id = str(uuid.uuid4())
    st.query_params["workflow"] = workflow_id

    return workflow_id


WORKFLOW_ID = get_workflow_id()

WORKFLOW_FILE = os.path.join(
    WORKFLOW_DIR,
    f"{WORKFLOW_ID}.json"
)


def load_workflow():

    if not os.path.exists(WORKFLOW_FILE):
        return {}

    try:
        with open(
            WORKFLOW_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return {}


def save_workflow(data):

    try:

        data["last_saved"] = datetime.now().isoformat()

        temp_file = WORKFLOW_FILE + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temp_file,
            WORKFLOW_FILE
        )

        return True

    except Exception:
        return False


def clear_current_workflow():

    try:

        if os.path.exists(WORKFLOW_FILE):
            os.remove(WORKFLOW_FILE)

    except Exception:
        pass


workflow = load_workflow()


# =========================================================
# APP HEADER
# =========================================================

st.title("🎬 AYANTVERSE.01 Content AI")

st.caption(
    "Story → Master Reference → Continuity Chain → "
    "Start/End Frames → Image Prompts → "
    "Image-to-Video Prompts → Google Flow"
)

st.divider()


# =========================================================
# PERMANENT AYANTVERSE.01 CHANNEL DIRECTION
# =========================================================

AYANTVERSE_01_DIRECTION = """
=========================================================
AYANTVERSE.01 — PERMANENT CHANNEL IDENTITY
=========================================================

This Content AI is created ONLY for the AYANTVERSE.01 channel.

The AI must never generate content as if this were another
channel or another creator.

PRIMARY CONTENT PILLARS:

1. WILDLIFE & ANIMAL MYSTERIES
- strange animal behavior
- unexplained wildlife facts
- rare animals
- extreme animal adaptations
- deep-ocean creatures
- animal survival mysteries
- unusual natural phenomena

2. EXTINCT ANIMALS & ANCIENT WORLD
- extinct animals
- prehistoric creatures
- dinosaurs
- ancient ecosystems
- prehistoric Earth
- ancient-world mysteries
- mass extinction mysteries
- ancient survival and exploration

3. SPACE & WHAT IF
- space mysteries
- planets
- moons
- black holes
- cosmic phenomena
- scientific what-if scenarios
- Earth-changing astronomical scenarios

CHANNEL STYLE:

Cinematic 3D animated mystery + facts + exploration.

The content should feel:
- cinematic
- mysterious
- curiosity-driven
- educational
- visually powerful
- exploration-focused
- factual where appropriate
- emotionally engaging
- suitable for AYANTVERSE.01

DEFAULT STORY FLOW:

STRONG HOOK
→ MYSTERY
→ EXPLORATION
→ DISCOVERY
→ REVEAL / PAYOFF

The story must be ONE continuous cinematic journey.

Do NOT create disconnected mini-stories.

Do NOT randomly switch to unrelated subjects.

Do NOT randomly change the main mystery.

FACTUAL RULE:

When the topic is based on real science, wildlife, extinct
animals, ancient history or space:

- do not present invented facts as confirmed facts
- do not present speculation as established science
- clearly treat WHAT-IF scenarios as hypothetical
- maintain scientifically reasonable visual logic

CONTINUITY:

Every scene must naturally continue from the previous scene.

Lock:
- character identity
- face
- skin
- age
- body proportions
- hairstyle
- beard
- moustache
- clothing
- shoes
- accessories
- location
- environment
- architecture
- landscape
- weather
- time of day
- lighting
- important objects
- object position
- character position
- body orientation
- gaze
- expression
- hand placement
- leg placement

Only the explicitly required action may change.

NEW STORY RULE:

Every new story starts with a NEW continuity state.

Characters and locations from previous stories must NOT
automatically carry into a new story.

Every recurring character created for the current story must
be locked after first appearance.

Every recurring location created for the current story must
be locked after first appearance.

AYANT:

Ayant does NOT have to appear unless the story or user idea
requires him.

When Ayant appears, his permanent clothing lock MUST apply.

NO RANDOM AI IMPROVISATION:

Never add:
- random characters
- random animals
- random objects
- random locations
- random buildings
- random events
- random dialogue
- random camera movement
- random weather
- random lighting changes
- random costume changes

Everything visible must have a story reason.

VISUAL TEXT:

Generated images and videos must NOT contain:
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
Ayant's explicitly required white "AYANT" clothing text.

LANGUAGE:

Story:
STANDARD NATURAL HINDI IN DEVANAGARI.

Image prompts:
ENGLISH.

Image-to-video prompts:
ENGLISH.

Dialogue:
STANDARD NATURAL HINDI ONLY.

CLIP SYSTEM:

Every clip is EXACTLY 8 SECONDS.

Every clip contains:
START FRAME + END FRAME + IMAGE-TO-VIDEO

REFERENCE CHAIN:

MASTER REFERENCE
→ CLIP 1 START
→ CLIP 1 END
→ CLIP 2 START
→ CLIP 2 END
→ CLIP 3 START
→ CLIP 3 END
→ continue until final clip.

The actual previously generated frame is always the PRIMARY
visual reference for the next frame.

Never treat the next frame as an unrelated new generation.
=========================================================
"""


# =========================================================
# NEW STORY BUTTON
# =========================================================

if st.button("🆕 नई Story शुरू करो"):

    clear_current_workflow()

    new_workflow_id = str(uuid.uuid4())

    st.query_params["workflow"] = new_workflow_id

    st.rerun()


# =========================================================
# CHANNEL LOCK DISPLAY
# =========================================================

st.markdown(
    """
    <div class="channel-box">
    <b>🔒 CHANNEL LOCKED: AYANTVERSE.01</b><br>
    🐺 Wildlife & Animal Mysteries<br>
    🦖 Extinct Animals & Ancient World<br>
    🌌 Space & What If<br>
    🎬 Cinematic 3D Mystery + Facts + Exploration
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# RESTORED WORKFLOW STATUS
# =========================================================

if workflow:

    st.success(
        "🔄 Saved workflow मिला है। "
        "Refresh के बाद completed stages restore कर दिए गए हैं।"
    )

    if workflow.get("last_saved"):

        st.caption(
            f"Last saved: {workflow['last_saved']}"
        )


# =========================================================
# VIDEO INPUT
# =========================================================

st.subheader("📝 अपनी कहानी या वीडियो आइडिया लिखो")

saved_idea = workflow.get("idea", "")

idea = st.text_area(
    "Video idea",
    value=saved_idea,
    placeholder=(
        "उदाहरण: समुद्र की गहराई में एक ऐसा जीव मिला "
        "जिसके बारे में वैज्ञानिक भी हैरान हैं..."
    ),
    height=180
)


# =========================================================
# VIDEO SETTINGS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    duration_options = [
        "30 सेकंड",
        "60 सेकंड",
        "90 सेकंड",
        "2 मिनट"
    ]

    saved_duration = workflow.get(
        "duration",
        duration_options[0]
    )

    if saved_duration not in duration_options:
        saved_duration = duration_options[0]

    duration = st.selectbox(
        "वीडियो duration",
        duration_options,
        index=duration_options.index(saved_duration)
    )


with col2:

    style_options = [
        "Cinematic Semi-Realistic 3D",
        "Realistic Cinematic",
        "3D Animated",
        "Epic Historical"
    ]

    saved_style = workflow.get(
        "style",
        style_options[0]
    )

    if saved_style not in style_options:
        saved_style = style_options[0]

    style = st.selectbox(
        "Visual Style",
        style_options,
        index=style_options.index(saved_style)
    )


with col3:

    aspect_options = [
        "9:16 Vertical",
        "16:9 Horizontal",
        "1:1 Square"
    ]

    saved_aspect = workflow.get(
        "aspect_ratio",
        aspect_options[0]
    )

    if saved_aspect not in aspect_options:
        saved_aspect = aspect_options[0]

    aspect_ratio = st.selectbox(
        "Format",
        aspect_options,
        index=aspect_options.index(saved_aspect)
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
AYANT CHARACTER CLOTHING IS PERMANENTLY LOCKED.

Whenever Ayant appears, he must wear exactly:

- black T-shirt
- white "AYANT" text clearly visible on the FRONT
- white "AYANT" text clearly visible on the BACK
- black pants
- clean white shoes

Do NOT change:
- shirt color
- shirt design
- shirt text
- pants
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

saved_character = workflow.get(
    "character",
    (
        "Ayant: young Indian male, wheatish skin, brown eyes, "
        "short trimmed beard and moustache, black hair tied in "
        "a high man-bun/top-knot, consistent face, body "
        "proportions and appearance across all scenes."
    )
)


character = st.text_area(
    "अगर कोई मुख्य character है तो उसकी fixed appearance यहाँ लिखो",
    value=saved_character,
    height=120
)


# =========================================================
# AUTO SAVE BASIC INPUTS
# =========================================================

workflow["idea"] = idea
workflow["duration"] = duration
workflow["style"] = style
workflow["aspect_ratio"] = aspect_ratio
workflow["character"] = character
workflow["expected_clips"] = expected_clips
workflow["expected_images"] = expected_images
workflow["channel"] = "AYANTVERSE.01"

save_workflow(workflow)


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
You are AYANTVERSE.01 Content AI.

{AYANTVERSE_01_DIRECTION}

==================================================
USER VIDEO IDEA
==================================================

{idea}

==================================================
VIDEO SETTINGS
==================================================

DURATION:
{duration}

EXACT CLIP COUNT:
{expected_clips}

VISUAL STYLE:
{style}

FORMAT:
{aspect_ratio}

CHARACTER:
{character}

AYANT CLOTHING:
{FIXED_AYANT_CLOTHING}

==================================================
STORY WRITING RULES
==================================================

Write ONE continuous cinematic Hindi story designed for EXACTLY
{expected_clips} sequential clips.

The story must follow:

STRONG HOOK
→ MYSTERY
→ EXPLORATION
→ DISCOVERY
→ REVEAL / PAYOFF

The opening must create immediate curiosity.

Every clip must naturally continue from the exact previous
moment.

Every clip must contain a simple visual action that can happen
within 8 seconds.

If a new character is required, create that character from the
current story and then keep the character visually locked.

If a new location is required, establish it clearly and then
keep it visually locked until the story explicitly moves.

Do NOT randomly add characters.

Do NOT randomly add locations.

Do NOT randomly add objects.

Do NOT randomly change the environment.

Do NOT randomly change weather.

Do NOT randomly change time of day.

Do NOT randomly change clothing.

Do NOT randomly add dialogue.

Do NOT describe image prompts.

Do NOT describe video prompts.

Do NOT add production instructions.

==================================================
HINDI LANGUAGE RULE
==================================================

Use clean, natural STANDARD HINDI.

Use standard Unicode Devanagari only.

Never use:
- Chinese
- Japanese
- Arabic
- Persian
- random Unicode
- gibberish

Dialogue, if required, must be natural spoken Hindi.

==================================================
VISUAL TEXT RULE
==================================================

Generated visuals must contain NO written text.

Do not add:
- subtitles
- captions
- labels
- signs
- posters
- banners
- logos
- watermarks
- random letters
- random words
- typography

EXCEPTION:

Ayant's explicitly required white "AYANT" clothing text.

==================================================
FINAL OUTPUT
==================================================

Return ONLY the final Hindi story.

Do not return explanations.

Do not return scene headings.

Do not return prompts.
"""

    return openrouter_request(prompt)


# =========================================================
# MASTER CONTINUITY + REFERENCE CHAIN
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
You are AYANTVERSE.01 Content AI's STRICT CONTINUITY ARCHITECT.

{AYANTVERSE_01_DIRECTION}

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

Before Clip 1 establish ONE MASTER REFERENCE IMAGE.

The Master Reference must define the visual identity of the
current story.

Lock:
- character identity
- face
- skin
- age
- body
- hair
- beard
- moustache
- clothing
- shoes
- accessories
- primary location
- environment
- background
- lighting
- visual style
- important objects

Do NOT import characters or locations from previous stories.

==================================================
CHARACTER BIBLE
==================================================

For every recurring character in THIS STORY define:

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
- clothing colors
- clothing design
- shoes
- accessories

Once defined, NEVER redesign the character.

==================================================
AYANT LOCK
==================================================

Whenever Ayant appears:

{character}

{FIXED_AYANT_CLOTHING}

==================================================
LOCATION BIBLE
==================================================

For every recurring location define exact physical details:

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
- landscape
- furniture
- horizon
- foreground
- background
- weather
- atmosphere
- season
- time of day
- lighting direction
- shadows

Do NOT simply say "same background".

A location can change ONLY when the story explicitly moves.

==================================================
OBJECT BIBLE
==================================================

For every important object define:

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

Never randomly replace, remove or duplicate an object.

==================================================
REAL FRAME CHAIN
==================================================

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

Only the explicitly required action/state may change.

Everything else must remain visually inherited.

==================================================
POSE / STATE TRANSFER
==================================================

For every scene define:

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
- new animals
- new objects
- new locations
- new buildings
- new trees
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

If no dialogue:

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

THEN:

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

Then continue with:

### SCENE 2
REFERENCE_SOURCE:
CLIP_1_END_FRAME

...

Continue until EXACTLY {expected_clips} scenes.

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
You are AYANTVERSE.01 Content AI's FINAL GOOGLE FLOW
CONTINUITY PROMPT DIRECTOR.

{AYANTVERSE_01_DIRECTION}

Your output will be manually used in Google Flow.

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

NEVER describe a later frame as a completely new independent
generation.

The actual previous generated frame is the PRIMARY visual
reference.

The prompt must preserve everything from that reference.

Only the explicitly required next action/state may change.

==================================================
REFERENCE CHAIN
==================================================

Scene 1:

START FRAME REFERENCE:
MASTER REFERENCE IMAGE

END FRAME REFERENCE:
ACTUAL SCENE 1 START FRAME

Scene 2:

START FRAME REFERENCE:
ACTUAL SCENE 1 END FRAME

END FRAME REFERENCE:
ACTUAL SCENE 2 START FRAME

Scene 3:

START FRAME REFERENCE:
ACTUAL SCENE 2 END FRAME

END FRAME REFERENCE:
ACTUAL SCENE 3 START FRAME

Continue this exact pattern until the final scene.

==================================================
REFERENCE IMAGE INSTRUCTION
==================================================

Every image prompt MUST clearly state:

REFERENCE IMAGE:
Use the specified previous generated frame as the PRIMARY
visual reference.

Preserve:
- exact character identity
- exact face
- exact body
- exact clothing
- exact location
- exact environment
- exact object placement
- exact lighting
- exact camera perspective
- exact composition

Then describe ONLY the required change.

Never redesign the scene.

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
- clothing
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

Preserve the exact physical environment:

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

Preserve every important object:

- same object
- same material
- same color
- same shape
- same size
- same details
- same orientation
- same hand
- same position

Only explicitly required movement is allowed.

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

Only the current scene's explicitly required action may change.

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
- animals
- objects
- locations
- buildings
- trees
- events
- actions
- dialogue
- camera movements

unless explicitly required by the current story state.

==================================================
START FRAME
==================================================

The Start Frame is NOT a fresh unrelated scene.

It MUST use the specified actual reference image.

State:
1. Which actual image is the reference.
2. What remains identical.
3. Exact required state.
4. Exact required action/state change.

==================================================
END FRAME
==================================================

The End Frame MUST use the actual Start Frame as its
PRIMARY reference.

It represents the exact next visual state after the action.

Do not redesign anything.

==================================================
IMAGE TO VIDEO
==================================================

START FRAME = actual generated Start Frame

END FRAME = actual generated End Frame

Animate ONLY the transition between these two frames.

Do NOT:
- regenerate the character
- redesign the environment
- change clothing
- change objects
- add characters
- add objects
- add events
- add random camera movements

Duration: exactly 8 seconds.

If dialogue exists:

Any spoken dialogue must be natural standard Hindi only,
with accurate Hindi pronunciation.

No other language.
No gibberish speech.

==================================================
OUTPUT FORMAT
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
# DISPLAY STORY
# =========================================================

def display_story(story):

    st.markdown("## 📖 AI GENERATED STORY")

    safe_story = html.escape(story).replace(
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


# =========================================================
# DISPLAY CONTINUITY
# =========================================================

def display_continuity(continuity_output):

    st.markdown(
        "## 🔒 MASTER CONTINUITY + REFERENCE CHAIN"
    )

    st.write(continuity_output)


# =========================================================
# DISPLAY FINAL SCENES
# =========================================================

def display_final_scenes(
    scene_output,
    expected_clips,
    expected_images
):

    scenes = parse_scenes(scene_output)

    st.markdown(
        "## 🎬 GOOGLE FLOW — REAL REFERENCE CHAIN"
    )

    st.warning(
        "⚠️ IMPORTANT: हर अगली image को independent नई image "
        "की तरह generate मत करना। जिस actual frame को "
        "REFERENCE IMAGE लिखा है, उसी generated frame को "
        "Google Flow में reference के रूप में इस्तेमाल करना है।"
    )

    st.markdown(
        "## 🧬 STEP 0 — MASTER REFERENCE IMAGE"
    )

    st.write(
        "सबसे पहले Master Reference Image generate करो। "
        "यही current story के character + location + objects "
        "की permanent visual identity का base होगा।"
    )

    st.info(
        "Master Reference को save करके रखो। "
        "Clip 1 Start Frame बनाते समय यही reference रहेगा।"
    )

    if len(scenes) != expected_clips:

        st.warning(
            f"⚠️ AI ने {expected_clips} scenes की जगह "
            f"{len(scenes)} scenes read किए। "
            "Workflow को दोबारा START करना बेहतर रहेगा।"
        )

        return

    st.success(
        f"✅ EXACTLY {expected_clips} clips तैयार हैं | "
        f"🖼️ EXACTLY {expected_images} images | "
        f"🎥 {expected_clips} video prompts | "
        "🔗 Real Reference Chain Ready"
    )

    for scene in scenes:

        st.markdown(
            f"## 🎬 CLIP / SCENE {scene['number']}"
        )

        st.caption(
            "Duration: EXACTLY 8 SECONDS | "
            "Actual Reference → Start Frame → End Frame → Video"
        )

        st.markdown("### 🔗 REFERENCE CHAIN")

        st.code(
            scene["reference_chain"],
            language="text"
        )

        st.markdown(
            "### 🟢 START FRAME — IMAGE PROMPT"
        )

        st.code(
            scene["start_frame_prompt"],
            language="text"
        )

        st.markdown(
            "### 🔴 END FRAME — IMAGE PROMPT"
        )

        st.code(
            scene["end_frame_prompt"],
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
        "🎉 Workflow complete! "
        f"{expected_clips} clips × 2 images = "
        f"{expected_images} images और "
        f"{expected_clips} Image-to-Video prompts "
        "Google Flow के लिए तैयार हैं।"
    )


# =========================================================
# RESTORE COMPLETED WORKFLOW
# =========================================================

if workflow.get("workflow_started"):

    if workflow.get("story_complete"):

        generated_story = workflow.get(
            "generated_story",
            ""
        )

        if generated_story:
            display_story(generated_story)

    if workflow.get("continuity_complete"):

        continuity_output = workflow.get(
            "continuity_output",
            ""
        )

        if continuity_output:
            display_continuity(continuity_output)

    if workflow.get("prompts_complete"):

        scene_output = workflow.get(
            "scene_output",
            ""
        )

        if scene_output:
            display_final_scenes(
                scene_output,
                expected_clips,
                expected_images
            )


# =========================================================
# MAIN WORKFLOW BUTTON
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

        workflow["workflow_started"] = True
        workflow["channel"] = "AYANTVERSE.01"
        workflow["idea"] = idea
        workflow["duration"] = duration
        workflow["style"] = style
        workflow["aspect_ratio"] = aspect_ratio
        workflow["character"] = character
        workflow["expected_clips"] = expected_clips
        workflow["expected_images"] = expected_images

        save_workflow(workflow)

        st.success(
            "AYANTVERSE.01 Content Workflow शुरू हो गया!"
        )

        # =================================================
        # VIDEO PLAN
        # =================================================

        st.markdown("## 🎬 VIDEO PLAN")

        st.write(f"**Channel:** AYANTVERSE.01")
        st.write(f"**Selected Duration:** {duration}")
        st.write(f"**Clips:** {expected_clips}")
        st.write(f"**Images:** {expected_images}")
        st.write("**Images per Clip:** 2 (Start + End)")
        st.write("**Clip Duration:** EXACTLY 8 SECONDS")
        st.write(
            "**Continuity:** Actual Previous Frame → Next Frame"
        )
        st.write(f"**Style:** {style}")
        st.write(f"**Format:** {aspect_ratio}")

        # =================================================
        # STORY
        # =================================================

        if (
            workflow.get("story_complete")
            and workflow.get("generated_story")
        ):

            generated_story = workflow["generated_story"]

            st.info(
                "📦 Saved Story already available — "
                "AI को दोबारा Story generate नहीं करवाई जा रही।"
            )

            display_story(generated_story)

        else:

            with st.spinner(
                "🤖 AYANTVERSE.01 के लिए continuous Hindi story लिखी जा रही है..."
            ):

                generated_story, story_error = generate_ai_story(
                    idea,
                    duration,
                    style,
                    aspect_ratio,
                    character,
                    expected_clips
                )

            if story_error:

                st.error(story_error)
                st.stop()

            workflow["generated_story"] = generated_story
            workflow["story_complete"] = True

            save_workflow(workflow)

            st.success("💾 Story successfully saved.")

            display_story(generated_story)

        # =================================================
        # MASTER CONTINUITY
        # =================================================

        if (
            workflow.get("continuity_complete")
            and workflow.get("continuity_output")
        ):

            continuity_output = workflow[
                "continuity_output"
            ]

            st.info(
                "📦 Saved Master Continuity already available — "
                "AI को दोबारा generate नहीं करवाया जा रहा।"
            )

            display_continuity(continuity_output)

        else:

            with st.spinner(
                "🔒 AYANTVERSE.01 Master Character + Location + "
                "Object + State Continuity तैयार हो रही है..."
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

                st.error(continuity_error)
                st.stop()

            workflow["continuity_output"] = continuity_output
            workflow["continuity_complete"] = True

            save_workflow(workflow)

            st.success(
                "💾 Master Continuity successfully saved."
            )

            display_continuity(continuity_output)

        # =================================================
        # FINAL PROMPTS
        # =================================================

        if (
            workflow.get("prompts_complete")
            and workflow.get("scene_output")
        ):

            scene_output = workflow["scene_output"]

            st.info(
                "📦 Saved Google Flow prompts already available — "
                "AI को दोबारा generate नहीं करवाया जा रहा।"
            )

            display_final_scenes(
                scene_output,
                expected_clips,
                expected_images
            )

        else:

            with st.spinner(
                "🎨 AYANTVERSE.01 Google Flow Reference Chain "
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

                st.error(scene_error)
                st.stop()

            workflow["scene_output"] = scene_output
            workflow["prompts_complete"] = True

            scenes = parse_scenes(scene_output)

            if len(scenes) == expected_clips:
                workflow["workflow_complete"] = True

            save_workflow(workflow)

            st.success(
                "💾 Final Google Flow prompts successfully saved."
            )

            display_final_scenes(
                scene_output,
                expected_clips,
                expected_images
            )
