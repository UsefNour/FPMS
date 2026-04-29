"""Generate a clean ERD diagram for the 14 FPMS models."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

DEST = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'screenshots')
os.makedirs(DEST, exist_ok=True)

fig, ax = plt.subplots(figsize=(18, 12))
ax.set_xlim(0, 18)
ax.set_ylim(0, 12)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Colour palette ────────────────────────────────────────────────────────────
C_USER    = '#1F497D'   # dark blue  – core user entities
C_TRAIN   = '#2E75B6'  # mid blue   – training
C_SOCIAL  = '#7030A0'  # purple     – social / chat
C_SPARR   = '#00B050'  # green      – sparring
C_EVENT   = '#C00000'  # red        – events
C_HEAD    = '#FFFFFF'
C_TEXT    = '#1A1A1A'

def draw_entity(ax, x, y, w, h, title, fields, color, fontsize=7.5):
    # header
    ax.add_patch(FancyBboxPatch((x, y + h - 0.52), w, 0.52,
                                boxstyle='round,pad=0.04', linewidth=1.2,
                                edgecolor=color, facecolor=color, zorder=3))
    ax.text(x + w/2, y + h - 0.26, title, ha='center', va='center',
            fontsize=fontsize+0.5, fontweight='bold', color=C_HEAD, zorder=4)
    # body
    ax.add_patch(FancyBboxPatch((x, y), w, h - 0.52,
                                boxstyle='round,pad=0.04', linewidth=1.2,
                                edgecolor=color, facecolor='white', zorder=2))
    row_h = (h - 0.52) / max(len(fields), 1)
    for i, (pk, fname, ftype) in enumerate(fields):
        fy = y + h - 0.52 - (i + 0.6) * row_h
        style = 'italic' if pk else 'normal'
        weight = 'bold' if pk else 'normal'
        ax.text(x + 0.12, fy, ('PK ' if pk else '   ') + fname,
                ha='left', va='center', fontsize=fontsize - 0.5,
                fontstyle=style, fontweight=weight, color=C_TEXT, zorder=4)
        ax.text(x + w - 0.08, fy, ftype,
                ha='right', va='center', fontsize=fontsize - 1.2,
                color='#666666', zorder=4)

def arrow(ax, x1, y1, x2, y2, label='', color='#888888'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.1,
                                connectionstyle='arc3,rad=0.05'), zorder=1)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my, label, fontsize=6, color=color, ha='center',
                bbox=dict(fc='white', ec='none', pad=1), zorder=5)

# ── Entities (x, y, w, h, title, [(pk, field, type)], colour) ────────────────
entities = [
    # Row 1 – core user
    (0.3,  8.5, 2.8, 3.2, 'User',
     [(True,'id','int'),(False,'username','str UNIQUE'),(False,'email','str UNIQUE'),
      (False,'password_hash','str'),(False,'is_admin','bool'),(False,'profile_pic','str')],
     C_USER),

    # Row 1 – training
    (3.4,  9.5, 2.8, 2.2, 'FighterProfile',
     [(True,'id','int'),(False,'user_id','FK→User'),(False,'weight_class','str'),
      (False,'fight_date','date'),(False,'se_angle','str')],
     C_TRAIN),

    (6.5,  9.5, 2.8, 2.2, 'CampPlan',
     [(True,'id','int'),(False,'user_id','FK→User'),(False,'opponent_name','str'),
      (False,'plan_phases','JSON'),(False,'created_at','datetime')],
     C_TRAIN),

    (9.6,  9.5, 2.8, 2.2, 'GamePlan',
     [(True,'id','int'),(False,'user_id','FK→User'),(False,'opponent_name','str'),
      (False,'round_objectives','JSON'),(False,'created_at','datetime')],
     C_TRAIN),

    (12.7, 9.5, 2.8, 2.2, 'WeightLog',
     [(True,'id','int'),(False,'user_id','FK→User'),(False,'weight','float'),
      (False,'date','date'),(False,'notes','str')],
     C_TRAIN),

    # Row 2 – social
    (0.3,  5.8, 2.8, 2.4, 'FriendRequest',
     [(True,'id','int'),(False,'sender_id','FK→User'),(False,'receiver_id','FK→User'),
      (False,'status','str'),(False,'created_at','datetime')],
     C_SOCIAL),

    (3.4,  5.8, 2.8, 2.2, 'Friendship',
     [(True,'id','int'),(False,'user1_id','FK→User'),(False,'user2_id','FK→User'),
      (False,'created_at','datetime')],
     C_SOCIAL),

    (6.5,  5.8, 2.8, 2.4, 'ChatMessage',
     [(True,'id','int'),(False,'sender_id','FK→User'),(False,'receiver_id','FK→User'),
      (False,'content','str'),(False,'is_read','bool'),(False,'timestamp','datetime')],
     C_SOCIAL),

    # Row 2 – shared
    (9.6,  5.8, 2.8, 2.2, 'Fighter',
     [(True,'id','int'),(False,'name','str'),(False,'weight_class','str'),
      (False,'fighting_style','str'),(False,'strengths','text')],
     C_TRAIN),

    # Row 3 – sparring
    (0.3,  2.8, 2.8, 2.6, 'SparringProfile',
     [(True,'id','int'),(False,'user_id','FK→User'),(False,'skill_level','str'),
      (False,'latitude','float'),(False,'longitude','float'),
      (False,'honesty_score','float')],
     C_SPARR),

    (3.4,  2.8, 2.8, 2.4, 'SparringSession',
     [(True,'id','int'),(False,'requester_id','FK→User'),(False,'partner_id','FK→User'),
      (False,'status','str'),(False,'session_date','datetime')],
     C_SPARR),

    (6.5,  2.8, 2.8, 2.4, 'SkillAssessment',
     [(True,'id','int'),(False,'session_id','FK→Session'),(False,'assessor_id','FK→User'),
      (False,'assessed_id','FK→User'),(False,'skill_rating','int')],
     C_SPARR),

    # Row 3 – events
    (9.6,  2.8, 2.8, 2.6, 'Event',
     [(True,'id','int'),(False,'organizer_id','FK→User'),(False,'name','str'),
      (False,'date','datetime'),(False,'weight_classes','str'),
      (False,'is_approved','bool')],
     C_EVENT),

    (12.7, 2.8, 2.8, 2.4, 'EventInterest',
     [(True,'id','int'),(False,'event_id','FK→Event'),(False,'user_id','FK→User'),
      (False,'status','str'),(False,'weight_class','str')],
     C_EVENT),
]

for (x, y, w, h, title, fields, color) in entities:
    draw_entity(ax, x, y, w, h, title, fields, color)

# ── Key relationships ─────────────────────────────────────────────────────────
rels = [
    # User → FighterProfile
    (3.1, 10.2, 3.4, 10.2, '1:1', C_USER),
    # User → CampPlan
    (3.1, 10.0, 6.5, 10.0, '1:N', C_TRAIN),
    # User → GamePlan
    (3.1, 9.8,  9.6,  9.8, '1:N', C_TRAIN),
    # User → WeightLog
    (3.1, 9.6,  12.7, 9.6, '1:N', C_TRAIN),
    # User → FriendRequest
    (1.7, 8.5,  1.7,  8.2, '1:N', C_SOCIAL),
    # User → Friendship
    (2.0, 8.5,  4.8,  8.0, '1:N', C_SOCIAL),
    # User → ChatMessage
    (2.2, 8.5,  7.9,  8.2, '1:N', C_SOCIAL),
    # User → SparringProfile
    (1.7, 8.5,  1.7,  5.4, '1:1', C_SPARR),
    # User → SparringSession
    (2.0, 8.5,  4.8,  5.2, '1:N', C_SPARR),
    # SparringSession → SkillAssessment
    (6.2, 4.0,  6.5,  4.0, '1:N', C_SPARR),
    # User → Event
    (2.2, 8.5,  10.0, 5.4, '1:N', C_EVENT),
    # Event → EventInterest
    (12.4, 4.0, 12.7, 4.0, '1:N', C_EVENT),
    # User → EventInterest
    (2.2, 8.5,  13.5, 5.2, '1:N', C_EVENT),
]
for (x1, y1, x2, y2, lbl, col) in rels:
    arrow(ax, x1, y1, x2, y2, lbl, col)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color=C_USER,  label='Core User'),
    mpatches.Patch(color=C_TRAIN, label='Training'),
    mpatches.Patch(color=C_SOCIAL,label='Social / Chat'),
    mpatches.Patch(color=C_SPARR, label='Sparring'),
    mpatches.Patch(color=C_EVENT, label='Events'),
]
ax.legend(handles=legend_items, loc='lower right', fontsize=8,
          framealpha=0.9, title='Module', title_fontsize=8)

ax.set_title('FPMS — Entity Relationship Overview (14 Models)',
             fontsize=13, fontweight='bold', color=C_USER, pad=10)

out = os.path.join(DEST, '01_database_schema.png')
plt.tight_layout()
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print(f'Saved: {out}')
