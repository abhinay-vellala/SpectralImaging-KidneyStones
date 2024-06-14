import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

df_radiomics = pd.read_csv("./Data/Harnsteine Features.csv")
df_types = pd.read_excel("./Data/Steintabelle 2021.xlsx")

print(f"Shape of Radiomics(Harnsteine) Features: {df_radiomics.shape}")
print(f"Shape of types data: {df_types.shape}")

# To extract IDs of patients from data and map it with 
def extract_ID(df, col):
    for idx, row in enumerate(df[col]):
        val = row.split()
        assert len(val) == 3
        assert type(int(val[1])) == int
        assert 'kev' in val[2]
        df.loc[idx, "ID_new"] = int(val[1])
        num = re.findall(r'\d+', val[2])
        assert len(num) == 1
        df.loc[idx, "kev"] = int(num[0]) 
    return df


df_radiomics = extract_ID(df_radiomics, "ID")

if "ID_new" in df_radiomics.columns:
    print(f"Extracted IDs values from Radiomics features data")

if "kev" in df_radiomics.columns:
    print(f"Extracted KEV values from Radiomics features data")


for idx, val in enumerate(df_radiomics["ID_new"]):
    if val in df_types["Fortlaufende Nummer "]:
        df_radiomics.loc[idx, "type"] = df_types["Steinart"].loc[df_types["Fortlaufende Nummer "]==val].values[0]


print("Checking for NA values in columns of Radiomics features:")

for i,v in enumerate(df_radiomics.isna().sum()):
    if v >0:
        print(f"NA Values in {df_radiomics.isna().sum().keys()[i]}: {v}")

df_radiomics.dropna(inplace=True)

print("NA values removed")

for i,v in enumerate(df_radiomics.isna().sum()):
    if v >0:
        print(f"NA Values in {df_radiomics.isna().sum().keys()[i]}: {v}")

df_radiomics.drop(columns=["ID", "ID_new", "image_path", "segmentation_path"], inplace=True)

for col in df_radiomics.columns:
    if "diagnostics" in col: 
        df_radiomics.drop(columns=[col], inplace=True)


print("Final Data:")
print(f'Shape: {df_radiomics.shape}')
print('Kev Value Counts:')
print(df_radiomics['kev'].value_counts())
print('Stone Types Value Counts:')
print(df_radiomics['type'].value_counts())

df_radiomics.to_excel("./Data/preprocessed_data.xlsx", index=False)

print("Data Written successfully!")