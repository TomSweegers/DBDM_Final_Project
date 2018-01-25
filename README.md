# DBDM_Final_Project
This Github repository contains all files made by Tom Sweegers for the final project in the course Databases and Datamining in Astronomy.

The final report is given by the file DBDM_final_project_report.pdf

The python programs that are created and used for the report are:
-	DB_Creation.py:	Makes the database of section 2 using the fits files and the csv file.
-	DB_Analysis.py:	Makes visual representations for SQL search queries that return more than 20 outputs. Uses the database. Figures made by this program are: 
o	JH_color.jpg
o	flux_diff.jpg
o	magnitudes_SN30.jpg
-	DB_Sample.py:	Makes a sample of 100.000 stars using the distribution of the stars from the database. Figures made by this program to see if the distribution of the sample is similar to that of the data are: 
o	color_distribution_database.jpg
o	color_distribution_sample.jpg
o	color_distribution_sample_overfitted.jpg
o	hist_distribution_database.jpg
o	hist_distribution_sample.jpg 
o	hist_distribution_sample_overfitted.jpg
-	Photometric_Redshift.py:	Makes linear and non-linear fits of the photometric redshift for section 4 of the report. Uses the files PhotoZFileA.vot and PhotoZFileB.vot. Figures made by this program are:
o	Redshift_Color_Multiplot.jpg 
o	neural_network.jpg

