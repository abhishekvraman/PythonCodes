import datetime
from datetime import timedelta
import os
from time import sleep
import json
import requests
import winsound
today = datetime.date.today()
old_time = datetime.datetime.now()
new_time = old_time
print('\n\nChecking for availability at ', new_time.hour,':',new_time.minute)

while new_time.hour<23:
    api_url_base = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=678001&date='+str(today.day)+'-'+str(today.month)+'-2021'
    #api_url_base = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=308&date'+str(today.day)+'-'+str(today.month)+'-2021'
    if (new_time-old_time>timedelta(minutes=5)):
        print('\n\nChecking for availability at ', new_time.hour,':',new_time.minute)
        old_time = new_time
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 RuxitSynthetic/1.0 v10139512092 t38550 ath9b965f92 altpub cvcv=2"}
    try:
        response = requests.get(api_url_base, headers = header)
        data = response.json()
        #print(data)
        list_of_centers = data['centers']
        for center in list_of_centers:
            for session in center['sessions']:
                if (session['available_capacity']>0 and session['min_age_limit']==18):
                    print('Avaialable in ', center['name'], ' with availablity of ',session["available_capacity"])
                    winsound.PlaySound('C:/Windows/Media/Ring07.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
                
        
    except Exception as e:
        print(str(e))
    sleep(30)
    new_time = datetime.datetime.now()       
os.system("shutdown /s /t 1")        
        
