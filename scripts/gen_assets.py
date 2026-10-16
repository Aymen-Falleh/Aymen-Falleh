#!/usr/bin/env python3
"""Generates the animated SVG assets for the GitHub profile README.
Palette comes from aymenfalleh.me (bg #101312, panel #171a18, ivory #f6efe4,
muted #aaa69e, amber #e9ac50, rule #393b36). ORANGE/HOT are the deeper orange
accents derived from the amber for gradients and the neon edge."""
import os
import random
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG = "#101312"
PANEL = "#171a18"
IVORY = "#f6efe4"
MUTED = "#aaa69e"
AMBER = "#e9ac50"
RULE = "#393b36"
ORANGE = "#d9822b"
HOT = "#ff8a1f"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
PULSE = "2.8s"  # --motion-pulse-duration on the portfolio


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)


# ---------------------------------------------------------------- banner
def banner():
    W, H, HOR = 1200, 340, 230
    rnd = random.Random(7)
    stars = []
    for _ in range(26):
        x, y = rnd.randint(20, W - 20), rnd.randint(14, 150)
        r = rnd.choice([0.8, 1.0, 1.3])
        d = rnd.choice([2.2, 2.8, 3.4, 4.1])
        b = rnd.random() * 3
        stars.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{IVORY}" opacity=".15">'
            f'<animate attributeName="opacity" values=".1;.9;.1" dur="{d}s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>'
        )

    verticals = "".join(
        f'<line x1="600" y1="{HOR}" x2="{600 + i * 110}" y2="{H}" stroke="{AMBER}" stroke-opacity=".30" stroke-width="1"/>'
        for i in range(-16, 17)
    )

    def pos(k):
        return HOR + 1.0 * k * k

    def op(p):
        return round(min(0.78, 0.08 + 0.7 * (p - HOR) / 110), 3)

    horizontals = []
    for k in range(0, 11):
        a, b = pos(k), pos(k + 1)
        horizontals.append(
            f'<rect x="0" y="{a}" width="{W}" height="1.4" fill="{AMBER}" opacity="{op(a)}">'
            f'<animate attributeName="y" from="{a}" to="{b}" dur="2.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" from="{op(a)}" to="{op(b)}" dur="2.4s" repeatCount="indefinite"/></rect>'
        )

    slits = "".join(
        f'<rect x="500" y="{y}" width="200" height="{h}" fill="{BG}"/>'
        for y, h in [(188, 2), (198, 3), (207, 4), (215, 5), (222, 6)]
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Aymen Falleh, AI/ML Engineer and Full-Stack Developer">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="floor"><rect x="0" y="{HOR}" width="{W}" height="{H - HOR}"/></clipPath>
<clipPath id="sky"><rect x="0" y="0" width="{W}" height="{HOR}"/></clipPath>
<filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="neon" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{"".join(stars)}
<g clip-path="url(#sky)">
<circle cx="600" cy="{HOR}" r="104" fill="{AMBER}" opacity=".35" filter="url(#glow)"/>
<circle cx="600" cy="{HOR}" r="88" fill="url(#sun)" opacity=".92"/>
{slits}
</g>
<g clip-path="url(#floor)">{verticals}{"".join(horizontals)}</g>
<rect x="0" y="{HOR - 1}" width="{W}" height="2.4" fill="{AMBER}" filter="url(#neon)"/>
<text x="36" y="54" font-family="{MONO}" font-size="22" font-weight="700" fill="{AMBER}" filter="url(#neon)">AF.</text>
<text x="{W - 36}" y="52" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}" letter-spacing="1.5">aymenfalleh.me</text>
<text x="600" y="96" text-anchor="middle" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="9" fill="{AMBER}" filter="url(#glow)" opacity=".8">AYMEN FALLEH<animate attributeName="opacity" values=".45;.95;.45" dur="{PULSE}" repeatCount="indefinite"/></text>
<text x="600" y="96" text-anchor="middle" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="9" fill="{IVORY}" stroke="{AMBER}" stroke-width=".8">AYMEN FALLEH</text>
<text x="600" y="132" text-anchor="middle" font-family="{MONO}" font-size="17" letter-spacing="4" fill="{AMBER}" filter="url(#neon)">AI/ML ENGINEER  ·  FULL-STACK DEVELOPER</text>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="{RULE}" stroke-width="1.5"/>
</svg>
'''
    write("banner.svg", svg)


# -------------------------------------------------------------- terminal
LINES = [
    ("cmd", "whoami"),
    ("out", "Aymen Falleh - AI/ML Engineer & Full-Stack Developer"),
    ("cmd", "cat mission.txt"),
    ("out", "Got an idea? I build the system that makes it real."),
    ("cmd", "ls stack/"),
    ("out", "python  pytorch  fastapi  django  nextjs  react  docker  postgres  redis"),
    ("cmd", "./ship --no-matter-what"),
    ("out", "[ok] shipped. every time."),
]


def terminal():
    W, H, PAD = 860, 330, 14
    FS, CW, X0 = 15, 9.0, 52
    CMD_DT, OUT_DT = 0.055, 0.018

    # timeline
    t = 0.6
    timing = []
    for kind, text in LINES:
        dt = CMD_DT if kind == "cmd" else OUT_DT
        timing.append((t, dt))
        t += len(text) * dt + (0.35 if kind == "cmd" else 0.6)
    T = round(t + 4.5, 2)

    def kt(vals):
        return ";".join(f"{min(v / T, 1):.5f}" for v in vals)

    clips, texts, cursors = [], [], []
    for i, ((kind, text), (start, dt)) in enumerate(zip(LINES, timing)):
        group = i // 2
        base = 80 + group * 62 + (26 if kind == "out" else 0)
        n = len(text)
        width = n * CW
        times = [0] + [start + j * dt for j in range(n)] + [T]
        wvals = [0] + [(j + 1) * CW for j in range(n)] + [width]
        xvals = [X0] + [X0 + (j + 1) * CW for j in range(n)] + [X0 + width]
        clips.append(
            f'<clipPath id="c{i}"><rect x="{X0}" y="{base - 17}" width="0" height="24">'
            f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt(times)}" values="{";".join(f"{v:g}" for v in wvals)}"/></rect></clipPath>'
        )
        color = IVORY if kind == "cmd" else AMBER
        flt = "" if kind == "cmd" else ' filter="url(#neon)"'
        if kind == "cmd":
            texts.append(
                f'<text x="28" y="{base}" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="{HOT}" opacity="0">$'
                f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{kt([0, start, T])}" values="0;1;1"/></text>'
            )
        texts.append(
            f'<text x="{X0}" y="{base}" xml:space="preserve" font-family="{MONO}" font-size="{FS}" '
            f'textLength="{width:g}" lengthAdjust="spacing" fill="{color}" clip-path="url(#c{i})"{flt}>{escape(text)}</text>'
        )
        # cursor: visible from this line's start until the next line starts
        nxt = timing[i + 1][0] if i + 1 < len(LINES) else None
        if nxt is not None:
            okt, okv = kt([0, start, nxt, T]), "0;1;0;0"
        else:
            okt, okv = kt([0, start, T]), "0;1;1"
        cursors.append(
            f'<rect x="{X0}" y="{base - 14}" width="8" height="17" fill="{AMBER}" opacity="0">'
            f'<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt(times)}" values="{";".join(f"{v:g}" for v in xvals)}"/>'
            f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{okt}" values="{okv}"/></rect>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 2 * PAD} {H + 2 * PAD}" width="{W + 2 * PAD}" height="{H + 2 * PAD}" role="img" aria-label="Animated terminal: whoami, cat mission.txt, ls stack, ship">
<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<filter id="neon" x="-5%" y="-40%" width="110%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="halo" x="-5%" y="-10%" width="110%" height="120%"><feGaussianBlur stdDeviation="6"/></filter>
{"".join(clips)}
</defs>
<g transform="translate({PAD} {PAD})">
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{AMBER}" stroke-width="3" filter="url(#halo)" opacity=".5"><animate attributeName="opacity" values=".25;.8;.25" dur="{PULSE}" repeatCount="indefinite"/></rect>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="40" fill="{BG}"/>
<rect y="40" width="{W}" height="1" fill="{RULE}"/>
<circle cx="26" cy="20" r="6" fill="{HOT}"/><circle cx="46" cy="20" r="6" fill="{AMBER}"/><circle cx="66" cy="20" r="6" fill="{MUTED}" opacity=".55"/>
<text x="{W / 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">aymen@portfolio: ~/shipping</text>
{"".join(texts)}
<g>{"".join(cursors)}<animate attributeName="opacity" values="1;0;0" keyTimes="0;0.5;1" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/></g>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="{RULE}" stroke-width="1.5"/>
</g>
</svg>
'''
    write("terminal.svg", svg)


# ------------------------------------------------------------------- CTA
def cta(filename="cta.svg", text="VIEW MY WORK  →  aymenfalleh.me", label="View my work at aymenfalleh.me"):
    W, H = 560, 100
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="pill"><rect x="14" y="14" width="{W - 28}" height="72" rx="36"/></clipPath>
<filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<rect x="14" y="14" width="{W - 28}" height="72" rx="36" fill="{AMBER}" filter="url(#glow)" opacity=".5"><animate attributeName="opacity" values=".3;.85;.3" dur="{PULSE}" repeatCount="indefinite"/></rect>
<rect x="14" y="14" width="{W - 28}" height="72" rx="36" fill="url(#g)"/>
<g clip-path="url(#pill)"><rect x="-140" y="0" width="110" height="{H}" fill="url(#sh)" transform="skewX(-20)"><animate attributeName="x" from="-140" to="700" dur="3.6s" repeatCount="indefinite"/></rect></g>
<text x="{W / 2}" y="59" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="800" letter-spacing="2" fill="{BG}">{escape(text)}</text>
</svg>
'''
    write(filename, svg)


# ------------------------------------------------------------------ hook
def hook():
    W, H, PAD = 860, 210, 14
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 2 * PAD} {H + 2 * PAD}" width="{W + 2 * PAD}" height="{H + 2 * PAD}" role="img" aria-label="Have an idea? Don't hesitate to contact me. Let's build it together.">
<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".5" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>
<filter id="neon" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="halo" x="-5%" y="-10%" width="110%" height="120%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b" filterUnits="userSpaceOnUse" x="-300" y="-8" width="1800" height="32"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<g transform="translate({PAD} {PAD})">
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{AMBER}" stroke-width="3" filter="url(#halo)" opacity=".5"><animate attributeName="opacity" values=".25;.85;.25" dur="{PULSE}" repeatCount="indefinite"/></rect>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<text x="28" y="38" font-family="{MONO}" font-size="14" fill="{MUTED}"><tspan fill="{HOT}" font-weight="700">$</tspan> ./build --together</text>
<rect x="212" y="25" width="8" height="16" fill="{AMBER}"><animate attributeName="opacity" values="1;0;0" keyTimes="0;0.5;1" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/></rect>
<g opacity="0">
<animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.9s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" begin="0.2s" dur="0.9s" fill="freeze"/>
<text x="{W / 2}" y="108" text-anchor="middle" font-family="{SANS}" font-size="50" font-weight="800" fill="{AMBER}" filter="url(#glow)" opacity=".8">Have an idea?<animate attributeName="opacity" values=".4;.95;.4" dur="{PULSE}" repeatCount="indefinite"/></text>
<text x="{W / 2}" y="108" text-anchor="middle" font-family="{SANS}" font-size="50" font-weight="800" fill="{IVORY}">Have an idea?</text>
</g>
<g opacity="0">
<animate attributeName="opacity" from="0" to="1" begin="0.9s" dur="0.9s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" begin="0.9s" dur="0.9s" fill="freeze"/>
<text x="{W / 2}" y="156" text-anchor="middle" font-family="{SANS}" font-size="21" fill="{IVORY}">Don't hesitate to contact me, <tspan fill="{AMBER}" font-weight="700" filter="url(#neon)">let's build it together.</tspan></text>
</g>
<rect x="-260" y="{H - 14}" width="260" height="4" fill="url(#s)" filter="url(#b)"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect>
<rect x="-260" y="{H - 13}" width="260" height="2" fill="url(#s)"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="{RULE}" stroke-width="1.5"/>
</g>
</svg>
'''
    write("hook.svg", svg)


# --------------------------------------------------------------- divider
def divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 16" width="1200" height="16" role="presentation">
<defs>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".5" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>
<filter id="b" filterUnits="userSpaceOnUse" x="-300" y="-8" width="1800" height="32"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<rect x="0" y="7" width="1200" height="2" fill="{RULE}"/>
<rect x="-260" y="6" width="260" height="4" fill="url(#s)" filter="url(#b)"><animate attributeName="x" from="-260" to="1200" dur="4s" repeatCount="indefinite"/></rect>
<rect x="-260" y="7" width="260" height="2" fill="url(#s)"><animate attributeName="x" from="-260" to="1200" dur="4s" repeatCount="indefinite"/></rect>
</svg>
'''
    write("divider.svg", svg)


banner()
terminal()
cta()
cta("cta-mail.svg", "EMAIL ME YOUR IDEA  →", "Email me your idea")
hook()
divider()
print("ok", os.listdir(OUT))
