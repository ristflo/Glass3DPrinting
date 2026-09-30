#!/usr/bin/env python
"""make_figures.py - regenerates every analytical figure of the cross-workspace synthesis.

The figures supersede the versions in Claude_Research_Workspace/latex/figures and
ChatGPT_Research_Workspace/latex/figures. Each block states what was wrong with the
earlier version and what was changed. Output: synthesis/figures/<name>.pdf and .png.

Run:  scripts/tmp/venv/Scripts/python.exe synthesis/scripts/make_figures.py
"""
import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, Circle
from scipy.optimize import least_squares
from scipy.special import iv

OUT = pathlib.Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---- shared style (validated categorical order: blue, orange, aqua, yellow; ordinal blue ramp)
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
RAMP = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "text.color": INK,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "axes.titlesize": 8.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "legend.frameon": False, "legend.fontsize": 7.5, "savefig.dpi": 300, "figure.dpi": 120,
})


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=220)
    plt.close(fig)
    print("wrote", name)


# =====================================================================================
# Fig: VFT viscosity curves
# Earlier versions: Claude drew all curves solid over 450-2300 degC, hiding extrapolation;
# ChatGPT marked extrapolation but used a redundant second panel and a different silica grade.
# Now: one panel, solid inside the fixed-point interval, dashed outside, direct labels,
# both silica grades shown so the grade dependence is visible.
# =====================================================================================
def vft(T_C, A, B, T0_C):
    return A + B / (T_C - T0_C)


def fit_vft(pts, A_fixed=None):
    lg = np.array([p[0] for p in pts], float)
    T = np.array([p[1] for p in pts], float)
    if A_fixed is None:
        r = least_squares(lambda x: vft(T, *x) - lg, x0=[-2.5, 4500, 250],
                          bounds=([-6, 100, -273], [2, 60000, 1200]))
        return tuple(r.x)
    r = least_squares(lambda x: vft(T, A_fixed, *x) - lg, x0=[6000, 250],
                      bounds=([100, -273], [80000, 1500]))
    return (A_fixed, r.x[0], r.x[1])


GLASSES = [  # (label, fixed points (log10 eta/dPa s, degC), colour, A fixed?)
    ("Soda-lime float", [(14.5, 514), (13.0, 546), (7.6, 726), (4.0, 1023)], BLUE, None),
    ("Borosilicate (BOROFLOAT 33)", [(14.5, 518), (13.0, 560), (7.6, 820), (4.0, 1270)], ORANGE, None),
    ("Boro-aluminosilicate (EAGLE XG)", [(14.5, 669), (13.0, 722), (7.6, 972)], AQUA, -1.93),
    ("Fused quartz (lamp grade)", [(14.5, 1125), (13.0, 1220), (7.6, 1710)], YELLOW, -1.93),
]
HPFS = [(14.5, 893), (13.0, 1042), (7.6, 1585)]  # Corning HPFS 7980, high-OH synthetic silica
FITS = {}
fig, ax = plt.subplots(figsize=(6.6, 4.1))
ax.axhspan(3.0, 4.5, color="#f0efec", lw=0, zorder=0)
ax.text(470, 3.45, "melt-extrusion nozzle window", ha="left", va="center", fontsize=7, color=INK2)
for y in (14.5, 13.0, 7.6, 4.0):
    ax.axhline(y, color=AXIS, lw=0.9, zorder=1)
for name, pts, c, Afix in GLASSES:
    A, B, T0 = fit_vft(pts, Afix)
    FITS[name] = (A, B, T0)
    lo, hi = min(p[1] for p in pts), max(p[1] for p in pts)
    Tin = np.linspace(lo, hi, 300)
    ax.plot(Tin, vft(Tin, A, B, T0), color=c, lw=2, zorder=3)
    Tex = np.linspace(hi, 2300, 300)
    ax.plot(Tex, vft(Tex, A, B, T0), color=c, lw=1.4, ls=(0, (4, 2.5)), zorder=3)
    ax.scatter([p[1] for p in pts], [p[0] for p in pts], s=26, color=c, edgecolor="white", lw=1.2, zorder=4)
    ax.plot([], [], color=c, lw=2, marker="o", ms=4.5, mec="white", label=name)
ax.scatter([p[1] for p in HPFS], [p[0] for p in HPFS], s=30, facecolor="white", edgecolor=YELLOW, lw=1.4, zorder=4)
ax.annotate("HPFS 7980 fixed points\n(high-OH synthetic silica:\nsame family, different curve)", xy=(1042, 13.0), xytext=(880, 10.6),
            fontsize=7, color=INK2, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
ax.scatter([990], [np.log10(6400)], marker="D", s=30, color=INK, zorder=6)
ax.annotate("G3DP nozzle exit\n990 °C, 640 Pa·s", xy=(990, np.log10(6400)), xytext=(560, 1.3), fontsize=7, color=INK2,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
ax.plot([], [], color=INK2, lw=2, label="solid: inside the published fixed points")
ax.plot([], [], color=INK2, lw=1.4, ls=(0, (4, 2.5)), label="dashed: extrapolation")
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.93), handlelength=2.2)
ax.set_yticks([0, 2, 4, 6, 7.6, 10, 13, 14.5])
ax.set_yticklabels(["0", "2", "working 4.0", "6", "softening 7.6", "10", "annealing 13.0", "strain 14.5"])
ax.set_xlim(450, 2300); ax.set_ylim(0, 16)
ax.set_xlabel("Temperature (°C)"); ax.set_ylabel(r"$\log_{10}$ viscosity (dPa·s)")
save(fig, "fig_vft_viscosity")
with open(OUT / "vft_fit_parameters.txt", "w", encoding="utf-8") as f:
    f.write("glass\tA\tB_K\tT0_degC\tdlog10eta_dT_at_1000C\n")
    for k, (A, B, T0) in FITS.items():
        f.write(f"{k}\t{A:.3f}\t{B:.0f}\t{T0:.0f}\t{-B / (1000 - T0) ** 2:.4f}\n")

# =====================================================================================
# Fig: gravity-fed flow versus nozzle temperature
# Earlier version (ChatGPT): flow vs an abstract viscosity axis, default colours, dense
# minor grid. Now: flow vs temperature through the soda-lime fit, which is the quantity an
# operator controls, with the two reported machine throughputs as reference lines.
# Plotted as a ratio about the working point, so no nozzle geometry has to be assumed:
# in Hagen-Poiseuille flow Q is proportional to 1/eta, hence Q/Q0 = eta0/eta.
# =====================================================================================
dT = np.linspace(-30, 30, 200)
fig, ax = plt.subplots(figsize=(5.6, 3.4))
for name, Tw, c, dy in [("Soda-lime float", 1023.0, BLUE, 0.0), ("Borosilicate (BOROFLOAT 33)", 1270.0, ORANGE, 0.0)]:
    A, B, T0 = FITS[name]
    rel = 10 ** (vft(Tw, A, B, T0) - vft(Tw + dT, A, B, T0))
    ax.plot(dT, rel, color=c, lw=2)
    ax.text(30.8, rel[-1], name.split(" (")[0] + f"\nabout {Tw:.0f} °C", fontsize=7.3, va="center", color=INK, linespacing=1.25)
    r10 = 10 ** (vft(Tw, A, B, T0) - vft(Tw + 10, A, B, T0))
    ax.scatter([10], [r10], s=26, color=c, edgecolor="white", lw=1.2, zorder=4)
    ax.annotate(f"+{100 * (r10 - 1):.0f} % at +10 °C", xy=(10, r10), xytext=(-27, 1.62 if c == BLUE else 1.42), fontsize=7.3, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
ax.axhline(1, color=AXIS, lw=0.8); ax.axvline(0, color=AXIS, lw=0.8)
ax.set_xlim(-30, 30); ax.set_ylim(0.4, 2.0)
ax.set_xlabel("Temperature error at the nozzle (°C)"); ax.set_ylabel("Gravity-fed flow relative to set point")
save(fig, "fig_flow_vs_temperature")

# =====================================================================================
# Fig: capillary instability, inviscid versus viscous limit
# Earlier version (Claude): both axes collapsed to a strip at the bottom of the canvas and
# the annotation sat outside the plot. Rebuilt with explicit limits and labels.
# =====================================================================================
x = np.linspace(0.01, 1.0, 500)
ray = np.sqrt(np.clip(x * iv(1, x) / iv(0, x) * (1 - x ** 2), 0, None))
sto = (1 - x ** 2) / (2 * (x ** 2 * (iv(0, x) / iv(1, x)) ** 2 - x ** 2 - 1))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 2.9))
a1.plot(x, ray, color=BLUE, lw=2)
xm = x[np.argmax(ray)]
a1.plot([xm, xm], [0, ray.max()], color=AXIS, lw=0.8)
a1.scatter([xm], [ray.max()], s=24, color=BLUE, edgecolor="white", lw=1.2, zorder=4)
a1.text(xm - 0.03, 0.05, f"fastest mode\n$ka$ = {xm:.2f}\n$\\lambda$ = {np.pi / xm:.2f} $d$", fontsize=7, ha="right", color=INK2)
a1.set_title("Inviscid jet (water-like)"); a1.set_ylabel(r"growth rate  $\omega\,\sqrt{\rho a^{3}/\sigma}$")
a1.set_ylim(0, 0.4)
a2.plot(x, sto, color=ORANGE, lw=2)
a2.scatter([0], [1 / 6], s=24, color=ORANGE, edgecolor="white", lw=1.2, zorder=4, clip_on=False)
a2.text(0.06, 1 / 6 + 0.012, r"$\omega \to \sigma/(6\eta a)$ as $ka \to 0$", fontsize=7, color=INK2)
a2.text(0.98, 0.115, "no preferred wavelength:\nbreak-up is slow, and the same\ntime $\\eta a/\\sigma$ sets seam healing",
        fontsize=7, ha="right", color=INK2)
a2.set_title("Viscous thread (molten glass, Oh ≫ 1)"); a2.set_ylabel(r"growth rate  $\omega\,\eta a/\sigma$")
a2.set_ylim(0, 0.2)
for a in (a1, a2):
    a.set_xlim(0, 1.0); a.set_xlabel("dimensionless wavenumber $ka$")
fig.tight_layout(w_pad=2.5)
save(fig, "fig_capillary_instability")

# =====================================================================================
# Fig: cooling of a deposited soda-lime cord
# Earlier version (Claude): two legends repeating the same four entries, rainbow colours for
# an ordered quantity, reference labels colliding with curves. Now: ordinal blue ramp for
# diameter, direct labels, one shared y-axis.
# =====================================================================================
rho_c, cp, eps, sb, h = 2500.0, 1200.0, 0.9, 5.670e-8, 15.0


def cool(d_mm, Tinf, T0=1050.0, tmax=120.0, dt=0.01):
    n = int(tmax / dt); Tk = np.empty(n); Tk[0] = T0 + 273.15; Ti = Tinf + 273.15
    for i in range(1, n):
        q = h * (Tk[i - 1] - Ti) + eps * sb * (Tk[i - 1] ** 4 - Ti ** 4)
        Tk[i] = Tk[i - 1] - dt * 4 * q / (rho_c * cp * d_mm / 1e3)
    return np.arange(n) * dt, Tk - 273.15


fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1), sharey=True)
for ax, Tinf, title in [(axes[0], 520.0, "Into a 520 °C build chamber (crucible-fed)"),
                        (axes[1], 25.0, "Into room-temperature air")]:
    for y in (726, 546):
        ax.axhline(y, color=AXIS, lw=0.9)
    ends = []
    for d, c in zip([2, 5, 10, 15], RAMP):
        t, Tc = cool(d, Tinf)
        ax.plot(t, Tc, color=c, lw=1.9)
        ends.append([Tc[-1], f"{d} mm"])
    pos = [e[0] for e in ends]
    for k in range(1, len(pos)):
        pos[k] = max(pos[k], pos[k - 1] + 52)
    shift = (sum(e[0] for e in ends) - sum(pos)) / len(pos)
    for (yv, lab), yl in zip(ends, pos):
        ax.text(122, yl + shift, lab, fontsize=7.5, va="center", color=INK)
    ax.set_title(title); ax.set_xlim(0, 120); ax.set_ylim(0, 1100); ax.set_xlabel("Time after deposition (s)")
axes[0].set_ylabel("Cord temperature (°C)")
axes[0].set_yticks([0, 200, 400, 546, 726, 900, 1050])
axes[0].set_yticklabels(["0", "200", "400", "annealing 546", "softening 726", "900", "1050"])
fig.text(0.5, -0.03, "Labels at the right give the cord diameter. Lumped radiative–convective model, released at 1050 °C.",
         ha="center", fontsize=7, color=INK2)
fig.tight_layout(w_pad=3.0)
save(fig, "fig_cord_cooling")


# =====================================================================================
# helpers for diagrams
# =====================================================================================
def rbox(ax, x, y, w, h, text, fc="#ffffff", ec=AXIS, fs=7.2, weight="normal", color=INK, lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, color=color, linespacing=1.35)


# =====================================================================================
# Fig: process taxonomy
# Earlier version (Claude): connector arrows were drawn through the child boxes and
# Micron3DP was listed under crucible-fed extrusion although it is a hot-nozzle machine.
# Now: elbow connectors along a side spine, corrected assignment, outcome line per branch.
# =====================================================================================
fig, ax = plt.subplots(figsize=(6.9, 4.7)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
rbox(ax, 31, 90, 38, 8, "Additive manufacturing of glass", fc="#f0efec", fs=8.5, weight="bold")
cols = [(3, "DIRECT", "glass is molten when it is deposited", "#e7f0fb", BLUE,
         [("Crucible-fed melt extrusion", "G3DP, G3DP2, G3DP3 (Evenline)\nkg/h, centimetre cords, soda-lime"),
          ("Rod-fed hot-nozzle extrusion", "Maple 2–4, Micron3DP, TU Darmstadt\nmm³/s, millimetre beads, soda-lime"),
          ("Laser filament / fibre deposition", "Missouri S&T, Hannover, KTH–Nobula\nfused silica, sub-millimetre tracks"),
          ("Laser melting of powder or paste", "L-PBF, powder-fed DED, paste + CO₂ laser\nporous or opaque in most reports")]),
        (53, "INDIRECT", "shaped cold, converted to glass in a furnace", "#fdeee6", ORANGE,
         [("Vat photopolymerisation + sintering", "Kotz 2017, Glassomer, UpNano two-photon\n1300 °C sintering, linear shrinkage"),
          ("Thermoplastic extrusion + sintering", "Mader 2021: silica nanocomposite filament"),
          ("Direct ink writing + sintering", "LLNL silica and silica–titania inks\noptical grade, gradient index"),
          ("Volumetric and binder routes", "micro-CAL (Toombs 2022),\nbinder jetting of recycled powder")])]
for x0, head, sub, fc, ec, items in cols:
    rbox(ax, x0, 74, 44, 10, "", fc=fc, ec=ec, lw=1.2)
    ax.text(x0 + 22, 80.6, head, ha="center", va="center", fontsize=8, weight="bold")
    ax.text(x0 + 22, 76.6, sub, ha="center", va="center", fontsize=7, color=INK2)
    cx = x0 + 22
    ax.plot([50, 50, cx, cx], [90, 87, 87, 84], color=MUTED, lw=0.9)
    spine = x0 + 2
    ax.plot([spine, spine], [74, 9.5], color=MUTED, lw=0.9)
    for i, (t, d) in enumerate(items):
        y = 55 - i * 17.5
        ax.plot([spine, x0 + 5], [y + 7, y + 7], color=MUTED, lw=0.9)
        rbox(ax, x0 + 5, y, 39, 14, "", fc="#ffffff", ec=AXIS)
        ax.text(x0 + 24.5, y + 10.3, t, ha="center", va="center", fontsize=6.9, weight="bold")
        ax.text(x0 + 24.5, y + 4.9, d, ha="center", va="center", fontsize=6.4, color=INK2, linespacing=1.3)
save(fig, "fig_taxonomy")

# =====================================================================================
# Fig: timeline as swimlanes
# Earlier version (Claude): twelve long labels on one axis, all overlapping and illegible.
# Now: one lane per process family, short labels alternating above and below the lane.
# =====================================================================================
LANES = [
    ("Crucible-fed\nextrusion", BLUE, [(2015, "G3DP"), (2017, "Milan columns"), (2018, "G3DP2 paper"), (2024, "G3DP3 masonry,\nrecycled glass")]),
    ("Rod-fed\nhot nozzle", ORANGE, [(2015, "Micron3DP demo"), (2018, "TU Darmstadt\nrod on float"), (2022, "Maple 2 and 3"), (2025, "Maple 4"), (2026, "toolpath vs\nstrength")]),
    ("Laser filament\n/ fibre", AQUA, [(2014, "rod-fed CO₂\n(Missouri S&T)"), (2017, "soda-lime\nfilament"), (2018, "LGD quartz\n(Hannover)"), (2021, "Nobula\nfounded"), (2022, "KTH bonding\nmap"), (2024, "Ra 21 nm;\nmicrolenses"), (2026, "closed-loop\nthermal camera")]),
    ("Laser powder\nmelting", YELLOW, [(2015, "SLM soda-lime"), (2019, "L-PBF in a\ncommercial machine"), (2022, "powder-fed DED"), (2024, "quartz DED\n95 % strength")]),
    ("Indirect routes\n(context)", MUTED, [(2017, "SLA and DIW\nof silica"), (2020, "gradient-index\nglass"), (2022, "micro-CAL")]),
]
fig, ax = plt.subplots(figsize=(7.0, 4.6)); ax.set_xlim(2013.2, 2027.0); ax.set_ylim(-0.75, len(LANES) - 0.25)
ax.grid(False)
for s in ("left", "top", "right"): ax.spines[s].set_visible(False)
ax.set_yticks([]); ax.set_xticks(range(2014, 2027, 2)); ax.tick_params(axis="x", length=3)
for yr in range(2014, 2027):
    ax.axvline(yr, color=GRID, lw=0.6, zorder=0)
for i, (lane, c, evs) in enumerate(LANES):
    y = len(LANES) - 1 - i
    ax.plot([2013.6, 2026.6], [y, y], color=AXIS, lw=0.8, zorder=1)
    ax.text(2013.1, y, lane, ha="right", va="center", fontsize=7.5, weight="bold", color=INK, linespacing=1.3)
    for j, (yr, lab) in enumerate(evs):
        up = (j % 2 == 0)
        ax.scatter([yr], [y], s=34, color=c, edgecolor="white", lw=1.3, zorder=3)
        ax.text(yr, y + (0.13 if up else -0.13), lab, ha="center", va="bottom" if up else "top",
                fontsize=6.3, color=INK2, linespacing=1.2)
save(fig, "fig_timeline")

# =====================================================================================
# Fig: crucible-fed printer, physical zones plus the downstream steps
# Merges the Claude machine schematic (labels overlapped the drawing) and the ChatGPT
# functional diagram (title collided with a box, one box unlabelled). Callouts now sit in a
# column to the right with leader lines; the process chain runs along the bottom.
# =====================================================================================
fig, ax = plt.subplots(figsize=(6.9, 4.9)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
WARM1, WARM2, WARM3 = "#fbd9cb", "#f6b79d", "#fdf3d6"
ax.add_patch(Rectangle((8, 66), 38, 30, fc=WARM1, ec=INK2, lw=1))
ax.add_patch(Polygon([[14, 70], [40, 70], [36, 90], [18, 90]], closed=True, fc=WARM2, ec=INK2, lw=0.9))
ax.text(27, 80, "molten glass", ha="center", va="center", fontsize=7.5)
ax.add_patch(Rectangle((21, 54), 12, 12, fc="#f0efec", ec=INK2, lw=1))
ax.add_patch(Polygon([[25, 54], [29, 54], [28, 48], [26, 48]], closed=True, fc=MUTED, ec=INK2, lw=0.8))
ax.add_patch(Rectangle((2, 20), 50, 30, fc=WARM3, ec=INK2, lw=1))
for i in range(5):
    ax.add_patch(FancyBboxPatch((18 - i * 0.6, 25.5 + i * 3.6), 18 + i * 1.2, 3.0, boxstyle="round,pad=0,rounding_size=1.4",
                                fc=WARM2, ec="#c98a70", lw=0.6))
ax.plot([27, 27], [48, 43.4], color="#e8916d", lw=2.2)
ax.add_patch(Rectangle((12, 22.5), 30, 2.4, fc=MUTED, ec=INK2, lw=0.8))
ax.annotate("", xy=(46, 23.7), xytext=(42.5, 23.7), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
calls = [(92, "Zone 1 · melter kiln and crucible", "1040–1200 °C; 2 kg (G3DP) to 25 kg (G3DP2) of soda-lime", (46, 88)),
         (79, "Zone 2 · heated ceramic nozzle", "800–1010 °C, bore 10–11.5 mm; flow set by melt head and\ntemperature, started by a torch and frozen by an air ring", (33, 60)),
         (63, "Thermal camera through a glass-ceramic window", "7.9 µm band reads the cord surface temperature", (28.5, 47)),
         (50, "Zone 3 · build chamber", "480–525 °C, just below the annealing point,\nso each layer stays rigid but stress relaxes", (52, 40)),
         (35, "Build plate on X–Y–Z (and rotary) axes", "travel speed sets bead width; part is one continuous path", (46.5, 23.7))]
for y, head, body, (tx, ty) in calls:
    ax.plot([tx, 57], [ty, y], color=MUTED, lw=0.7)
    ax.text(58, y + 1.2, head, fontsize=7.4, weight="bold", va="bottom")
    ax.text(58, y + 0.2, body, fontsize=6.6, color=INK2, va="top", linespacing=1.3)
steps = ["Condition melt", "Deposit cord", "Soak in chamber", "Anneal in a\nseparate lehr", "Finish and\nmeasure"]
for i, s in enumerate(steps):
    x0 = 2 + i * 19.8
    rbox(ax, x0, 3, 16.6, 9, s, fc="#ffffff", ec=AXIS, fs=6.8)
    if i < len(steps) - 1:
        ax.annotate("", xy=(x0 + 19.6, 7.5), xytext=(x0 + 16.8, 7.5), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.8))
ax.text(2, 14.2, "Process chain: deposition rate alone does not give production rate", fontsize=7, color=INK2)
save(fig, "fig_crucible_printer")

# =====================================================================================
# Fig: laser filament deposition head
# Earlier version (Claude): caption text inside the canvas, labels touching the beams.
# =====================================================================================
fig, ax = plt.subplots(figsize=(6.6, 3.7)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.add_patch(Rectangle((6, 10), 50, 6, fc=MUTED, ec=INK2, lw=0.8))
for i in range(4):
    ax.add_patch(FancyBboxPatch((14, 16.5 + i * 5.2), 26, 4.4, boxstyle="round,pad=0,rounding_size=2", fc="#cde2fb", ec=BLUE, lw=0.7))
mx, my = 40, 39.5
for xs in (22, 58):
    ax.add_patch(Polygon([[xs - 3, 92], [xs + 3, 92], [mx, my]], closed=True, fc=ORANGE, ec="none", alpha=0.35))
ax.plot([4, mx - 1.5], [62, my + 0.8], color=BLUE, lw=2.2)
ax.add_patch(Rectangle((0, 58), 8, 8, fc="#f0efec", ec=INK2, lw=0.8))
ax.add_patch(Circle((mx, my), 2.6, fc=ORANGE, ec=INK2, lw=0.8))
calls = [(90, "CO₂ laser beams, 10.6 µm", "2–120 W; lateral, four-beam or coaxial ring;\nabsorbed at the glass surface, no nozzle contact", (52, 80)),
         (69, "Melt zone", "1700–2200 °C for fused silica, 0.25–1 mm across", (mx + 2.4, my + 1)),
         (52, "Pyrometer or thermal camera", "melt temperature fed back to laser power", (mx + 1.5, my + 2.4)),
         (35, "Deposited tracks", "0.2 mm layers; fully dense, transparent", (40.5, 26)),
         (18, "Substrate on a motion stage", "fused quartz or float glass, optionally preheated", (56, 13))]
for y, head, body, (tx, ty) in calls:
    ax.plot([tx, 63], [ty, y], color=MUTED, lw=0.7)
    ax.text(64, y + 1.4, head, fontsize=7.4, weight="bold", va="bottom")
    ax.text(64, y + 0.2, body, fontsize=6.6, color=INK2, va="top", linespacing=1.3)
ax.text(0, 70, "Feeder: fibre 0.1–0.2 mm\nor rod 1–3 mm,\n90–400 mm/min", fontsize=6.6, color=INK2, va="bottom", linespacing=1.3)
save(fig, "fig_laser_filament_head")

# =====================================================================================
# Fig (new): deposition rate versus deposited feature size of the direct routes
# =====================================================================================
fig, ax = plt.subplots(figsize=(6.2, 3.7))
boxes = [("Crucible-fed extrusion\nG3DP to G3DP3", 9, 16, 240, 570, BLUE, (8, 370), "right"),
         ("Rod-fed hot nozzle\nMaple 4 in the 2026 study", 1.5, 2.0, 4, 8, ORANGE, (2.5, 5.6), "left"),
         ("Laser filament deposition\nfused silica", 0.1, 1.0, 0.008, 0.25, AQUA, (1.3, 0.045), "left")]
for lab, x0, x1, y0, y1, c, (tx, ty), ha in boxes:
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec=c, alpha=0.30, lw=0))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec=c, lw=1.4))
    ax.text(tx, ty, lab, fontsize=7.5, va="center", ha=ha, color=INK, linespacing=1.3)
ax.text(0.2, 25, "unoccupied:\ntransparent glass at sub-millimetre\nresolution and useful volume rate", fontsize=7, color=MUTED,
        ha="left", va="center", style="italic", linespacing=1.3)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.05, 120); ax.set_ylim(0.003, 2000)
ax.set_xticks([0.1, 1, 10, 100]); ax.set_xticklabels(["0.1", "1", "10", "100"])
ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000]); ax.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax.minorticks_off()
ax.set_xlabel("Deposited bead or track width (mm)"); ax.set_ylabel("Volumetric deposition rate (mm³/s)")
save(fig, "fig_rate_vs_feature")

# =====================================================================================
# Fig (new): reported bending strength by route (different test set-ups, see caption)
# =====================================================================================
rows = [("Drawn soda-lime rod, unprinted feedstock\n(Chhadeh 2026)", 73.5 - 12.5, 73.5 + 12.5, 73.5, "mean ± s.d."),
        ("Quartz, coaxial powder-fed laser DED\n(Lang 2024)", 72.4 - 6.0, 72.4 + 6.0, 72.4, "mean ± s.d."),
        ("Crucible-fed soda-lime cylinders, annealed\n(Inamura 2018)", 41, 56, None, "range"),
        ("Rod-fed soda-lime, 90° infill\n(Chhadeh 2026)", None, None, 56, "mean"),
        ("Rod-fed soda-lime, 0° infill\n(Chhadeh 2026)", None, None, 40, "mean"),
        ("Soda-lime laser powder-bed fusion\n(Datsiou 2021)", 6.2, 6.9, None, "range")]
fig, ax = plt.subplots(figsize=(6.6, 3.5))
for i, (lab, lo, hi, m, kind) in enumerate(rows):
    y = len(rows) - 1 - i
    if lo is not None:
        ax.plot([lo, hi], [y, y], color=BLUE, lw=5, solid_capstyle="round", alpha=0.45)
    if m is not None:
        ax.scatter([m], [y], s=42, color=BLUE, edgecolor="white", lw=1.3, zorder=3)
    right = hi if hi is not None else m
    val = f"{m:g} MPa ({kind})" if m is not None and lo is None else (f"{m:g} ± {hi - m:g} MPa" if m is not None else f"{lo:g}–{hi:g} MPa")
    ax.text(right + 2.5, y, val, va="center", fontsize=7.2, color=INK2)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.2)
ax.set_xlim(0, 112); ax.set_ylim(-0.6, len(rows) - 0.4); ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.set_xlabel("Bending strength (MPa)")
save(fig, "fig_bending_strength")
print("fit constants:", {k: tuple(round(v, 3) for v in vals) for k, vals in FITS.items()})
