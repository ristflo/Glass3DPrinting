#!/usr/bin/env python
"""make_figures.py - generates the analytical figures for the LaTeX monograph into latex/figures/.
All plots are derived from published fixed points / textbook relations cited in the monograph.
"""
import pathlib, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, Circle, FancyArrowPatch
from scipy.optimize import least_squares
from scipy.special import iv, kv

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIG = ROOT / "latex" / "figures"; FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 200})

# ------------------------------------------------------------------ Fig 1: VFT viscosity curves
# Fixed points (degC) at log10(eta / dPa s) = 14.5 (strain), 13.0 (annealing), 7.6 (softening), 4.0 (working)
# Sources: Pilkington/Valley Design soda-lime float datasheet; SCHOTT BOROFLOAT 33 thermal properties sheet;
# Heraeus quartz lamp materials sheet; Corning EAGLE XG PI sheet (working point extrapolated from the 3 lower points).
GLASSES = {
    "Soda-lime float (SLS)":            {"pts": [(14.5, 514), (13.0, 546), (7.6, 726), (4.0, 1023)], "c": "#1f77b4"},
    "Borosilicate (BOROFLOAT 33)":      {"pts": [(14.5, 518), (13.0, 560), (7.6, 820), (4.0, 1270)], "c": "#2ca02c"},
    "Alkaline-earth boro-aluminosilicate (EAGLE XG)": {"pts": [(14.5, 669), (13.0, 722), (7.6, 972)], "c": "#ff7f0e"},
    "Fused silica (Heraeus lamp grade)":{"pts": [(14.5, 1125), (13.0, 1220), (7.6, 1710)], "c": "#d62728"},
}
def vft(T, A, B, T0): return A + B / (T - T0)
def fit_vft(pts):
    lg = np.array([p[0] for p in pts]); T = np.array([p[1] for p in pts]) + 273.15
    if len(pts) >= 4:
        res = least_squares(lambda x: vft(T, *x) - lg, x0=[-2.5, 4500, 500], bounds=([-6, 100, 0], [2, 60000, 1400]))
        return res.x
    # only three fixed points: fix the infinite-temperature intercept at the universal value
    # log10(eta_inf / Pa s) = -2.93 (Mauro et al. 2009, PNAS 106:19780) -> -1.93 in dPa s
    A = -1.93
    res = least_squares(lambda x: vft(T, A, *x) - lg, x0=[6000, 500], bounds=([100, 0], [80000, 1600]))
    return np.array([A, res.x[0], res.x[1]])
fig, ax = plt.subplots(figsize=(6.4, 4.0))
T = np.linspace(450, 2300, 800)
table_rows = []
for name, g in GLASSES.items():
    A, B, T0 = fit_vft(g["pts"]); table_rows.append((name, A, B, T0 - 273.15))
    ax.plot(T, vft(T + 273.15, A, B, T0), color=g["c"], lw=1.8, label=name)
    ax.scatter([p[1] for p in g["pts"]], [p[0] for p in g["pts"]], color=g["c"], s=16, zorder=5)
ax.axhspan(2.0, 4.5, color="gold", alpha=0.18, lw=0); ax.text(2000, 3.2, "melt-extrusion window\n$10^{2}$-$10^{4.5}$ dPa s", fontsize=7.5, ha="center", va="center")
ax.axhspan(7.6, 8.5, color="grey", alpha=0.12, lw=0)
for y, lab in [(14.5, "strain"), (13.0, "annealing"), (7.6, "softening (Littleton)"), (4.0, "working")]:
    ax.axhline(y, color="k", lw=0.5, ls=":"); ax.text(2290, y + 0.15, lab, fontsize=7, ha="right")
ax.set_xlabel("Temperature (°C)"); ax.set_ylabel(r"$\log_{10}\,\eta$  (dPa s)"); ax.set_ylim(0, 16); ax.set_xlim(450, 2300)
ax.legend(fontsize=7, loc="upper right"); fig.tight_layout(); fig.savefig(FIG / "fig_vft_viscosity.pdf"); plt.close(fig)
with open(FIG / "vft_fit_parameters.txt", "w", encoding="utf-8") as f:
    f.write("glass\tA\tB(K)\tT0(degC)\n")
    for r in table_rows: f.write(f"{r[0]}\t{r[1]:.3f}\t{r[2]:.0f}\t{r[3]:.0f}\n")

# ------------------------------------------------------------------ Fig 2: Rayleigh-Plateau / Tomotika dispersion
# inviscid Rayleigh (1878): omega^2 = (sigma/(rho a^3)) * x I1(x)/I0(x) * (1 - x^2), x = k a
# Stokes limit (Rayleigh 1892 / Tomotika 1935, viscous thread in inviscid surroundings): omega = sigma/(2 mu a) * (1 - x^2)/(1 + x^2 - x^2 I0^2/I1^2)... use standard form:
#   omega_visc = (sigma/(2 mu a)) * (1 - x^2) / (1 + x^2 - x^2 * (I0(x)/I1(x))**2) is negative-definite in that form; use Weber/Chandrasekhar expression:
#   omega = (sigma/(2 mu a)) * (1 - x^2) * I1(x) / (x * I0(x) - ... ) -> implement Chandrasekhar (1961) eq. 4.130 for Oh->inf:
#   omega = (sigma/(2 mu a)) * (1 - x^2) * [ x^2 (I0/I1)^2 - x^2 - 1 ]^{-1} * (-1) ... we compute numerically via the full Chandrasekhar viscous dispersion instead.
def rayleigh_inviscid(x): return np.sqrt(np.clip(x * iv(1, x) / iv(0, x) * (1 - x**2), 0, None))
def stokes_thread(x):
    # Chandrasekhar 1961, viscous thread, negligible inertia: omega* = omega mu a / sigma
    # omega* = (1 - x^2) / (2 * (x^2 + 1 - x^2 * (I0(x)/I1(x))**2 )) * (-1)  -> positive for x<1
    F = x**2 * (iv(0, x) / iv(1, x))**2 - x**2 - 1
    return (1 - x**2) / (2 * F)
x = np.linspace(0.02, 1.2, 400)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
ax1.plot(x, rayleigh_inviscid(x), color="#1f77b4", lw=1.8, label="inviscid (Rayleigh 1878)")
xm = x[np.argmax(rayleigh_inviscid(x))]
ax1.axvline(xm, color="k", ls=":", lw=0.8); ax1.text(xm + 0.02, 0.05, f"$ka$ = {xm:.3f}\n$\\lambda$ = {2*np.pi/xm:.2f} a = {np.pi/xm:.2f} d", fontsize=7)
ax1.set_xlabel("dimensionless wavenumber  $ka$"); ax1.set_ylabel(r"$\omega \sqrt{\rho a^3/\sigma}$"); ax1.set_title("inertial (low viscosity) limit", fontsize=8); ax1.legend(fontsize=7)
ax2.plot(x, stokes_thread(x), color="#d62728", lw=1.8, label="viscous thread, Oh → ∞\n(Rayleigh 1892 / Tomotika 1935)")
ax2.set_xlabel("dimensionless wavenumber  $ka$"); ax2.set_ylabel(r"$\omega \mu a/\sigma$"); ax2.set_title("viscous (molten glass) limit", fontsize=8); ax2.legend(fontsize=7)
ax2.annotate("growth fastest as $k \\to 0$:\nlong-wave, slow ($\\tau \\sim \\mu a/\\sigma$)", xy=(0.05, stokes_thread(np.array([0.05]))[0]), xytext=(0.35, 0.4), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
fig.tight_layout(); fig.savefig(FIG / "fig_rayleigh_plateau.pdf"); plt.close(fig)

# ------------------------------------------------------------------ Fig 3: transient cooling of an extruded glass cord (lumped + radiation)
# dT/dt = -(4/(rho cp d)) * [ h (T - Tinf) + eps sigma_SB (T^4 - Tinf^4) ],  rho=2500, cp=1200 (molten SLS approx), eps=0.9
rho, cp, eps, sb = 2500.0, 1200.0, 0.9, 5.670e-8
def cool(d_mm, T0=1050.0, Tinf=520.0, h=15.0, tmax=120.0):
    d = d_mm / 1e3; dt = 0.01; n = int(tmax / dt); T = np.empty(n); T[0] = T0 + 273.15; Ti = Tinf + 273.15
    for i in range(1, n):
        q = h * (T[i-1] - Ti) + eps * sb * (T[i-1]**4 - Ti**4)
        T[i] = T[i-1] - dt * 4.0 * q / (rho * cp * d)
    return np.arange(n) * dt, T - 273.15
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
for d, c in [(2, "#1f77b4"), (5, "#2ca02c"), (10, "#ff7f0e"), (15, "#d62728")]:
    t, Tc = cool(d); ax1.plot(t, Tc, color=c, lw=1.6, label=f"d = {d} mm, chamber 520 °C")
    t2, Tc2 = cool(d, Tinf=25.0); ax2.plot(t2, Tc2, color=c, lw=1.6, label=f"d = {d} mm, ambient 25 °C")
for ax in (ax1, ax2):
    ax.axhline(726, color="k", ls=":", lw=0.8); ax.text(118, 735, "softening 726 °C", fontsize=7, ha="right")
    ax.axhline(546, color="k", ls="--", lw=0.6); ax.text(118, 555, "annealing 546 °C", fontsize=7, ha="right")
    ax.set_xlabel("time after extrusion (s)"); ax.set_ylabel("cord temperature (°C)"); ax.legend(fontsize=6.5); ax.set_ylim(0, 1100)
ax1.set_title("heated build chamber (G3DP-type)", fontsize=8); ax2.set_title("open air (cane-fed desktop type)", fontsize=8)
fig.tight_layout(); fig.savefig(FIG / "fig_cord_cooling.pdf"); plt.close(fig)

# ------------------------------------------------------------------ Fig 4: process taxonomy
fig, ax = plt.subplots(figsize=(6.8, 4.2)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
def box(x, y, w, h, text, fc="#f2f2f2", ec="k", fs=7.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5", fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal")
def arrow(x1, y1, x2, y2): ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8, lw=0.8, color="k"))
box(30, 88, 40, 9, "Additive manufacturing of glass", fc="#dddddd", bold=True, fs=9)
box(2, 67, 46, 11, "DIRECT\nglass molten at deposition", fc="#ffe0b2", bold=True, fs=7)
box(52, 67, 46, 11, "INDIRECT\nshaped cold, sintered to glass later", fc="#cfe8ff", bold=True, fs=7)
arrow(45, 88, 25, 77); arrow(55, 88, 75, 77)
direct = [("Crucible-fed melt extrusion\n(G3DP1-3, Evenline, Micron3DP;\nkiln 1000-1200 °C, ceramic/Pt-Rh nozzle)", 2, 48),
          ("Cane / rod-fed hot-nozzle extrusion\n(Maple 2/3/4; ~1000 °C nozzle,\nunheated or warm build chamber)", 2, 32),
          ("Laser filament / fibre deposition\n(Missouri S&T–Notre Dame DGF, LZH LGD,\nKTH–Nobula DGLD; CO2 laser >2000 °C)", 2, 16),
          ("Powder-bed / powder-fed laser melting\n(Fateri 2015, Datsiou 2019/21, Spirrett 2023,\nLang 2024; L-PBF and DED)", 2, 0)]
for text, x, y in direct: box(x, y, 46, 12, text, fc="#fff3e0", fs=6.8); arrow(25, 68, 25, y + 12)
indirect = [("Vat photopolymerisation of silica\nnanocomposites + debind/sinter\n(Kotz 2017, Glassomer)", 52, 48),
            ("Thermoplastic FDM/FFD of silica\nnanocomposite + sinter (Mader 2021)", 52, 32),
            ("Direct ink writing of silica sols /\nslurries + sinter (LLNL, Nguyen 2017,\nDestino 2018; MIT-LL 250 °C route)", 52, 16),
            ("Volumetric CAL, binder jetting,\nsol-gel two-photon routes\n(Toombs 2022; Vitriform3D/ORNL)", 52, 0)]
for text, x, y in indirect: box(x, y, 46, 12, text, fc="#e3f2fd", fs=6.8); arrow(75, 68, 75, y + 12)
fig.savefig(FIG / "fig_taxonomy.pdf", bbox_inches="tight"); plt.close(fig)

# ------------------------------------------------------------------ Fig 5: schematic of a crucible-fed molten-glass extrusion printer (G3DP architecture)
fig, ax = plt.subplots(figsize=(6.4, 5.0)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 112)
ax.add_patch(Rectangle((30, 62), 40, 30, fc="#ffccbc", ec="k", lw=1.2)); ax.text(50, 88.5, "KILN CARTRIDGE / MELTER  ~1000-1200 °C", ha="center", fontsize=7.5, weight="bold")
ax.add_patch(Polygon([[36, 66], [64, 66], [60, 84], [40, 84]], closed=True, fc="#ff8a65", ec="k")); ax.text(50, 75, "molten glass\n(crucible, ~10-30 kg)", ha="center", va="center", fontsize=7)
ax.add_patch(Rectangle((44, 50), 12, 12, fc="#ffe0b2", ec="k")); ax.text(50, 56, "nozzle kiln\n~900-1000 °C", ha="center", va="center", fontsize=6.5)
ax.add_patch(Polygon([[47, 50], [53, 50], [51, 44], [49, 44]], closed=True, fc="#bdbdbd", ec="k")); ax.text(58, 57, "ceramic (AZS / alumina) or Pt-Rh\nnozzle, Ø 5-15 mm, gravity-fed flow", fontsize=6.5, va="center")
ax.add_patch(Rectangle((15, 8), 70, 36, fc="#fff8e1", ec="k", lw=1.2)); ax.text(50, 41, "BUILD / ANNEALING CHAMBER  ~480-560 °C (near annealing point)", ha="center", fontsize=7, weight="bold")
for i in range(6): ax.add_patch(Rectangle((38 - i, 12 + i * 3.4), 24 + 2 * i, 3.0, fc="#ffab91", ec="#8d6e63", lw=0.6))
ax.text(50, 30.5, "deposited cords\n(bead 3-12 mm)", ha="center", fontsize=6.5)
ax.add_patch(Rectangle((28, 9), 44, 2.5, fc="#9e9e9e", ec="k")); ax.text(50, 6.3, "ceramic build plate on X-Y(-θ) stage; Z on nozzle or bed", ha="center", fontsize=6.5)
ax.add_patch(Circle((50, 47), 0.7, fc="#ff5722", ec="none"))
ax.annotate("IR camera / pyrometer\n(emissivity ≈ 0.95-0.98)", xy=(52, 46), xytext=(76, 68), fontsize=6.5, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.annotate("shears / torch\nat nozzle exit", xy=(48, 45), xytext=(6, 54), fontsize=6.5, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.text(4, 110, "Three thermal zones (melter, nozzle, build chamber) are controlled independently;\nprint bed motion sets cord placement while flow rate is set by melt head and nozzle temperature.", fontsize=6.8, va="top")
fig.savefig(FIG / "fig_g3dp_schematic.pdf", bbox_inches="tight"); plt.close(fig)

# ------------------------------------------------------------------ Fig 6: laser filament-fed schematic (DGF / LGD / DGLD)
fig, ax = plt.subplots(figsize=(6.4, 4.2)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 116)
ax.add_patch(Rectangle((10, 8), 80, 6, fc="#9e9e9e", ec="k")); ax.text(50, 4, "substrate (fused silica / soda-lime plate), optionally pre-heated", ha="center", fontsize=6.5)
for i in range(4): ax.add_patch(Rectangle((35, 14 + i * 5), 30, 4.5, fc="#b3e5fc", ec="#0277bd", lw=0.6))
ax.add_patch(Circle((65, 36), 3.5, fc="#ff7043", ec="k")); ax.text(70, 40, "melt zone\n1700-2200 °C\n(Ø 0.25-1 mm)", fontsize=6.5)
ax.plot([80, 65], [90, 38], color="#c62828", lw=2.5, alpha=0.7); ax.plot([50, 65], [90, 38], color="#c62828", lw=2.5, alpha=0.7)
ax.text(65, 92, "CO2 laser (10.6 µm), 5-120 W, single, split or coaxial beams", ha="center", fontsize=6.8)
ax.plot([20, 63], [70, 38], color="#0277bd", lw=2.2); ax.text(14, 74, "feedstock: fibre 0.1-0.2 mm (F300),\nrod 1-3 mm (borosilicate / SLS);\nfeed 90-400 mm/min", fontsize=6.5)
ax.add_patch(Rectangle((8, 62), 10, 8, fc="#eeeeee", ec="k")); ax.text(13, 66, "feeder", ha="center", va="center", fontsize=6.5)
ax.annotate("pyrometer / thermal camera\nclosed-loop laser power (PID)", xy=(66, 39), xytext=(70, 60), fontsize=6.5, arrowprops=dict(arrowstyle="->", lw=0.6))
ax.text(4, 114, "Non-contact laser heating removes the nozzle-corrosion limit and reaches fused-silica working temperatures;\nthe price is a millimetre-scale melt zone, low deposition rate and steep thermal gradients (stress, bubbles, striae).", fontsize=6.6, va="top")
fig.savefig(FIG / "fig_laser_filament_schematic.pdf", bbox_inches="tight"); plt.close(fig)

# ------------------------------------------------------------------ Fig 7: timeline
events = [(2014, "Luo/Kinzel: CO2-laser rod-fed glass (Missouri S&T)"), (2015, "MIT G3DP (Klein et al.); Micron3DP; Fateri SLM"), (2016, "MIT patents filed; Luo soda-lime filament-fed"),
          (2017, "G3DP2 Milan columns; Kotz/Glassomer; LLNL DIW; Brun sewing machine"), (2018, "Inamura G3DP2 paper; LZH LGD (Procedia CIRP); Glassomer GmbH founded"),
          (2019, "Datsiou L-PBF; Laval chalcogenide FDM"), (2021, "Nobula3D founded (KTH); Mader FFD silica"), (2022, "KTH filament bonding study; Toombs micro-CAL; Maple 3 launched"),
          (2023, "Spirrett powder-fed DED; Evenline/RIT recycled glass; Nobula printer launch"), (2024, "MIT/Evenline glass masonry (G3DP3); LGD homogeneity (Ra 21 nm)"),
          (2025, "Critical review (Appl. Sci.); Maple 4; Utah international glass-printer project"), (2026, "Closed-loop DGF temperature control (Addit. Manuf.); JMMP review")]
fig, ax = plt.subplots(figsize=(6.8, 3.4)); ax.axis("off"); ax.set_xlim(2013.3, 2026.9); ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color="k", lw=1)
for i, (y, t) in enumerate(events):
    s = 1 if i % 2 == 0 else -1; ax.plot([y, y], [0, 0.45 * s], color="#616161", lw=0.7); ax.scatter([y], [0], s=14, color="#d84315", zorder=5)
    ax.text(y, 0.5 * s, f"{y}\n{t}", ha="center", va="bottom" if s > 0 else "top", fontsize=5.6, wrap=True)
fig.savefig(FIG / "fig_timeline.pdf", bbox_inches="tight"); plt.close(fig)
print("figures written:", sorted(p.name for p in FIG.iterdir()))
