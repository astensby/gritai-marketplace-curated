---
name: warm-terracotta-light
description: Warm Editorial Light design system for premium light-mode web interfaces. A sophisticated aesthetic combining warm paper backgrounds with terracotta accents and editorial typography. Use when building light-mode websites, dashboards, editorial content with warm neutrals, marketing or landing pages, or any Next.js/React/Tailwind project wanting this light editorial aesthetic.
argument-hint: [component-or-page]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Warm Editorial Light Design System

A warm, sophisticated light-mode design language. Paper-like backgrounds, subtle shadows instead of glows, terracotta as the hero accent. Same typography and font stack as the dark terracotta system.

## Quick Start

1. Copy colors/fonts from [references/tailwind-config.ts](references/tailwind-config.ts) into your Tailwind config
2. Add Google Fonts: `Instrument Serif`, `DM Sans`, `IBM Plex Mono`
3. Follow patterns below

## Color Palette

### Primary (Terracotta — unchanged from dark)
```
accent-500: #d97757  <- Primary CTA, links, emphasis
accent-400: #e67e5a  <- Hover states
accent-600: #cc5a36  <- Active states, hero accent
```

### Backgrounds (Warm Off-Whites)
```
paper:      #FAFAF8  <- Page background
paper-mid:  #F2F0ED  <- Secondary surfaces, sidebars
paper-term: #F5F3F0  <- Terminal/code backgrounds
card:       #FFFFFF  <- Card surfaces
```

### Text (Warm Darks)
```
ink:        #2D2A26  <- Primary text (warm charcoal)
ink-soft:   #6B6560  <- Secondary text
ink-muted:  #9A9590  <- Muted labels, captions
```

### Semantic Colors
```
sage:       #5A7052  <- Prompts, success states (darker for light bg)
teal:       #5F8F86  <- Links, info accents
amber:      #B7791F  <- Warnings, gold highlights
error:      #C53030  <- Errors (darker red for light bg)
info:       #2B6CB0  <- Info states (darker blue)
```

### Borders & Dividers
```
border-subtle: rgba(0, 0, 0, 0.06)  <- Card borders, dividers
border-medium: rgba(0, 0, 0, 0.10)  <- Stronger separation
grid-empty:    #DDD9D3 at 60%       <- Empty grid blocks (visible on light bg)
```

## Typography

| Purpose | Font | Class |
|---------|------|-------|
| Headlines | Instrument Serif | `font-display` |
| Body | DM Sans | `font-sans` |
| Code/Terminal | IBM Plex Mono | `font-mono` |

**Sizing principle:** Go generous. Body text at 1.1rem+, headlines large and confident. Let text breathe with wide line heights. This system favors readability over density.

```jsx
// Hero headline
<h1 className="font-display text-6xl sm:text-7xl lg:text-8xl" style={{ color: '#2D2A26' }}>

// Section headline with accent
<h2 className="font-display text-4xl sm:text-5xl" style={{ color: '#2D2A26' }}>
  Topic <span className="italic" style={{ color: '#5F8F86' }}>keyword</span>
</h2>

// Sub-section headline
<h3 className="font-display text-2xl sm:text-3xl" style={{ color: '#2D2A26' }}>

// Body text
<p className="text-lg sm:text-xl leading-relaxed" style={{ color: '#6B6560' }}>

// Lead/intro paragraph
<p className="text-xl sm:text-2xl leading-relaxed" style={{ color: '#6B6560' }}>
```

## Component Patterns

### Cards
```jsx
// Standard card (white on paper)
<div
  className="rounded-2xl p-8 sm:p-10"
  style={{
    background: '#FFFFFF',
    border: '1px solid rgba(0, 0, 0, 0.06)',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
  }}
>

// Elevated card (hover or featured)
<div
  className="rounded-2xl p-10 sm:p-12"
  style={{
    background: '#FFFFFF',
    border: '1px solid rgba(0, 0, 0, 0.06)',
    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
  }}
>
```

### Buttons
```jsx
// Primary (terracotta)
<button
  className="px-6 py-3 font-semibold rounded-xl transition-all"
  style={{
    background: '#CC5A36',
    color: '#FFFFFF',
    boxShadow: '0 2px 8px rgba(204, 90, 54, 0.2)',
  }}
>

// Secondary (outline on light)
<button
  className="px-6 py-3 rounded-xl transition-colors"
  style={{
    background: 'transparent',
    border: '1px solid rgba(0, 0, 0, 0.1)',
    color: '#2D2A26',
  }}
>
```

### Badges
```jsx
// Terracotta
<span
  className="px-3 py-1 rounded-full text-sm font-medium"
  style={{ background: 'rgba(204, 90, 54, 0.08)', color: '#CC5A36' }}
>

// Sage (success)
<span
  className="px-3 py-1 rounded-full text-sm font-medium"
  style={{ background: 'rgba(90, 112, 82, 0.08)', color: '#5A7052' }}
>

// Teal (info)
<span
  className="px-3 py-1 rounded-full text-sm font-medium"
  style={{ background: 'rgba(95, 143, 134, 0.08)', color: '#5F8F86' }}
>
```

### Terminal Window (Light variant)
```jsx
<div
  className="rounded-xl overflow-hidden"
  style={{
    background: '#F5F3F0',
    border: '1px solid rgba(0, 0, 0, 0.06)',
    boxShadow: '0 8px 30px -10px rgba(0, 0, 0, 0.15)',
  }}
>
  {/* Header with traffic lights */}
  <div className="px-4 py-3 flex items-center gap-2" style={{ borderBottom: '1px solid rgba(0, 0, 0, 0.06)' }}>
    <div className="w-3 h-3 rounded-full" style={{ background: '#ff5f56' }} />
    <div className="w-3 h-3 rounded-full" style={{ background: '#ffbd2e' }} />
    <div className="w-3 h-3 rounded-full" style={{ background: '#27ca40' }} />
    <span className="ml-4 text-sm font-mono" style={{ color: '#9A9590' }}>terminal</span>
  </div>
  {/* Content */}
  <div className="p-4 font-mono text-sm">
    <span style={{ color: '#5A7052' }}>$</span>
    <span className="ml-2" style={{ color: '#2D2A26' }}>command</span>
  </div>
</div>
```

## Animation (Framer Motion)

```jsx
// Fade in on scroll
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.5 }}
>

// Staggered children
const staggerContainer = {
  animate: { transition: { staggerChildren: 0.1 } }
};

<motion.div variants={staggerContainer} initial="initial" whileInView="animate">
  {items.map((item, i) => (
    <motion.div key={i} variants={{ initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } }}>
```

## Page Layout

**Sizing principle:** Use the full viewport. `max-w-7xl` (80rem/1280px) as default container, `max-w-screen-2xl` (96rem/1536px) for hero and full-width sections. Generous padding: `py-24 sm:py-32` for sections, `px-6 sm:px-8 lg:px-12` for horizontal breathing room.

```jsx
<div className="min-h-screen" style={{ background: '#FAFAF8' }}>
  {/* Paper grain texture */}
  <div
    className="fixed inset-0 pointer-events-none opacity-[0.03]"
    style={{
      backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
    }}
  />

  {/* Hero section — full width */}
  <section className="relative py-24 sm:py-32 overflow-hidden">
    <div className="max-w-screen-2xl mx-auto px-6 sm:px-8 lg:px-12 relative">
      {/* content */}
    </div>
  </section>

  {/* Content section */}
  <section className="py-24 sm:py-32" style={{ borderTop: '1px solid rgba(0, 0, 0, 0.06)' }}>
    <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      {/* content */}
    </div>
  </section>
</div>
```

## Key Differences from Dark Terracotta

| Property | Dark | Light |
|----------|------|-------|
| Page bg | `#1a1a18` | `#FAFAF8` |
| Card bg | `#2d2b28` + opacity | `#FFFFFF` |
| Terminal bg | `#282828` | `#F5F3F0` |
| Text primary | `#f5f2ed` cream | `#2D2A26` charcoal |
| Text muted | `#a8a49c` | `#6B6560` |
| Prompts | `#b8bb26` bright green | `#5A7052` sage |
| Borders | implied / none | `rgba(0,0,0,0.06)` |
| Depth | Glow orbs + blur | Box shadows |
| Texture | Scanlines | Paper grain |
| Accent | Terracotta (same) | Terracotta (same) |

## Resources

- [references/tailwind-config.ts](references/tailwind-config.ts) — Full Tailwind configuration with all colors, fonts, shadows
