from connectVantage import connectVantage
from connectSQL import connectSQL
from synchSage import synchSage

# Se connecter à vantage
head = connectVantage()

# Se connecter à SQL
conn = connectSQL()

# Synchroniser Invoice
synchSage(head, conn)

# Se deconnecter de SQL
conn.close()
