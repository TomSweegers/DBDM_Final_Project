#!/usr/bin/env python

# ----- Made by Tom Sweegers for the final project of the course DBDM -----

#python program used to create a sample of 100000 simulated stars from the database Final_Project.db
#It takes Y, J and H observations and displays the result in a Y-J, J-H plot.


import numpy as np
import sqlite3 as lite
import matplotlib.pyplot as plt
from astroML.plotting import hist
from pandas import read_sql_query as sql
from sklearn.mixture import GaussianMixture


def YJH_tables(con):
    #show the table names in the database with the images taken with Y, J or H filters
    Tables = sql("SELECT Filename FROM file_info WHERE Filter='Y' OR Filter='J' OR Filter='H';", con)

    print Tables


def color(con):
    #get the Y-J and J-H color from the stars (Class=-1)
    YJ_color = []
    JH_color = []
    for i in range(3):
        #get the Y,J and H magnitudes from the database
        YJH = (sql("SELECT Y.Mag1-J.Mag1,J.Mag1-H.Mag1 FROM Field_"+str(i+1)+"_Y as Y JOIN Field_"+str(i+1)+"_J as J ON Y.StarID=J.StarID JOIN Field_"+str(i+1)+"_H as H ON J.StarID=H.StarID WHERE Y.Class=-1;", con))

        #Filter out the nan values from the data
        YJ_temp = YJH[:]['Y.Mag1-J.Mag1'].tolist()
        JH_temp = YJH[:]['J.Mag1-H.Mag1'].tolist()
        for j in range(len(YJ_temp)):
            if not np.isnan(YJ_temp[j]+JH_temp[j]):
                YJ_color.append(YJ_temp[j])
                JH_color.append(JH_temp[j])

    return YJ_color, JH_color


def plot_function(YJ_color, JH_color, savename):
    #create a scatter plot of the Y-J versus the J-H color
    #and create one figure of 2 histogram plots for Y-J (top) and J-H (bottom).
    title_font = {'size':'16','weight':'normal','verticalalignment':'bottom'}
    axis_font = {'size':'14'}

    plt.figure(figsize=(5,5))
    plt.scatter(YJ_color, JH_color, s=4, edgecolors='none')

    plt.title('Distribution of stars', **title_font)
    plt.xlabel('Y-J color', **axis_font)
    plt.ylabel('J-H color', **axis_font)

    plt.savefig('color_distribution_'+savename+'.jpg', dpi=1200)
    plt.cla()

    f, axarr = plt.subplots(2)
    plt.subplots_adjust(hspace=0.25)
    axarr[0].hist(YJ_color, bins=250, normed=True, edgecolor='none')
    axarr[1].hist(JH_color, bins=250, normed=True, edgecolor='none')
    
    axarr[0].set_title("graphical normal test", **title_font)
    axarr[0].set_xlabel("Y-J color", **axis_font)
    axarr[1].set_xlabel("J-H color")
    axarr[0].set_xlim([-1.,0.5])
    axarr[1].set_xlim([-1.,3])

    plt.savefig('Hist_distribution_'+savename+'.jpg', dpi=1200)
    plt.cla()


def statistics(x):
    #calculate the statisitcs of the distribution x with the sum of 5 gaussians
    #x = np.asarray(x)[:, np.newaxis]
    model = GaussianMixture(5)
    res = model.fit(x)
    print model.means_
    
    #use this distribution to create a sample of 100.000 stars
    sample, label = res.sample(n_samples=100000)
    
    return sample


if __name__ == "__main__":
    #open the database
    con = lite.connect('Final_Project.db')
    
    #obtain the Y-J and J-H colors from the database and show the result visually.
    YJH_tables(con)
    YJ, JH = color(con)
    plot_function(YJ, JH, 'database')
    
    #create a 100.000 star sample and show the result visually
    sample = statistics(np.vstack((YJ, JH)).T)
    plot_function(sample[:,0], sample[:,1], 'sample')




