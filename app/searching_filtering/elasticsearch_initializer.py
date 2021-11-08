from app import df
from elasticsearch import Elasticsearch
import pandas as pd
import os

if not os.path.exists('resources/courseInfo.json'):
    print("\n************************** INITIALIZING JSON FILE NEEDED TO IMPORT TO ELASTIC SEARCH **************************\n")

    with open('courseInfo.json', 'w') as js_file:
        for index, row in df.iterrows():
            js_file.write(row["Name":"Term"].to_json())
            js_file.write("\n")
    
    print("\n****************************************** FILE SUCCESSFULLY CREATED ******************************************\n")
