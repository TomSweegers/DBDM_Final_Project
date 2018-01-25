#!/usr/bin/env python

# ----- Made by Tom Sweegers for the final project of the course DBDM -----

#python program used to visualize several search queries about the database Final_Project.db

import numpy as np
import sqlite3 as lite
import matplotlib.pyplot as plt
from pandas import read_sql_query as sql


def SN_counts(con):
    #show the table names in the database between two MJD's
    Tables = sql("SELECT Filename FROM file_info WHERE MJD BETWEEN 56800 AND 57300;", con)    
    #count the number of stars with S/N>5 in each table
    for table in Tables['Filename']:
        N = sql("SELECT COUNT(*) FROM "+table+" WHERE Flux1/dFlux1>5;", con)         
        print table, N['COUNT(*)'][0] 


def JH_color(con):
    #get the objects with J-H fluxes bigger than 1.5 from all 3 Fields
    objects = []
    JH_value = []
    for i in range(3):
        temp = (sql("SELECT H.StarID, J.Mag1-H.Mag1 FROM Field_"+str(i+1)+"_H as H JOIN Field_"+str(i+1)+"_J as J ON H.StarID=J.StarID WHERE J.Mag1-H.Mag1>1.5;", con))

        objects.append(temp[:]['StarID'].tolist())
        JH_value.append(temp[:]['J.Mag1-H.Mag1'].tolist())

    return objects, JH_value


def flux_diff(con):
    #find the objects that differ more than 20 times the flux uncertainty from the mean flux in all Ks filters.
    objects = []
    difference = []
    for i in range(3):
        if (i==1):
            #field 2 is observed in only 1 Ks filter
            diff = "20*Ks1.dFlux1 - Ks1.Flux1"
            temp = (sql("SELECT Ks1.StarID, "+diff+" FROM Field_"+str(i+1)+"_Ks_E001 as Ks1 WHERE "+diff+" > 0;", con))
        elif (i==2):
            #field 3 is only observed in 2 Ks filters
            diff = "20*(Ks1.dFlux1+Ks2.dFlux1) - (Ks1.Flux1+Ks2.Flux1)"
            temp = (sql("SELECT Ks1.StarID, "+diff+" FROM Field_"+str(i+1)+"_Ks_E001 as Ks1 JOIN Field_"+str(i+1)+"_Ks_E002 as Ks2 ON Ks1.StarID=Ks2.StarID WHERE "+diff+" > 0;", con))
        elif (i==0):
            #field 1 is observed in 3 Ks filters
            diff = "20*(Ks1.dFlux1+Ks2.dFlux1+Ks3.dFlux1) - (Ks1.Flux1+Ks2.Flux1+Ks3.Flux1)" 
            temp = (sql("SELECT Ks1.StarID, "+diff+" FROM Field_"+str(i+1)+"_Ks_E001 as Ks1 JOIN Field_"+str(i+1)+"_Ks_E002 as Ks2 ON Ks1.StarID=Ks2.StarID JOIN Field_"+str(i+1)+"_Ks_E003 as Ks3 ON Ks1.StarID=Ks3.StarID WHERE "+diff+" > 0;", con))

        objects.append(temp[:]['StarID'].tolist())
        difference.append(temp[:][diff].tolist())

    return objects, difference


def scatter_plot(x, y, title, xlabel, savename):
    #create a scatter plot of x versus y
    #x and y contain 3 lists, 1 for each field, these are given 3 different colors
    #and 3 different images since the StarID's of the different fields are very different
    title_font = {'size':'20','weight':'normal','verticalalignment':'bottom'}
    axis_font = {'size':'14'}

    f, axarr = plt.subplots(3)
    plt.subplots_adjust(hspace=0.5)

    c = ['darkcyan', 'c', 'cyan']
    for i in range(3):
        axarr[2-i].scatter(x[i], y[i], s=4, color=c[i], edgecolors='none')
        axarr[2-i].set_xlabel(xlabel+' for field '+str(i+1), **axis_font)

    axarr[0].set_title(title, **title_font)
    axarr[1].set_ylabel('Star ID', **axis_font)

    plt.savefig(savename+'.jpg', dpi=1200)
    plt.cla()


def magnitudes_SN30(con):
    #get the magnitudes of all stars with S/N>30 from field 2
    command = ("SELECT Y.StarID, Y.Mag1, Z.Mag1, J.Mag1, H.Mag1, Ks.Mag1 FROM Field_2_Y as Y JOIN Field_2_Z as Z ON Y.StarID=Z.StarID JOIN Field_2_J as J ON Y.StarID=J.StarID JOIN Field_2_H as H ON Y.StarID=H.StarID JOIN Field_2_Ks_E001 as Ks ON Y.StarID=Ks.StarID WHERE Y.Flux1/Y.dFlux1>30 AND Y.Class=-1;")
    cursor = con.cursor()
    cursor.execute(command)
    
    objects = []
    magnitudes = []
    for row in cursor:
        objects.append(row[0])
        magnitudes.append([row[1], row[2], row[3], row[4], row[5]])

    mag_names = ['Y', 'Z', 'J', 'H', 'Ks-E001']

    #create a scatter plot of objects versus all sorts of magnitudes.
    title_font = {'size':'18','weight':'normal','verticalalignment':'bottom'}
    axis_font = {'size':'12'}

    f, axarr = plt.subplots(5, figsize=(7,10), sharex=True)
    
    c = ['darkslategray', 'darkcyan', 'c', 'turquoise', 'cyan']
    for i in range(5):
        axarr[i].scatter(objects, (np.asarray(magnitudes).T)[i], s=4, color=c[i], edgecolors='none')
        axarr[i].set_ylabel(mag_names[i], **axis_font)

    axarr[0].set_title("Magnitudes for stars with S/N>30 in field 2", **title_font)
    axarr[4].set_xlabel('Star ID', **axis_font)

    plt.savefig('magnitudes_SN30.jpg', dpi=1200)
    plt.cla()



if __name__ == "__main__":
    #open the database
    con = lite.connect('Final_Project.db')

    #section 2.2 of the report
    SN_counts(con)
    
    #section 2.3 of the report
    objects, JH_value = JH_color(con)
    scatter_plot(JH_value, objects, "Objects with J-H > 1.5", "J-H color", "JH_color")

    #section 2.4 of the report
    objects, difference = flux_diff(con)
    scatter_plot(difference, objects, "Objects with large flux uncertainty", "20 * flux uncertainty - mean flux", "flux_diff")

    #section 2.6 of the report
    magnitudes_SN30(con)




