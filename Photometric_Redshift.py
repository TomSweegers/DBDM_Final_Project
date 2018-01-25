#!/usr/bin/env python

# ----- Made by Tom Sweegers for the final project of the course DBDM -----

#python program used to apply regression techniques to predict photometric redshifts of galaxies.
#build by Tom Sweegers using some of the following code from Jarle Brinchmann:
#-Exploring Regression for problem set - solution.ipynb
#-Problem 4 - solution.ipynb
#-Neural networks.ipynb
#these files can be found in the github directory https://github.com/jbrinchmann/DDM2017

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from astropy.table import Table
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from astroML.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


#global information for the figures made in this code 
sns.set(style="white")
sns.set_palette('colorblind')

title_font = {'size':'16','weight':'normal','verticalalignment':'bottom'}
axis_font = {'size':'14'}


def Read_Votdata(filename):
    #import the data from the filename
    t = Table().read(filename)
    UG = np.array(t['u-g'])
    GR = np.array(t['g-r'])
    RI = np.array(t['r-i'])
    IZ = np.array(t['i-z'])
    z_spec = np.array(t['z_spec'])

    #place the arrays as horizontal columns next to each other in an array
    #np.hstack places the arrays behind each other
    X = np.vstack((UG, GR, RI, IZ, z_spec)).T
    M = np.vstack((UG, GR, RI, IZ)).T
    return X, M


def Multiplot(X, savename):
    df = pd.DataFrame(X, columns=['u-g', 'g-r', 'r-i', 'i-z', 'z_spec'])
    sns_plot = sns.PairGrid(df, diag_sharey=False)

    sns_plot.map_lower(sns.kdeplot, cmap="Blues_d")
    sns_plot.map_upper(plt.scatter)
    sns_plot.map_diag(sns.kdeplot)

    sns_plot.savefig(savename)


def PCA(M):
    pca = PCA(whiten=True, n_components=4)
    pca.fit(M)

    #make a histogram telling how many independent components we have from the colors
    plt.bar(np.arange(len(pca.explained_variance_)),pca.explained_variance_ratio_)
    plt.title('standardised PCA', **title_font)
    plt.xlabel('Component', **axis_font)
    plt.savefig("PCA_colors_not_transformed.jpg")

    #transform the 4d data and make a multiplot
    M_trans = pca.transform(M)
    df_trans = pd.DataFrame(M_trans, columns=('PC1', 'PC2', 'PC3', 'PC4'))
    sns_plot = sns.pairplot(df_trans)
    plt.suptitle('PCA transformed 4d data')
    sns_plot.savefig('PCA_transformed_4d_multiplot.jpg')

    #transform the 4D data and reduce to 2 dimensions
    pca2D = PCA(whiten=True, n_components=2)
    M_trans = pca2D.fit_transform(M)

    #make a multiplot for the transformed 2 dimensional data
    df_trans = pd.DataFrame(M_trans, columns=('PC1', 'PC2'))
    sns_plot = sns.pairplot(df_trans)
    plt.suptitle('PCA transformed 2D data')
    sns_plot.savefig("PCA_transformed_2D_multiplot.jpg")


def Training_Error(z_phot, z_spec):
    residuals = z_phot - z_spec
    rel_residuals = residuals / (1 + z_spec)

    return np.median(np.abs(rel_residuals))


def linearregression(M, z_spec, M_B, z_spec_B):
    #apply linear regression techniques on M to find a function for z_phot
    model = LinearRegression(fit_intercept=True)
    res = model.fit(M, z_spec)
    coeff = list(res.coef_)
    print "The best fit model is:"
    print "z_phot = {0:.3f} + {1:.3f} (u-g) + {2:.3f} (g-r) + {3:.3f} (r-i) + {4:.3f} (i-z)".format(coeff[0], coeff[1], coeff[2], coeff[3], coeff[4])

    #test if z_phot is predicted to have a value close to z_spec
    z_phot = model.predict(M)
    print "The training error on the fit is:", Training_Error(z_phot, z_spec)

    #calculate the training error using file B
    z_phot_B = coeff[0]+coeff[1]*M_B[:,0]+coeff[2]*M_B[:,1]+coeff[3]*M_B[:,2]+coeff[4]*M_B[:,3]
    print "The estimated error for the test file B is:", Training_Error(z_phot_B,z_spec_B)


def neural_network(M, z_spec, M_B, z_spec_B):
    #use neural network regression to predict the photometric redshift
    nn = MLPRegressor()
    nn.fit(M, z_spec)
    
    z_phot = nn.predict(M)
    z_phot_B = nn.predict(M_B)

    print "The training error on the fit using Neural Networks is:", Training_Error(z_phot, z_spec)
    print "The estimated error on the fit using Neural Networks is:", Training_Error(z_phot_B, z_spec_B)

    #make a figure showing the deviation of the photometric to the spectroscopic redshift
    plt.figure(figsize=(7,7))
    plt.scatter(z_phot, z_spec, color="blue", s=5)
    plt.xlim(0.05, 0.6)
    plt.ylim(0.05, 0.6)
    plt.plot([0.1, 0.55], [0.1, 0.55], color="red")
    plt.xlabel("photometric redshift", **axis_font)
    plt.ylabel("spectroscopic redshift", **axis_font)
    plt.title("difference between z_phot and z_spec", **title_font)
    plt.savefig("neural_network.jpg")


if __name__ == "__main__":
    X, M = Read_Votdata("PhotoZFileA.vot")
    X_B, M_B = Read_Votdata("PhotoZFileB.vot")

    Multiplot(X, "Redshift_Color_Multiplot.jpg")
    #PCA(M) #principle component analysis on the data was tryed but seemed inneccesairy for a low training error. 
    #If even more time was given, this would have been finished and the regression techniques might have given an even lower training error.

    linearregression(M, X[:,4], M_B, X_B[:,4])
    neural_network(M, X[:,4], M_B, X_B[:,4])




