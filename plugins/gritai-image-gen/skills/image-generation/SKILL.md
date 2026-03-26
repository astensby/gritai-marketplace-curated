---
name: image-generation
description: >
  Use this skill when the user asks about generating images, creating pictures, making illustrations,
  producing visual content, creating photorealistic images, AI image generation, creating graphics,
  text-to-image conversion, drawing scenes, rendering visuals, making artwork, designing visuals,
  Google Imagen, Gemini image model, creating photos, generating art, making banners, producing
  thumbnails, creating concept art, visualizing ideas, or anything related to turning text descriptions
  into images. Trigger this skill whenever image creation or generation is mentioned or implied.
allowed-tools: Bash, Read, Write
argument-hint: "[description of image to generate]"
---

# Image Generation with Imagen MCP Server

This plugin provides the `generate_image` MCP tool, which generates images using Google's Gemini image models via the Gemini API. Call `generate_image` with a text prompt and optional parameters to produce PNG images saved to the current working directory.

## Tool Parameters

- `prompt` (required) -- Detailed text description of the image to generate.
- `negativePrompt` (optional) -- What to avoid in the image.
- `aspectRatio` (optional) -- One of `1:1`, `16:9`, `9:16`, `4:3`, `3:4`. Defaults to `1:1`.
- `numImages` (optional) -- Number of images to generate, 1 to 4. Defaults to 1.
- `model` (optional) -- Model to use. Defaults to `gemini-2.5-flash-image`.

## Model Selection

Choose the model based on the user's needs:

- **gemini-2.5-flash-image** (default) -- Fast generation, 1024px resolution. Use for most requests, quick iterations, social media content, and high-volume tasks. Prefer this unless the user explicitly asks for higher quality or 4K.
- **gemini-3-pro-image-preview** -- Advanced model with up to 4K resolution, reasoning capabilities, and Google Search grounding. Use when the user requests professional quality, high resolution, print-ready images, or detailed/complex scenes.

## Prompt Engineering

Write prompts that are specific and descriptive. Always include:

1. **Subject** -- Clearly state what appears in the image.
2. **Lighting** -- Specify lighting conditions (golden hour, studio lighting, dramatic shadows, soft diffused light).
3. **Composition** -- Describe framing and perspective (close-up, wide angle, bird's eye view, centered).
4. **Style** -- Define the visual style (photorealistic, watercolor, oil painting, cinematic, minimalist).
5. **Mood** -- Set the emotional tone (serene, dramatic, whimsical, moody, vibrant).

### Good vs. Mediocre Prompts

Mediocre: `"a dog in a park"`

Good: `"A golden retriever running through a sun-dappled meadow in late afternoon light, captured with a shallow depth of field, warm golden tones, joyful and energetic mood, photorealistic style"`

Mediocre: `"a city at night"`

Good: `"A rain-soaked Tokyo street at midnight with neon signs reflecting off wet pavement, shot from a low angle, cyberpunk aesthetic, moody atmosphere with deep blues and vivid pinks, cinematic composition"`

## Aspect Ratio Guidance

Select the aspect ratio that fits the intended use:

- **1:1** -- Social media posts, profile pictures, square formats, icons, thumbnails.
- **16:9** -- Landscape photography, desktop wallpapers, presentation slides, YouTube thumbnails, cinematic scenes.
- **9:16** -- Phone wallpapers, Instagram/TikTok stories, vertical posters, mobile-first content.
- **4:3** -- Traditional photography, documents, web content, blog images.
- **3:4** -- Portrait photography, posters, book covers, vertical prints.

If the user does not specify, infer the best ratio from context. Default to `1:1` when uncertain.

## Negative Prompts

Use `negativePrompt` to steer the model away from unwanted elements. Apply negative prompts when:

- The user mentions things they do not want in the image.
- Previous generations included artifacts or unwanted elements.
- Aiming for a specific quality level.

Common negative prompt patterns:
- Quality control: `"blurry, low quality, distorted, pixelated, artifacts"`
- Style control: `"cartoonish, oversaturated, flat lighting"`
- Content control: `"text, watermark, logo, border, frame"`

## Batch Generation

Set `numImages` up to 4 to generate multiple variations in one call. Use batch generation when:

- The user wants options to choose from.
- Exploring different interpretations of a prompt.
- The user explicitly requests multiple images.

## Output

Generated images are saved as PNG files in the current working directory with the naming pattern:

```
generated_image_<TIMESTAMP>_<N>.png
```

Where `<TIMESTAMP>` is the Unix epoch in milliseconds and `<N>` is the image index (1-based).

After generation, inform the user of the saved file paths. Use the Read tool to display the generated images so the user can see the results immediately.

## Error Handling

If generation fails, check for:
- Safety filter blocks -- suggest the user rephrase the prompt.
- API quota limits -- inform the user to check their Gemini API quota.
- API key issues -- confirm GEMINI_API_KEY is configured in the plugin settings.
