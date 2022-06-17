from connectVantage import connectVantage
from connectSQL import connectSQL
from synchSQL import synchSQL

# Se connecter à vantage
head = connectVantage()

# Se connecter à SQL
conn = connectSQL()

# Synchroniser Invoice
synchSQL('Invoice','VantageInvoice',head,conn)

# Synchroniser InvoiceLine
synchSQL('InvoiceLine','VantageInvoiceLine', head,conn)

# Se deconnecter de SQL
conn.close()
