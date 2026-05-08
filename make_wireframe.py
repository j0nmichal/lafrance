from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

OUT = "uscold-admin-wireframe.pdf"
W, H = landscape(A4)   # 297 x 210 mm in points  (841.9 x 595.3 pt)

c = canvas.Canvas(OUT, pagesize=landscape(A4))

# ── Palette ──────────────────────────────────────────────────────────────────
BG       = (0.039, 0.086, 0.157)   # #0A1628
PANEL    = (0.055, 0.110, 0.188)   # slightly lighter navy
SIDEBAR  = (0.047, 0.098, 0.173)
ACCENT   = (0.000, 0.831, 1.000)   # #00D4FF
MIST     = (0.659, 0.749, 0.816)   # #A8BFD0
TEXT     = (0.941, 0.965, 0.980)   # #F0F6FA
BORDER   = (0.200, 0.300, 0.400)
GREEN    = (0.204, 0.827, 0.600)
GRAY     = (0.300, 0.350, 0.400)
RED_SOFT = (0.969, 0.529, 0.529)
WHITE    = (1, 1, 1)

def rgb(t): return t

def fill(t):  c.setFillColorRGB(*t)
def stroke(t): c.setStrokeColorRGB(*t)

def rect(x, y, w, h, fill_color=None, stroke_color=None, lw=0.5, radius=0):
    if fill_color:   fill(fill_color)
    if stroke_color: stroke(stroke_color); c.setLineWidth(lw)
    if fill_color and stroke_color:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1) if radius else c.rect(x, y, w, h, fill=1, stroke=1)
    elif fill_color:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0) if radius else c.rect(x, y, w, h, fill=1, stroke=0)
    elif stroke_color:
        c.roundRect(x, y, w, h, radius, fill=0, stroke=1) if radius else c.rect(x, y, w, h, fill=0, stroke=1)

def text(x, y, s, size=7, color=TEXT, bold=False, align='left'):
    fill(color)
    fname = 'Helvetica-Bold' if bold else 'Helvetica'
    c.setFont(fname, size)
    if align == 'center':
        c.drawCentredString(x, y, s)
    elif align == 'right':
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)

def label(x, y, s, size=5.5, color=MIST):
    text(x, y, s, size=size, color=color)

def toggle(x, y, on=False, w=20, h=10):
    col = GREEN if on else GRAY
    rect(x, y, w, h, fill_color=col, radius=5)
    dot_x = x + w - 7 if on else x + 3
    rect(dot_x, y + 2, 6, 6, fill_color=WHITE, radius=3)

def input_box(x, y, w, h=12, placeholder='', value=''):
    rect(x, y, w, h, fill_color=(0.06, 0.12, 0.20), stroke_color=BORDER, lw=0.4, radius=2)
    s = value if value else placeholder
    col = TEXT if value else (*MIST, )
    fill(MIST if not value else TEXT)
    c.setFont('Helvetica', 5.5)
    c.drawString(x + 4, y + 3.5, s)

def section_head(x, y, s, w):
    fill((0.07, 0.15, 0.25))
    c.rect(x, y, w, 13, fill=1, stroke=0)
    text(x + 5, y + 4, s.upper(), size=5.5, color=ACCENT, bold=True)

def badge(x, y, s, color=MIST, bg=None):
    c.setFont('Helvetica', 5)
    sw = c.stringWidth(s, 'Helvetica', 5)
    bw = sw + 8
    bh = 9
    if bg:
        rect(x, y, bw, bh, fill_color=bg, radius=2)
    else:
        rect(x, y, bw, bh, stroke_color=color, lw=0.5, radius=2)
    fill(color)
    c.drawString(x + 4, y + 2.5, s)
    return bw + 4

# ── Page background ───────────────────────────────────────────────────────────
fill(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# ── Grid overlay (subtle) ─────────────────────────────────────────────────────
c.setStrokeColorRGB(0, 0.83, 1, alpha=0.03)
c.setLineWidth(0.3)
GRID = 24
for gx in range(0, int(W), GRID):
    c.line(gx, 0, gx, H)
for gy in range(0, int(H), GRID):
    c.line(0, gy, W, gy)

# ── Layout constants ──────────────────────────────────────────────────────────
TOP_BAR_H  = 32
SIDEBAR_W  = 168
MARGIN     = 10
MAIN_X     = SIDEBAR_W
MAIN_W     = W - SIDEBAR_W
CONTENT_Y  = H - TOP_BAR_H
FORM_PAD   = 14

# ─────────────────────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────────────────────
rect(0, H - TOP_BAR_H, W, TOP_BAR_H, fill_color=(0.05, 0.10, 0.18))
c.setStrokeColorRGB(*BORDER)
c.setLineWidth(0.5)
c.line(0, H - TOP_BAR_H, W, H - TOP_BAR_H)

# Logo
text(14, H - 20, "US COLD", size=9, color=ACCENT, bold=True)
text(60, H - 20, "— Admin", size=9, color=MIST)

# Save status area
rect(W - 160, H - 26, 80, 14, stroke_color=BORDER, lw=0.4, radius=2)
text(W - 155, H - 21, "● Saved", size=6, color=GREEN)

# Add Facility button
rect(W - 72, H - 26, 62, 14, fill_color=(0.0, 0.50, 0.62), radius=2)
text(W - 57, H - 21, "+ Add Facility", size=6, color=WHITE, bold=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
rect(0, 0, SIDEBAR_W, CONTENT_Y, fill_color=SIDEBAR)
c.setStrokeColorRGB(*BORDER)
c.setLineWidth(0.5)
c.line(SIDEBAR_W, 0, SIDEBAR_W, CONTENT_Y)

# Sidebar search
SY = CONTENT_Y - 10
input_box(6, SY - 14, SIDEBAR_W - 12, 13, placeholder="🔍  Search facilities…")

# Filter pills
FY = SY - 34
pill_labels = ["All", "Published", "Unpublished"]
pill_colors = [ACCENT, MIST, MIST]
pill_fills  = [(0.0, 0.40, 0.50), None, None]
px = 6
for i, pl in enumerate(pill_labels):
    pw = 42 if pl == 'Unpublished' else 28
    if i == 0:
        rect(px, FY, pw, 12, fill_color=pill_fills[0], radius=2)
        text(px + pw/2, FY + 3.5, pl, size=5.5, color=WHITE, align='center')
    else:
        rect(px, FY, pw, 12, stroke_color=BORDER, lw=0.5, radius=2)
        text(px + pw/2, FY + 3.5, pl, size=5.5, color=MIST, align='center')
    px += pw + 4

# State filter dropdown
label(6, FY - 12, "FILTER BY STATE")
input_box(6, FY - 26, SIDEBAR_W - 12, 13, placeholder="All States  ▾")

# Facility list items
LY   = FY - 50
items = [
    ("Allentown Cold Storage",    "PA", True,  True),
    ("Atlanta Refrigerated Svcs", "GA", False, False),
    ("Charlotte Cold Storage",    "NC", True,  False),
    ("Chicago — O'Hare",          "IL", True,  True),
    ("Cincinnati Cold Chain",     "OH", True,  False),
    ("Dallas Central",            "TX", True,  True),
    ("Denver Cold Storage",       "CO", False, False),
    ("Detroit Freezer",           "MI", True,  False),
    ("Houston South",             "TX", True,  True),
    ("Indianapolis Hub",          "IN", True,  False),
    ("Kansas City Cold",          "MO", True,  False),
    ("Los Angeles — Vernon",      "CA", True,  True),
]

for i, (name, state, published, selected) in enumerate(items):
    iy = LY - i * 18
    if iy < 10: break
    # Item background
    if selected:
        rect(0, iy - 2, SIDEBAR_W, 18, fill_color=(0.06, 0.14, 0.24))
        c.setStrokeColorRGB(*ACCENT)
        c.setLineWidth(1.5)
        c.line(0, iy - 2, 0, iy + 16)
    # Name + state
    text(10, iy + 5, name[:26], size=6, color=TEXT if selected else (0.7, 0.8, 0.85))
    text(SIDEBAR_W - 22, iy + 5, state, size=5.5, color=ACCENT if selected else MIST)
    # Published dot
    fill(GREEN if published else GRAY)
    c.circle(SIDEBAR_W - 8, iy + 7, 2.5, fill=1, stroke=0)
    # Divider
    if not selected:
        c.setStrokeColorRGB(*BORDER)
        c.setLineWidth(0.3)
        c.line(6, iy - 2, SIDEBAR_W - 6, iy - 2)

# Scroll hint
text(SIDEBAR_W / 2, 14, "↑ scroll for more", size=5, color=MIST, align='center')
text(SIDEBAR_W / 2, 7, f"39 total facilities", size=5, color=MIST, align='center')

# ─────────────────────────────────────────────────────────────────────────────
# MAIN PANEL — Edit Form
# ─────────────────────────────────────────────────────────────────────────────
MX  = MAIN_X + FORM_PAD
MXR = MAIN_X + MAIN_W / 2 + 4          # right column start
COL = (MAIN_W - FORM_PAD * 2 - 8) / 2   # column width
FH  = 12                                 # field height
FG  = 18                                 # field gap (label+input)
SG  = 6                                  # section gap

# Panel header
rect(MAIN_X, CONTENT_Y - 36, MAIN_W, 36, fill_color=(0.05, 0.11, 0.19))
text(MX, CONTENT_Y - 14, "Dallas Central", size=11, color=TEXT, bold=True)
text(MX, CONTENT_Y - 26, "TX  ·  Dallas", size=7, color=MIST)

# Published toggle in header
text(W - 130, CONTENT_Y - 16, "PUBLISHED", size=5.5, color=MIST)
toggle(W - 95, CONTENT_Y - 22, on=True)
text(W - 68, CONTENT_Y - 16, "LIVE", size=5.5, color=GREEN)

# Last updated
text(W - 130, CONTENT_Y - 28, "Updated 2 hours ago", size=5, color=MIST)

# ── SECTION 1: Basic Info ─────────────────────────────────────────────────────
CY = CONTENT_Y - 50
section_head(MAIN_X, CY, "Basic Information", MAIN_W - FORM_PAD)

CY -= FG
label(MX, CY + 2, "FACILITY NAME *")
input_box(MX, CY - FH, COL * 2 + 8, FH, value="Dallas Central")

CY -= FG + 2
label(MX, CY + 2, "STATE")
input_box(MX, CY - FH, 44, FH, value="TX")
label(MX + 52, CY + 2, "CITY")
input_box(MX + 52, CY - FH, COL - 60, FH, value="Dallas")
label(MXR, CY + 2, "ZIP")
input_box(MXR, CY - FH, 52, FH, value="75207")

CY -= FG + 2
label(MX, CY + 2, "ADDRESS")
input_box(MX, CY - FH, COL * 2 + 8, FH, value="1234 Industrial Blvd")

CY -= FG + 2
label(MX, CY + 2, "PHONE")
input_box(MX, CY - FH, COL, FH, value="(214) 555-0100")
label(MXR, CY + 2, "CONTACT EMAIL")
input_box(MXR, CY - FH, COL, FH, placeholder="contact@uscold.com")

# ── SECTION 2: Capacity & Temperature ────────────────────────────────────────
CY -= FG + SG
section_head(MAIN_X, CY, "Capacity & Temperature", MAIN_W - FORM_PAD)

CY -= FG
label(MX, CY + 2, "PALLET POSITIONS")
input_box(MX, CY - FH, COL, FH, value="12,500")
label(MXR, CY + 2, "SQUARE FOOTAGE")
input_box(MXR, CY - FH, COL, FH, value="285,000")

CY -= FG + 2
label(MX, CY + 2, "TEMP MIN (°F)")
input_box(MX, CY - FH, 60, FH, value="-10")
label(MX + 70, CY + 2, "TEMP MAX (°F)")
input_box(MX + 70, CY - FH, 60, FH, value="34")

# ── SECTION 3: Capabilities ───────────────────────────────────────────────────
CY -= FG + SG
section_head(MAIN_X, CY, "Capabilities", MAIN_W - FORM_PAD)

CY -= 8
TOGGLE_W = 80
TY = CY
TX = MX

# Row 1 toggles
toggles_r1 = [
    ("Rail Access", True),
    ("Quick Freeze", True),
    ("Automated", False),
    ("Layer Pick", False),
]
for name, on in toggles_r1:
    toggle(TX, TY - 10, on=on)
    text(TX + 26, TY - 6, name, size=6, color=TEXT if on else MIST)
    TX += (MAIN_W - FORM_PAD * 2) / 4

# Rail carrier conditional field
TY -= 20
label(MX, TY + 2, "RAIL CARRIER  (shown when Rail Access is on)")
input_box(MX, TY - FH, 100, FH, value="BNSF")

# Row 2 toggles
TY -= FG + 6
TX = MX
toggles_r2 = [
    ("Organic", False),
    ("Repack", True),
    ("Export / Import", False),
    ("Dedicated", True),
]
for name, on in toggles_r2:
    toggle(TX, TY - 10, on=on)
    text(TX + 26, TY - 6, name, size=6, color=TEXT if on else MIST)
    TX += (MAIN_W - FORM_PAD * 2) / 4

# Quick Freeze Auto conditional
TY -= 20
toggle(MX + (MAIN_W - FORM_PAD * 2) / 4, TY - 10, on=False)
text(MX + (MAIN_W - FORM_PAD * 2) / 4 + 26, TY - 6, "Auto Quick Freeze  (shown when Quick Freeze is on)", size=6, color=MIST)

# ── SECTION 4: Certifications ─────────────────────────────────────────────────
CY = TY - FG - SG
section_head(MAIN_X, CY, "Certifications", MAIN_W - FORM_PAD)

CY -= 8
TX = MX
for name, on in [("BRCGS", True), ("USDA", True), ("FDA", False), ("SQF", False)]:
    toggle(TX, CY - 10, on=on)
    text(TX + 26, CY - 6, name, size=6, color=TEXT if on else MIST)
    TX += (MAIN_W - FORM_PAD * 2) / 4

# ── SECTION 5: Media & Notes ─────────────────────────────────────────────────
CY -= FG + SG
section_head(MAIN_X, CY, "Media & Notes", MAIN_W - FORM_PAD)

CY -= FG
label(MX, CY + 2, "IMAGE URL")
input_box(MX, CY - FH, COL * 2 + 8, FH, placeholder="https://…")

CY -= FG + 2
label(MX, CY + 2, "NOTES")
rect(MX, CY - 28, COL * 2 + 8, 28, fill_color=(0.06, 0.12, 0.20), stroke_color=BORDER, lw=0.4, radius=2)
fill(MIST)
c.setFont('Helvetica', 5.5)
c.drawString(MX + 4, CY - 14, "Internal notes about this facility…")

# ── Action buttons ────────────────────────────────────────────────────────────
BY = 16
rect(MX, BY, 70, 16, fill_color=(0.0, 0.50, 0.62), radius=2)
text(MX + 35, BY + 5, "Save Changes", size=6, color=WHITE, bold=True, align='center')

rect(MX + 78, BY, 70, 16, stroke_color=BORDER, lw=0.5, radius=2)
text(MX + 113, BY + 5, "Discard", size=6, color=MIST, align='center')

rect(W - 90, BY, 70, 16, stroke_color=(0.55, 0.20, 0.20), lw=0.5, radius=2)
text(W - 55, BY + 5, "Delete Facility", size=6, color=RED_SOFT, align='center')

# ── Scroll hint on main ───────────────────────────────────────────────────────
text(MAIN_X + MAIN_W / 2, 7, "↕  scroll to see full form", size=5, color=MIST, align='center')

# ─────────────────────────────────────────────────────────────────────────────
# ANNOTATIONS / CALLOUTS
# ─────────────────────────────────────────────────────────────────────────────
def callout(x, y, s, arrow_dx=0, arrow_dy=0):
    c.setStrokeColorRGB(1, 0.85, 0.2)
    c.setFillColorRGB(1, 0.85, 0.2)
    c.setFont('Helvetica', 5)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    sw = c.stringWidth(s, 'Helvetica', 5)
    bw = sw + 8
    c.roundRect(x - bw/2, y, bw, 10, 2, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(x, y + 3, s)
    if arrow_dx or arrow_dy:
        c.setFillColorRGB(1, 0.85, 0.2)
        c.setStrokeColorRGB(1, 0.85, 0.2)
        c.line(x, y, x + arrow_dx, y + arrow_dy)
    c.setDash([])

callout(SIDEBAR_W / 2, H - 9, "Sidebar — all 39 facilities")
callout(MAIN_X + MAIN_W / 2, H - 9, "Main panel — edit form scrolls vertically")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — Delete Confirmation Modal + Add New Facility empty form
# ─────────────────────────────────────────────────────────────────────────────
c.showPage()

# Background
fill(BG)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Grid
c.setStrokeColorRGB(0, 0.83, 1, alpha=0.03)
c.setLineWidth(0.3)
for gx in range(0, int(W), GRID):
    c.line(gx, 0, gx, H)
for gy in range(0, int(H), GRID):
    c.line(0, gy, W, gy)

# Page label
text(W / 2, H - 18, "PAGE 2 — Modal States & New Facility", size=8, color=MIST, align='center')

# ── Delete Confirmation Modal ─────────────────────────────────────────────────
MX2 = 40
MY2 = H - 40
MW2 = 220
MH2 = 130

# Backdrop
c.setFillColorRGB(0, 0, 0, alpha=0.6)
c.rect(0, 0, W / 2, H - 32, fill=1, stroke=0)

# Modal card
rect(MX2, MY2 - MH2, MW2, MH2, fill_color=(0.06, 0.13, 0.22), stroke_color=(0.2, 0.35, 0.45), lw=0.8, radius=4)

# Modal content
text(MX2 + 12, MY2 - 18, "Delete Facility", size=8, color=TEXT, bold=True)
text(MX2 + 12, MY2 - 32, "This action cannot be undone.", size=6, color=RED_SOFT)
text(MX2 + 12, MY2 - 44, "Type the facility name to confirm:", size=6, color=MIST)

# Confirm input
rect(MX2 + 12, MY2 - 72, MW2 - 24, 14, fill_color=(0.04, 0.09, 0.16), stroke_color=RED_SOFT, lw=0.5, radius=2)
text(MX2 + 16, MY2 - 66, "Dallas Central", size=6, color=TEXT)

# Match indicator
fill(GREEN)
c.setFont('Helvetica', 5.5)
c.drawString(MX2 + 12, MY2 - 80, "✓ Name matches — deletion enabled")

# Buttons
rect(MX2 + 12, MY2 - 106, 88, 14, stroke_color=BORDER, lw=0.5, radius=2)
text(MX2 + 56, MY2 - 101, "Cancel", size=6, color=MIST, align='center')

rect(MX2 + 112, MY2 - 106, 96, 14, fill_color=(0.55, 0.12, 0.12), radius=2)
text(MX2 + 160, MY2 - 101, "Delete Permanently", size=6, color=RED_SOFT, bold=True, align='center')

callout(MX2 + MW2 / 2, MY2 - MH2 - 12, "Delete modal — name-match required to enable confirm")

# ── Save Status States ────────────────────────────────────────────────────────
SX = W / 2 + 20
SY2 = H - 50
text(SX, SY2, "SAVE STATUS INDICATOR STATES", size=7, color=ACCENT, bold=True)

states = [
    ("Saving…",    (0.8, 0.8, 0.3), "POST or PATCH in flight"),
    ("● Saved",    GREEN,            "200 OK — fades after 2 s"),
    ("✕ Error",    RED_SOFT,         "Non-2xx or network failure"),
]
for i, (label_s, col, note) in enumerate(states):
    bx = SX
    by = SY2 - 24 - i * 26
    rect(bx, by, 90, 16, fill_color=(0.05, 0.10, 0.18), stroke_color=BORDER, lw=0.4, radius=2)
    text(bx + 10, by + 5, label_s, size=6.5, color=col)
    text(bx + 100, by + 5, note, size=5.5, color=MIST)

# ── Add New Facility (blank form state) ──────────────────────────────────────
NX = SX
NY = SY2 - 120

text(NX, NY, "ADD NEW FACILITY — blank form state", size=7, color=ACCENT, bold=True)

NY -= 14
section_head(NX, NY, "Basic Information", 260)
NY -= FG
label(NX + 5, NY + 2, "FACILITY NAME *")
input_box(NX + 5, NY - FH, 250, FH, placeholder="Enter facility name…")
NY -= FG + 2
label(NX + 5, NY + 2, "STATE")
input_box(NX + 5, NY - FH, 40, FH, placeholder="TX")
label(NX + 53, NY + 2, "CITY")
input_box(NX + 53, NY - FH, 100, FH, placeholder="City name")

NY -= FG + SG
# Published toggle default = OFF for new facilities
text(NX + 5, NY, "PUBLISHED", size=5.5, color=MIST)
toggle(NX + 55, NY - 10, on=False)
text(NX + 82, NY - 6, "Draft (hidden from public page)", size=5.5, color=GRAY)

NY -= 26
rect(NX + 5, NY, 70, 16, fill_color=(0.0, 0.50, 0.62), radius=2)
text(NX + 40, NY + 5, "Create Facility", size=6, color=WHITE, bold=True, align='center')

callout(NX + 130, NY - 12, "POST → auto-selects new row in sidebar after create")

# ── Field type legend ─────────────────────────────────────────────────────────
LX = SX
LY2 = 60
text(LX, LY2 + 14, "LEGEND", size=6, color=MIST, bold=True)

items_leg = [
    ("Text input",      "name, city, state, zip, phone, email, rail_carrier, image_url"),
    ("Number input",    "pallet_positions, square_footage, temp_min_f, temp_max_f"),
    ("Toggle switch",   "All boolean fields — rail_access, quick_freeze, automated, etc."),
    ("Textarea",        "notes"),
    ("Conditional",     "rail_carrier shows only when rail_access = ON"),
    ("Conditional",     "quick_freeze_auto shows only when quick_freeze = ON"),
]
for i, (kind, desc) in enumerate(items_leg):
    text(LX, LY2 - i * 9, f"  {kind}", size=5.5, color=TEXT, bold=True)
    text(LX + 65, LY2 - i * 9, f"→  {desc}", size=5.5, color=MIST)

c.save()
print(f"Saved: {OUT}")
