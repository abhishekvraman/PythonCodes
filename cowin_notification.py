import datetime
import json
import requests
import winsound
today = datetime.date.today()

api_url_base = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=678001&date='+str(today.day)+'-'+str(today.month)+'-2021'
site = 'https://apisetu.gov.in/public/marketplace/api/cowin#/Appointment%20Availability%20APIs/calendarByPin'
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 RuxitSynthetic/1.0 v10139512092 t38550 ath9b965f92 altpub cvcv=2"}
response = requests.get(api_url_base, headers = header)


data = response.json()
list_of_centers = data['centers']
for center in list_of_centers:
    for session in center['sessions']:
        if (session['available_capacity']>0 and session['min_age_limit']==18):
            print("Avaialable in ", session['name'])
            while True:
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        else:
            print("Not Avaialable in ", center['name'])
            
            

        