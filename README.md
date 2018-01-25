# DBDM_Final_Project
This Github repository contains all files made by Tom Sweegers for the final project in the course Databases and Datamining in Astronomy.

The final report is given by the file DBDM_final_project_report.pdf

The python programs that are created and used for the report are:
-	DB_Creation.py:	Makes the database called final_project.db for section 2 of the report using the fits files and the csv file.
-	DB_Analysis.py:	Makes visual representations for SQL search queries that return more than 20 outputs. Uses the database. Figures made by this program are: 
    -- JH_color.jpg 
    -- flux_diff.jpg
    -- magnitudes_SN30.jpg
-	DB_Sample.py:	Makes a sample of 100.000 stars using the distribution of the stars from the database created by DB_Creation.py. Figures made by this program to see if the distribution of the sample is similar to that of the data are: 
    -- color_distribution_database.jpg
    -- color_distribution_sample.jpg
    -- color_distribution_sample_overfitted.jpg
    -- hist_distribution_database.jpg
    -- hist_distribution_sample.jpg 
    -- hist_distribution_sample_overfitted.jpg
-	Photometric_Redshift.py:	Makes linear and non-linear fits of the photometric redshift for section 4 of the report. Uses the files PhotoZFileA.vot and PhotoZFileB.vot. Figures made by this program are:
    -- Redshift_Color_Multiplot.jpg 
    -- neural_network.jpg

