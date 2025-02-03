from django.shortcuts import render
from django.views import View
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
# Create your views here.

class ShowDataView(View):
    def get(self, request, *args, **kwargs):
        url = 'https://www.rttnews.com/corpinfo/fdacalendar.aspx'
        data = []
        for page in range(7):
            page_data = self.request_data(url + f"?PageNum={page}")
            data.extend(page_data)

        return render(request, 'core/main.html', {'data': data})

    def request_data(self, url):
        headers = {"Accept": "*/*",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"
                   }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            data = []
            rows = soup.find_all('div', class_='grid-row')
            for row in rows:
                company_name = row.find('div', class_='tblcontent1').get_text(strip=True)
                drug = row.find('div', class_='tblcontent2').get_text(strip=True)
                event = row.find('div', class_='tblcontent3').get_text(strip=True)
                outcome = row.find('div', class_='tblcontent4').get_text(strip=True)

                data.append({
                    'Name': company_name,
                    'Drug': drug,
                    'Event': event[10:],
                    'Date': event[:10]
                })
            return data

        else:
            print(f"Status code: {response.status_code}")
            return []

