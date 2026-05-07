# Persona 5 UI Design Skill

Apply Persona 5-style UI/UX design principles to the current task. Use the research and developer documentation below as your design bible. When implementing any UI component, animation, screen, or interaction in **any project**, evaluate it against these principles before writing code.

**This skill is global — it applies to any game, app, or web project. P5 UI is a shared visual language you can apply across all your work.**

---

## Source Research

### Primary Academic Source
**"Studi Visual UI dan UX pada Gim Persona 5 Royal"**
- Journal: DIVAGATRA – Jurnal Penelitian Mahasiswa Desain (Universitas Komputer Indonesia)
- Year: 2024
- URL: https://ojs.unikom.ac.id/index.php/divagatra/article/view/12339
- ResearchGate: https://www.researchgate.net/publication/385703960_Studi_Visual_UI_dan_UX_pada_Gim_Persona_5_Royal
- Focus: Visual analysis of UI/UX design principles in Persona 5 Royal — typography, color, motion, layout

### Developer Primary Source
**"Creative method for UI in the Persona series ~ UI case examples from Persona 5"**
- Event: CEDEC + KYUSHU 2017 (Computer Entertainment Developers Conference)
- Presenters: Masayoshi Sutoh (Art Director / Lead UI Designer), Kazuhisa Wada (Director)
- Summary: https://personacentral.com/persona-5-panel-concept-development-ui/
- Focus: How Atlus built Persona 5's visual identity — concept, iteration, cultural grounding

### Supporting Sources
- **GDC 2025** — Koji Ise (Lead UI Designer, Atlus): "From Persona to Metaphor: ReFantazio — Creating a Visual Identity for a New Series"
- **Georgetown University CCTP-748 (2018)**: "Identify Cultural Reference in Persona 5's UI Design, and Why It Immerse Gaming Experience" — Peircean semiotic analysis of P5 UI — https://blogs.commons.georgetown.edu/cctp-748-spring2018/2018/05/05/identify-cultural-factors-in-persona-5s-ui-design-and-its-influence-on-gaming-experience/
- **The Game Design Forum**: "Examining JRPG UI" (PDF survey) — http://thegamedesignforum.com/features/JRPG_UI_SURVEY.pdf
- **DIVA Portal thesis**: Narrative Structure in Persona 5 — https://www.diva-portal.org/smash/get/diva2:1580898/FULLTEXT01.pdf

---

## Core Design Principles

### 1. Aggressive Geometry & Diagonal Energy
- Avoid rectangles. Use parallelograms, trapezoids, angled clips (`clip-path: polygon(...)`)
- Every panel, button, and card should have at least one angled edge
- Diagonals create tension and movement — static boxes feel dead
- Web: use `style={{ clipPath: 'polygon(...)' }}` or custom CSS shapes
- Godot: use StyleBoxFlat with custom skew, or TextureRect with diagonal mask

### 2. Color System — High Contrast, Minimal Palette
- Primary: black (`#0a0a0a`), red (`#c41a1f`), white/cream
- Accent: gold (`#ffcc00`) for highlights, confirmation, and focus states
- Never use mid-tones as dominant colors — everything is either very dark or very bright
- Red is for selection, confirmation, danger, and emphasis — never decorative
- Black backgrounds make colors pop; avoid grey backgrounds
- Project-specific palettes map directly onto this system

### 3. Typography — Loud Display Font + Tiny Mono Labels
- Headlines: display font, large, often rotated ±1°–3°, sometimes skewed
- UI labels: monospace, 8–11px, ALL CAPS, wide letter-spacing (`tracking-[0.3em]`)
- Never mix two display fonts — one loud, one mono, nothing else
- Numbers are always displayed in the display font at large sizes
- Text can overlap geometry — labels sit on top of colored shapes

### 4. Motion — Fast, Deliberate, Punctuated
- Transitions: 150–300ms for micro-interactions, 600–900ms for screen transitions
- Easing: ease-out for enters (things arrive fast), ease-in for exits (things leave with intention)
- Never use linear easing — it reads as mechanical, not cinematic
- Idle animations (flicker, pulse) should be slow and subtle — 3–6s cycle
- In Godot: use Tween with EASE_OUT/EASE_IN, never Linear

### 5. Information Hierarchy — Scannable at a Glance
- One dominant element per screen (the thing the user must act on)
- Supporting information is small, muted, and monospace
- Use thin horizontal rules, slash separators, and breadcrumb labels to structure space
- Never center-align body content — left-align creates reading flow
- Counter-rotate some elements (headline vs. label) to create dynamic tension

### 6. UI as Character — Every Element Has Personality
- Buttons feel like stamps or stickers — hard edges, no soft shadows
- Hover/focus states should feel like the UI is responding, not just changing color
- Selected states should feel committed — red fill, white text, no ambiguity
- Background decoration (kanji, numbers, lines) should be near-invisible (3–6% opacity)
- The UI should look hand-designed, not generated — use asymmetry intentionally

### 7. Camera & 3D Interaction
- Zoom in on selection: camera should arrive at a slightly off-center angle (not straight-on)
- Alternate yaw direction between selections so consecutive views feel different
- Highlight on camera arrival, not on click — let the camera travel complete first
- Highlight should be temporary (1.5–2s) — a flash, not a state
- Auto-rotate at idle; lock camera on selection

### 8. Sound Design Philosophy (from CEDEC 2017)
- UI sounds should be short, punchy, and distinct between action types
- Click ≠ Confirm ≠ Cancel ≠ Navigate — each needs its own audio signature
- Sound reinforces the "stamp" quality of interactions

---

## How to Apply This Skill

When invoked, review the current task or the file/component provided and:

1. **Audit**: Identify any elements that violate the principles above (soft shadows, rounded corners, centered text, grey mid-tones, symmetric layouts, linear animations)
2. **Redesign**: Propose specific implementation — Tailwind classes, clip-path values, color tokens, animation durations, or Godot node settings
3. **Implement**: Write or modify the code directly, referencing the principles as comments where the reasoning isn't obvious
4. **Check**: After implementation, verify the component reads as "designed by a human with strong opinions" — not AI-generated or default

If the user pastes a component or describes a screen, apply the above to improve it.
If the user says `/p5-ui [component name]`, find that component in the codebase and audit + improve it.
