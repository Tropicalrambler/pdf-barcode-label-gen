# pdf-barcode-label-gen
Generate multiple EAN13 barcode labels in PDF from ERPNext's Production Planning Tool.csv files


## Install
Install dependencies:
Python
Pip
Reportlab
Babel
pyBarcode
Then, simply clone this repository to a folder of your choice in your computer.

## Configuration
For now, you should directly edit the python script to alter the search strings. A configuraiton file will be added in the near future.


## Usage
This script is for usage with ERPNext's Production Planning Tool.
It requires a .csv file that this tool generates, named:
ProductionPlanningTool.csv

You can either make the script executable, add to the $PATH variable, or simply copy the .csv file downloaded to the scripts folder location and run:

python barcode-label.gen.py

## Expected results
The program will parse through the .csv and find the barcodes as per the search string. It will count how many labels are necessary as per the materials list, and generate the appropriate amount of barcode labels, then place them in a PDF file.  Once the PDF file is done creating, it will delete the ProductionPlanningTool.csv file, and open the newly created PDF file, which I have set to be date-time stamped.

This script has been tested in MAC OS X, and using a TSC TPP-442 Pro label printer.  I am using 50mm x 38mm labels with blue thermal transfer ink.  The results are excellent so far. Once set up correctly, the process from generating the .csv, to printing the labels, takes 5 minutes.
