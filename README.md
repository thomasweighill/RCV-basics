# RCV and minority representation

This is a python code base for running the four main models of racially polarized ranked choice voting developed by the MGGG Redistricting Lab. These models will be fully described in an upcoming report.

To use this code base, copy and adapt `run_all_models_and_print_output.py` by adjusting the parameters to suit the particular election or jurisdiction you want to study. Then run the new file to cycle through all four models and all five scenarios. The results will be printed as rows of values separated by &s for easy input into LaTeX tables.

The `template_table.tex` file contains a basic template for recording these results, including a very brief overview of the models and a blank table with headers.

The repo also contains the Census and election data used in the case studies (Terrebonne Parish LA, Cincinnati OH, Jones County NC and Pasadena TX) in the upcoming report. 
