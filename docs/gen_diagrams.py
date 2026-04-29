"""Generate architecture and use-case diagrams for FPMS appendices."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle

DEST = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'screenshots')
os.makedirs(DEST, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 1: Application Architecture
# ─────────────────────────────────────────────────────────────────────────────

def fbox(ax, x, y, w, h, label, color, fontsize=9, tc='white', sub=None, zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.06',
                                linewidth=1.5, edgecolor=color, facecolor=color, zorder=zorder))
    ty = y + h / 2 + (0.08 if sub else 0)
    ax.text(x + w / 2, ty, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=tc, zorder=zorder + 1)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.13, sub, ha='center', va='center',
                fontsize=fontsize - 1.5, color=tc, alpha=0.85, zorder=zorder + 1)

C_GREY   = '#555555'
C_BLUE   = '#1F497D'
C_MID    = '#2E75B6'
C_PURPLE = '#7030A0'
C_GREEN  = '#00B050'
C_RED    = '#C00000'
C_AMBER  = '#FF8C00'

fig1, ax1 = plt.subplots(figsize=(17, 9))
ax1.set_xlim(0, 17); ax1.set_ylim(0, 9)
ax1.axis('off')
fig1.patch.set_facecolor('#FAFAFA')
ax1.set_facecolor('#FAFAFA')

# Flask app outer shell
ax1.add_patch(FancyBboxPatch((3.3, 0.8), 4.5, 7.8, boxstyle='round,pad=0.1',
                              linewidth=2, edgecolor=C_BLUE, facecolor='#EEF3FA', zorder=1))
ax1.text(5.55, 8.4, 'Flask Application (app.py)', ha='center', fontsize=9.5,
         fontweight='bold', color=C_BLUE)

# Internal Flask components
fbox(ax1, 3.7, 6.5, 3.7, 0.75, 'Login Manager', '#3A6EA8', fontsize=8.5, sub='Flask-Login')
fbox(ax1, 3.7, 5.4, 3.7, 0.75, 'WebSocket Engine', C_PURPLE, fontsize=8.5, sub='Flask-SocketIO')
fbox(ax1, 3.7, 4.3, 3.7, 0.75, 'ORM Layer', C_AMBER,   fontsize=8.5, sub='SQLAlchemy 2.x')
fbox(ax1, 3.7, 3.2, 3.7, 0.75, 'Template Engine',  '#3A6EA8', fontsize=8.5, sub='Jinja2 + Bootstrap 5')
fbox(ax1, 3.7, 1.1, 3.7, 0.75, 'Form Validation',  '#3A6EA8', fontsize=8.5, sub='WTForms / Flask-WTF (CSRF)')

# Client
fbox(ax1, 0.2, 3.8, 2.2, 1.2, 'Web Browser', C_GREY, fontsize=9, sub='HTTP / WebSocket')

# Database
fbox(ax1, 3.7, 2.1, 3.7, 0.85, 'SQLite Database', C_AMBER, fontsize=9, sub='fpms.db  (14 models)')

# Blueprints
bps = [
    ('Auth Blueprint',      '/login  /signup  /logout',          C_GREY,   8.3, 7.9),
    ('Main Blueprint',      '/dashboard  /index',                C_MID,    8.3, 6.9),
    ('Training Blueprint',  '/profile  /camp_planner  /weight…', C_MID,    8.3, 5.9),
    ('Social Blueprint',    '/friends  /chat  /messages',        C_PURPLE, 8.3, 4.9),
    ('Fighters Blueprint',  '/fighters  /compare_fighters',      C_MID,    8.3, 3.9),
    ('Sparring Blueprint',  '/sparring_profile  /dashboard',     C_GREEN,  8.3, 2.9),
    ('Events Blueprint',    '/events  /admin/events',            C_RED,    8.3, 1.9),
]

for label, sub, color, bx, by in bps:
    fbox(ax1, bx, by, 5.5, 0.72, label, color, fontsize=8.5, sub=sub)

# Arrow helper
def arr(ax, x1, y1, x2, y2, color='#333333', lw=1.3, style='->', ls='solid', rad=0.0):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, connectionstyle=f'arc3,rad={rad}'))

# Browser ↔ Flask (HTTP)
arr(ax1, 2.4, 4.4, 3.3, 4.4, color=C_GREY, style='<->')
ax1.text(2.85, 4.55, 'HTTP', fontsize=7.5, color=C_GREY, ha='center')

# Browser ↔ SocketIO (WebSocket)
arr(ax1, 2.2, 4.1, 3.7, 5.55, color=C_PURPLE, style='<->', ls='dashed', rad=-0.25)
ax1.text(2.5, 4.85, 'WS', fontsize=7.5, color=C_PURPLE, ha='center')

# Flask → each Blueprint
for _, _, color, bx, by in bps:
    arr(ax1, 7.8, by + 0.36, 8.3, by + 0.36, color=color)

# ORM → DB
arr(ax1, 5.55, 4.3, 5.55, 2.95, color=C_AMBER)
ax1.text(5.75, 3.6, 'SQL', fontsize=7, color=C_AMBER)

# Blueprint → DB (shared)
arr(ax1, 8.3, 2.54, 7.4, 2.54, color=C_AMBER, rad=0.0)
ax1.text(7.85, 2.65, 'ORM', fontsize=6.5, color=C_AMBER, ha='center')

ax1.set_title('Figure D.1 — FPMS Application Architecture: Blueprint Structure and Data Flow',
              fontsize=11, fontweight='bold', color=C_BLUE, pad=10)

out1 = os.path.join(DEST, 'app_architecture.png')
plt.tight_layout()
plt.savefig(out1, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print(f'Saved: {out1}')

# ─────────────────────────────────────────────────────────────────────────────
# DIAGRAM 2: Use Case Diagram
# ─────────────────────────────────────────────────────────────────────────────

fig2, ax2 = plt.subplots(figsize=(18, 12))
ax2.set_xlim(0, 18); ax2.set_ylim(0, 12)
ax2.axis('off')
fig2.patch.set_facecolor('#FAFAFA')
ax2.set_facecolor('#FAFAFA')

# System boundary
ax2.add_patch(Rectangle((2.8, 0.3), 14.8, 11.2, linewidth=2, edgecolor=C_BLUE,
                          facecolor='none', linestyle='--', zorder=1))
ax2.text(10.2, 11.38, 'FPMS System Boundary', ha='center', fontsize=9,
         color=C_BLUE, style='italic')

# Actor helper (stick figure style with label)
def actor(ax, x, y, label):
    ax.add_patch(plt.Circle((x, y + 1.05), 0.24, color='#1F497D', zorder=5))
    ax.plot([x, x],       [y + 0.81, y + 0.32], color='#1F497D', lw=2.2, zorder=5)
    ax.plot([x-0.38, x+0.38], [y + 0.62, y + 0.62], color='#1F497D', lw=2.2, zorder=5)
    ax.plot([x, x-0.32], [y + 0.32, y - 0.12], color='#1F497D', lw=2.2, zorder=5)
    ax.plot([x, x+0.32], [y + 0.32, y - 0.12], color='#1F497D', lw=2.2, zorder=5)
    ax.text(x, y - 0.28, label, ha='center', va='top', fontsize=8.5,
            fontweight='bold', color='#1F497D')

actor(ax2, 1.4, 9.2, 'Guest')
actor(ax2, 1.4, 4.8, 'Registered\nUser')
actor(ax2, 1.4, 0.8, 'Admin')

# Module group helper
def module(ax, x, y, w, h, title, color, uses):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1',
                                 linewidth=1.5, edgecolor=color,
                                 facecolor=color + '22', zorder=2))
    ax.text(x + w / 2, y + h - 0.15, title, ha='center', va='top',
            fontsize=8.5, fontweight='bold', color=color)
    row_h = (h - 0.45) / max(len(uses), 1)
    for i, uc in enumerate(uses):
        uy = y + h - 0.45 - (i + 0.55) * row_h
        ell = mpatches.Ellipse((x + w / 2, uy), w * 0.82, row_h * 0.68,
                                linewidth=1, edgecolor=color, facecolor='white', zorder=3)
        ax.add_patch(ell)
        ax.text(x + w / 2, uy, uc, ha='center', va='center',
                fontsize=6.8, color='#1A1A1A', zorder=4)

# Auth (top-left inside boundary)
module(ax2, 3.1, 9.0, 4.2, 2.2, 'Authentication', C_GREY, [
    'Register account',
    'Log in',
    'Log out',
])

# Training (top-right inside boundary)
module(ax2, 7.7, 7.5, 9.8, 3.7, 'Training Module', C_MID, [
    'View personalised dashboard',
    'Manage fighter profile',
    'Generate camp plan',
    'Generate game plan',
    'Log weight / track cut',
    'View risk & readiness',
    'Manage opponent database',
])

# Social (middle-left)
module(ax2, 3.1, 5.2, 4.2, 3.5, 'Social Module', C_PURPLE, [
    'Send friend request',
    'Accept / decline request',
    'Real-time chat',
    'View friend profile',
])

# Sparring (middle-right)
module(ax2, 7.7, 3.4, 4.6, 3.5, 'Sparring Module', C_GREEN, [
    'Create sparring profile',
    'Discover partners',
    'Request sparring session',
    'Assess partner skill',
])

# Events (right)
module(ax2, 12.7, 0.5, 4.6, 6.2, 'Events Module', C_RED, [
    'Browse events (public)',
    'Create event',
    'Edit / delete own event',
    'Register interest',
    'Withdraw interest',
    'View my events',
    'Admin event panel',
])

# Connections — Guest
ax2.annotate('', xy=(3.1, 10.0), xytext=(1.8, 10.0),
             arrowprops=dict(arrowstyle='-', color=C_GREY, lw=1.2))
ax2.annotate('', xy=(12.7, 3.5), xytext=(1.8, 9.5),
             arrowprops=dict(arrowstyle='-', color=C_RED, lw=1.0,
                             connectionstyle='arc3,rad=0.15'))

# Connections — Registered User
for (tx, ty, color, rad) in [
    (3.1, 10.2, C_GREY,   0.0),
    (7.7,  9.3, C_MID,    0.0),
    (3.1,  6.9, C_PURPLE, 0.0),
    (7.7,  5.0, C_GREEN,  0.0),
    (12.7, 4.8, C_RED,    0.1),
]:
    ax2.annotate('', xy=(tx, ty), xytext=(1.8, 5.55),
                 arrowprops=dict(arrowstyle='-', color=color, lw=1.0,
                                 connectionstyle=f'arc3,rad={rad}'))

# Connections — Admin
ax2.annotate('', xy=(12.7, 1.2), xytext=(1.8, 1.6),
             arrowprops=dict(arrowstyle='-', color=C_RED, lw=1.2,
                             connectionstyle='arc3,rad=0.1'))

ax2.set_title('Figure D.2 — FPMS Use Case Diagram: Actors and System Interactions',
              fontsize=11, fontweight='bold', color=C_BLUE, pad=10)

legend_items = [
    mpatches.Patch(color=C_GREY,   label='Authentication'),
    mpatches.Patch(color=C_MID,    label='Training'),
    mpatches.Patch(color=C_PURPLE, label='Social'),
    mpatches.Patch(color=C_GREEN,  label='Sparring'),
    mpatches.Patch(color=C_RED,    label='Events'),
]
ax2.legend(handles=legend_items, loc='lower left', fontsize=8, framealpha=0.9, ncol=5,
           bbox_to_anchor=(0.05, -0.03))

out2 = os.path.join(DEST, 'use_case_diagram.png')
plt.tight_layout()
plt.savefig(out2, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print(f'Saved: {out2}')
