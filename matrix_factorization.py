from collect_json import data_pipeline
import pandas as pd
import numpy as np

folder = '../data/'

feature_matrix = data_pipeline(folder, 'combine')

U,Sigma,V = np.linalg.svd(feature_matrix.as_matrix())
