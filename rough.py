import pandas as pd
import pickle

df=pd.read_csv('ml_model_fastapi/insurance.csv')
# print(df.head())

with open('ml_model_fastapi/model.pkl','rb') as f:
    model=pickle.load(f)

print(model)