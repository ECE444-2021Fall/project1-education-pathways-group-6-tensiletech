from app import df, es
from elasticsearch import Elasticsearch, ElasticsearchException, helpers
import pandas as pd
import os

cur_path = os.path.dirname(__file__)
if not os.path.isfile(os.path.join(cur_path, '../resources/courseInfo.json')):
    print("\n************************** INITIALIZING JSON FILE NEEDED TO IMPORT TO ELASTIC SEARCH **************************\n")
    es_df = df.reset_index()
    with open(os.path.join(cur_path, '../resources/courseInfo.json'), 'w') as js_file:
        for index, row in es_df.iterrows():
            js_file.write(row["Code":"Term"].to_json())
            js_file.write("\n")
    
    print("\n****************************************** FILE SUCCESSFULLY CREATED ******************************************\n")

    # config elasticsearch
    # create the json file for search data if not yet created
    f = open(os.path.join(cur_path, 'resources/courseInfo.json'),)
    doc = []
    for i in f.readlines():
        doc.append(i)

    try:
        data = helpers.bulk(es, doc, index="course_info")
        print("Successfully uploaded data onto the elastic cloud cluster index!", data)
    except ElasticsearchException as error:
        print("Failed to upload elasticsearch data")
        print(error)
else:
    print("JSON file already imported to the resoucrse folder and uploaded to ElasticSearch!")
