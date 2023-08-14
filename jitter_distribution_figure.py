"""
Function to create a figure showing the individual data points, mean, 
standard deviation, and distribution of multiple categories. 

INPUT
jitter_distribution_figure(data, cats)
data:     N x 1 numpy array containing the data points to be plotted
cats:     N x 1 list of character vectors representing the 
          corresponding groups of the data points
          
OPTIONAL INPUT
jitter_plot(..., 'PARAM1', val1, 'PARAM2', val2, ...)
 
    'Colors'       Color of the jitter plots, num of cells should 
                   correspond to categories{[r,g,b], [r,g,b], ...}. 
                   Defaults to lines colormap. 
    'Markersize'   Markersize of data points.
                   Defaults to 200.   
    'Linewidth'    Linewidth of the mean and std plot.
                   Defaults to 3.  
    'Capsize'      Capsize of the mean and std plot. 
                   Defaults to 15.
    'YLim'         Ylim [min max]
                   Defaults to standard lims. 
    'YLabel'       Ylabel {str}. 
                   Defaults to empty string.
    'DistType'     'Kernel' or 'Gaussian'. 
                   Defaults to Kernel. 
    'PlotType'     'Interal' or 'External'.
                   The option 'Interal' plots the distribution to the
                   right of the mean and errorbar. 
                   The option 'External' plots the distribution to the
                   right of the figure outline.   
                   Defaults to External. 

Copyright (c) Matlab (original) version:
                2022, Eline Zwijgers, Sint Maartenskliniek, 
                e.zwijgers@maartenskliniek.nl
                 
              Python version:
                2023, Carmen Ensink, Sint Maartenksliniek,
                c.ensink@maartenskliniek.nl

"""


def jitter_distribution_figure(data=False, cats=False, **kwargs):
    
    # Import dependencies
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    
    # Input errors
    if type(data) == bool or type(cats) == bool:
        raise Exception("Not enough input arguments")
    elif len(data) != len(cats):
        raise Exception('Data and category vector should be the same length')
    
    # Category settings
    catnames = list(dict.fromkeys(cats))
    
    # Default plot settings
    colormap = mpl.colormaps['Dark2']
    cols = colormap([0])
    for n in range(1, len(catnames)):
        cols = np.vstack((cols, colormap([n])))
    marker_size = 150
    line_width = 3
    cap_size = 5
    dist_type = 'Kernel'
    plot_type = 'External'
    y_label = ''

    # Optional plot settings
    for item, value in kwargs.items():
        if item == 'Colors':
            if len(cols) != len(catnames):
                print('Number of colors is not equal to the number of categories. The default colors are used')
            else:
                cols = value
        if item == 'Markersize':
            marker_size = value
        if item == 'Linewidth':
            line_width = value
        if item == 'Capsize':
            cap_size = value
        if item == 'YLim':
            y_lim = value
        if item == 'YLabel':
            y_label = value
        if item == 'DistType':
            if value != 'Kernel' and value != 'Gaussian':
                print('Unknown DistType. Choose between "Kernel" and "Gaussian". The default distribution (Kernal) is used.')
            else:
                dist_type = value
        if item == 'PlotType':
            if value != 'Internal' and value != 'External':
                print('Unknown PlotType. Choose between "External" and "Internal". The default plot setting (External) is used.')
            else:
                plot_type = value
    
    # Plotting
    match plot_type:
        case 'External':
            # Jitter plot
            fig, axs = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [3, 1]})
            
            for n in range(0,len(catnames)):
                thisCat = catnames[n]
                indices = [i for i, s in enumerate(cats) if thisCat in s]
                thisData = data[indices].flatten()
                xJitter, yJitter, xMean, yMean, xError, yError = Jitter(thisData, n)
                
                axs[0].scatter(xJitter, yJitter, s=marker_size, color=cols[n], edgecolors='none', alpha=0.6) #MarkerSize=marker_size, MarkerFaceColor=col, MarkerEdgeColor=None, MarkerFaceAlpha=0.6)
                axs[0].errorbar(xMean, yMean, yerr=yError, ecolor='k', elinewidth=line_width, capsize=cap_size)
                axs[0].scatter(xMean, yMean, s=marker_size, color='k', edgecolors='none')                
                
            # Format axis of jitter plot
            axs[0].set(xticks=np.arange(start=0, stop=len(catnames), step=1), xticklabels=catnames)
            axs[0].set_xlim([-0.5, len(catnames)+0.05])
            axs[0].set(ylabel=y_label)
            for item,value in kwargs.items():
                if item=='YLim':
                    axs[0].set_ylim(y_lim)
            
            # Distribution plot
            for n in range(0,len(catnames)):
                thisCat = catnames[n]
                indices = [i for i, s in enumerate(cats) if thisCat in s]
                thisData = data[indices].flatten()
                xDistribution, yDistribution = Distribution(thisData, dist_type)
                axs[1].plot(xDistribution, yDistribution, color=cols[n], linewidth=0.7*line_width)
                axs[1].fill_between(x=xDistribution, y1=yDistribution, y2=0, color=cols[n], alpha=0.4, edgecolor='none')
            
            # Format axis of distribution plot
            for item,value in kwargs.items():
                if item=='YLim':
                    axs[1].set_ylim(y_lim)
            axs[1].set(xticks=[], yticks=[])  
            axs[1].spines['bottom'].set_color('none')
            axs[1].spines['left'].set_color('none')
            axs[1].spines['right'].set_color('none')
            axs[1].spines['top'].set_color('none')
            
            
        case 'Internal':
            # Jitter plot combined with distribution plot
            fig, axs = plt.subplots(nrows=1, ncols=1)
            
            for n in range(0, len(catnames)):
                thisCat = catnames[n]
                indices = [i for i, s in enumerate(cats) if thisCat in s]
                thisData = data[indices].flatten()
                
                # Scale of distribution
                kde = sm.nonparametric.KDEUnivariate(data)
                kde.fit()
                ydens = kde.density
                match dist_type:
                    case 'Kernel':
                        scale = 0.20/np.max(ydens)
                    case 'Gaussian':
                        scale = 0.1/np.max(ydens)
                
                xJitter, yJitter, xDistribution, yDistribution, xMean, yMean, xError, yError = Jitter_distribution(thisData, n, dist_type, scale)
                
                # Plot Jitter
                axs.scatter(xJitter, yJitter, s=marker_size, color=cols[n], edgecolors='none', alpha=0.6)
                
                # Plot distribution
                axs.plot(xDistribution, yDistribution, color=cols[n], linewidth=0.7*line_width)
                axs.fill_between(x=xDistribution, y1=yDistribution, y2=0, color=cols[n], alpha=0.4, edgecolor='none')
                
                
                axs.errorbar(xMean, yMean, yerr=yError, ecolor='k', elinewidth=line_width, capsize=cap_size)
                axs.scatter(xMean, yMean, s=marker_size, color='k', edgecolors='none')                
            
            # Format axis
            axs.set(xticks=np.arange(start=0, stop=len(catnames), step=1), xticklabels=catnames)
            axs.set_xlim([-0.5, len(catnames)+0.05])
            axs.set(ylabel=y_label)
            for item,value in kwargs.items():
                if item=='YLim':
                    axs[0].set_ylim(y_lim)
    
    return





def Jitter(data, pos):
    
    # Import dependencies
    import numpy as np
    from scipy import stats
    import statsmodels.api as sm
    from scipy.interpolate import interp1d
                
    kde = sm.nonparametric.KDEUnivariate(data)
    kde.fit()
    density = kde.density
    value = kde.support
    density = density[np.argwhere(value>=np.min(data))].flatten()
    value = value[np.argwhere(value>=np.min(data))].flatten()
    density = density[np.argwhere(value<=np.max(data))].flatten()
    value = value[np.argwhere(value<=np.max(data))].flatten()
    value[0] = np.min(data)
    value[-1] = np.max(data)
    
    width = 0.05/np.max(density)
    set_jitterstrength = interp1d(value, density*width, kind='linear')
    jitterstrength = set_jitterstrength(data)
    jit = 2*(np.random.uniform(low=0, high=1, size=len(data))-0.5)
    
    xJitter = pos + jit*jitterstrength
    yJitter = data
    
    xMean = pos+0.2
    yMean = np.nanmean(data)
    xError = pos+0.2
    yError = np.nanstd(data)
        
    return xJitter, yJitter, xMean, yMean, xError, yError


def Distribution(data, dist_type):
    
    # Import dependencies
    import numpy as np
    from scipy import stats
    import statsmodels.api as sm
    
    match dist_type:
        case 'Gaussian':
            mean_data = np.nanmean(data)
            std_data = np.nanstd(data)
            xnormdis = np.arange(start=-3*std_data+mean_data, stop=3*std_data+mean_data, step=0.001)
            y_norm = stats.norm.pdf(xnormdis, mean_data, std_data)
            xDistribution = y_norm
            yDistribution = xnormdis
        case 'Kernel':
            kde = sm.nonparametric.KDEUnivariate(data)
            kde.fit()
            density = kde.density
            value = kde.support
            xDistribution = density
            yDistribution = value
    return xDistribution, yDistribution



def Jitter_distribution(data, pos, dist_type, scale):
    # Import dependencies
    import numpy as np
    from scipy import stats
    import statsmodels.api as sm
    from scipy.interpolate import interp1d
                
    kde = sm.nonparametric.KDEUnivariate(data)
    kde.fit()
    density = kde.density
    value = kde.support
    density = density[np.argwhere(value>=np.min(data))].flatten()
    value = value[np.argwhere(value>=np.min(data))].flatten()
    density = density[np.argwhere(value<=np.max(data))].flatten()
    value = value[np.argwhere(value<=np.max(data))].flatten()
    value[0] = np.min(data)
    value[-1] = np.max(data)
    
    width = 0.05/np.max(density)
    set_jitterstrength = interp1d(value, density*width, kind='linear')
    jitterstrength = set_jitterstrength(data)
    jit = 2*(np.random.uniform(low=0, high=1, size=len(data))-0.5)
    
    xJitter = pos + jit*jitterstrength
    yJitter = data
    
    match dist_type:
        case 'Gaussian':
            mean_data = np.nanmean(data)
            std_data = np.nanstd(data)
            xnormdis = np.arange(start=-3*std_data+mean_data, stop=3*std_data+mean_data, step=0.001)
            y_norm = stats.norm.pdf(xnormdis, mean_data, std_data)
            y_norm[0] = 0
            y_norm[-1] = 0
            y_norm = y_norm*scale
            
            xDistribution = y_norm+pos+0.20
            yDistribution = xnormdis
            xMean = pos+0.2
            yMean = mean_data
            xError = pos+0.2
            yError = std_data
        
        case 'Kernel':
            kde = sm.nonparametric.KDEUnivariate(data)
            kde.fit()
            value = kde.support
            f = kde.density*scale
            min_f = np.min(f)
            offset = pos+0.2-min_f
            
            xDistribution = f+offset
            yDistribution = value
            xMean = pos+0.2
            yMean = np.nanmean(data)
            xError = pos+0.2
            yError = np.nanstd(data)
            
    return xJitter, yJitter, xDistribution, yDistribution, xMean, yMean, xError, yError
    
    