BASE = "https://www.talleylambert.com/classlight/"

lessons = [
    # tues 2
    "Intro Quantitative Microscopy",
    "Objective Lenses",
    "Koehler Illumination",
    # wed 3
    "Phase Darkfield DIC",
    "Fluorescence Microscopy",
    # thurs 4
    "Digital Cameras",
    "Digital Imaging",
    # fri 5
    "Basics Image Processing",
    # sat 6
    "Image corrections and segmentation",
    "Image correlation",
    # sun 7
    "Live Cell Imaging",
    "Fluorescent Proteins",
    "TIRF Microscopy",
    # mon 8
    "Concepts Machine Learning",
    "Intro Deep Learning",
    # tues 9
    "ML in Bioimage Analysis",
    "Expansion Microscopy"
    # wed 10
    "Confocal Microscopy",
    "Live Confocal",
    "Multi-photon",
    # thurs 11
    "3D Analysis and Deconvolution",
    "Limitations on Quantitative Imaging",
    # fri 12
    "Tracking",
    "Photobleaching and FRAP"
    # sat 13
    "Light-sheet 1",
    "Light-sheet 2",
    # sun 14
    "Super-resolution Localization",
    "Super-resolution SIM",
]

if __name__ == "__main__":
    for i, lesson in enumerate(lessons):
        name = lesson.lower().replace(" ", "-")
        print(f"{BASE}{i+1:02}-{name}")
