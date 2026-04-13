import ephem
import math
from datetime import datetime, timezone

moon = ephem.Moon()
moon.compute(datetime.now(timezone.utc))

phase = moon.phase          # 0-100, percentage illuminated
age = moon.age / 86400      # days since new moon (ephem returns seconds)

# Map to named phase
def get_phase_name(age):
    if age < 1.85:   return "New Moon"
    elif age < 7.38: return "Waxing Crescent"
    elif age < 9.22: return "First Quarter"
    elif age < 14.76: return "Waxing Gibbous"
    elif age < 16.61: return "Full Moon"
    elif age < 22.15: return "Waning Gibbous"
    elif age < 23.99: return "Last Quarter"
    elif age < 29.53: return "Waning Crescent"
    else:             return "New Moon"

phase_name = get_phase_name(age)
illumination = round(moon.phase, 1)
date_str = datetime.now(timezone.utc).strftime("%d %b %Y")

# Compute the terminator path for the moon disc
# The moon is a circle; the terminator is an ellipse scaled by cos(phase_angle)
# phase_angle in [0, 2pi] maps age 0->29.53 days
phase_angle = (age / 29.53) * 2 * math.pi
cx, cy, r = 60, 60, 48

# Terminator x-scale: cos of phase angle
# Negative = lit on right (waxing), positive = lit on left (waning)
terminator_scale = math.cos(phase_angle)
waxing = age < 14.765

# Build the SVG clip path for the illuminated portion
# Strategy: always draw a full circle, then overlay a "dark" crescent
# using two arcs -- one semicircle and one ellipse arc

def moon_path(r, term_scale, waxing):
    """
    Returns SVG path for the dark (unlit) portion of the moon.
    r: radius
    term_scale: cos(phase_angle), -1..1
    waxing: bool
    """
    # The lit half is always a semicircle on the right (waxing) or left (waning)
    # The terminator is an ellipse with x-radius = abs(term_scale)*r
    rx = abs(term_scale) * r
    
    if waxing:
        # Dark side on the left: left semicircle + terminator ellipse
        # If term_scale < 0 (past new, before half): dark crescent on left
        # If term_scale > 0 (past half, before full): dark sliver on left
        if term_scale <= 0:
            # Dark = left semicircle + right-bulging ellipse (covers more than half)
            sweep_ellipse = 1  # ellipse sweeps right (same direction as left semicircle)
        else:
            # Dark = left semicircle + left-bulging ellipse (covers less than half)
            sweep_ellipse = 0
        path = (
            f"M {r},{r-r} "           # top of circle
            f"A {r},{r} 0 0,0 {r},{r+r} "  # left semicircle (top to bottom, sweep=0)
            f"A {rx},{r} 0 0,{sweep_ellipse} {r},{r-r}"  # ellipse back to top
        )
    else:
        # Waning: dark side on the right
        if term_scale >= 0:
            sweep_ellipse = 0
        else:
            sweep_ellipse = 1
        path = (
            f"M {r},{r-r} "
            f"A {r},{r} 0 0,1 {r},{r+r} "  # right semicircle
            f"A {rx},{r} 0 0,{sweep_ellipse} {r},{r-r}"
        )
    return path

dark_path = moon_path(r, terminator_scale, waxing)

svg = f"""<svg width="340" height="110" viewBox="0 0 340 110"
     xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Current moon phase: {phase_name}, {illumination}% illuminated">
  <title>Moon Phase</title>

  <!-- background -->
  <rect width="340" height="110" rx="10" fill="#0a0f1e"/>

  <!-- stars -->
  <circle cx="20"  cy="15" r="1"   fill="#ffffff" opacity="0.6"/>
  <circle cx="50"  cy="8"  r="0.8" fill="#ffffff" opacity="0.4"/>
  <circle cx="140" cy="12" r="1"   fill="#ffffff" opacity="0.5"/>
  <circle cx="190" cy="6"  r="0.8" fill="#ffffff" opacity="0.3"/>
  <circle cx="230" cy="18" r="1"   fill="#ffffff" opacity="0.6"/>
  <circle cx="270" cy="9"  r="0.8" fill="#ffffff" opacity="0.4"/>
  <circle cx="310" cy="14" r="1"   fill="#ffffff" opacity="0.5"/>
  <circle cx="160" cy="95" r="0.8" fill="#ffffff" opacity="0.3"/>
  <circle cx="290" cy="88" r="1"   fill="#ffffff" opacity="0.4"/>
  <circle cx="80"  cy="90" r="0.8" fill="#ffffff" opacity="0.3"/>

  <!-- moon disc (lit portion = full circle in lunar white) -->
  <circle cx="60" cy="55" r="{r}" fill="#dde8f0"/>

  <!-- dark overlay for unlit portion -->
  <path d="{dark_path}" fill="#0a0f1e" transform="translate(12,7)"/>

  <!-- text -->
  <text x="130" y="38" font-family="monospace" font-size="13"
        font-weight="600" fill="#e8eeff">{phase_name}</text>
  <text x="130" y="58" font-family="monospace" font-size="11"
        fill="#8899cc">Illumination: {illumination}%</text>
  <text x="130" y="76" font-family="monospace" font-size="11"
        fill="#8899cc">Age: {age:.1f} days</text>
  <text x="130" y="96" font-family="monospace" font-size="10"
        fill="#4a5a80">Updated: {date_str} UTC</text>
</svg>"""

with open("moon.svg", "w") as f:
    f.write(svg)

print(f"Generated: {phase_name}, {illumination}% illuminated, age {age:.1f}d")
