"""
 * Sensor Eval
 * objects_classification_test.py
 * @author Jialiang Shi
 """

import pandas as pd
from filedriver.objects_classification import DumpJson

inputPath = 'objects_info.csv'
info = pd.read_csv(inputPath)
info = info[:32093]
DumpJson(info, 'data.json')