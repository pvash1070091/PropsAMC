from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import DocumentForm
import requests,xlrd,xlwt,openpyxl
from .models import Document,Address


# Create your views here.

def index(request):
    return HttpResponse("Heelo Piyush")

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name=form.cleaned_data['description']
            d1=Document.objects.get(description=name)
            #request.FILES['document'].name
            loc=d1.document.path
            wb = xlrd.open_workbook(loc) 
            sheet = wb.sheet_by_index(0)
            b=''
            for i in range(sheet.nrows):
                b=b+', '+sheet.cell_value(i, 0)
                print(sheet.cell_value(i, 0))
            b=b[1:]
            address = b 
#Check if someone had already searched the address before.If the address has been searched before 
#then we will not hit the api again instead use the stored values of latitude and longitude fo that address.

            if Address.objects.filter(add=b).exists():
                abd=Address.objects.get(add=b)
                print('Latitude',abd.lat)
                print('Longitude',abd.lon) 
            else:       
                api_key = "AIzaSyCX60SAryNxXfC-l_knhx1T1EpLEB34SGA"
                api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
                api_response_dict = api_response.json()
            #  print(api_response_dict)
                if api_response_dict['status'] == 'OK':
                    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
                    print('Latitude:', latitude)
                    print('Longitude:', longitude)
#Here is the code which will save longitude and latitude corresponding to the address
                abc=Address()
                abc.add=b
                abc.lat=latitude
                abc.lon=longitude
                abc.save()
#This will write in the exel file , the value of latitude and longitude respectively
                workbook = openpyxl.load_workbook(loc)
                sheet = workbook.get_sheet_names()[0]
                worksheet = workbook.get_sheet_by_name(sheet)
                worksheet.cell(row=i, column=2).value = latitude
                worksheet.cell(row=i, column=3).value = longitude

                workbook.save(loc)
    else:
        form = DocumentForm()
    return render(request, 'polls/model_form_upload.html', {
        'form': form
    })

