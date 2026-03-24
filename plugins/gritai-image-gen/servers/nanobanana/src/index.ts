#!/usr/bin/env node

/**
 * Nano Banana MCP Server
 *
 * This MCP server provides image generation capabilities using Google's Nano Banana
 * (Imagen 3) model via the Gemini API. It allows Claude to generate photorealistic
 * images from text descriptions.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool as MCPTool,
} from "@modelcontextprotocol/sdk/types.js";
import { GoogleGenerativeAI } from "@google/generative-ai";

// Validate environment variables
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!GEMINI_API_KEY) {
  console.error("Error: GEMINI_API_KEY environment variable is required");
  process.exit(1);
}

// Initialize Google Generative AI client
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

// MCP Server configuration
const SERVER_NAME = "imagen-mcp-server";
const SERVER_VERSION = "1.0.0";

// Aspect ratios supported by Imagen
type AspectRatio = "1:1" | "16:9" | "9:16" | "4:3" | "3:4";

// Supported Gemini image generation models
type ImageModel = "gemini-2.5-flash-image" | "gemini-3-pro-image-preview";

// Tool input schema
interface GenerateImageInput {
  prompt: string;
  negativePrompt?: string;
  aspectRatio?: AspectRatio;
  numImages?: number;
  model?: ImageModel;
}

// Create MCP server instance
const server = new Server(
  {
    name: SERVER_NAME,
    version: SERVER_VERSION,
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  const tools: MCPTool[] = [
    {
      name: "generate_image",
      description:
        "Generate high-quality, photorealistic images using Google's Imagen model. " +
        "Provides detailed, naturally lit images with minimal artifacts. " +
        "Supports various aspect ratios and can generate multiple images per request.",
      inputSchema: {
        type: "object",
        properties: {
          prompt: {
            type: "string",
            description:
              "Detailed text description of the image to generate. " +
              "Be specific about subjects, lighting, composition, style, and mood. " +
              "Example: 'A serene mountain lake at sunset with vibrant orange and pink clouds reflecting on the water'",
          },
          negativePrompt: {
            type: "string",
            description:
              "Optional text describing what to avoid in the image. " +
              "Example: 'blurry, low quality, distorted, artificial'",
          },
          aspectRatio: {
            type: "string",
            enum: ["1:1", "16:9", "9:16", "4:3", "3:4"],
            description:
              "Aspect ratio of the generated image. " +
              "1:1 for square (default), 16:9 for landscape, 9:16 for portrait, 4:3 or 3:4 for traditional formats",
            default: "1:1",
          },
          numImages: {
            type: "number",
            description: "Number of images to generate (1-4). Default is 1.",
            minimum: 1,
            maximum: 4,
            default: 1,
          },
          model: {
            type: "string",
            enum: ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"],
            description:
              "Image generation model to use. " +
              "'gemini-2.5-flash-image' (default) - Fast, optimized for high-volume, 1024px resolution. " +
              "'gemini-3-pro-image-preview' - Advanced, professional quality, up to 4K resolution, with reasoning and Google Search grounding.",
            default: "gemini-2.5-flash-image",
          },
        },
        required: ["prompt"],
      },
    },
  ];

  return { tools };
});

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "generate_image") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }

  const args = request.params.arguments as unknown as GenerateImageInput;

  // Validate input
  if (!args.prompt || args.prompt.trim() === "") {
    return {
      content: [
        {
          type: "text",
          text: "Error: Prompt is required and cannot be empty",
        },
      ],
      isError: true,
    };
  }

  const aspectRatio = args.aspectRatio || "1:1";
  const numImages = Math.min(Math.max(args.numImages || 1, 1), 4);
  const selectedModel = args.model || "gemini-2.5-flash-image";

  try {
    // Log request (for debugging)
    console.error(`Generating ${numImages} image(s) with prompt: "${args.prompt.substring(0, 50)}..."`);
    console.error(`Aspect ratio: ${aspectRatio}`);
    console.error(`Model: ${selectedModel}`);

    // Initialize Gemini image generation model with user's selection
    const model = genAI.getGenerativeModel({
      model: selectedModel
    });

    // Build the generation config
    const generationConfig: any = {
      candidateCount: numImages,
    };

    // Generate the image using the prompt directly
    // gemini-2.5-flash-image returns actual image data
    const result = await model.generateContent(args.prompt);

    const response = result.response;

    // Check if we got a response
    if (!response || !response.candidates || response.candidates.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: "Error: No images were generated. This could be due to safety filters or API limitations.",
          },
        ],
        isError: true,
      };
    }

    // Extract generated images from the response
    // gemini-2.5-flash-image returns actual image data in inlineData
    const parts = response.candidates?.[0]?.content?.parts || [];
    const images: string[] = [];

    for (const part of parts) {
      if ((part as any).inlineData) {
        const imageData = (part as any).inlineData.data;
        images.push(imageData);
      } else if ((part as any).text) {
        console.error("Warning: Received text instead of image:", (part as any).text);
      }
    }

    if (images.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: `Warning: No image data was returned. The model may have returned text instead.\n` +
                  `Response: ${response.text()}`,
          },
        ],
        isError: false,
      };
    }

    // Save images to files in the current directory
    const fs = await import('fs');
    const savedFiles: string[] = [];

    for (let i = 0; i < images.length; i++) {
      const filename = `generated_image_${Date.now()}_${i + 1}.png`;
      const buffer = Buffer.from(images[i], 'base64');
      fs.writeFileSync(filename, buffer);
      savedFiles.push(filename);
    }

    return {
      content: [
        {
          type: "text",
          text: `✅ Successfully generated ${images.length} image(s) from prompt: "${args.prompt}"\n\n` +
                `Model: ${selectedModel}\n` +
                `Aspect ratio: ${aspectRatio}\n\n` +
                `Saved to:\n${savedFiles.map(f => `  - ${f}`).join('\n')}`,
        },
      ],
    };
  } catch (error: any) {
    console.error("Error generating image:", error);

    let errorMessage = "Failed to generate image: ";

    if (error.message?.includes("API key")) {
      errorMessage += "Invalid or missing API key. Please check your GEMINI_API_KEY configuration.";
    } else if (error.message?.includes("quota")) {
      errorMessage += "API quota exceeded. Please check your Gemini API quota limits.";
    } else if (error.message?.includes("safety")) {
      errorMessage += "Content was blocked by safety filters. Try modifying your prompt.";
    } else {
      errorMessage += error.message || "Unknown error occurred";
    }

    return {
      content: [
        {
          type: "text",
          text: errorMessage,
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start the MCP server
 */
async function main() {
  console.error(`Starting ${SERVER_NAME} v${SERVER_VERSION}`);
  console.error("API Key configured:", GEMINI_API_KEY ? "Yes" : "No");
  console.error("Transport: STDIO");
  console.error("Ready to accept requests...\n");

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

// Handle errors
process.on("uncaughtException", (error) => {
  console.error("Uncaught exception:", error);
  process.exit(1);
});

process.on("unhandledRejection", (error) => {
  console.error("Unhandled rejection:", error);
  process.exit(1);
});

// Start server
main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
