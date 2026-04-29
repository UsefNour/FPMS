"""Generate a Gantt chart for the FPMS project timeline (Nov 2025 – Apr 2026)."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from datetime import date

DEST = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'screenshots')
os.makedirs(DEST, exist_ok=True)

# ── Colour palette ─────────────────────────────────────────────────────────────
C_ETHICS = '#7030A0'   # purple
C_RES    = '#2E75B6'   # blue
C_DEV    = '#00B050'   # green
C_TEST   = '#FF8C00'   # amber
C_WRITE  = '#C00000'   # red
C_REVIEW = '#1F497D'   # dark blue

# ── Task definitions: (label, start, end, colour, row) ────────────────────────
# row order: bottom = 0 (drawn first), top = highest
tasks = [
    # row, label,                                     start,              end,                colour
    (9,  'Ethics Approval',                           date(2025, 11,  1), date(2025, 11, 20), C_ETHICS),
    (8,  'Background Research & Literature Review',   date(2025, 11,  1), date(2026,  1, 20), C_RES),
    (7,  'Requirements Analysis',                     date(2025, 11, 15), date(2026,  2,  7), C_RES),
    (6,  'Iteration 1 — Auth & Fighter Profile',      date(2025, 12,  1), date(2025, 12, 31), C_DEV),
    (5,  'Iteration 2 — Training Core',               date(2026,  1,  1), date(2026,  1, 31), C_DEV),
    (4,  'Iteration 3 — Social & Sparring',           date(2026,  2,  1), date(2026,  2, 28), C_DEV),
    (3,  'Iteration 4 — Events & Blueprint Refactor', date(2026,  3,  1), date(2026,  3, 31), C_DEV),
    (2,  'Manual Testing & Evaluation',               date(2026,  3, 15), date(2026,  4, 20), C_TEST),
    (1,  'Report Writing & Finalisation',             date(2026,  3,  1), date(2026,  4, 28), C_WRITE),
    (0,  'Supervisor Review & Submission Prep',       date(2026,  4,  7), date(2026,  4, 30), C_REVIEW),
]

fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Draw bars
bar_height = 0.55
for (row, label, start, end, color) in tasks:
    ax.barh(row, (end - start).days, left=mdates.date2num(start),
            height=bar_height, color=color, alpha=0.88,
            edgecolor='white', linewidth=0.8, zorder=3)
    # label inside bar if wide enough, else right of bar
    bar_w = (end - start).days
    mid = mdates.date2num(start) + bar_w / 2
    if bar_w >= 14:
        ax.text(mid, row, label, ha='center', va='center',
                fontsize=7.8, color='white', fontweight='bold', zorder=4)
    else:
        ax.text(mdates.date2num(end) + 1, row, label, ha='left', va='center',
                fontsize=7.8, color=color, fontweight='bold', zorder=4)

# ── Axes formatting ────────────────────────────────────────────────────────────
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))

ax.set_xlim(mdates.date2num(date(2025, 11, 1)),
            mdates.date2num(date(2026,  5,  5)))
ax.set_ylim(-0.6, len(tasks) - 0.4)

ax.set_yticks([])
ax.tick_params(axis='x', labelsize=9, rotation=30)
ax.grid(axis='x', which='major', color='#CCCCCC', linewidth=0.8, zorder=0)
ax.grid(axis='x', which='minor', color='#EEEEEE', linewidth=0.4, zorder=0)

for spine in ax.spines.values():
    spine.set_visible(False)

# ── Milestone marker — submission deadline ─────────────────────────────────────
sub_date = mdates.date2num(date(2026, 4, 30))
ax.axvline(sub_date, color='#C00000', linewidth=1.5, linestyle='--', zorder=2)
ax.text(sub_date + 0.5, len(tasks) - 1.1, 'Submission\n30 Apr 2026',
        fontsize=7.5, color='#C00000', va='top', fontweight='bold')

# ── Legend ─────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color=C_ETHICS, label='Ethics & Administration'),
    mpatches.Patch(color=C_RES,    label='Research & Requirements'),
    mpatches.Patch(color=C_DEV,    label='Development Iterations'),
    mpatches.Patch(color=C_TEST,   label='Testing & Evaluation'),
    mpatches.Patch(color=C_WRITE,  label='Report Writing'),
    mpatches.Patch(color=C_REVIEW, label='Review & Submission Prep'),
]
ax.legend(handles=legend_items, loc='lower left', fontsize=7.5,
          framealpha=0.9, ncol=3, bbox_to_anchor=(0, -0.32))

ax.set_title('Figure 2.1 — FPMS Project Gantt Chart (November 2025 – April 2026)',
             fontsize=11, fontweight='bold', color='#1F497D', pad=10)

plt.tight_layout()
out = os.path.join(DEST, 'gantt_chart.png')
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print(f'Saved: {out}')
