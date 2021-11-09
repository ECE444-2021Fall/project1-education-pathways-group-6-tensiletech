from app import df
from elasticsearch import Elasticsearch
import pandas as pd
import os

cur_path = os.path.dirname(__file__)
if not os.path.isfile(os.path.join(cur_path, '../resources/courseInfo.json')):
    print("\n************************** INITIALIZING JSON FILE NEEDED TO IMPORT TO ELASTIC SEARCH **************************\n")

    with open(os.path.join(cur_path, '../resources/courseInfo.json'), 'w') as js_file:
        for index, row in df.iterrows():
            js_file.write(row["Name":"Term"].to_json())
            js_file.write("\n")
    
    print("\n****************************************** FILE SUCCESSFULLY CREATED ******************************************\n")
else:
    print("JSON file already imported to the resoucrse folder!")
