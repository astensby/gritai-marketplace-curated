# Nano Banana MCP Server

A Model Context Protocol (MCP) server that provides AI image generation capabilities using Google's Nano Banana (Imagen 3) model via the Gemini API.

## Features

- **Photorealistic Image Generation**: Create high-quality images from text descriptions
- **Multiple Aspect Ratios**: Support for 1:1, 16:9, 9:16, 4:3, and 3:4 formats
- **Negative Prompts**: Specify what to avoid in generated images
- **Batch Generation**: Generate up to 4 images per request
- **STDIO Transport**: Compatible with Claude Code and other MCP clients

## Prerequisites

- Node.js 18 or higher
- Google Gemini API key

## Installation

```bash
cd mcp-servers/nanobanana
npm install
npm run build
```

## Configuration

Set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or configure it in GritAgent's Settings → API Keys.

## Usage

### With Claude Code

Add to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "nanobanana": {
      "transport": "stdio",
      "command": "node",
      "args": ["/path/to/mcp-servers/nanobanana/dist/index.js"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

### With GritAgent

1. Configure your Gemini API key in Settings → API Keys
2. Enable the "Nano Banana Image Generation" tool in your project's Tools panel
3. Use natural language instructions:
   - "Generate an image of a sunset over mountains"
   - "Create a photorealistic portrait of a cat"
   - "Make a 16:9 landscape image of a futuristic city"

## Available Tools

### `generate_image`

Generate images using Google's Nano Banana (Imagen 3) model.

**Parameters:**
- `prompt` (required): Detailed text description of the image to generate
- `negativePrompt` (optional): Things to avoid in the image
- `aspectRatio` (optional): One of "1:1", "16:9", "9:16", "4:3", "3:4" (default: "1:1")
- `numImages` (optional): Number of images to generate, 1-4 (default: 1)

**Example:**
```json
{
  "prompt": "A serene mountain lake at sunset with vibrant orange and pink clouds",
  "negativePrompt": "blurry, low quality, distorted",
  "aspectRatio": "16:9",
  "numImages": 2
}
```

## Development

### Build
```bash
npm run build
```

### Watch Mode
```bash
npm run dev
```

### Test
```bash
npm start
```

## Troubleshooting

### "API key not found" error
- Ensure `GEMINI_API_KEY` is set in your environment
- Verify the key is configured in GritAgent Settings → API Keys
- Restart the app after configuring the key

### "Content blocked by safety filters"
- Try rephrasing your prompt to be less ambiguous
- Avoid potentially sensitive content
- Use more specific, descriptive language

### "Quota exceeded"
- Check your Gemini API usage quota in Google Cloud Console
- Wait for quota to reset (usually at midnight UTC)
- Consider upgrading your API plan

## Implementation Notes

**Current Limitation:** This demo server uses the Gemini text generation API, which currently provides text descriptions rather than actual image data. For production image generation, you would need to:

1. **Enable Vertex AI API** in Google Cloud Console
2. **Use `@google-cloud/vertexai` package** instead of `@google/generative-ai`
3. **Configure service account credentials** for Vertex AI authentication
4. **Call the Imagen 3 model** directly via Vertex AI endpoint

The MCP server structure is complete and ready - only the image generation API integration needs to be updated when Imagen becomes available via the Gemini API or when Vertex AI integration is added.

## License

MIT

## Author

GritAI
