import pyodbc

def connectSQL() :
    conn =  pyodbc.connect('Driver={SQL Server};'
                    'Server=SAGESRV\SAGESRV;'
                    'Database=VANTAGE;'
                    'Trusted_Connection=yes;')
    return conn
