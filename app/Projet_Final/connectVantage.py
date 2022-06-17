import requests
import json


# Se connecter à vantage
def connectVantage():
    url = 'https://api.vantage.online/application/loginsingle/'
    Myauth = ('a74ea006-35ad-4411-bb39-cbd6dc90e1b5', 'siTIGo}iJ2S4iLKB8uqO=1SL[Fsm#F')
    r = requests.post (url, auth = Myauth)
    s = json.loads(r.text)
    tok = s["Token"]
    head = {'Authorization': 'Bearer '+str(tok)}
    return head
