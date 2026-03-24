// Warm Editorial Light Design System
// Copy the relevant parts into your tailwind.config.ts

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Warm paper backgrounds
        paper: {
          50: "#FFFFFF", // Card surfaces
          100: "#FAFAF8", // Page background
          200: "#F5F3F0", // Terminal/code background
          300: "#F2F0ED", // Secondary surfaces
          400: "#E8E4DF", // Borders, dividers
          500: "#DDD9D3", // Empty grid blocks
          600: "#CBC4B6", // Disabled states
        },
        // Warm ink text
        ink: {
          50: "#9A9590", // Muted (captions, labels)
          100: "#6B6560", // Secondary text
          200: "#4A4540", // Medium emphasis
          300: "#2D2A26", // Primary text (warm charcoal)
          400: "#1C1915", // Headings, high contrast
        },
        // Claude-inspired warm terracotta (primary accent — same scale as dark)
        accent: {
          50: "#fdf4f0",
          100: "#fbe6de",
          200: "#f7ccc0",
          300: "#f0a892",
          400: "#e67e5a",
          500: "#d97757", // <- Primary
          600: "#cc5a36", // <- Hero accent
          700: "#a84a2d",
          800: "#8a3e28",
          900: "#723625",
        },
        // Sage green (prompts, success)
        sage: {
          50: "#f0f4f1",
          100: "#dce6df",
          200: "#b5ccba",
          300: "#8bb396",
          400: "#6d9a77",
          500: "#5A7052", // <- Primary (darker for light bg)
          600: "#4a5d44",
          700: "#3d4d38",
          800: "#323f2f",
          900: "#283327",
        },
        // Teal (links, info)
        teal: {
          50: "#f0f5f4",
          100: "#dce9e7",
          200: "#b8d3cf",
          300: "#8fbdb6",
          400: "#72a89f",
          500: "#5F8F86", // <- Primary
          600: "#4d756d",
          700: "#405f59",
          800: "#364e49",
          900: "#2d403c",
        },
        // Amber (warnings, gold highlights)
        amber: {
          50: "#fdf8ed",
          100: "#f9edcf",
          200: "#f2d99e",
          300: "#e8c06a",
          400: "#dca93f",
          500: "#B7791F", // <- Primary (darker for light bg)
          600: "#9a651a",
          700: "#7d5217",
          800: "#664315",
          900: "#543813",
        },
      },
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
        display: ["Instrument Serif", "Georgia", "serif"],
        mono: ["IBM Plex Mono", "Menlo", "monospace"],
      },
      boxShadow: {
        // Light theme: shadows instead of glows
        card: "0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.05)",
        elevated:
          "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05)",
        terminal: "0 8px 30px -10px rgba(0, 0, 0, 0.15)",
        // Subtle accent glow (used sparingly)
        "accent-soft": "0 0 20px rgba(217, 119, 87, 0.15)",
      },
      borderColor: {
        subtle: "rgba(0, 0, 0, 0.06)",
        medium: "rgba(0, 0, 0, 0.10)",
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease",
        "fade-in-up": "fadeInUp 0.5s ease",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      // Typography plugin configuration for prose (light mode)
      typography: {
        DEFAULT: {
          css: {
            "--tw-prose-body": "#6B6560",
            "--tw-prose-headings": "#2D2A26",
            "--tw-prose-lead": "#4A4540",
            "--tw-prose-links": "#CC5A36",
            "--tw-prose-bold": "#2D2A26",
            "--tw-prose-counters": "#9A9590",
            "--tw-prose-bullets": "#DDD9D3",
            "--tw-prose-hr": "rgba(0, 0, 0, 0.06)",
            "--tw-prose-quotes": "#2D2A26",
            "--tw-prose-quote-borders": "#CC5A36",
            "--tw-prose-captions": "#9A9590",
            "--tw-prose-code": "#CC5A36",
            "--tw-prose-pre-code": "#2D2A26",
            "--tw-prose-pre-bg": "#F5F3F0",
            "--tw-prose-th-borders": "rgba(0, 0, 0, 0.1)",
            "--tw-prose-td-borders": "rgba(0, 0, 0, 0.06)",
          },
        },
      },
    },
  },
  plugins: [
    // require("@tailwindcss/typography"), // Optional: for prose styles
  ],
};

export default config;

/*
Google Fonts to add to your layout:

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=IBM+Plex+Mono:wght@400;500;600&family=Instrument+Serif&display=swap" rel="stylesheet" />

Or with next/font:

import { DM_Sans, Instrument_Serif, IBM_Plex_Mono } from 'next/font/google';

const dmSans = DM_Sans({ subsets: ['latin'], variable: '--font-sans' });
const instrumentSerif = Instrument_Serif({ subsets: ['latin'], weight: '400', variable: '--font-display' });
const ibmPlexMono = IBM_Plex_Mono({ subsets: ['latin'], weight: ['400', '500', '600'], variable: '--font-mono' });
*/
