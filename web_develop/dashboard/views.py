from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np

# Create your views here.
def gettable():
    df = pd.read_json("https://restcountries.eu/rest/v2/all")
    df_country = df[df['name'] == "China"]
    list_border = df_country['borders'].values.tolist()
    print(list_border[0])
    df_result = df[df['alpha3Code'].isin(list_border[0])]
    df_result_t = df_result[['name', 'region', 'area', 'population', 'flag']]
    #     print(df_result_t)
    alldata = []
    for i in range(df_result_t.shape[0]):
        temp = df_result_t.iloc[i]
        alldata.append(dict(temp))
    pass
    return alldata



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
    # print(dataForMapGraph)
    df = df.nlargest(10, ['value'])
    contryNames = df['name'].values.tolist()
    bordrsLen = df['value'].values.tolist()
    table_Data = gettable()
    print(len(table_Data))
    context = {'contryNames': contryNames, 'bordrsLen': bordrsLen, 'dataForMapGraph': dataForMapGraph, 'data': table_Data}
    return render(request, 'index.html', context)

if __name__ == '__main__':
    indexPage()