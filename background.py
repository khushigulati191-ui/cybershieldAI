"""
Animated background: a subtle glowing hex network with floating light
particles, evoking a live security-scan grid rather than generic decoration.

Implementation note: this used to be injected as a separate `position:
fixed` <div> inside the markdown tree. That broke in practice — Streamlit
wraps markdown content in several nested containers, and those containers
can establish their own CSS stacking context (fade-in transitions use
`transform`/`opacity` on wrapper divs). Once that happens, a fixed element
with `z-index: -1` gets trapped behind that ancestor's own painted
background instead of the full page, so it silently renders invisible.

The fix: build one self-contained SVG (hex grid + pulse lines + floating
particles, animated via its own internal <style>/@keyframes), base64-encode
it, and attach it as a CSS `background-image` directly on Streamlit's own
top-level container (`[data-testid="stAppViewContainer"]`). That's a
stable, well-known attachment point, and a pure CSS background paint can't
get trapped behind anything the way a DOM element can.
"""

import base64
import math
import random

import streamlit as st

# Fixed seed so the hex grid layout (and which nodes/pulses are "active")
# stays stable across Streamlit reruns instead of jumping around every time
# the user clicks a button.
_SEED = 11
_WIDTH, _HEIGHT = 2400, 1400


def _hex_points(cx: float, cy: float, r: float) -> str:
    """SVG polygon points for a flat-top hexagon centered at (cx, cy)."""
    pts = []
    for i in range(6):
        angle = math.radians(60 * i)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)


def _build_hex_elements(rows: int = 15, cols: int = 28, hex_r: float = 58):
    """Compute a flat-top hex grid plus a handful of 'active' pulse lines
    between neighboring nodes, tiled across the SVG canvas."""
    rng = random.Random(_SEED)
    hex_w, hex_h = hex_r * 1.5, hex_r * math.sqrt(3)
    nodes = {}
    for row in range(rows):
        for col in range(cols):
            cx = col * hex_w + hex_r
            cy = row * hex_h + (hex_h / 2 if col % 2 else 0) + hex_r
            nodes[(row, col)] = (cx, cy)

    outlines = "".join(
        f'<polygon class="hex-cell" points="{_hex_points(cx, cy, hex_r * 0.92)}" '
        f'style="animation-delay:{rng.uniform(0, 8):.2f}s"/>'
        for (cx, cy) in nodes.values()
    )

    active_keys = rng.sample(list(nodes.keys()), k=max(6, len(nodes) // 8))
    dots = "".join(
        f'<circle class="hex-node" cx="{nodes[k][0]:.1f}" cy="{nodes[k][1]:.1f}" r="3.6" '
        f'style="animation-delay:{rng.uniform(0, 4):.2f}s"/>'
        for k in active_keys
    )

    lines = []
    for row, col in active_keys:
        for dr, dc in ((0, 1), (1, 0)):
            neighbor = (row + dr, col + dc)
            if neighbor in nodes and rng.random() > 0.35:
                x1, y1 = nodes[(row, col)]
                x2, y2 = nodes[neighbor]
                lines.append(
                    f'<line class="hex-pulse" x1="{x1:.1f}" y1="{y1:.1f}" '
                    f'x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'style="animation-delay:{rng.uniform(0, 5):.2f}s"/>'
                )

    return outlines, "".join(lines), dots


def _build_particles(count: int = 20) -> str:
    """Small glowing dots that drift upward and fade, looped via CSS."""
    rng = random.Random(_SEED + 1)
    circles = []
    for _ in range(count):
        cx = rng.uniform(30, _WIDTH - 30)
        cy = rng.uniform(_HEIGHT * 0.35, _HEIGHT - 10)
        circles.append(
            f'<circle class="particle" cx="{cx:.1f}" cy="{cy:.1f}" r="2.8" '
            f'style="animation-delay:{rng.uniform(0, 14):.2f}s; '
            f'animation-duration:{rng.uniform(12, 22):.1f}s"/>'
        )
    return "".join(circles)


def _build_svg() -> str:
    outlines, lines, dots = _build_hex_elements()
    particles = _build_particles()

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_WIDTH} {_HEIGHT}">
<defs>
<style>
.hex-cell {{ fill:none; stroke:rgba(56,189,248,0.22); stroke-width:1.4;
  animation: hexBreathe 8s ease-in-out infinite; }}
.hex-node {{ fill:#22d3ee; filter:drop-shadow(0 0 6px rgba(34,211,238,0.95));
  animation: nodePulse 4s ease-in-out infinite; }}
.hex-pulse {{ fill:none; stroke:rgba(34,211,238,0.65); stroke-width:1.6;
  stroke-dasharray:8 220; animation: pulseTravel 5s linear infinite; }}
.particle {{ fill:#38bdf8; filter:drop-shadow(0 0 4px rgba(56,189,248,0.9));
  animation-name: floatUp; animation-timing-function: ease-in;
  animation-iteration-count: infinite; }}
@keyframes hexBreathe {{ 0%,100% {{ stroke-opacity:0.45; }} 50% {{ stroke-opacity:1; }} }}
@keyframes nodePulse {{ 0%,100% {{ opacity:0.45; }} 50% {{ opacity:1; }} }}
@keyframes pulseTravel {{
  0% {{ stroke-dashoffset:220; opacity:0; }}
  12% {{ opacity:1; }} 88% {{ opacity:1; }}
  100% {{ stroke-dashoffset:0; opacity:0; }} }}
@keyframes floatUp {{
  0% {{ transform:translateY(0); opacity:0; }}
  10% {{ opacity:0.9; }} 85% {{ opacity:0.5; }}
  100% {{ transform:translateY(-{_HEIGHT + 100}px); opacity:0; }} }}
</style>
</defs>
<rect width="{_WIDTH}" height="{_HEIGHT}" fill="#05070d"/>
{outlines}
{lines}
{dots}
{particles}
</svg>"""


def render_background():
    """Attach the animated hex-network + particle artwork as a background
    image on Streamlit's own app container. Call once near the top of
    app.py, before any visible content."""
    encoded = base64.b64encode(_build_svg().encode("utf-8")).decode("ascii")

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: #05070d;
            background-image:
                radial-gradient(ellipse 900px 500px at 15% -5%, rgba(99,102,241,0.20), transparent 60%),
                radial-gradient(ellipse 900px 600px at 90% 8%, rgba(34,211,238,0.16), transparent 55%),
                url("data:image/svg+xml;base64,{encoded}");
            background-size: cover, cover, cover;
            background-position: center, center, center center;
            background-repeat: no-repeat, no-repeat, no-repeat;
            background-attachment: fixed, fixed, fixed;
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

