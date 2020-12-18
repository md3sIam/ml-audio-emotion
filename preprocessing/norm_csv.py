import pandas as pd
import os


DATA_PATH = os.path.normpath(os.path.abspath('../Data'))
ORIGIN_CSV = os.path.join(DATA_PATH, 'feature_csv.csv')

df = pd.read_csv(ORIGIN_CSV)

# Каждый столбец нужно нормализовать
