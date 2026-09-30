import os

sections_dir = 'research_workspace/latex/sections'
os.makedirs(sections_dir, exist_ok=True)

files = {
    '01_introduction_taxonomy.tex': r'''
\section{Introduction \& Taxonomy}
Additive manufacturing (AM) of glass has historically been challenging due to the extreme temperatures and rapid cooling gradients required. The taxonomy of glass AM generally bifurcates into direct molten extrusion and indirect processes. Direct molten glass deposition, pioneered by groups such as the MIT Mediated Matter lab, involves heating glass to its working temperature and extruding it continuously \cite{klein2015additive, oxman2015glass}. Indirect methods include powder bed fusion (SLS/SLM) \cite{fateri2014additive} and photopolymer resin sintering (e.g., Glassomer) \cite{kotz2017three}. This monograph focuses on direct molten glass extrusion.
''',
    '02_rheology_thermal_materials_physics.tex': r'''
\section{Rheology, Thermal, \& Materials Physics}
The viscosity of molten glass is highly temperature-dependent, which dictates its extrudability and structural stability. This behavior is typically modeled using the Vogel-Fulcher-Tammann (VFT) equation:
\begin{equation}
\log_{10}\eta = A + \frac{B}{T - T_0}
\end{equation}
where $\eta$ is the viscosity, $ is the absolute temperature, and , B, T_0$ are empirical constants dependent on the glass composition (e.g., fused silica, borosilicate, soda-lime). 

In addition to viscosity, the gravitational slumping and surface tension must be controlled. The capillary Rayleigh-Plateau instability can cause liquid glass cords to break into droplets, meaning the extrusion rate and cooling must be precisely tuned to solidify the glass before slumping or bead breakup occurs \cite{klein2015additive}.
''',
    '03_nozzle_mechanics_hardware_kinematics.tex': r'''
\section{Nozzle Mechanics, Hardware, \& Kinematics}
Direct molten glass printers typically feature a dual-heated chamber design. The upper chamber serves as a kiln cartridge to melt the glass at temperatures up to 1000--1900\circ depending on the material. The lower chamber acts as an annealing lehr.

The crucible and extrusion nozzle must withstand high temperatures and chemical corrosion from molten silicates. Common materials include alumina, zirconia, and refractory metals like platinum/rhodium alloys or molybdenum \cite{klein2015additive}. The motion control system is often a multi-axis CNC or industrial robotic arm (as seen in G3DP2) \cite{inamura2018g3dp2}, capable of continuous deposition of large masses of glass.
''',
    '04_in_situ_thermal_management_annealing.tex': r'''
\section{In-situ Thermal Management \& Annealing}
Controlling the cooling gradient is the most critical aspect of glass AM. Thermal shock failure results from internal stresses generated when different regions of the printed object cool and contract at varying rates. Transient heat transfer equations dictate the cooling profile:
\begin{equation}
q = -k \nabla T
\end{equation}

In-situ annealing lehrs are integrated into the print volume to slowly lower the temperature through the glass transition range, mitigating residual stresses. Polarimetric photoelastic stress analysis is often employed to verify the efficacy of the annealing process \cite{oxman2015glass}.
''',
    '05_defect_mechanisms_optical_quality.tex': r'''
\section{Defect Mechanisms \& Optical Quality}
Several defect mechanisms threaten the structural integrity and optical clarity of 3D printed glass:
\begin{itemize}
    \item \textbf{Devitrification:} Spontaneous crystallization if the glass is held at the liquidus temperature for too long.
    \item \textbf{Optical Clarity Degradation:} Internal air bubble nucleation and seed entrapment.
    \item \textbf{Layer Seam Optics:} Wave-front distortion and loss of transmittance (\%$) due to the grooved surface finish inherent to layer-by-layer deposition.
\end{itemize}
''',
    '06_academic_landscape_directory.tex': r'''
\section{Academic Landscape Directory}
A number of global research institutions are pushing the boundaries of molten glass 3D printing.

\begin{table*}[h]
\centering
\caption{Global Academic Research Groups Directory}
\begin{tabularx}{\textwidth}{l l l X}
\toprule
\textbf{Institution} & \textbf{Key Lab/PI} & \textbf{Apparatus} & \textbf{Key Findings} \\
\midrule
MIT & Mediated Matter (Neri Oxman) & G3DP, G3DP2 & Pioneer of optically transparent direct extrusion, large-scale structures \\
TU Delft & Glass \& Translucent Structures & -- & Structural glass applications, casting and AM \\
LLNL & Lawrence Livermore Nat. Lab & Direct Deposition & Optical components and gradient index lenses \\
Fraunhofer & IKTS, ISC, IPT & -- & Industrial integration and materials science \\
\bottomrule
\end{tabularx}
\end{table*}
''',
    '07_commercial_systems_market_economics.tex': r'''
\section{Commercial Systems, Market, \& Economics}
The commercial landscape for molten glass AM is emerging, shifting from laboratory prototypes to pilot-scale commercial machines.

\begin{table*}[h]
\centering
\caption{Commercial \& Industrial Landscape}
\begin{tabularx}{\textwidth}{l l X l}
\toprule
\textbf{Entity} & \textbf{Machine} & \textbf{Target Market} & \textbf{Maturity/TRL} \\
\midrule
Maple Glass Printing & V4 Printer & Artisan, Bespoke Optics & Commercializing \\
Evenline & -- & Artistic, Architectural & Startup \\
Nobula & -- & Specialized / Research & Prototype \\
\bottomrule
\end{tabularx}
\end{table*}

\subsection{Comparisons}
\begin{table*}[h]
\centering
\caption{Process Comparisons}
\begin{tabularx}{\textwidth}{l l l l}
\toprule
\textbf{Metric} & \textbf{Molten Extrusion} & \textbf{SLS/SLM} & \textbf{SLA (Glassomer)} \\
\midrule
Temperature (\circ) & 1000--1500 & Ambient (build), High (laser) & Ambient (print), 1300 (sinter) \\
Optical Quality & High (Transparent) & Low to Medium (Opaque/Translucent) & High (Transparent) \\
Build Envelope & Large (Robotic arm) & Limited to powder bed & Limited to vat \\
\bottomrule
\end{tabularx}
\end{table*}
''',
    '08_open_frontiers_research_roadmap.tex': r'''
\section{Open Frontiers \& Research Roadmap}
Future research in glass additive manufacturing is focused on:
\begin{enumerate}
    \item Closed-loop monitoring via computer vision and pyrometry for real-time extrusion compensation.
    \item Multi-material glass printing for gradient index optics (GRIN) and integrated photonics.
    \item Improved high-temperature seals and corrosion-resistant nozzles for long-duration prints.
\end{enumerate}
'''
}

for filename, content in files.items():
    path = os.path.join(sections_dir, filename)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")

references_content = r'''
@article{klein2015additive,
  title={Additive manufacturing of optically transparent glass},
  author={Klein, John and Stern, Michael and Franchin, Giorgia and Kayser, Markus and Inamura, Chikara and Houk, Shreya and Weaver, James C and Becker, Peter and Bove, V Michael and Oxman, Neri},
  journal={3D Printing and Additive Manufacturing},
  volume={2},
  number={3},
  pages={92--105},
  year={2015},
  publisher={Mary Ann Liebert, Inc. 140 Huguenot Street, 3rd Floor New Rochelle, NY 10801 USA}
}

@article{oxman2015glass,
  title={Glass I (G3DP)},
  author={Oxman, Neri and Klein, John and Stern, Michael and Inamura, Chikara and Houk, Peter and others},
  journal={MIT Media Lab},
  year={2015}
}

@article{inamura2018g3dp2,
  title={G3DP2: A new era of architectural glass 3D printing},
  author={Inamura, Chikara and Houk, Peter and Oxman, Neri and others},
  journal={3D Printing and Additive Manufacturing},
  year={2018}
}

@article{fateri2014additive,
  title={Additive manufacturing of glass objects by selective laser melting},
  author={Fateri, M and Gebhardt, A},
  journal={Physics Procedia},
  volume={56},
  pages={257--264},
  year={2014},
  publisher={Elsevier}
}

@article{kotz2017three,
  title={Three-dimensional printing of transparent fused silica glass},
  author={Kotz, Frederik and Arnold, Karl and Bauer, Werner and Schild, Dieter and Keller, Nicolas and Sachsenheimer, Klaus and Nargang, Tobias M and Richter, Christian and Helmer, Dorothea and Rapp, Bastian E},
  journal={Nature},
  volume={544},
  number={7650},
  pages={337--339},
  year={2017},
  publisher={Nature Publishing Group}
}
'''
with open('research_workspace/latex/references.bib', 'w') as f:
    f.write(references_content.strip() + "\n")

print("LaTeX sections and references created.")
