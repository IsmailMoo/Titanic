
from flask import Flask, request
import pandas as pd
import numpy as np
import json
import pickle
import os

app = Flask(__name__)
model_path = os.path.join(os.path.pardir,'models')
model_file_path = os.path.join(model_path,'lr_model.pki')
scaler_file_path = os.path.join(model_path,'lr_scaler.pki')

scalar = pickle.load(open(scaler_file_path))
model = pickle.load(open(model_file_path))

#columns 
columns = [u'Age', u'Fare']

