#!/usr/bin/env python
# coding: utf-8
#
# Neng Lu
# nengl@student.unimelb.edu.au
# ANU & Unimelb
# Canberra, Australia


import litho1pt0 as litho
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm

crust1pt0_clist = [
# Platforms  # Green
    "#008000",  # 0: Platform
    "#00b300",  # 1: Slow, thin Platform
    
# Archean  # DimGray
    "#696969",  # 2: Archean (Antarctica)
    "#696969",  # 3: Early Archean
    "#696969",  # 4: Late Archean
    
# Proterozoic  # Gray
    "#808080", # 5: Early/mid  Proter.,
    "#808080", # 6: Early/mid  Proter. (Antarctica, slow)
    "#808080", # 7: Late Proter.
    "#808080", # 8: Slow late Proter.

# Arcs # Brown"#A52A2A"
    "#b30000", # 9: Island arc
    "#e60000", # 10: Forearc  
    "#ff6666", # 11: Continental arc
    "#ff9999", # 12: Slow continental arc 

# Extended crust # DarkSeaGreen
    "#8FBC8F", # 13: Extended crust
    "#8FBC8F", # 14: Fast extended crust (Antarctica)  

# Orogens #SaddleBrown
    "#ff751a", # 15: Orogen (Antarctica), thick upper, thin lower crust
    "#ff6600", # 16: Orogen, thick upper crust, very thin lower crust 
    "#ff8533", # 17: Orogen, thick upper crust, fast middle crust
    "#b34700", # 18: Orogen with slow lower crust (Andes)
    "#ff9933", # 19: Slow orogen (Himalaya)  
    
# Margin # LightGreen
    "#90EE90", # 20: Margin-continent/shield  transition
    "#90EE90", # 21: Slow Margin/Shield (Antarctica)


# Rifted and Extended   #LightGrey
    "#D3D3D3",  # 22: Rift

# Phanerozoic # Khaki
    "#F0E68C", # 23: Phanerozoic
    "#F0E68C", # 24: Fast Phanerozoic (E. Australia, S. Africa, N. Siberia)  
  
# Oceans and plateau
    "#2196c4", # 25: Normal oceanic
    "#2196c4", # 26: Oceans 3 Myrs and younger
    "#2196c4", # 27: Melt affected o.c. and oceanic plateaus
    "#bee5f4", # 28: Continental shelf
    "#bee5f4", # 29: Continental slope, margin, transition

# Other 
    "#2196c4", # 30: Inactive ridge, Alpha Ridge
    "#2196c4", # 31: Thinned cont. crust, Red Sea
    "#bee5f4", # 32: Oceanic plateau with cont. crust
    "#2196c4", # 33: Caspian depression
    "#2196c4", # 34: Intermed. cont./oc. crust, Black Sea
    "#2196c4"  # 35: Caspian Sea oceanic
]

bounds = np.linspace(-0.5,35.5,len(crust1pt0_clist)+1)
norm_crust1pt0 = mpl.colors.BoundaryNorm(bounds, len(crust1pt0_clist))
cmap_crust1pt0 = mpl.colors.LinearSegmentedColormap.from_list('litho1 cmap', crust1pt0_clist, len(crust1pt0_clist))
