# Frontend Style Guidelines

Use this reference when a frontend needs stronger visual direction, better taste, and less generic output.

## Goal

Create interfaces that feel intentional. Avoid layouts that read like untouched starter kits, generic dashboards, or safe AI-generated UI.

## Core Principle

Start by deciding what kind of interface this should be. Calm, editorial, technical, bold, playful, dense, premium, operational, and minimal are all valid directions. Generic is not.

## Work Inside Existing Systems

- If the product already has a recognizable design system, preserve it.
- Improve it by tightening hierarchy, rhythm, states, and composition.
- Do not inject a disconnected visual style just to make it look different.

## Typography

- Avoid default system-looking typography when the project allows alternatives.
- Prefer font choices with character and a clear job:
  - Distinct display or headline face for personality
  - Clean body face for reading
  - Monospace face only when data density or technical tone benefits from it
- Build visible hierarchy with scale, spacing, case, and weight changes.
- Do not let every heading, label, and paragraph collapse into the same visual texture.

## Color and Surfaces

- Choose a deliberate palette instead of default blue-on-white or purple-on-white patterns.
- Use CSS variables or theme tokens so the visual system is coherent.
- Build depth with layered surfaces, gradients, subtle texture, glows, or framed regions where appropriate.
- Use accent colors intentionally for emphasis, status, or navigation landmarks.
- Keep contrast strong enough for readability.

## Layout and Composition

- Avoid default card-grid plus sidebar compositions unless they are clearly right for the product.
- Give the page a focal point.
- Use asymmetry, framing, stacked sections, dense data bands, or oversized type when it helps the product feel more specific.
- Keep spacing rhythmic and intentional; empty space should look chosen, not accidental.

## Motion

- Use a few meaningful animations for load-in, transitions, hierarchy, or content reveal.
- Avoid excessive micro-interactions that add noise.
- Respect reduced-motion settings.
- Prefer motion that supports comprehension over motion that merely decorates.

## Background Treatment

- Do not rely on a flat single-color backdrop by default.
- Consider gradients, radial highlights, soft noise, ruled patterns, geometric shapes, or image treatment when they support the product tone.
- Keep background treatments subordinate to content readability.

## Components and States

- Buttons, cards, tabs, tables, and forms should reflect the chosen visual direction rather than looking like untouched library defaults.
- Ensure hover, active, selected, loading, empty, success, warning, and error states are readable and intentional.
- Reuse primitives when patterns repeat, but style them with enough specificity that they feel native to the product.

## Responsiveness and Accessibility

- Validate both mobile and desktop layouts.
- Preserve keyboard navigation and visible focus states.
- Maintain readable contrast and text sizing.
- Do not trade away usability for style.

## Anti-Patterns

- Default Inter or system font everywhere with no other typographic decisions.
- Flat white or flat dark background with a few centered cards and no depth.
- Generic purple gradients unrelated to the product.
- Random decorative animation that does not explain anything.
- Repeated panels with identical spacing and no focal hierarchy.
- Library-default controls dropped in without styling integration.

## Fast Review Prompts

Ask these before finishing:

1. Would this still look the same if it belonged to ten unrelated apps?
2. Is there a visible design point of view?
3. Do typography, color, layout, and motion support the same aesthetic?
4. Does the interface remain readable and usable on smaller screens?
