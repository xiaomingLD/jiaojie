"""
 * Sensor Eval
 * add_omiga_csv.py
 * @author Jialiang Shi
 """
import pandas as pd
from filedriver.add_omiga_csv import AddOmigaToCsv

inputPath = 'objects_info.csv'
outputPath = 'out.csv'
AddOmigaToCsv(inputPath,outputPath)