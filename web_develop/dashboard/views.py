from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.template.loader import get_template
from .utils import render_to_pdf

#function to get list of borders with china
def gettable():
    df = pd.read_json("https://restcountries.eu/rest/v2/all")
    df_country = df[df['name'] == "China"]
    list_border = df_country['borders'].values.tolist()
    df_result = df[df['alpha3Code'].isin(list_border[0])]
    df_result_t = df_result[['name', 'region', 'area', 'population', 'flag']]
    alldata = []
    for i in range(df_result_t.shape[0]):
        temp = df_result_t.iloc[i]
        alldata.append(dict(temp))
    pass
    return alldata

#function to create and generate pdf file from the dashboard contents.
def generatePDF(request):
    template = get_template('pdf_generator.html')
    df = pd.read_json("https://restcountries.eu/rest/v2/all")
    df['value'] = df.borders.map(len)
    df = df.nlargest(10, ['value'])
    contryNames = df['name'].values.tolist()
    bordrsLen = df['value'].values.tolist()
    list_data = df[['name', 'value']]
    list_top_ten_countries = []
    for i in range(list_data.shape[0]):
        temp = list_data.iloc[i]
        list_top_ten_countries.append(dict(temp))
    table_Data = gettable()
    context = {'contryNames': contryNames, 'bordrsLen': bordrsLen, 'data': table_Data,'list_top_ten_countries':list_top_ten_countries}
    html = template.render(context)
    pdf = render_to_pdf('pdf_generator.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "dashboard-contents.pdf"
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

#maindashboard html and backend code
def indexPage(request):
    df = pd.read_json("https://restcountries.eu/rest/v2/all")
    df['value'] = df.borders.map(len)
    df = df.nlargest(10, ['value'])
    contryNames = df['name'].values.tolist()
    bordrsLen = df['value'].values.tolist()
    table_Data = gettable()
    context = {'contryNames': contryNames, 'bordrsLen': bordrsLen, 'data': table_Data}
    return render(request, 'index.html', context)

# main function of code
if __name__ == '__main__':
    indexPage()