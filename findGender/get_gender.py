import requests 
import csv
import pandas as pd

# api-endpoint
URL = "https://api.namsor.com/onomastics/api/json/gender/"
genders = []
global genders_tb
genders_tb = pd.DataFrame(index=None)

with open('gsoc_tratado_slot_3.csv',encoding='utf8',errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        try:
            nome = "a"
            sobrenome = "a"

            try:
                nome = row[2].split(' ')[0]
            except Exception as e:
                print(e)
            
            try:
                sobrenome = row[2].split(' ')[1]
            except Exception as e:
                print(e)
            
            if nome == "" :
                nome = "a"
            if sobrenome == "":
                sobrenome = "a"

            url_temp = URL + nome + "/" + sobrenome

            requestData = requests.get(url = url_temp)
            data = requestData.json()
            genders.append(data["gender"])
            genders_tb = genders_tb.append(pd.Series(data["gender"], index=None), ignore_index=True)

            print(data)
            print(data["gender"])
            print(line_count)
        except Exception as e:
            print(e)
        line_count += 1

    print(genders)
    print('Processed lines: ')
    print(line_count)


genders_tb.to_csv("genders.csv",index=False)