import pandas as pd
import os

df_radiomics = pd.DataFrame()

for root, folder, files in os.walk('./Data/new'):
    for file in files:
        tempdf = pd.read_csv(os.path.join(root, file))
        df_radiomics = pd.concat([df_radiomics, tempdf])
        print(f'DONE: {file}')

df_radiomics.reset_index(inplace=True, drop=True)

df_types = pd.read_excel("./Data/Steintabelle 2021.xlsx")

for idx, val in enumerate(df_radiomics["ID"]):
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

df_radiomics.drop(columns=["ID", "image_path", "segmentation_path"], inplace=True)

for col in df_radiomics.columns:
    if "diagnostics" in col: 
        df_radiomics.drop(columns=[col], inplace=True)


print("Final Data:")
print(f'Shape: {df_radiomics.shape}')
# print('Kev Value Counts:')
# print(df_radiomics['kev'].value_counts())
print('Stone Types Value Counts:')
print(df_radiomics['type'].value_counts())

df_radiomics.to_excel("./Data/preprocessed_data_ssl.xlsx", index=False)

print("Data Written successfully!")