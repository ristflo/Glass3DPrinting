#!/usr/bin/env python
"""build_bib.py - assembles latex/references.bib from doi.org BibTeX (sources/data/bibtex_raw/*.bib),
re-keyed to the manifest keys, plus curated manual entries (patents, datasheets, company pages, videos).
Then checks that every \\cite key used in latex/sections/*.tex is defined."""
import re, pathlib, glob
ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "data" / "bibtex_raw"
OUT = ROOT / "latex" / "references.bib"

def rekey(text, key):
    text = text.strip()
    text = re.sub(r"^@(\w+)\{[^,]*,", lambda m: f"@{m.group(1)}{{{key},", text, count=1)
    # doi.org sometimes omits url; add one from DOI
    if "url" not in text.lower():
        m = re.search(r"DOI\s*=\s*\{([^}]+)\}", text, re.I)
        if m:
            text = text[:-1].rstrip() + f",\n  url = {{https://doi.org/{m.group(1)}}}\n}}"
    return text

entries = []
for f in sorted(RAW.glob("*.bib")):
    entries.append(rekey(f.read_text(encoding="utf-8"), f.stem))

MANUAL = r"""
@mastersthesis{klein2015thesis,
  title = {Additive manufacturing of optically transparent glass},
  author = {Klein, John S.},
  school = {Massachusetts Institute of Technology, Program in Media Arts and Sciences},
  address = {Cambridge, MA}, year = {2015}, type = {S.M. thesis},
  note = {Advisor: Neri Oxman},
  url = {http://hdl.handle.net/1721.1/101831}
}
@misc{inglessis2017glass2,
  title = {Glass 2.0: Templating Light in 3D Printed Glass Architecture},
  author = {Inglessis, Nassia and Oxman, Neri},
  howpublished = {Project documentation, STUDIO INI / Mediated Matter Group, MIT Media Lab (Members Week 2016; exhibited as GLASS II, La Triennale di Milano, April 2017)},
  year = {2017},
  url = {https://www.nassia-inglessis.com/6813836-gl1}
}
@misc{zhou2025caustics,
  title = {Computational Caustic Design for Surface Light Source},
  author = {Zhou, Sizhuo and Sun, Yuou and Deng, Bailin and Zhang, Juyong},
  howpublished = {arXiv preprint arXiv:2511.09361},
  year = {2025},
  url = {https://arxiv.org/abs/2511.09361}
}
@article{dgf2026control,
  title = {Temperature control of digital glass forming processes},
  author = {Tiwari, Balark and Khadka, Nishan and Capps, Nicholas and Bos, Andre and Meredith, Douglas and Bernardin, John and Kinzel, Edward C. and Landers, Robert G.},
  journal = {Additive Manufacturing}, volume = {127}, pages = {105306}, year = {2026},
  publisher = {Elsevier BV}, doi = {10.1016/j.addma.2026.105306}, url = {https://doi.org/10.1016/j.addma.2026.105306}
}
@article{fluegel2007,
  title = {Glass viscosity calculation based on a global statistical modelling approach},
  author = {Fluegel, Alexander},
  journal = {Glass Technology: European Journal of Glass Science and Technology Part A},
  volume = {48}, number = {1}, pages = {13--30}, year = {2007},
  publisher = {Society of Glass Technology},
  url = {https://www.ingentaconnect.com/content/sgt/gta/2007/00000048/00000001/art00003}
}
@article{mauro2009,
  title = {Viscosity of glass-forming liquids},
  author = {Mauro, John C. and Yue, Yuanzheng and Ellison, Adam J. and Gupta, Prabhat K. and Allan, Douglas C.},
  journal = {Proceedings of the National Academy of Sciences}, volume = {106}, number = {47}, pages = {19780--19784},
  year = {2009}, publisher = {National Academy of Sciences}, doi = {10.1073/pnas.0911705106},
  url = {https://doi.org/10.1073/pnas.0911705106}
}
@article{doremus2002,
  title = {Viscosity of silica},
  author = {Doremus, Robert H.},
  journal = {Journal of Applied Physics}, volume = {92}, number = {12}, pages = {7619--7629}, year = {2002},
  publisher = {AIP Publishing}, doi = {10.1063/1.1515132}, url = {https://doi.org/10.1063/1.1515132}
}
@article{luo2014jmse,
  title = {Additive Manufacturing of Glass},
  author = {Luo, Junjie and Pan, Heng and Kinzel, Edward C.},
  journal = {Journal of Manufacturing Science and Engineering}, volume = {136}, number = {6}, pages = {061024},
  year = {2014}, publisher = {ASME}, doi = {10.1115/1.4028531}, url = {https://doi.org/10.1115/1.4028531}
}
@inproceedings{hostetler2018sff,
  title = {Fiber-Fed Printing of Free-Form Free-Standing Glass Structures},
  author = {Hostetler, John M. and Goldstein, Jonathan T. and Bristow, Douglas A. and Landers, Robert G. and Kinzel, Edward C.},
  booktitle = {Proceedings of the 29th Annual International Solid Freeform Fabrication Symposium}, address = {Austin, TX},
  year = {2018}, publisher = {University of Texas at Austin},
  url = {https://repositories.lib.utexas.edu/items/69dd5655-bb7f-4746-aa95-133ff2b21217}
}
@book{rappkotz2024book,
  title = {Additive Manufacturing of Glass: From Science to Applications},
  editor = {Rapp, Bastian E. and Kotz-Helmer, Frederik},
  year = {2024}, publisher = {Elsevier}, address = {Amsterdam}, isbn = {9780323854887},
  url = {https://www.sciencedirect.com/book/9780323854887/additive-manufacturing-of-glass}
}
@misc{patent_us9919510,
  title = {Methods and apparatus for additive manufacturing with molten glass},
  author = {Inamura, Chikara and Lizardo, Daniel and Stern, Michael and Houk, Peter and Achituv, Tal and Oxman, Neri},
  howpublished = {U.S. Patent 9,919,510 B2, assignee Massachusetts Institute of Technology; filed 23 Oct 2016, granted 20 Mar 2018},
  year = {2018}, publisher = {United States Patent and Trademark Office},
  url = {https://patents.google.com/patent/US9919510B2/en}
}
@misc{patent_us10464305,
  title = {Methods and apparatus for additive manufacturing with molten glass},
  author = {Inamura, Chikara and Lizardo, Daniel and Stern, Michael and Houk, Peter and Achituv, Tal and Oxman, Neri},
  howpublished = {U.S. Patent 10,464,305 B2 (continuation), assignee Massachusetts Institute of Technology, granted 5 Nov 2019},
  year = {2019}, publisher = {United States Patent and Trademark Office},
  url = {https://patents.google.com/patent/US10464305B2/en}
}
@misc{patent_us10266442,
  title = {Methods and apparatus for additive manufacturing of glass},
  author = {Stern, Michael and Dave, Shreya and Houk, Peter and Oxman, Neri and Franchin, Giorgia and Inamura, Chikara and Kayser, Markus and Klein, John},
  howpublished = {U.S. Patent 10,266,442 B2, assignee Massachusetts Institute of Technology; application 14/697,564 filed 27 Apr 2015, granted 23 Apr 2019},
  year = {2019}, publisher = {United States Patent and Trademark Office},
  url = {https://patents.google.com/patent/US10266442B2/en}
}
@misc{patent_corning2021,
  title = {Additive manufacturing systems and method for making glass articles},
  author = {Drewnowski, Christopher W. and Harding, Traci N. and Laskowski, Christina M. and Matusick, Joseph M. and Morgan, Kenneth S. and Peris, James P. and Peterson, Irene M. and Sonner, Thomas M.},
  howpublished = {U.S. Patent Application US 2021/0101818 A1, applicant Corning Incorporated; priority 28 Nov 2016, published 8 Apr 2021 (abandoned)},
  year = {2021}, publisher = {United States Patent and Trademark Office},
  url = {https://patents.google.com/patent/US20210101818A1/en}
}
@misc{schott_borofloat,
  title = {{BOROFLOAT\textregistered{} 33 -- Thermal Properties (technical data sheet)}},
  author = {{SCHOTT AG}}, year = {2024}, publisher = {SCHOTT AG, Mainz},
  howpublished = {Datasheet: working point \SI{1270}{\celsius} ($10^{4}$ dPa s), softening \SI{820}{\celsius}, annealing \SI{560}{\celsius}, strain \SI{518}{\celsius}},
  url = {https://www.schott.com/en-cz/products/borofloat/-/media/project/onex/products/b/borofloat/downloads/borofloat33_therm_eng_web.pdf}
}
@misc{heraeus_quartz,
  title = {Quartz materials and fused silica for lamp applications (technical brochure)},
  author = {{Heraeus Covantics}}, year = {2023}, publisher = {Heraeus, Hanau},
  howpublished = {Brochure: softening \SI{1710}{\celsius}, annealing \SI{1220}{\celsius}, strain \SI{1125}{\celsius}},
  url = {https://www.heraeus-covantics.com/media/Media/Documents/Products_and_Solutions/LAMP/EN/Quartz_lamp_materials_EN.pdf}
}
@misc{corning_eaglexg,
  title = {{Corning\textregistered{} EAGLE XG\textregistered{} Glass -- Product Information Sheet}},
  author = {{Corning Incorporated}}, year = {2019}, publisher = {Corning Incorporated, Corning NY},
  howpublished = {Datasheet: softening \SI{972}{\celsius}, annealing \SI{722}{\celsius}, strain \SI{669}{\celsius}, CTE \SI{3.2e-6}{\per\kelvin}},
  url = {https://www.corning.com/media/worldwide/cdt/documents/EAGLE_XG_Glass_PI_Sheet.pdf}
}
@misc{valleydesign_sls,
  title = {Soda-lime float glass properties},
  author = {{Valley Design Corp.}}, year = {2023}, publisher = {Valley Design Corp.},
  howpublished = {Datasheet: strain \SI{514}{\celsius}, annealing \SI{546}{\celsius}, softening \SI{726}{\celsius}},
  url = {https://valleydesign.com/sodalime/}
}
@misc{evenline_web,
  title = {Molten Glass 3D Printer -- Technology},
  author = {{Evenline Inc.}}, year = {2025}, publisher = {Evenline Inc., Rochester NY},
  howpublished = {Company web page (3D Glass Printer Mark III, \qtyproduct{325 x 325 x 380}{mm}, printing at \SI{2000}{\degree}F)},
  url = {https://www.evenline.co/technology}
}
@misc{oxman_platform,
  title = {Glass 3D Printing (platform page)},
  author = {{OXMAN}}, year = {2024}, publisher = {OXMAN},
  url = {https://www.oxman.com/platforms/glass-3d-printing}
}
@misc{medialab_glass2,
  title = {Project Overview: Glass II},
  author = {{MIT Media Lab, Mediated Matter Group}}, year = {2018}, publisher = {MIT Media Lab},
  url = {https://www.media.mit.edu/projects/g3p-ii/overview/}
}
@misc{video_glass1,
  title = {GLASS (G3DP process video, 2015)},
  author = {{Mediated Matter Group}}, year = {2015}, publisher = {Wikimedia Commons (CC BY-SA 4.0)},
  url = {https://commons.wikimedia.org/wiki/File:Matter-glass-printer.webm}
}
@misc{video_glass2,
  title = {GLASS II -- Mediated Matter (G3DP2 column installation video, 2017)},
  author = {{Mediated Matter Group}}, year = {2017}, publisher = {Vimeo / Wikimedia Commons (CC BY-SA 4.0)},
  url = {https://player.vimeo.com/video/211778198}
}
@misc{video_lexus2017,
  title = {Neri Oxman (MIT Mediated Matter Group) -- Lexus Design Event 2017 -- Milan Design Week},
  author = {{Lexus Design}}, year = {2017}, publisher = {Vimeo},
  url = {https://vimeo.com/215835768}
}
@misc{maple_web,
  title = {Australian startup begins production of world's ``first affordable 3D glass printer''},
  author = {{Australian Manufacturing Forum}}, year = {2025}, publisher = {AuManufacturing},
  howpublished = {News article on Maple Glass Printing and the Maple 4 desktop glass printer (company site mapleglassprinting.com returned HTTP 404 on 26 Sep 2026)},
  url = {https://www.aumanufacturing.com.au/australian-startup-begins-production-of-worlds-first-affordable-3d-glass-printer}
}
@misc{maple_youtube,
  title = {Maple Glass Printing -- YouTube channel (process videos; Formnext 2023 demonstration)},
  author = {{Maple Glass Printing Pty Ltd}}, year = {2023}, publisher = {YouTube},
  url = {https://www.youtube.com/@MapleGlassPrinting}
}
@misc{maple_aniwaa,
  title = {Maple Glass Printing Maple 3 overview -- an industrial 3D printer},
  author = {{Aniwaa}}, year = {2024}, publisher = {Aniwaa Pte. Ltd.},
  howpublished = {Build volume \qtyproduct{170 x 200 x 300}{mm}, price approx.\ USD 45,000, released 2022},
  url = {https://www.aniwaa.com/product/3d-printers/maple-glass-printing-maple-3/}
}
@misc{maple_ammedia,
  title = {3D Printing Brings Sustainability, Accessibility to Glass Manufacturing},
  author = {{Additive Manufacturing Media}}, year = {2023}, publisher = {Gardner Business Media},
  url = {https://www.additivemanufacturing.media/articles/3d-printing-brings-sustainability-accessibility-to-glass-manufacturing-}
}
@misc{threednatives2025,
  title = {The Top Glass 3D Printers on the Market},
  author = {{3Dnatives}}, year = {2025}, publisher = {3Dnatives},
  url = {https://www.3dnatives.com/en/the-top-glass-printers-on-the-market-02102025/}
}
@misc{nobula_web,
  title = {Nobula -- Glass 3D Printing made Fast, Affordable, and Energy Efficient},
  author = {{Nobula3D AB}}, year = {2025}, publisher = {Nobula3D AB, Stockholm},
  url = {https://www.nobula3d.com/}
}
@misc{nobula_aniwaa,
  title = {Nobula3D Glass 3D printer overview},
  author = {{Aniwaa}}, year = {2024}, publisher = {Aniwaa Pte. Ltd.},
  howpublished = {Build volume \qtyproduct{180 x 180 x 100}{mm}, up to \SI{2200}{\celsius}, Z resolution \SI{0.1}{mm}, machine \qtyproduct{1000 x 400 x 600}{mm}, 50 kg},
  url = {https://www.aniwaa.com/product/3d-printers/nobula3d-glass-3d-printer/}
}
@misc{nobula_kthventures,
  title = {Nobula 3D -- portfolio company},
  author = {{KTH Ventures}}, year = {2024}, publisher = {KTH Holding AB},
  url = {https://kthventures.se/en/portfolio/nobula-3d}
}
@misc{nobula_fabbaloo,
  title = {Swedish Startup Nobula3D Introduces Advanced Glass 3D Printing Method},
  author = {{Fabbaloo}}, year = {2023}, publisher = {Fabbaloo},
  url = {https://www.fabbaloo.com/news/swedish-startup-nobula3d-introduces-advanced-glass-3d-printing-method}
}
@misc{micron3dp_acers,
  title = {3D printing reaches the final materials frontier -- Micron3DP innovates in glass},
  author = {{American Ceramic Society}}, year = {2015}, publisher = {Ceramic Tech Today},
  url = {https://ceramics.org/ceramic-tech-today/3d-printing-reaches-the-final-materials-frontier-micron3dp-innovates-in-glass/}
}
@misc{micron3dp_3dprint2017,
  title = {Micron3DP Completes Installation of Pioneering Glass 3D Printer, Prepares for Beta Release},
  author = {{3DPrint.com}}, year = {2017}, publisher = {3DR Holdings},
  url = {https://3dprint.com/167638/micron3dp-glass-3d-printer-beta/}
}
@misc{acers2024recent,
  title = {3D-printed glass: Shining a light on recent developments},
  author = {{American Ceramic Society}}, year = {2024}, publisher = {Ceramic Tech Today},
  url = {https://ceramics.org/ceramic-tech-today/3d-printed-glass-recent-developments/}
}
@misc{mitnews2024bricks,
  title = {Engineers 3D print sturdy glass bricks for building structures},
  author = {{MIT News Office}}, year = {2024}, publisher = {Massachusetts Institute of Technology},
  url = {https://news.mit.edu/2024/engineers-3d-print-sturdy-glass-bricks-building-structures-0920}
}
@misc{rit2023,
  title = {RIT hosts glass 3D printer for research, multidisciplinary exploration},
  author = {{Rochester Institute of Technology}}, year = {2023}, publisher = {RIT News},
  url = {https://www.rit.edu/news/rit-hosts-glass-3d-printer-research-multidisciplinary-exploration}
}
@misc{llnl2018,
  title = {Lab scientists successfully print glass optics},
  author = {{Lawrence Livermore National Laboratory}}, year = {2018}, publisher = {LLNL News},
  url = {https://www.llnl.gov/news/lab-scientists-successfully-print-glass-optics}
}
@misc{glassomer_interview,
  title = {Interview with Glassomer's Dorothea Helmer: 3D Printing Fused Silica Glass on Desktop SLA Machines},
  author = {{3DPrint.com}}, year = {2020}, publisher = {3DR Holdings},
  url = {https://3dprint.com/261177/interview-with-glassomers-dorothea-helmer-3d-printing-fused-silica-glass-on-desktop-sla-machines/}
}
@misc{glassomer_crunchbase,
  title = {Glassomer -- Crunchbase Company Profile \& Funding},
  author = {{Crunchbase}}, year = {2025}, publisher = {Crunchbase Inc.},
  url = {https://www.crunchbase.com/organization/glassomer}
}
@misc{utah2025,
  title = {U leads international project to develop glass 3D printer (STELLAR, NSF, USD 1.4 M)},
  author = {{University of Utah, Price College of Engineering}}, year = {2025}, publisher = {University of Utah},
  url = {https://www.price.utah.edu/2025/03/25/u-leads-international-project-to-develop-glass-3d-printer}
}
@misc{ornl2026,
  title = {Vitriform3D and ORNL give glass a second life through 3D printing},
  author = {{Oak Ridge National Laboratory}}, year = {2026}, publisher = {ORNL News},
  url = {https://www.ornl.gov/news/vitriform3d-and-ornl-give-glass-second-life-through-3d-printing}
}
@misc{mosci_web,
  title = {3D Printing Optics and Microfluidics from Glass},
  author = {{MO SCI LLC}}, year = {2024}, publisher = {MO SCI, Rolla MO},
  url = {https://mo-sci.com/3d-printing-glass-optics-microfluidics/}
}
@misc{notredame_dgf,
  title = {Digital Glass Forming -- Laser Precision Manufacturing Laboratory},
  author = {{University of Notre Dame}}, year = {2025}, publisher = {University of Notre Dame},
  url = {https://laserlab.nd.edu/research/digital-glass-forming/}
}
@misc{monash_maple,
  title = {Maple Glass Printing -- Generator founders},
  author = {{Monash Innovation}}, year = {2023}, publisher = {Monash University},
  url = {https://www.monash.edu/monash-innovation/impact/generator-founders/maple-glass-printing}
}
@misc{wiki_plateau,
  title = {Plateau--Rayleigh instability},
  author = {{Wikipedia contributors}}, year = {2026}, publisher = {Wikimedia Foundation},
  url = {https://en.wikipedia.org/wiki/Plateau%E2%80%93Rayleigh_instability}
}
@misc{commons_caustics,
  title = {Caustic patterns of a 3D printed glass structure (photograph, CC BY-SA 4.0)},
  author = {Oxman, Neri}, year = {2015}, publisher = {Wikimedia Commons},
  url = {https://commons.wikimedia.org/wiki/File:Caustic_patterns_of_a_3D_printed_glass_structure.jpg}
}
@misc{regolithvac2024,
  title = {Additive Manufacturing with Molten Lunar Regolith under Vacuum Conditions},
  author = {{ResearchGate preprint listing}}, year = {2024}, publisher = {ResearchGate},
  url = {https://www.researchgate.net/publication/378587502_Additive_Manufacturing_with_Molten_Lunar_Regolith_under_Vacuum_Conditions}
}
"""
entries.append(MANUAL.strip())
OUT.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
defined = set(re.findall(r"@\w+\{([^,\s]+),", OUT.read_text(encoding="utf-8")))
used = set()
for tex in glob.glob(str(ROOT / "latex" / "sections" / "*.tex")):
    for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]+)\}", pathlib.Path(tex).read_text(encoding="utf-8")):
        used.update(k.strip() for k in m.group(1).split(","))
print(f"defined: {len(defined)}  used: {len(used)}")
missing = sorted(used - defined)
print("MISSING:", missing if missing else "none")
print("unused:", sorted(defined - used))
