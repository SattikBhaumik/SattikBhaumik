import math
from datetime import datetime, timezone

def moon_phase(date):
    """
    Calculates moon age in days (0-29.53) using a simple astronomical formula.
    No external dependencies.
    """
    known_new = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    cycle = 29.53058867
    delta = (date - known_new).total_seconds() / 86400
    age = delta % cycle
    return age

def get_phase_name(age):
    if age < 1.85:    return "New Moon"
    elif age < 7.38:  return "Waxing Crescent"
    elif age < 9.22:  return "First Quarter"
    elif age < 14.76: return "Waxing Gibbous"
    elif age < 16.61: return "Full Moon"
    elif age < 22.15: return "Waning Gibbous"
    elif age < 23.99: return "Last Quarter"
    else:             return "Waning Crescent"

def get_phase_emoji(name):
    return {
        "New Moon":        "🌑",
        "Waxing Crescent": "🌒",
        "First Quarter":   "🌓",
        "Waxing Gibbous":  "🌔",
        "Full Moon":       "🌕",
        "Waning Gibbous":  "🌖",
        "Last Quarter":    "🌗",
        "Waning Crescent": "🌘",
    }[name]

def illumination(age):
    """Fraction illuminated via cosine of phase angle."""
    phase_angle = (age / 29.53058867) * 2 * math.pi
    return round((1 - math.cos(phase_angle)) / 2 * 100, 1)

now = datetime.now(timezone.utc)
age = moon_phase(now)
phase_name = get_phase_name(age)
emoji = get_phase_emoji(phase_name)
illum = illumination(age)
date_str = now.strftime("%d %b %Y")

svg = f"""<svg width="340" height="110" viewBox="0 0 340 110"
     xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Moon phase: {phase_name}, {illum}% illuminated">
  <title>Moon Phase</title>
  <rect width="340" height="110" rx="10" fill="#0a0f1e"/>

  <!-- stars -->
  <circle cx="20"  cy="15" r="1"   fill="#ffffff" opacity="0.6"/>
  <circle cx="50"  cy="8"  r="0.8" fill="#ffffff" opacity="0.4"/>
  <circle cx="140" cy="12" r="1"   fill="#ffffff" opacity="0.5"/>
  <circle cx="190" cy="6"  r="0.8" fill="#ffffff" opacity="0.3"/>
  <circle cx="230" cy="18" r="1"   fill="#ffffff" opacity="0.6"/>
  <circle cx="270" cy="9"  r="0.8" fill="#ffffff" opacity="0.4"/>
  <circle cx="310" cy="14" r="1"   fill="#ffffff" opacity="0.5"/>
  <circle cx="80"  cy="90" r="0.8" fill="#ffffff" opacity="0.3"/>
  <circle cx="290" cy="88" r="1"   fill="#ffffff" opacity="0.4"/>

  <!-- moon emoji rendered as text -->
  <text x="55" y="68" font-size="52" text-anchor="middle"
        font-family="Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji">{emoji}</text>

  <!-- phase info -->
  <text x="100" y="36" font-family="monospace" font-size="13"
        font-weight="600" fill="#e8eeff">{phase_name}</text>
  <text x="100" y="56" font-family="monospace" font-size="11"
        fill="#8899cc">Illumination: {illum}%</text>
  <text x="100" y="74" font-family="monospace" font-size="11"
        fill="#8899cc">Age: {age:.1f} days</text>
  <text x="100" y="94" font-family="monospace" font-size="10"
        fill="#4a5a80">Updated: {date_str} UTC</text>
</svg>"""

with open("moon.svg", "w") as f:
    f.write(svg)

print(f"Done: {phase_name} {emoji} — {illum}% illuminated, age {age:.1f}d")
