"""
Examples of figure funtions
 
Matlab (original) version:
    2022, Eline Zwijgers, Sint Maartenskliniek, 
    e.zwijgers@maartenskliniek.nl

Python version:
    2023, Carmen Ensink, Sint Maartenksliniek,
    c.ensink@maartenskliniek.nl

"""

# Import dependencies
import numpy as np
import matplotlib as mpl
from jitter_distribution_figure import jitter_distribution_figure
from scatter_distribution_figure import scatter_distribution_figure

# Random data
data = np.append(np.append(np.random.rand(50), np.random.rand(50)+1.6), np.random.rand(50)+1.4)
cats = list(['Group A'])*50 + list(['Group B'])*50  + list(['Group C'])*50

datax = np.append(np.append(np.random.rand(50), np.random.rand(50)+3), 1.5*(np.random.rand(50)+1.5))
datay = np.append(np.append(0.5*datax[0:50]+2+0.4*np.random.rand(50), 0.7*datax[50:100]+1.8+np.random.rand(50)), 0.4*datax[100:150]+2.4+0.6*(np.random.rand(50)))

color = dict()
color['c1'] = np.array(mpl.colors.to_rgb('#75bbfd')) # Blue
color['c2'] = np.array(mpl.colors.to_rgb('#f10c45')) # Red
color['c3'] = np.array(mpl.colors.to_rgb('#fcb001')) # Yellow

colors = np.array([[],[],[]]).T
for c in color:
    colors = np.vstack((colors, color[c].T))
    

# Jitter plot
Fig1 = jitter_distribution_figure(data, cats, YLabel='Y label', DistType='Gaussian', Colors=colors)

Fig2 = jitter_distribution_figure(data, cats, YLabel='Y label', PlotType='Internal', Colors=colors)

# Scatter plot 
Fig3 = scatter_distribution_figure(datax, datay, cats, YLabel='Y label', XLabel='X label', DistType='Kernel', Colors=colors)
