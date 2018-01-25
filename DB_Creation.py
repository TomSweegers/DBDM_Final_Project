#!/usr/bin/env python

# ----- Made by Tom Sweegers for the final project of the course DBDM -----

#python program used to create a database of all fits files present in the current directory
#build by Tom Sweegers starting from the file "make_tables_python.py" from Jarle Brinchmann

import glob
import math
import numpy as np
import sqlite3 as lite
from astropy.io import fits
from astropy.table import Table


def getKey(item):
    #function needed to sort an array on the second column
    return item[1]


def load_data(filename=None, check=False):
    #returns the data from a fits file
    #if check, print the column names to see if they match the database columns
    if filename: 
        hdulist = fits.open(filename)
        data = hdulist[1].data
        if check:
            cols = hdulist[1].columns
            print cols.names
        hdulist.close
        return data
    else: 
        raise IOError("No input file given")


def load_database(dbname="Final_Project.db"):
    #Loads the fits tables into a database. 
    con = lite.connect(dbname)
    
    with con:
        #Start with the information on the tables with the file_info.csv file
        t = Table().read("file_info_for_problem.csv")
        command = """CREATE TABLE IF NOT EXISTS file_info (ID INT, FieldID INT, Filename varchar(20), Filter varchar(5), MJD DOUBLE, Airmass DOUBLE, Exptime DOUBLE, UNIQUE(ID));"""
        
        con.execute(command)
        for row in t:
            #make the filename such that it corresponds to the actual fits files
            row[2] = "Field_"+str(row[1])+"_"+row[3]
            if (row[3] == 'Ks'):
                #sort the Ks files on MJD to see which E number the file has
                temp = [[line[0],line[4]] for line in t if line[1]==row[1] and line[3]==row[3]]
                sort = sorted(temp, key=getKey)
                for i in range(len(sort)):
                    if (row[0] == sort[i][0]):
                        row[2] = row[2]+"_E"+"{:03d}".format(i+1)
            
            command = """INSERT INTO file_info VALUES({0},{1},'{2}','{3}',{4},{5},{6});""".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            con.execute(command)

        #Now create all databases fot the fits files in the current folder
        fits_files = glob.glob('*.fits')
        for fname in fits_files: 
            #Create a command to create the table.
            table = fname[:-5]
            tablename = table.replace("-","_") #replaces the dashes by underscores
            command = """CREATE TABLE IF NOT EXISTS {0} (RunningID INT, X DOUBLE, Y DOUBLE, Flux1 DOUBLE, dFlux1 DOUBLE, Flux2 DOUBLE, dFlux2 DOUBLE, flux3 DOUBLE, dFlux3 DOUBLE, Ra DOUBLE, Dec DOUBLE, Class INT, Mag1 DOUBLE, dMag1 DOUBLE, Mag2 DOUBLE, dMag2 DOUBLE, Mag3 DOUBLE, dMag3 DOUBLE, StarID INT, UNIQUE(RunningID), PRIMARY KEY(RunningID));""".format(tablename)
                        
            #Execute this command.
            con.execute(command)
            
            #Loop over the table entries and insert these into the table.
            data = load_data(fname, True)
            for row in data:
                #make it a list so that nan values can be converted to NULL
                row = list(row)
                for i in range(len(row)):
                    if math.isnan(row[i]):
                        row[i] = "NULL"
                #command line to add the row to the database        
                command = "INSERT INTO {0} VALUES({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19});".format(tablename,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18])
                con.execute(command)


if __name__ == "__main__":
    load_database()



