from connectVantage import connectVantage
from connectSQL import connectSQL
from synchSQL import synchSQL
import datetime
import requests


# Se connecter à vantage
head = connectVantage()


#p= requests.patch(Path+"("+str(ID)+")",headers=head, json = {IsExported : })
Path = 'https://api.vantage.online/Invoice(10065)'
#requests.patch(Path,headers=head, json = {ExportedDate : datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")})

print(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
today=str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
print(today)
p=requests.patch(Path,headers=head, json ={'ExportedDate' : today+str("+01:00")})
print(p)
