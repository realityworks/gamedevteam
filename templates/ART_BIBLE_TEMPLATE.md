# [Game Title] — Art Bible & Visual Style Guide

**Version**: 1.0  
**Author**: Art Director  
**Technical Sign-off**: Technical Artist  
**Production Sign-off**: Producer  

---

## 1. Visual Pillars & Creative Identity

### 1.1 Aesthetic Tone & Genre
- **Primary Art Style**: [e.g. Stylized Hand-Painted PBR, Dark Gothic Low-Poly, Clean Sci-Fi Cel-Shaded]
- **Mood / Atmosphere**: [e.g. Melancholic yet vibrant, neon-lit grit, whimsical steampunk]
- **Target Visual References**: [List of 3-5 influential games, concept art books, or cinema references]

### 1.2 The Three Visual Pillars
1. **[Pillar 1 - e.g. Silhouette Clarity]**: Characters and threats recognizable within 100 milliseconds.
2. **[Pillar 2 - e.g. Atmospheric Contrast]**: High contrast between danger (warm/saturated) and safety (cool/muted).
3. **[Pillar 3 - e.g. Tactile Materials]**: Surfaces look physically tangible with distinct wear and tear.

---

## 2. Color Palette & Lighting Rules

### 2.1 Global Color Harmony
- **Key Palette**:
  - Dominant Neutral (60%): `#2A2D34` (Deep slate environment background)
  - Secondary Tone (30%): `#3F88C5` (Structures and interactables)
  - Accent / Danger (10%): `#D72638` (Enemy tells, critical telegraphs, health UI)

### 2.2 Lighting Direction & Signposting
- **Safety / Sanctuary**: Warm gold / amber fill lights (3000K).
- **Hazard / Tension**: Harsh fluorescent greens or deep crimson directional highlights (6500K+).
- **Leading Lines**: Edge highlights and specular glints guide the player toward valid paths.

---

## 3. Asset Specifications & Budgets

| Category | Max Vertices / Polycount | Texture Resolution | Material Types |
| :--- | :--- | :--- | :--- |
| **Player Character** | 25,000 tris | 2048 x 2048 (ORM) | Master Character PBR + SSS |
| **Standard Enemy** | 8,000 tris | 1024 x 1024 (ORM) | Standard Opaque PBR |
| **Hero Boss** | 40,000 tris | 2048 x 2048 (ORM) | Dissolve / Emissive Master |
| **Modular Environment Tile** | 1,500 tris | 1024 x 1024 (Packed) | Triplanar / World-aligned |
| **Small Prop** | 300 - 800 tris | 512 x 512 (Packed) | Shared Trim Sheet |

---

## 4. Animation & VFX Guidelines

- **Frame Rate**: VFX must evaluate at full 60 FPS without GPU particle stalls.
- **Telegraphing**: Enemy attacks have clear 3-phase visual arcs: Windup (Silhouette expansion), Release (High-contrast smear), Follow-through (Recovery settle).
- **Affordance Rules**: Any interactable object must pulse or glint on proximity.
