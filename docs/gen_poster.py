"""FPMS degree-show poster — 1280 × 1920 px, academic conference style."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.image as mpimg
import numpy as np

DEST = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'screenshots')
DPI  = 100
W, H = 12.8, 19.2   # 1280 × 1920 px

NAVY  = '#1B2A4A'
BLUE  = '#2E75B6'
DBLUE = '#1F497D'
WHITE = '#FFFFFF'
LGREY = '#F0F4F8'
DGREY = '#222233'
MGREY = '#556677'

fig = plt.figure(figsize=(W, H), dpi=DPI)
fig.patch.set_facecolor(WHITE)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.axis('off'); ax.set_facecolor(WHITE)

# ─── helpers ──────────────────────────────────────────────────────────────────
def shdr(x, y, w, label, c=DBLUE, fs=11):
    ax.text(x, y, label, ha='left', va='bottom',
            fontsize=fs, fontweight='bold', color=c, zorder=4)
    ax.plot([x, x+w], [y-0.04, y-0.04], color=c, lw=1.8, zorder=4)
    return y - 0.26   # return y just below the underline

def blt(x, y, text, fs=8.6, c=DGREY, gap=0.32):
    ax.text(x,        y, '▸', ha='left', va='top', fontsize=fs,
            color=BLUE, fontweight='bold', zorder=4)
    ax.text(x+0.26, y, text, ha='left', va='top',
            fontsize=fs, color=c, zorder=4)
    return y - gap

def add_img(path, lx, by, iw, ih):
    if not os.path.exists(path):
        ax.add_patch(Rectangle((lx,by),iw,ih, facecolor=LGREY,
                                edgecolor=BLUE, linewidth=1, zorder=8))
        return
    img = mpimg.imread(path)
    # crop to target aspect ratio so nothing is stretched
    target = iw / ih
    h, w = img.shape[:2]
    if w / h > target:          # too wide — crop sides
        new_w = int(h * target)
        x0 = (w - new_w) // 2
        img = img[:, x0:x0+new_w]
    else:                       # too tall — show top (most useful content)
        new_h = int(w / target)
        img = img[:new_h, :]
    # blue border
    ax.add_patch(Rectangle((lx-0.06, by-0.06), iw+0.12, ih+0.12,
                            facecolor=BLUE, linewidth=0, zorder=8))
    a = fig.add_axes([lx/W, by/H, iw/W, ih/H])
    a.imshow(img, aspect='auto', interpolation='lanczos')
    a.axis('off')

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER  y = 17.2 → 19.2
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(Rectangle((0, 17.2), W, 2.0, facecolor=NAVY, zorder=1))
ax.add_patch(Rectangle((0, 17.2), W, 0.10, facecolor=BLUE, zorder=2))

# FPMS — large, anchored top so it never clips
ax.text(W/2, 19.10, 'FPMS', ha='center', va='top',
        fontsize=46, fontweight='bold', color=WHITE, zorder=3)
# Full title — below FPMS
ax.text(W/2, 18.42, 'Fighter Performance Management System',
        ha='center', va='top', fontsize=16, fontweight='bold',
        color='#9DC3E6', zorder=3)
# Tagline — below full title
ax.text(W/2, 18.04,
        'A combat sports training platform: camp planning · sparring · weight management · events · real-time chat',
        ha='center', va='top', fontsize=9, color='#C0D5E8', style='italic', zorder=3)
# Student name
ax.text(0.45, 17.72, 'Youssef Nour',
        ha='left', va='top', fontsize=12, fontweight='bold', color=WHITE, zorder=3)
# Student details
ax.text(0.45, 17.44,
        'Student ID: 23019868     UFCFFF-30 Final Year Project     UWE Bristol     2025–26',
        ha='left', va='top', fontsize=8.5, color='#7A9AB5', zorder=3)

# ═══════════════════════════════════════════════════════════════════════════════
# BODY  y = 2.70 → 17.20     columns separated at x = 6.30
# ═══════════════════════════════════════════════════════════════════════════════
ax.plot([6.30, 6.30], [2.80, 17.10], color='#CCDDEE', lw=0.9, zorder=2)

LX, LW = 0.38, 5.68    # left col
RX, RW = 6.52, 6.05    # right col

# ════════════════════════════ LEFT COLUMN ═════════════════════════════════════
Y = 17.05   # cursor

# ── Introduction ──────────────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Introduction')
for line in [
    'Combat sports athletes manage their preparation with disconnected tools —',
    'paper notebooks, spreadsheets, separate event websites and WhatsApp groups.',
    'None understand fight-camp periodisation, weight-class targets or sparring',
    'compatibility. FPMS unifies all of this in a single accessible platform.',
]:
    ax.text(LX, Y, line, ha='left', va='top', fontsize=9, color=DGREY, zorder=4)
    Y -= 0.168
Y -= 0.24

# ── Aims & Objectives ─────────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Aims & Objectives')
for obj in [
    'O1   Research existing sports management tools and combat-sports user needs.',
    'O2   Derive functional and non-functional requirements as numbered use cases.',
    'O3   Build a Flask web app with real-time WebSocket and a relational database.',
    'O4   Test the system against all requirements with manual black-box testing.',
    'O5   Critically reflect on development process, decisions and shortcomings.',
]:
    ax.text(LX, Y, obj, ha='left', va='top', fontsize=9, color=DGREY, zorder=4)
    Y -= 0.30
Y -= 0.24

# ── System Requirements ───────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'System Requirements')
ax.text(LX, Y, '40 Functional  ·  17 Non-Functional  ·  15 Use Cases',
        ha='left', va='top', fontsize=8.8, color=BLUE, fontweight='bold', zorder=4)
Y -= 0.26

rows = [
    ('Authentication',   'Registration, hashed passwords, CSRF, session management.'),
    ('Training',         'Camp planner, game plan builder, adaptive phase count.'),
    ('Weight/Readiness', '7-day weight trend, composite 0–100 readiness score.'),
    ('Social',           'Friend request lifecycle, WebSocket chat, unread counts.'),
    ('Sparring',         'Haversine partner matching, session workflow, peer rating.'),
    ('Events',           'Public discovery, interest/registration, admin panel.'),
]
for mod, desc in rows:
    ax.add_patch(FancyBboxPatch((LX, Y-0.28), LW, 0.30,
        boxstyle='round,pad=0.03', linewidth=0, facecolor='#EAF1F9', zorder=3))
    ax.text(LX+0.12, Y-0.13, mod, ha='left', va='center',
            fontsize=8.6, fontweight='bold', color=DBLUE, zorder=4)
    ax.text(LX+1.68, Y-0.13, desc, ha='left', va='center',
            fontsize=8.4, color=DGREY, zorder=4)
    Y -= 0.36
Y -= 0.22

# ── Development Methodology ───────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Development Methodology')
ax.text(LX, Y,
    'Iterative Agile approach: four two-to-three-week iterations, each delivering',
    ha='left', va='top', fontsize=9, color=DGREY, zorder=4); Y -= 0.168
ax.text(LX, Y,
    'a demonstrable vertical slice of functionality.',
    ha='left', va='top', fontsize=9, color=DGREY, zorder=4); Y -= 0.22

for label, desc in [
    ('Iteration 1:', 'Project scaffold, database schema, authentication, fighter profile.'),
    ('Iteration 2:', 'Camp planner, game plan, weight tracker, risk-readiness score.'),
    ('Iteration 3:', 'Friend system, real-time WebSocket chat, sparring matching.'),
    ('Iteration 4:', 'Events module, admin panel, Blueprint refactor, full testing.'),
]:
    ax.text(LX,      Y, label, ha='left', va='top', fontsize=8.8,
            fontweight='bold', color=BLUE, zorder=4)
    ax.text(LX+1.14, Y, desc,  ha='left', va='top', fontsize=8.8,
            color=DGREY, zorder=4)
    Y -= 0.30
Y -= 0.22

# ── Testing & Results ─────────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Testing & Results')
ax.text(LX, Y,
    'Manual black-box testing across all 44 routes — each exercised with a',
    ha='left', va='top', fontsize=9, color=DGREY, zorder=4); Y -= 0.168
ax.text(LX, Y,
    'passing path and at least one error/access-control scenario.',
    ha='left', va='top', fontsize=9, color=DGREY, zorder=4); Y -= 0.22

for num, label in [
    ('44/44', 'routes tested — 100% coverage across all 7 Blueprints'),
    ('40/40', 'functional requirements verified (Must/Should/Could)'),
    ('17/17', 'non-functional requirements met (ISO/IEC 9126)'),
    ('   0',  'Must-have requirements failed or left unimplemented'),
]:
    ax.add_patch(FancyBboxPatch((LX, Y-0.26), 0.84, 0.28,
        boxstyle='round,pad=0.03', linewidth=0, facecolor=NAVY, zorder=3))
    ax.text(LX+0.42, Y-0.12, num, ha='center', va='center',
            fontsize=8.2, fontweight='bold', color=WHITE, zorder=4)
    ax.text(LX+0.96, Y-0.12, label, ha='left', va='center',
            fontsize=8.6, color=DGREY, zorder=4)
    Y -= 0.36
Y -= 0.22

# ── Conclusion ────────────────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Conclusion')
for line in [
    'FPMS demonstrates that a solo developer, working iteratively over twelve',
    'weeks, can deliver a multi-module platform covering the full preparation',
    'lifecycle of an amateur fighter. The Blueprint architecture, Haversine',
    'matching and decision-tree algorithms proved effective within Flask.',
]:
    ax.text(LX, Y, line, ha='left', va='top', fontsize=9, color=DGREY, zorder=4)
    Y -= 0.168
Y -= 0.24

# ── Future Work ───────────────────────────────────────────────────────────────
Y = shdr(LX, Y, LW, 'Future Work')
for fw in [
    'Pytest integration tests targeting all 44 routes.',
    'Deploy to cloud: PostgreSQL, HTTPS, environment-variable secrets.',
    'Wearable integration: Garmin / Apple HealthKit for weight import.',
    'Real-user testing with amateur fighters at a local gym.',
]:
    Y = blt(LX, Y, fw, fs=8.8, gap=0.30)

# ════════════════════════════ RIGHT COLUMN ════════════════════════════════════

# ── Key Features (6 cards, from top) ─────────────────────────────────────────
RY = 17.05
RY = shdr(RX, RY, RW, 'Key Features')

features = [
    ('Camp Planner',
     'Keyword-analyses opponent strengths/weaknesses to generate a periodised',
     'training plan. Phase count adapts to weeks remaining: 3, 4 or 5 phases.'),
    ('Game Plan Builder',
     '15-branch decision tree produces round-by-round tactical strategy covering',
     'preferred range, techniques to drill, what to avoid, and per-round goals.'),
    ('Weight & Readiness Score',
     'Daily weight log with 7-day trend. Composite 0–100 readiness score shows',
     'deductions: weight overage, training days, plan absence, fight proximity.'),
    ('Sparring Finder',
     'Partners ranked by compatibility: skill-level gap, style match and distance',
     'via Haversine formula. Partners scoring below 50 are excluded from results.'),
    ('Events',
     'Public event discovery with multi-field filter (no login needed). Users can',
     'create events, register interest and manage their own event listings.'),
    ('Real-Time Chat',
     'WebSocket messaging via Flask-SocketIO. Live unread-count badges update',
     'across all pages; messages persist between sessions in the database.'),
]

CARD_H = 0.72
CARD_GAP = 0.10
for i, (title, line1, line2) in enumerate(features):
    cy = RY - i * (CARD_H + CARD_GAP)
    # card background
    ax.add_patch(FancyBboxPatch((RX, cy-CARD_H), RW, CARD_H,
        boxstyle='round,pad=0.05', linewidth=0.8,
        edgecolor='#CCDAEB', facecolor='#EAF1F9', zorder=3))
    # left accent
    ax.add_patch(Rectangle((RX, cy-CARD_H), 0.07, CARD_H,
        facecolor=BLUE, linewidth=0, zorder=4))
    ax.text(RX+0.18, cy-0.14, title, ha='left', va='top',
            fontsize=9.2, fontweight='bold', color=DBLUE, zorder=5)
    ax.text(RX+0.18, cy-0.36, line1, ha='left', va='top',
            fontsize=8.3, color=DGREY, zorder=5)
    ax.text(RX+0.18, cy-0.53, line2, ha='left', va='top',
            fontsize=8.3, color=DGREY, zorder=5)

# bottom of last card
shots_top = RY - 6*(CARD_H+CARD_GAP) - 0.18

# ── Application Screenshots ───────────────────────────────────────────────────
shdr(RX, shots_top, RW, 'Application Screenshots')
SY = shots_top - 0.26
SH = 2.55   # each screenshot height

add_img(os.path.join(DEST, '02_dashboard.png'), RX, SY-SH, RW, SH)
ax.text(RX+RW/2, SY-SH-0.18,
        'Figure 1 — Dashboard: fight countdown, weight status, camp phase and readiness score',
        ha='center', va='top', fontsize=7.8, color=MGREY, style='italic', zorder=12)

SY2 = SY - SH - 0.40
add_img(os.path.join(DEST, '04_sparring_dashboard.png'), RX, SY2-SH, RW, SH)
ax.text(RX+RW/2, SY2-SH-0.18,
        'Figure 2 — Sparring partner finder: Haversine-ranked cards with skill and distance',
        ha='center', va='top', fontsize=7.8, color=MGREY, style='italic', zorder=12)

arch_top = SY2 - SH - 0.40

# ── System Architecture ───────────────────────────────────────────────────────
shdr(RX, arch_top, RW, 'System Architecture')
AY = arch_top - 0.28
for line in [
    'Server-rendered Flask app structured as 7 Blueprints (auth, main, training,',
    'social, fighters, sparring, events). SQLAlchemy 2.x maps 14 model classes',
    'to SQLite (switchable to PostgreSQL via one URI change). Shared extensions',
    '(LoginManager, SocketIO) in extensions.py prevent circular imports.',
]:
    ax.text(RX, AY, line, ha='left', va='top', fontsize=8.8, color=DGREY, zorder=4)
    AY -= 0.165

# ═══════════════════════════════════════════════════════════════════════════════
# TECHNOLOGIES STRIP  y = 1.38 → 2.70
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(Rectangle((0, 1.38), W, 1.32, facecolor=LGREY, zorder=1))
ax.text(0.45, 2.50, 'Technologies Used', ha='left', va='center',
        fontsize=11, fontweight='bold', color=DBLUE, zorder=3)

tech = [('Python 3.13',NAVY),('Flask 3.x',DBLUE),('SQLAlchemy','#8B4513'),
        ('Flask-SocketIO','#5B2C8D'),('Bootstrap 5','#563D7C'),
        ('WTForms',DBLUE),('SQLite','#777')]
pw, ph = 1.54, 0.42
px0 = 0.45
for i,(name,col) in enumerate(tech):
    px = px0 + i*(pw+0.13)
    ax.add_patch(FancyBboxPatch((px,1.52),pw,ph,
        boxstyle='round,pad=0.06',linewidth=1.5,
        edgecolor=col,facecolor=WHITE,zorder=3))
    ax.text(px+pw/2,1.52+ph/2,name,ha='center',va='center',
            fontsize=8.8,fontweight='bold',color=col,zorder=4)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER  y = 0 → 1.38
# ═══════════════════════════════════════════════════════════════════════════════
ax.add_patch(Rectangle((0,0),W,1.38,facecolor=NAVY,zorder=1))
ax.add_patch(Rectangle((0,1.30),W,0.08,facecolor=BLUE,zorder=2))
ax.text(W/2,1.00,'UFCFFF-30  —  Software Engineering for Business  —  Final Year Project',
        ha='center',va='center',fontsize=12,fontweight='bold',color='#9DC3E6',zorder=3)
ax.text(W/2,0.62,'Faculty of Environment and Technology  ·  UWE Bristol  ·  2025–26',
        ha='center',va='center',fontsize=10,color='#7A9AB5',zorder=3)
ax.text(W/2,0.28,'Supervisor: Steve Battle  ·  steve.battle@uwe.ac.uk',
        ha='center',va='center',fontsize=9,color='#4A6070',style='italic',zorder=3)

# ── save ──────────────────────────────────────────────────────────────────────
out = os.path.join(DEST,'poster.png')
plt.savefig(out,dpi=DPI,bbox_inches=None,facecolor=WHITE,pad_inches=0)
plt.close()
print(f'Saved: {out}  ({W*DPI:.0f}×{H*DPI:.0f} px)')
