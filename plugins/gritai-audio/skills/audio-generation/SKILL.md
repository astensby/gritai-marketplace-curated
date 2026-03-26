---
name: audio-generation
description: >
  Use this skill when the user asks about generating audio, text-to-speech, TTS,
  creating voiceovers, narration, podcast audio, voice synthesis, speech generation,
  ElevenLabs, audio content, reading text aloud, converting text to audio, producing
  spoken word, making audio files from text, dubbing, or any task involving turning
  written content into speech or sound. Activate whenever audio or speech generation
  is mentioned or implied.
allowed-tools: Bash, Read, Write
---

# Audio Generation with ElevenLabs MCP

This plugin wraps the ElevenLabs MCP server, launched via `uvx elevenlabs-mcp`.
It exposes tools for text-to-speech, voice cloning, and audio generation through
the ElevenLabs API.

## Prerequisites

Before invoking any ElevenLabs tool, verify the following:

1. Confirm `ELEVENLABS_API_KEY` is set in the environment. If it is missing,
   instruct the user to set it before proceeding.
2. Confirm `uv` is installed and available on the PATH. The MCP server is
   launched with `uvx elevenlabs-mcp`, which requires `uv`.

## Common Use Cases

### Text-to-Speech for Written Content
Convert articles, blog posts, documentation, or any written text into natural
sounding audio. Break long documents into logical sections before generating
audio to maintain quality and manageability.

### Voiceovers for Presentations or Videos
Generate voiceover tracks for slide decks, video narration, or explainer
content. Match the voice tone and pace to the visual content.

### Podcast Content Generation
Produce spoken segments for podcasts, including intros, outros, and full
episode narration. Consider using distinct voices for different speakers
or segments.

### Audio Narration
Create narration for stories, tutorials, guides, or educational material.
Adjust voice characteristics to suit the genre and audience.

## Tips for Good Results

- Select a voice that matches the content type. Use a warm, conversational
  voice for podcasts and a clear, authoritative voice for documentation.
- Use punctuation deliberately to control pacing. Commas introduce short
  pauses; periods introduce longer ones. Em dashes and ellipses add
  dramatic pauses.
- Use SSML tags when available to fine-tune pronunciation, emphasis, and
  timing for professional-grade output.
- Consider the target audience when choosing voice characteristics such as
  age, accent, and speaking style.
- For long-form content, split text into paragraphs or sections and generate
  audio for each segment individually. This allows easier editing and
  re-generation of specific parts.
- Preview a short sample before generating the full content to confirm the
  voice and settings are appropriate.

## Safety Considerations

- Always confirm with the user before generating audio. Do not generate
  audio without explicit approval.
- Respect ElevenLabs content policies. Do not generate audio that impersonates
  real individuals without consent or that contains harmful content.
- Warn the user about API usage costs before generating large volumes of audio.
- Do not use voice cloning features on voices the user does not have rights to
  clone.
