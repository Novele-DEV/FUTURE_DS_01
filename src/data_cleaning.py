#laoding data
#cleaning data
#saving cleaned version of data

#universal file paths for cleanliness
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

file_path = os.path.join(BASE_DIR, "data", "raw", "raw_data.csv")
output_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")

#actual processing
import pandas as pd

#function to laod data
def load_data(path):
    return pd.read_csv(path)

#funtion to clean data
def clean_data(dataFrame):
    #remove any null values
    dataFrame = dataFrame.dropna()

    #remove description
    #dataFrame = dataFrame.drop(columns=["Description"])
    
    #first convert column to datetime format
    dataFrame["InvoiceDate"]=pd.to_datetime(dataFrame["InvoiceDate"])
    #remove time part of invoice date
    dataFrame["InvoiceDate"]=dataFrame["InvoiceDate"].dt.date
    #split over year and month
    dataFrame["Year"]=pd.to_datetime(dataFrame["InvoiceDate"]).dt.year
    dataFrame["Month"]=pd.to_datetime(dataFrame["InvoiceDate"]).dt.month

    return dataFrame


def save_data(dataFrame,path):
    dataFrame.to_csv(path,index=False)

if __name__ == "__main__":
    '''dataFrame = df'''
    df = load_data(file_path)
    df = clean_data(df)
    save_data(df, output_path)
    print("Data cleaned and saved.")