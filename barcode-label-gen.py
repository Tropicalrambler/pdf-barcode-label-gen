#!/usr/bin/env python
# ^^^^^^^^^^^^^^^^^^^ World famous shebang line!
#  TESTED!  18-DEC-2016  ON TSC TPP-442 Pro,  WORKS GREAT!

######  DEPENDENCIES!!  Requires pip, reportlab, pybarcode, babel

#######################################################################################
#
#   1. Import modules
#
#######################################################################################
# 1.1 Python default modules  csv, sys, random, string, os
# os:  file operations
# sys:
# locale:
# datetime:
# time:
# subprocess:
# random: For generating random numbers.
# string: 
import os, sys, locale, datetime, time, subprocess, random, string, csv

# https://docs.python.org/2/library/htmlparser.html
from HTMLParser import HTMLParser
# TODO:  Develop simple GUI to generate from csv.
from Tkinter import *
import tkFileDialog

# 1.2 Dependent modules _ must ensure that you install these beforehand!

# 1.2.1 pyBarcode.  
# MAC OS X. Linux install:
# sudo pip install barcode
import barcode

# 1.2.2 Reportlab modules
# sudo pip install reportlab

# 1.2.2.1 Reportlab Graphics
# from reportlab.graphics.barcode import code39, code128, code93, qr, usps
# Reference: Constructor functions are located here: reportlab.graphics.barcode.eanbc.py
from reportlab.graphics.barcode import eanbc
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF  # To Render the PDF

# 1.2.2.2 Reportlab lib
# If you want letter size labels.
# from reportlab.lib.pagesizes import letter

from reportlab.lib.units import mm # Converts mm to points.
from reportlab.lib import colors # Color management
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# 1.2.2.3 Reportlab pdfgen PDF canvas generator
from reportlab.pdfgen import canvas

# 1.2.2.4 Reportlab pdfmetric, TTFont  (to enable your own font)  FIXME
# Functions calling these are not working  FIXME
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1.2.2.5 platypus - "Page Layout and Typography Using Scripts"
from reportlab.platypus import Paragraph # Paragraph style from reportlab

# 1.3 Babel modules
# sudo pip install babel
from babel import Locale
from babel.dates import UTC, format_date, format_datetime, format_time, get_timezone
from babel.numbers import format_number, format_decimal, format_percent


#######################################################################################
#
#   2. File Opening and Formatting variables
#
#######################################################################################

# 2.1 Variables of file and data ot open
fileName_w_ext = "ProductionPlanningTool.csv"
accessModeUniv_nl = "rU"
accessMode_W = "w"
accessMode_WB = "wb"
dot_pdf = ".pdf"

# 2.2 Register a csv Dialect  (can be changed to suit specific csv files)
# Changing this will help you parse through .csv's which have different formats
csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

# 2.3 strip original filename of extension and store it in a variable
# This variable can be used to save file with same input file name.
fileName_wo_ext = os.path.splitext(os.path.basename(fileName_w_ext))[0]
fileName_PDF_w_ext = fileName_wo_ext + dot_pdf

# 2.3 Formatting Variables, fonts, locale settings, clear command line
#locale.setlocale(locale.LC_ALL, 'en_US')  # see python doc 22.2 internationalization
here = Locale('es', 'GT')
nl = "\n"
dot = "."
space = " "
colon = ":"
dash = "-"

# 2.5 Tildes unicode http://www.fileformat.info/info/unicode/char/00f3/index.htm
a_acute_unicode = b'\xC3\xA1'
e_acute_unicode = b'\xC3\xA9'
i_acute_unicode = b'\xC3\xAD'
o_acute_unicode = b'\xC3\xB3'
u_acute_unicode = b'\xC3\xBA'
n_tilde_unicode = b'\xC3\xB1'
per_unicode = b'\x25'
registered_unicode = b'\xc2\xae'
copyright_unicode = b'\xc2\xa9'

# 2.6 decode unicode characters and assign to a variable
a_tilde_utf = a_acute_unicode.decode('utf8')
e_tilde_utf = e_acute_unicode.decode('utf8')
i_tilde_utf = i_acute_unicode.decode('utf8')
o_tilde_utf = o_acute_unicode.decode('utf8')
u_tilde_utf = u_acute_unicode.decode('utf8')
n_enie_utf = n_tilde_unicode.decode('utf8')
percent_utf = per_unicode.decode('utf8')
registered_utf = registered_unicode.decode('utf8')
copyright_utf = copyright_unicode.decode('utf8')

# 2.7 HTML elements for searching or creating strings
html_par_open = "<p>"
html_par_close = "</p>"
html_br = "<br>"
html_div_open = "<div>"
html_div_close = "</div>"
html_span_open = "<span>"
html_span_close = "</span>"
font_path = "fonts/"
load_font_roboto = font_path + "roboto/Roboto-Regular.ttf"
image_logo_filename = './assets/logo.jpg'
# 2.8 Clear the command line.  helpful for debugging.
clear_command_line = os.system('cls' if os.name == 'nt' else 'clear')
clear_command_line

#######################################################################################
#
#   3. Page size / label size / margins
#
#######################################################################################
# 3.1 GENERAL USER MODIFIABLE VARIABLES.
# These variables represent the most important properties of the barcode.
# We begin with the page or label size in millimeters.
#--------------------------------------------------------------------------------------
#  IMPORTANT NOTE ABOUT LABEL PRINTING!!!
# Label printers use the x axis as the width, same here.
# As a general rule, the widest part of the label will be also the x axis.
# I have found that the process of generating and printing labels flows faster when
# they are loaded as a "portrait" print. Trying to set orientation at print time
# results in a slow process.
label_height_mm = 38 # default = 38
label_width_mm = 50 # default = 50
lft_mgn = 2 #Left margin in mm (helps to wrap paragraph lines)
rgt_mgn = 2 #Right margin in mm  (helps to wrap paragraph lines)

#######################################################################################
#
#   4. Fixed Variables for labels (Days until expiration, field text, etc.)
#
#######################################################################################
#No extra spaces, the string concatenators will handle that.  Just the data.
#test_bar_code = "1234567800069"
#test_prod_desc = "Pillow Case Large"
#test_prod_weight = "20"
#test_prod_unit = "Oz."
# 4.2  This will be concatenated when generating the pdf file
# together with datetime string.
dest_filename = "barcode-labels"

# 4.3 Line where "Date of production" is printed
line3_produced_date_text = "Produced:"

# 4.4 line where "Expiration date" is printed
line4_expiration_date_text = "Expires:"

# 4.5 Global expiration days, TODO: Set as a default when this data is missing
days_to_expiration = 10
currency_symb = "$"

# 4.6 Price to be printed below barcode. Numbers larger than $99,000 not recommended.
# can use together with 4.7, or by itself.
test_price = 30.99

# 4.7 Text string to be printed below barcode. This also tests using vowels with accents
below_barcode_string = 'Hidrop' + o_tilde_utf + 'nico.'

#######################################################################################
#
#   5. Colors
#
#######################################################################################

# 5.1 Desired colors in RGB value o to 255
rgb_pantone_3005_c_blue = (0,117,201)
rgb_pantone_000_c_white = (255,255,255)
rgb_pantone_black = (0,0,0)

# 5.2 Desired colors in HEX
hex_pantone_3005_c_blue = "#0075c9"
hex_pantone_000_c_white = "#ffffff"
hex_pantone_black = "#000000"

# 5.3 Convert colors to intensity mode 0- 100%
rgb_pantone_black_int_red = rgb_pantone_black[0]/float(255)
rgb_pantone_black_int_grn = rgb_pantone_black[1]/float(255)
rgb_pantone_black_int_blu = rgb_pantone_black[2]/float(255)

rgb_pantone_3005_c_blue_int_red = rgb_pantone_3005_c_blue[0]/float(255)
rgb_pantone_3005_c_blue_int_grn = rgb_pantone_3005_c_blue[1]/float(255)
rgb_pantone_3005_c_blue_int_blu = rgb_pantone_3005_c_blue[2]/float(255)

# 5.3 bar color assignment
bar_red = rgb_pantone_black_int_red
bar_grn = rgb_pantone_black_int_grn
bar_blu = rgb_pantone_black_int_blu

# 5.4 text color assignment
txt_red = rgb_pantone_black_int_red
txt_grn = rgb_pantone_black_int_grn
txt_blu = rgb_pantone_black_int_blu

# 5.5 bar_stroke_color assignment
stk_red = rgb_pantone_black_int_red
stk_grn = rgb_pantone_black_int_grn
stk_blu = rgb_pantone_black_int_blu

#######################################################################################
#
#   6. Barcode Style parameters
#
#######################################################################################
# 6.1 FONTS Available fonts for the barcode human readable text for reportlab.
# Mac expert, standard, symbol, winansi, zapfdingbats, courier, courier bold corierboldoblique courieroblique, helvetica bold, helvetica bold oblique, symbol, times bold times bold italic times italic timesroman zapfdingbats.
barcode_font_name = 'Helvetica'                           # String. default 'Helvetica'
barcode_font_size = 11                                     # Number. mm. default = 11

# 6.2 Bars
# 6.2.1 Color. method. default = colors.black, or colors.Color(R,G,B,1), or colors.
bar_fill_color = colors.Color(bar_red,bar_grn,bar_blu,alpha=1)

# 6.2.2 Individual bar Height, Width, stroke width 
bar_height_mm = 14                                              # Number. default =  13
bar_width_mm = .41                                              # Number. default = .41
bar_stroke_width = .05                                          # Number. default = .05

# 6.2.3 Stroke Color. method. default = colors.black
bar_stroke_color = colors.Color(stk_red,stk_grn,stk_blu,alpha=1)

# 6.2.4 Human Readable text color. method. default = colors.black
barcode_text_color = colors.Color(txt_red,txt_grn,txt_blu,alpha=1)

# 6.2.5 Human Readable text switch ON/OFF  (TRUE/FALSE)
barcode_human_readable = 'TRUE'                               # Boolean. Default 'TRUE'

# 6.3 Code NOT WORKING!  FIXME
barcode_use_quiet_space = 0              # Number integer. 0 = no, 1 = YES. Default = 1
left_quiet_space = 1                     # Number integer default = 1 DO NOT CHANGE!!
right_quiet_space = 1                    # Number integer default = 1 DO NOT CHANGE!!

"""
FURTHER REFERENCE
http://pydoc.net/Python/reportlab/3.3.0/reportlab.graphics.barcode/
"""
# 6.4 Defining the quiet space value FIXME
if barcode_use_quiet_space == 'yes':
    quiet_space = 'TRUE'

#######################################################################################
#
#   7. Paragraph style parameters for Product Name 
#
#######################################################################################
prod_style_name = 'Pr-styl'                 #name your style:  'Stylename'
prod_font_name ='Helvetica'                # default = 'Helvetica'
prod_font_size = 11                        # default = 12
prod_leading = 12                          # default = 12
prod_left_indent = 0                       # default = 0
prod_right_indent = 0                      # default = 0
prod_first_line_indent = 0                 # default = 0
prod_alignment = TA_LEFT                   # default = TA_LEFT
prod_space_before = 0                      # default = 0
prod_space_after = 0                       # default = 0
prod_bullet_font_name = 'Times-Roman'      # default = 'Times-Roman'
prod_bullet_font_size = 10                 # default = 10
prod_bullet_indent = 0                     # default = 0
prod_text_color = hex_pantone_black        # default = hex_pantone_black
prod_back_color = None                     # default = None
prod_word_wrap = None                      # default = None
prod_border_width = 0                      # default = 0
prod_border_padding = 0                    # default = 0
prod_border_color = None                   # default = None
prod_border_radius = None                  # default = None
prod_allow_widows = 1                      # default = 1
prod_allow_orphans = 0                     # default = 0
prod_text_transform = None                 # 'uppercase' | 'lowercase' | None
prod_end_dots = None                       # default = None
prod_split_long_words = 1                  # default = 1

#######################################################################################
#
#   8. Paragraph style parameters for line below product name 
#
#######################################################################################
line3_style_name = 'line3'                  #name your style:  'Stylename'
line3_font_name ='Helvetica'                # default = 'Helvetica'
line3_font_size = 12                        # default = 12
line3_leading = 12                          # default = 12
line3_left_indent = 0                       # default = 0
line3_right_indent = 0                      # default = 0
line3_first_line_indent = 0                 # default = 0
line3_alignment = TA_LEFT                   # default = TA_LEFT
line3_space_before = 0                      # default = 0
line3_space_after = 0                       # default = 0
line3_bullet_font_name = 'Times-Roman'      # default = 'Times-Roman'
line3_bullet_font_size = 10                 # default = 10
line3_bullet_indent = 0                     # default = 0
line3_text_color = hex_pantone_black        # default = hex_pantone_black
line3_back_color = None                     # default = None
line3_word_wrap = None                      # default = None
line3_border_width = 0                      # default = 0
line3_border_padding = 0                    # default = 0
line3_border_color = None                   # default = None
line3_border_radius = None                  # default = None
line3_allow_widows = 1                      # default = 1
line3_allow_orphans = 0                     # default = 0
line3_text_transform = None                 # 'uppercase' | 'lowercase' | None
line3_end_dots = None                       # default = None
line3_split_long_words = 1                  # default = 1

#######################################################################################
#
#   9. Paragraph style parameters for second line below product name 
#
#######################################################################################
line4_style_name = 'line4'                  #name your style:  'Stylename'
line4_font_name ='Helvetica'                # default = 'Helvetica'
line4_font_size = 12                        # default = 12
line4_leading = 12                          # default = 12
line4_left_indent = 0                       # default = 0
line4_right_indent = 0                      # default = 0
line4_first_line_indent = 0                 # default = 0
line4_alignment = TA_LEFT                   # default = TA_LEFT
line4_space_before = 0                      # default = 0
line4_space_after = 0                       # default = 0
line4_bullet_font_name = 'Times-Roman'      # default = 'Times-Roman'
line4_bullet_font_size = 10                 # default = 10
line4_bullet_indent = 0                     # default = 0
line4_text_color = hex_pantone_black        # default = hex_pantone_black
line4_back_color = None                     # default = None
line4_word_wrap = None                      # default = None
line4_border_width = 0                      # default = 0
line4_border_padding = 0                    # default = 0
line4_border_color = None                   # default = None
line4_border_radius = None                  # default = None
line4_allow_widows = 1                      # default = 1
line4_allow_orphans = 0                     # default = 0
line4_text_transform = None                 # 'uppercase' | 'lowercase' | None
line4_end_dots = None                       # default = None
line4_split_long_words = 1                  # default = 1

#######################################################################################
#
#   10. Paragraph style parameters for line below product name 
#
#######################################################################################
below_barcode_style_name = 'below-barcode'          # name your style:  'Stylename'
below_barcode_font_name ='Helvetica-bold'           # default = 'Helvetica'
below_barcode_font_size = 8                         # default = 8
below_barcode_leading = 12                          # default = 12
below_barcode_left_indent = 0                       # default = 0
below_barcode_right_indent = 0                      # default = 0
below_barcode_first_line_indent = 0                 # default = 0
below_barcode_alignment = TA_LEFT                   # default = TA_LEFT
below_barcode_space_before = 0                      # default = 0
below_barcode_space_after = 0                       # default = 0
below_barcode_bullet_font_name = 'Times-Roman'      # default = 'Times-Roman'
below_barcode_bullet_font_size = 10                 # default = 10
below_barcode_bullet_indent = 0                     # default = 0
below_barcode_text_color = hex_pantone_black        # default = hex_pantone_black
below_barcode_back_color = None                     # default = None
below_barcode_word_wrap = None                      # default = None
below_barcode_border_width = 0                      # default = 0
below_barcode_border_padding = 0                    # default = 0
below_barcode_border_color = None                   # default = None
below_barcode_border_radius = None                  # default = None
below_barcode_allow_widows = 1                      # default = 1
below_barcode_allow_orphans = 0                     # default = 0
below_barcode_text_transform = None                 # 'uppercase' | 'lowercase' | None
below_barcode_end_dots = None                       # default = None
below_barcode_split_long_words = 0                  # default = 1

#######################################################################################
#
#   11. Move everything by x or y mm
#
#######################################################################################
# 11.1 This moves everything by the specified mm. Useful for adjustments on the fly!
# x axis + moves to right, - moves to left
# y axis + moves up, - moves down
move_x_mm = 0
move_y_mm = 0

#######################################################################################
#
#   12. Rotate everything 90 deg to the right, upside down, 90 to the left 
#   TODO: Pending!
#######################################################################################
# 12.1 Select rotation!


#######################################################################################
#
#   13. Positions of elements on page
#
#######################################################################################

# 13.1 Element Individual Starting Positions
# Elements must be placed, measuring from bottom left of label.
# The general structure is
# lINE 1=  Product name and weight
# LINE 2= Product name and wight continued
# LINE 3= Produced:  (date of production)
# LINE 4= Expires: (date of expiration)
# BARCODE =   EAN-13 Barcode
# LINE 5 = Price
# TODO:  If nothing specified ,an IF function should default to CENTERING EVERYTHING
# In relation to the chosen page size below
# with DEFAULTS!  For quick and easy setup.

# 13.2 Product Text position
prod_x_pos_mm = 1           # 51mm x 38mm default = 3
prod_y_pos_mm = 30          # 51mm x 38mm default = 30

# 13.3 "Date of production"
line_3_x_pos_mm = 1             # 51mm x 38mm default = 3
line_3_y_pos_mm = 25.2            # 51mm x 38mm default = 25

# 13.4 "Expiration date"
#This line is set at 12.4mm from x origin to align the ":" for easier reading.
line_4_x_pos_mm = 10.4          # 51mm x 38mm default = 12.4
line_4_y_pos_mm = 21            # 51mm x 38mm default = 21

# 13.5 Barcode position
barcode_x_pos_mm = 5            # 51mm x 38mm default = 7
barcode_y_pos_mm = 5            # 51mm x 38mm default = 5

# 13.6 Usually the price or another description goes here
below_barcode_x_pos_mm = 3      # 51mm x 38mm default = 19 for centered price
below_barcode_y_pos_mm = .5      # 51mm x 38mm default = 1

# 13.7 a Small number that returns the label group amount.
# If you print 40 labels for a particular code, you can serialize it
# for ease of counting.
label_series_x_pos_mm = 0       # 51mm x 38mm default = 0
label_series_y_pos_mm = 0       # 51mm x 38mm default = 0

# 13.8 logo position
image_logo_x_pos_mm = 16       # 51mm x 38mm default = 0
image_logo_y_pos_mm = 30       # 51mm x 38mm default = 0
image_logo_height_mm = 5      # 51mm x 38mm default = 5

#######################################################################################
#
#   9. Element Wrappers. in mm. Creates a "virtual box" so that text doesn't flow out
#
#######################################################################################

#line_1_2_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
#line_1_2_y_wrap_mm = label_height_mm-bar_height_mm

prod_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
prod_y_wrap_mm = label_height_mm-bar_height_mm

#Create a wrapper for line 3, so text cuts off rather than intrude elsewhere
line_3_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
line_3_y_wrap_mm = label_height_mm-bar_height_mm

#Create a wrapper for line 4, so text cuts off rather than intrude elsewhere
line_4_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
line_4_y_wrap_mm = label_height_mm-bar_height_mm

#Create a wrapper for line 4, so text cuts off rather than intrude elsewhere
below_barcode_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
below_barcode_y_wrap_mm = label_height_mm-bar_height_mm

#Create a wrapper for label series, so text cuts off rather than intrude elsewhere
label_series_x_wrap_mm = label_width_mm-lft_mgn-rgt_mgn
label_series_y_wrap_mm = label_height_mm-bar_height_mm

#######################################################################################
#
#   9A. Program variables that involve flow control  CAREFUL!
#
#######################################################################################

# 2.4  THE VALID PREFIX.  If you change this, no barcodes will be printed!
valid_gs1_prefix = "74011688"
# 2.5 Search string used right before product name 
desc_search_string = "Etiqueta Normal"
desc_ending_html = html_par_close

# Empty list that will contain the key,value pairs of Barcode and product, to dump into
# the PDF creation function.
all_unique_labels_lst = []

#######################################################################################
#
#   10. date calculations  (default date is today)
#
#######################################################################################

# 10.1 Date calculation and formatting.
# default= today, or can be specified date(2016, 14, 11)
production_date = datetime.date.today()
production_date_print = format_date(production_date,"dd.LLLyyyy" ,locale='es_GT')

# 10.2 Expiration date calculation and formatting
#Calculates from the production date stated above.
expiration_date = production_date + datetime.timedelta(days=days_to_expiration) 
expiration_date_print = format_date(expiration_date,"dd.LLLyyyy" ,locale='es_GT')

# 10.3 Destination Filename Variable that includes dates
file_datetime = format_datetime(datetime.datetime.now(), "yyyy-MM-dd-kk-mm-ss", locale='es_GT')
date_time_fileName_PDF_w_ext = file_datetime + dash + dest_filename + dot_pdf
#######################################################################################
#
#   11. Currency formatting
#
#######################################################################################

#2.3 Using python string formatting 
#test_price_str = str("%0.2f" % test_price)  # no commas
# below format with commas and two decimal points.
#test_format_price = locale.format("%0.2f",test_price, grouping=True)
format_price_print = format_decimal(test_price, format='#,##0.##;-#', locale='es_GT')

######################################################
#
#   12. mm to point converter
#
######################################################
"""
For our label, the position must be specified in points.  Above the user enters the 
values in mm, and these will convert from mm to points.  The move_x_mm and move_y_mm
will shift the position of all the items in the label together, when specified by the user.

"""

prod_x_pos = (prod_x_pos_mm+move_x_mm)*mm #10
prod_y_pos = (prod_y_pos_mm+move_y_mm)*mm #95

line_3_x_pos = (line_3_x_pos_mm+move_x_mm)*mm #10
line_3_y_pos = (line_3_y_pos_mm+move_y_mm)*mm #75

line_4_x_pos = (line_4_x_pos_mm+move_x_mm)*mm #10
line_4_y_pos = (line_4_y_pos_mm+move_y_mm)*mm #65

barcode_x_pos = (barcode_x_pos_mm+move_x_mm)*mm #10
barcode_y_pos = (barcode_y_pos_mm+move_y_mm)*mm #95

bar_width = bar_width_mm*mm
bar_height = bar_height_mm*mm

below_barcode_x_pos = (below_barcode_x_pos_mm+move_x_mm)*mm
below_barcode_y_pos = (below_barcode_y_pos_mm+move_y_mm)*mm

label_series_x_pos = (label_series_x_pos_mm+move_x_mm)*mm
label_series_y_pos = (label_series_y_pos_mm+move_y_mm)*mm

image_logo_x_pos = (image_logo_x_pos_mm+move_x_mm)*mm
image_logo_y_pos = (image_logo_y_pos_mm+move_y_mm)*mm

prod_x_wrap = (prod_x_wrap_mm+move_x_mm)*mm
prod_y_wrap = (prod_y_wrap_mm+move_y_mm)*mm

line_3_x_wrap = (line_3_x_wrap_mm+move_x_mm)*mm
line_3_y_wrap = (line_3_y_wrap_mm+move_y_mm)*mm

line_4_x_wrap = (line_4_x_wrap_mm+move_x_mm)*mm
line_4_y_wrap = (line_4_y_wrap_mm+move_y_mm)*mm

below_barcode_x_wrap = (below_barcode_x_wrap_mm+move_x_mm)*mm
below_barcode_y_wrap = (below_barcode_y_wrap_mm+move_y_mm)*mm

label_series_x_wrap = (label_series_x_wrap_mm+move_x_mm)*mm
label_series_y_wrap = (label_series_y_wrap_mm+move_y_mm)*mm

image_logo_height = (image_logo_height_mm+move_y_mm)*mm

######################################################
#
#   12.B Concatenating the text strings
#
######################################################
#2.3 Concatenating the Strings required by the label.
line_3_text = line3_produced_date_text + production_date_print
line_4_text = line4_expiration_date_text + expiration_date_print 
below_barcode_text = below_barcode_string #currency_symb + format_price_print

######################################################
#
#   12.C Creating Application class for TkInter window usage
#TODO: Adjust window properly.
######################################################
"""
class BarcodeLabelGen_old:
    def __init__(self, master):

            frame = Frame(master)
            frame.pack()

            self.file_select = Entry(master)
            self.file_select.pack(side=LEFT)
            self.file_select.delete(0,END)
            self.file_select.insert(0,fileName_w_ext)
            
            self.button = Button(
                frame, text="SALIR", fg="red", command=frame.quit)
            self.button.pack(side=LEFT)

            self.hi_there = Button(frame, text="Abrir Archivo .csv", command=self.say_hi)
            self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print "Aqui cargaremos el archivo!"

class BarcodeLabelGen(Frame):

    def __init__(self, parent):
        
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.button = Button(parent, text="CERRAR", fg="red", command=parent.quit)
        self.button.pack(side=LEFT)
        self.initUI()
        


    def initUI(self):

        self.parent.title("Etiquetas PDF")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Abrir", command=self.onOpen)
        menubar.add_cascade(label="Archivo", menu=fileMenu)        

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):

        ftypes = [('Comma Separated Values', '*.csv'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text
"""
#######################################################################################
#
#   13. BEGIN DEFINE LABEL CREATION FUNCTION TODO: Create two types of labels!
#
#######################################################################################

def create51mmx38mmlabels():

    ###################################################################################
    #
    #   13.1 Create a drawing object to contain everything
    #
    ###################################################################################
    """
    Create a PDFCanvas object where we will deposit all the  elements of the PDF. drawing object, and then add the barcode to the drawing. Add styles to platypus style Then using renderPDF, you place
    the drawing on the PDF. Finally, you save the file.
    """
    PDFcanvas = canvas.Canvas(date_time_fileName_PDF_w_ext)
    PDFcanvas.setPageSize((label_width_mm*mm, label_height_mm*mm))

    ###################################################################################
    #
    #   13.2 Apply paragraph styles for entire document
    #
    ###################################################################################

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name=prod_style_name, fontName=prod_font_name, fontSize=prod_font_size, leading=prod_leading, leftIndent=prod_left_indent, rightIndent=prod_right_indent, firstLineIndent=prod_first_line_indent, alignment=prod_alignment, spaceBefore=prod_space_before, spaceAfter=prod_space_after, bulletFontName=prod_bullet_font_name, bulletFontSize=prod_bullet_font_size, bulletIndent=prod_bullet_indent, textColor=prod_text_color, backColor=prod_back_color, wordWrap=prod_word_wrap, borderWidth=prod_border_width, borderPadding=prod_border_padding, borderColor=prod_border_color, borderRadius=prod_border_radius, allowWidows=prod_allow_widows, allowOrphans=prod_allow_orphans, textTransform=prod_text_transform, endDots=prod_end_dots, splitLongWords=prod_split_long_words))
    styles.add(ParagraphStyle(name=line3_style_name, fontName=line3_font_name, fontSize=line3_font_size, leading=line3_leading, leftIndent=line3_left_indent, rightIndent=line3_right_indent, firstLineIndent=line3_first_line_indent, alignment=line3_alignment, spaceBefore=line3_space_before, spaceAfter=line3_space_after, bulletFontName=line3_bullet_font_name, bulletFontSize=line3_bullet_font_size, bulletIndent=line3_bullet_indent, textColor=line3_text_color, backColor=line3_back_color, wordWrap=line3_word_wrap, borderWidth=line3_border_width, borderPadding=line3_border_padding, borderColor=line3_border_color, borderRadius=line3_border_radius, allowWidows=line3_allow_widows, allowOrphans=line3_allow_orphans, textTransform=line3_text_transform, endDots=line3_end_dots, splitLongWords=line3_split_long_words))
    styles.add(ParagraphStyle(name=line4_style_name, fontName=line4_font_name, fontSize=line4_font_size, leading=line4_leading, leftIndent=line4_left_indent, rightIndent=line4_right_indent, firstLineIndent=line4_first_line_indent, alignment=line4_alignment, spaceBefore=line4_space_before, spaceAfter=line4_space_after, bulletFontName=line4_bullet_font_name, bulletFontSize=line4_bullet_font_size, bulletIndent=line4_bullet_indent, textColor=line4_text_color, backColor=line4_back_color, wordWrap=line4_word_wrap, borderWidth=line4_border_width, borderPadding=line4_border_padding, borderColor=line4_border_color, borderRadius=line4_border_radius, allowWidows=line4_allow_widows, allowOrphans=line4_allow_orphans, textTransform=line4_text_transform, endDots=line4_end_dots, splitLongWords=line4_split_long_words))
    styles.add(ParagraphStyle(name=below_barcode_style_name, fontName=below_barcode_font_name, fontSize=below_barcode_font_size, leading=below_barcode_leading, leftIndent=below_barcode_left_indent, rightIndent=below_barcode_right_indent, firstLineIndent=below_barcode_first_line_indent, alignment=below_barcode_alignment, spaceBefore=below_barcode_space_before, spaceAfter=below_barcode_space_after, bulletFontName=below_barcode_bullet_font_name, bulletFontSize=below_barcode_bullet_font_size, bulletIndent=below_barcode_bullet_indent, textColor=below_barcode_text_color, backColor=below_barcode_back_color, wordWrap=below_barcode_word_wrap, borderWidth=below_barcode_border_width, borderPadding=below_barcode_border_padding, borderColor=below_barcode_border_color, borderRadius=below_barcode_border_radius, allowWidows=below_barcode_allow_widows, allowOrphans=below_barcode_allow_orphans, textTransform=below_barcode_text_transform, endDots=below_barcode_end_dots, splitLongWords=below_barcode_split_long_words))

    ###################################################################################
    #
    #   13.3 Set the FONT load_font_roboto = font_path + "roboto/Roboto-Regular.ttf"
    #   FIXME
    ###################################################################################
    #barcode_font = FIXME r"/Users/retina/devtools/python-barcode/EAN13-BarcodePDF/fonts/roboto/RobotoRegular.ttf"
    #barcode_font = r"/fonts/roboto/RobotoRegular.ttf"
    #barcode_font = "fonts/roboto/RobotoRegular.ttf" FIXME
    #pdfmetrics.registerFont(TTFont('vera','RobotoRegular.ttf'))

    ###################################################################################
    #
    #   13.4 Loop through the list creating the individual labels
    #
    ###################################################################################
    #The enumerate function allows access to the list items while the for loop iterates
    for index, each_label_tuple in enumerate(all_unique_labels_lst):
        # Index variable is initiated above, and returns the index or position of the list item being iterated.
        #print("this is the index: " + str(index))
        # each_label_tuple is initiated above, and is usedby enumerate to return the
        # contents of the current list item being iterated.
        #print("this is the tuple item: " + str(each_label_tuple))
        ###############################################################################
        #
        #   13.4.1 Obtain the contents of the unique label list tuples
        #
        ###############################################################################
        curr_tuple_label_desc = str(each_label_tuple[0])
        curr_tuple_label_barcode = str(each_label_tuple[1])
        #print("Current Code from tuple: " + curr_tuple_label_barcode)
        #print("Current Product from tuple: " + curr_tuple_label_desc)
        ###############################################################################
        #
        #   13.4.2 Draw the EAN-13 Code
        #
        ###############################################################################
        # Pass barcode creation parameters to reportlab, any order, as name=value pairs.
        # Order may be changed, since reportlab maps name=value pairs automatically.
        # Source code for ordering
        # http://pydoc.net/Python/reportlab/3.3.0/reportlab.graphics.barcode.eanbc/

        barcode_eanbc13 = eanbc.Ean13BarcodeWidget(value=curr_tuple_label_barcode,fontName=barcode_font_name,fontSize=barcode_font_size,x=barcode_x_pos,y=barcode_y_pos,barFillColor=bar_fill_color,barHeight=bar_height,barWidth=bar_width,barStrokeWidth=bar_stroke_width,barStrokeColor=bar_stroke_color,textColor=barcode_text_color,humanReadable=barcode_human_readable,quiet=barcode_use_quiet_space,lquiet=1,rquiet=1)

        ###############################################################################
        #
        #   13.4.? Create the drawing using the same size as the label indicated above
        #
        ###############################################################################
        #size of drawing?
        
        d = Drawing(label_width_mm*mm, label_height_mm*mm)

        ###############################################################################
        #
        #   13.4.? Set the text fill color for strings
        #
        ###############################################################################

        PDFcanvas.setFillColorRGB(txt_red,txt_grn,txt_blu) #choose your font color

        ###############################################################################
        #
        #   13.4.? OPTIONAL.   Populate the PDF with strings and images
        #
        ###############################################################################

        #PDFcanvas.drawString(line_1_x_pos,line_1_y_pos,line_1_txt)
        #PDFcanvas.drawString(line_2_x_pos,line_2_y_pos,line_2_txt)
        #PDFcanvas.drawString(line_3_x_pos,line_3_y_pos,line_3_txt)
        #PDFcanvas.drawString(line_4_x_pos,line_4_y_pos,line_4_txt)
        PDFcanvas.drawString(image_logo_x_pos+65, image_logo_y_pos,registered_utf)
        PDFcanvas.drawImage(image_logo_filename, image_logo_x_pos, image_logo_y_pos, width=None, height=image_logo_height, mask=None, preserveAspectRatio=True,  anchor='c')

        ###############################################################################
        #
        #   13.4.? Add the barcode and position it on the PDFcanvas
        #
        ###############################################################################

        d.add(barcode_eanbc13)
        # Place the generated barcode on the page.
        # (Drawing object, Barcode object, x position, y position)
        renderPDF.draw(d, PDFcanvas, 0, 0)

        #PDFcanvas.setFont('vera', 32)
        #This draws the text strings, gets position numbers from variables at beggining of file.

        """ OPTIONAL IF YOU REGISTER A BARCODE FONT, THIS IS ANOTHER WAY TO SET IT UP
        barcode_string = '<font name="Free 3 of 9 Regular" size="12">%s</font>'
            barcode_string = barcode_string % "1234567890"
        """
        #line_1_and_2 = '<font name="Helvetica" size="12">%s</font>'
        #line_1_and_2 = line_1_and_2 % line_1_txt

        ###############################################################################
        #
        #   13.4.? Add the Product description as a paragraph
        #
        ###############################################################################

        label_prod_desc_area = Paragraph(curr_tuple_label_desc, style=styles["Pr-styl"])
        label_prod_desc_area.wrapOn(PDFcanvas, prod_x_wrap, prod_y_wrap)
        label_prod_desc_area.drawOn(PDFcanvas, prod_x_pos, prod_y_pos, mm)

        ###############################################################################
        #
        #   13.4.? Add line 3 (below Prod description 1 or 2 lines) as a paragraph
        #
        ###############################################################################

        label_line3_area = Paragraph(line_3_text, style=styles["line3"])
        label_line3_area.wrapOn(PDFcanvas, line_3_x_wrap, line_3_y_wrap)
        label_line3_area.drawOn(PDFcanvas, line_3_x_pos, line_3_y_pos, mm)
        
        ###############################################################################
        #
        #   13.4.? Add line 4 (below line 3) as a paragraph
        #
        ###############################################################################

        label_line4_area = Paragraph(line_4_text, style=styles["line4"])
        label_line4_area.wrapOn(PDFcanvas, line_4_x_wrap, line_4_y_wrap)
        label_line4_area.drawOn(PDFcanvas, line_4_x_pos, line_4_y_pos, mm)

        ###############################################################################
        #
        #   13.4.? Add below barcode as a paragraph
        #   NOTE:  This is NOT the group of human readable numbers below barcode!
        ###############################################################################

        label_below_barcode_area = Paragraph(below_barcode_text, style=styles["below-barcode"])
        label_below_barcode_area.wrapOn(PDFcanvas, below_barcode_x_wrap, below_barcode_y_wrap)
        label_below_barcode_area.drawOn(PDFcanvas, below_barcode_x_pos, below_barcode_y_pos, mm)

        ###############################################################################
        #
        #   13.4.? Show the PDF
        #
        ###############################################################################

        PDFcanvas.showPage()

        ###############################################################################
        #
        #   13.4.? Save the PDF in its current state.
        #
        ###############################################################################

        PDFcanvas.save()

    ###################################################################################
    #
    #   13.4 END LOOPING THROUGH LIST CREATING INDIVIDUAL LABELS
    #
    ###################################################################################

#######################################################################################
#
#   13. END DEFINE LABEL CREATION FUNCTION
#
#######################################################################################

#######################################################################################
#
#   14. BEGIN READING CSV FILE HEADERS FOR INDEXING
#
#######################################################################################
# 14.1 This portion reads only the headers of the file, and assigns them to variables.
# with    This protects you, by using with and the one at the bottom, it ensures that
# if there is an error, it will close the file automatically.

with open (fileName_w_ext, accessModeUniv_nl) as csvFileHeaders:
    csvRead = csv.reader(csvFileHeaders, dialect='mydialect')
    headers = csvRead.next()
    header_length = str(len(headers))
    #print(nl + 'There are ' + header_length + ' headers (columns) in this file.' + nl)

    # 14.2 Assigns header text content to variables.
    #---------------------------------------  CSV COLUMN 1 ----------------------------
    try:
        header1 = headers[0]
    except IndexError:
        print('This csv file does not have a single column, please try again')
    else:
        #print('This csv file has at least one column')
        #----------------------------------  CSV COLUMN 2 -----------------------------
        try:
            header2 = headers[1]
        except IndexError:
            print('This csv file has less than two columns, please try again')
        else:
            #print('This csv file has at least two columns')
            #------------------------------  CSV COLUMN 3 -----------------------------
            try:
                header3 = headers[2]
            except IndexError:
                print('This csv file has less than three columns, please try again')
            else:
                #print('This csv file has at least three columns')
                #--------------------------  CSV COLUMN 4 -----------------------------
                try:
                    header4 = headers[3]
                except IndexError:
                    print('This csv file has less than four columns, please try again')
                else:
                    #print('This csv file has at least four columns')
                    #----------------------  CSV COLUMN 5 -----------------------------
                    try:
                        header5 = headers[4]
                    except IndexError:
                        print('This csv file has less than five columns')
                    else:
                        #print('This csv file has at least five columns')
                        #------------------  CSV COLUMN 6 -----------------------------
                        try:
                            header6 = headers[5]
                        except IndexError:
                            print('This csv file has less than six columns')
                        else:
                            #print('This csv file has at least six columns')
                            #--------------  CSV COLUMN 7 -----------------------------
                            try:
                                header7 = headers[6]
                            except IndexError:
                                print('This csv file has less than seven columns')
                            else:
                                #print('This csv file has at least seven columns')
                                #----------  CSV COLUMN 8 -----------------------------
                                try:
                                    header8 = headers[7]
                                except IndexError:
                                    print('This csv file has less than eight columns')
                                else:
                                    #print('This csv file has at least eight columns')
                                    #------  CSV COLUMN 9 -----------------------------
                                    try:
                                        header9 = headers[8]
                                    except IndexError:
                                        print('This csv file has less than nine columns')
                                    else:
                                        #print('This csv file has at least nine columns')
                                        #--  CSV COLUMN 10 ----------------------------
                                        try:
                                            header10 = headers[9]
                                        except IndexError:
                                            print('This csv file has less than ten columns')
                                        else:
                                            print('This csv file has at least ten columns')

    #verifies the content of the first line of the file.
    #print("These are the headers: " + str(headers) + nl)

#######################################################################################
#
#   14. END READING CSV FILE HEADERS FOR INDEXING
#
#######################################################################################

#######################################################################################
#
#   14A. Opening the GUI app, calling the BarcodeLabelGen
#TODO
#######################################################################################
"""
root = Tk()
app = BarcodeLabelGen(root)
root.geometry("300x250+300+300")
root.mainloop()
root.destroy() # optional; see description below
"""

#######################################################################################
#
#   15. BEGIN PROCESSING THE CSV FILE DATA
#
#######################################################################################
with open (fileName_w_ext, accessModeUniv_nl) as csvFileContents:
    # Read the file contents using csv library.
    # Calls the function .DictReader
    # don't worry about loading into a list up to about 30MB size files.

    # Opening with the DictReader class
    RowDict = csv.DictReader(csvFileContents, dialect='mydialect')
    
    #prints the dictionary item and its memory address at the moment
    #print RowDict

    ###################################################################################
    #
    #   15.2 Iterate through each row and add barcodes to a tuple, append to list
    #
    ###################################################################################

    for row in RowDict :
        ###############################################################################
        #
        #   15.2.1 Map each column to a variable for processing
        #
        ###############################################################################

        # This field holds the codes. Will be searched for barcodes
        field_item_code = row[header1]
        
        # This field will be stripped of HTML to get prod desc.
        field_item_desc = row[header2]
        field_item_stock_uom = row[header3]
        # This field has the required quantity. For each number, a label has to be created.  
        field_req_qty = row[header4]
        field_warehouse = row[header5]
        field_reqstd_qty = row[header6]
        field_ordered_qty = row[header7]
        field_actual_qty = row[header8]

#Clean up functions for ProductionPlanningTool.csv
        ###############################################################################
        #
        #   15.2.2 Process field_item_code  (Is it a VALID GS1 code?)
        # RFE TODO: Evaluate all columns, search against a list containing valid barcodes.
        ###############################################################################
        # First of all, evaluate the existence a valid_gs1_prefix exists TRUE or FALSE
        is_a_barcode = valid_gs1_prefix in field_item_code
        # TODO: Evaluate ALL columns. create a function to map correct col to var.
        # so that the column order of the csv is IRRELEVANT. However,
        
        if is_a_barcode == True:
            #Convert field_item_code to a string
            field_item_code_str = str(field_item_code)
            field_item_code_len = len(field_item_code_str)
            #print("Found a Barcode: " + field_item_code_str + " and the string that has it is " + str(field_item_code_len) + " characters long.")
            # Find barcode position in a string. By default, the end equals string length, but it can be specified.
            barcode_to_extract_begins_at = field_item_code_str.find(valid_gs1_prefix,0,field_item_code_len)
            #print barcode_to_extract_begins_at
            # Slice the string, begin at prefix found position, end at string end.
            extracted_barcode_as_is = field_item_code_str[barcode_to_extract_begins_at:field_item_code_len]
            # Slice the string, begin at prefix found position, count 12 digits
            extracted_barcode_no_check = field_item_code_str[barcode_to_extract_begins_at:barcode_to_extract_begins_at+12]
            #print extracted_barcode_as_is
            #print extracted_barcode_no_check

            ###########################################################################
            #
            #   15.2.2.1 Validate whether it is a correct barcode, otherwise exit.
            # 
            ###########################################################################
            barcode_with_calc_check_sum = barcode.ean.EuropeanArticleNumber13(extracted_barcode_no_check, writer=None)
            if str(barcode_with_calc_check_sum) == extracted_barcode_as_is:
                #print("Barcode has been correctly obtained, continuing program.")
                curr_label_barcode = extracted_barcode_as_is
            else:
                #print("Will use barcode with correctly calculated checksum: " + str(barcode_with_calc_check_sum))
                curr_label_barcode = barcode_with_calc_check_sum
            #print("Barcode found: " + curr_label_barcode + nl)
            ###########################################################################
            #
            #   15.2.2.2 Process the field_item_desc.
            #
            ###########################################################################
            #Convert field_item_desc to a string
            field_item_desc_str = str(field_item_desc)
            #find the length
            field_item_desc_len = len(field_item_desc_str)
            #find the length of the search string used to position slicing cursor
            desc_search_string_len = len(desc_search_string)
            # find length of the HTML ending tag for the string.
            desc_ending_html_len = len(desc_ending_html)
            #print("The Barcode desc is now: " + field_item_desc_str + nl + " and it is " + str(field_item_desc_len) + " characters long.")
            #Find the ending HTML tag, and set as ending point of selection for the slicing
            desc_to_extract_ends_at = field_item_desc_str.find(desc_ending_html,0,field_item_desc_len)
            # Find where to extract in the string
            desc_to_extract_begins_at = field_item_desc_str.find(desc_search_string,0,field_item_desc_len)
            #print barcode_to_extract_begins_at
            # Slice the string, begin at description search string, add length of search string, add one char for space, end string where HTML tag starts.
            extracted_desc_as_is = field_item_desc_str[desc_to_extract_begins_at+desc_search_string_len+1:desc_to_extract_ends_at]
            #print("The product description is: |" + extracted_desc_as_is + "|")
            # Set the extracted description as the current label Product.
            curr_label_product = extracted_desc_as_is

            ###########################################################################
            #
            #   15.2.2.3 Process the field_req_qty.  
            #
            ###########################################################################
            # Convert the required quantity to an integer. First to float, then to integer
            #http://stackoverflow.com/questions/1841565/valueerror-invalid-literal-for-int-with-base-10
            field_req_qty_int = int(float(field_req_qty))
            field_req_qty_str = str(field_req_qty_int)
            #Setting the current label required quantity to prevent changing code if processing is modified.
            curr_label_req_qty = field_req_qty_int
            #print("You need to print " + field_req_qty_str + " labels of: "+ nl + curr_label_product + nl + curr_label_barcode)
            ###########################################################################
            #
            #   15.2.2.4 Create the tuple containing data for the current label.  
            #
            ###########################################################################
            curr_label_tuple = (curr_label_product,curr_label_barcode)
            ###########################################################################
            #
            #   15.2.2.5 Create a list containing the tuples with barcode and product.
            #
            ###########################################################################
            for lbl in range(field_req_qty_int):
                all_unique_labels_lst.append(curr_label_tuple)
                #print("Tuple at 0: " + str(curr_label_tuple[0]) + " Tuple at 1: " + \
                #str(curr_label_tuple[1]))
        #if ends here.  No need to return anything, just finish.
        #else:
            #print("This row did NOT have a valid EAN-13 Code, moving to the next")
    ###################################################################################
    #
    #   15.3 Count the amount of labels to be printed (tuples in the list)
    #
    ###################################################################################
    label_amount_to_print = len(all_unique_labels_lst)
    #PRINT THE ENTIRE LIST OF BARCODE, PRODUCT DESCRIPTION TUPLES.  SUCCESS!!!
    #print all_unique_labels_lst
    print("There are " + str(label_amount_to_print) + " labels to be printed...")
#######################################################################################
#
#   15. END PROCESSING THE CSV FILE DATA
#
#######################################################################################

#######################################################################################
#
#   16. BEGIN CALL Create51mmx38mmlabel function
#
#######################################################################################
    if __name__ == "__main__":
        create51mmx38mmlabels()
        ###############################################################################
        #
        #   16.1 Show success message!
        #
        ###############################################################################
        end_datetime = format_datetime(datetime.datetime.now(), "yyyy.MMMdd  kk:mm:ss", locale='en_US')
        
        print("Success! Finished processing at " + end_datetime + ". Please search for the file")
        #print a_tilde_utf + space + e_tilde_utf + space + i_tilde_utf + space + o_tilde_utf + space + u_tilde_utf + space + n_enie_utf + space + percent_utf + space + registered_utf + space + copyright_utf
        ###############################################################################
        #
        #   16.2 Delete the original file
        #
        ###############################################################################
        # This is done because in a production environment, every time you download a
        # file to generate the labels, it might be automatically renamed, when this
        # happens, this script will not generate labels from the correct file.
        # It also keeps things clean and tidy!
        os.remove(fileName_w_ext)

