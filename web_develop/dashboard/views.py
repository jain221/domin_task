from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np

# Create your views here.
df = pd.read_json("https://restcountries.eu/rest/v2/all")

def indexPage(request):
    df = pd.read_json("https://restcountries.eu/rest/v2/all")
    df['value'] = df.borders.map(len)
    code = df['alpha2Code'].values.tolist()
    code3 = df['alpha3Code'].values.tolist()
    contryNames = df['name'].values.tolist()
    bordrsLen = df['value'].values.tolist()
    data = {'code': code, 'code3': code3, 'name': contryNames, 'value': bordrsLen}
    df3 = pd.DataFrame(data)
    dataForMapGraph = getDataforMap(contryNames, df3)
    # print(dataForMap)
    df = df.nlargest(10, ['value'])
    contryNames = df['name'].values.tolist()
    bordrsLen = df['value'].values.tolist()
    context = {'contryNames': contryNames, 'bordrsLen': bordrsLen, 'dataForMapGraph': dataForMapGraph}
    return render(request, 'index.html', context)

def getDataforMap(name,df3):
    dataForMap=[]
    for i in name:
        try:
            tempdf=df3[df3['name']==i]
            temp={}
            temp["code3"]=list(tempdf['code3'].values)[0]
            temp["name"]=i
            temp["value"]=list(tempdf['value'].values)[0]
            temp["code"]=list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    # print (len(dataForMap))
    return dataForMap