"""
 Function to create a scatter plot showing the individual data points
 and the distributions on the X and Y axis. 

 INPUT
 scatter_distribution_figure(datax, datay, cats)
 datax:    N x 1 numpy array containing x-values of the data to be plotted
 datay:    N x 1 numpy array containing y-values of the data to be plotted 
 cats:     N x 1 list of character vectors representing the 
           corresponding groups of the data points

 OPTIONAL INPUT
 scatter_plot(..., KWARG1 = value1, KWARG2 = value2, ...)
 
     'Colors'       Color of the jitter plots, num of rows should 
                    correspond to categories: np.array([[r,g,b], [r,g,b], ...]). 
                    Defaults to copper colormap 
     'Markersize'   Markersize of data points.
                    Defaults to 100. 
     'Trendline'    True or False. 
                    Defaults to False.  
     'XLim'         Xlim: np.array([min, max])
                    Defaults to standard lims. 
     'YLim'         Ylim: np.array([min, max])
                    Defaults to standard lims. 
     'XLabel'       Xlabel: string. 
                    Defaults to empty string. 
     'YLabel'       Ylabel: string. 
                    Defaults to empty string.
     'DistType'     'Kernel' or 'Gaussian'. 
                    Defaults to Kernel.

 Copyright (c) Matlab (original) version:
                 2022, Eline Zwijgers, Sint Maartenskliniek, 
                 e.zwijgers@maartenskliniek.nl
                 
               Python version:
                 2023, Carmen Ensink, Sint Maartenksliniek,
                 c.ensink@maartenskliniek.nl

"""

def scatter_distribution_figure(datax=False, datay=False, cats=False, **kwargs):
    
    # Import dependencies
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    
    if type(datax) == bool or type(datay) == bool or type(cats) == bool:
        print("Not enough input arguments")
    if len(datax) != len(datay):
        print("Datax and datay arrays should be the same length")
    if len(datax) != len(cats):
        print("Data and category arrays should be the same length")
    
    # Category settings
    catnames = list(dict.fromkeys(cats))
    
    # Default plot settings
    colormap = mpl.colormaps['Dark2']
    cols = colormap([0])
    for n in range(1, len(catnames)):
        cols = np.vstack((cols, colormap([n])))
    marker_size = 100
    trendline = False
    plot_type = 'Kernel'
    x_label = ''
    y_label = ''
    font_size = 20

    # Optional plot settings
    for item, value in kwargs.items():
        if item == 'Colors':
            if len(cols) != len(catnames):
                print('Number of colors is not equal to the number of categories. The default colors are used')
            else:
                cols = value
        if item == 'Markersize':
            marker_size = value
        if item == 'Trendline':
            trendline = value
        if item == 'XLim':
            x_lim = value
        if item == 'YLim':
            y_lim = value
        if item == 'XLabel':
            x_label = value
        if item == 'YLabel':
            y_label = value
        if item == 'PlotType':
            if value != 'Kernel' and value != 'Gaussian':
                print('Unknown DistType. Choose between "Kernel" and "Gaussian". The default distribution (Kernal) is used.')
            else:
                plot_type = value
    
    # Plots
    fig, axs = plt.subplots(nrows=2, ncols=2, gridspec_kw={'width_ratios': [3, 1], 'height_ratios': [1,3] })
    
    # Scatter plot 
    for n in range(0,len(catnames)):
        thisCat = catnames[n]
        indices = [i for i, s in enumerate(cats) if thisCat in s]
        thisDatax = datax[indices].flatten()
        thisDatay = datay[indices].flatten()
        axs[1,0].scatter(thisDatax, thisDatay, s=marker_size, color=cols[n], edgecolors='none', alpha=0.6, label = thisCat)
        xTrendline, yTrendline = Scatter_trendline(thisDatax, thisDatay, trendline)
        axs[1,0].plot(xTrendline, yTrendline, color=cols[n], linewidth=2, alpha=1)
    
    # Format axis of scatter plot
    axs[1,0].set(xlabel=x_label)
    axs[1,0].set(ylabel=y_label)
    for item,value in kwargs.items():
        if item=='XLim':
            axs[1,0].set_xlim(x_lim)
    for item,value in kwargs.items():
        if item=='YLim':
            axs[1,0].set_ylim(y_lim)
    # axs[1,0].rcParams['axes.autolimit_mode'] = 'round_numbers'
    
    if len(catnames)>1:
        axs[1,0].legend()
    
    # Distribution plot y-axis
    for n in range(0,len(catnames)):
        thisCat = catnames[n]
        indices = [i for i, s in enumerate(cats) if thisCat in s]
        thisDatay = datay[indices].flatten()
        xDistribution, yDistribution, xPatch, yPatch= Distribution(thisDatay, 'y', plot_type)
        axs[1,1].plot(xDistribution, yDistribution, color=cols[n], linewidth=1.5)
        axs[1,1].fill_between(x=xDistribution, y1=yDistribution, y2=0, color=cols[n], alpha=0.4, edgecolor='none')
    
    # Format axis of distribution plot y-axis
    axs[1,1].sharey(axs[1,0])
    axs[1,1].tick_params(axis='both', colors='none')
    axs[1,1].spines['bottom'].set_color('none')
    axs[1,1].spines['left'].set_color('none')
    axs[1,1].spines['right'].set_color('none')
    axs[1,1].spines['top'].set_color('none')
    
    
    # Distribution plot x-axis
    for n in range(0,len(catnames)):
        thisCat = catnames[n]
        indices = [i for i, s in enumerate(cats) if thisCat in s]
        thisDatax = datax[indices].flatten()
        xDistribution, yDistribution, xPatch, yPatch= Distribution(thisDatax, 'x', plot_type)
        axs[0,0].plot(xDistribution, yDistribution, color=cols[n], linewidth=1.5)
        axs[0,0].fill_between(x=xDistribution, y1=yDistribution, y2=0, color=cols[n], alpha=0.4, edgecolor='none')
    
    # Format axis of distribution plot x-axis
    axs[0,0].sharex(axs[1,0])
    axs[0,0].tick_params(axis='both', colors='none')
    axs[0,0].spines['bottom'].set_color('none')
    axs[0,0].spines['left'].set_color('none')
    axs[0,0].spines['right'].set_color('none')
    axs[0,0].spines['top'].set_color('none')
    
    axs[0,1].tick_params(axis='both', colors='none')  
    axs[0,1].spines['bottom'].set_color('none')
    axs[0,1].spines['left'].set_color('none')
    axs[0,1].spines['right'].set_color('none')
    axs[0,1].spines['top'].set_color('none')
    
    plt.show(block=False)
    
    return
    
# Functions 
def Scatter_trendline(datax, datay, trendline):
    
    # Import dependencies
    from sklearn import linear_model
    import numpy as np
    
    if trendline == False:
        xTrendline = np.array([])
        yTrendline = np.array([])
    elif trendline == True:
        model = linear_model.LinearRegression(fit_intercept=True) 
        modelfit = model.fit(np.reshape(datax,(-1,1)),np.reshape(datay,(-1,1)))
        xTrendline = np.arange(start=np.min(datax)-0.05, stop=np.max(datax)+0.05, step=0.01)
        yTrendline = xTrendline*modelfit.coef_ + modelfit.intercept_
    
    return xTrendline, (yTrendline.T).flatten()
    
    
    
def Distribution(data, direction, plot_type):
    
    # Import dependencies
    import numpy as np
    from scipy import stats
    import statsmodels.api as sm
    
    mean_data = np.nanmean(data)
    std_data = np.nanstd(data)
    xnormdis = np.arange(start=-3*std_data+mean_data, stop=3*std_data+mean_data, step=0.001)
    y_norm = stats.norm.pdf(xnormdis, mean_data, std_data)
    
    if plot_type == 'Gaussian':
        if direction == 'y':
            xDistribution = y_norm/10
            yDistribution = xnormdis
            y_norm[0] = 0
            y_norm[-1] = 0
            xPatch = y_norm/10
            yPatch = xnormdis
        elif direction == 'x':
            xDistribution = xnormdis
            yDistribution = y_norm/10
            y_norm[0] = 0
            y_norm[-1] = 0
            xPatch = xnormdis
            yPatch = y_norm/10
    elif plot_type == 'Kernel':
        kde = sm.nonparametric.KDEUnivariate(data)
        kde.fit()
        density = kde.density
        value = kde.support
            
        if direction == 'y':
            xDistribution = density
            yDistribution = value
            xPatch = density
            yPatch = value
        elif direction == 'x':
            xDistribution = value
            yDistribution = density
            xPatch = value
            yPatch = density
                    
    return xDistribution, yDistribution, xPatch, yPatch

