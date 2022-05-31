import datetime
import requests
import json
import pyodbc

def synchSQL(Table_Vantage, Table_SQL, head, conn):
    cursor = conn.cursor()
    # Acquérir data
    Path = 'https://api.vantage.online/'+ Table_Vantage
    GetData = requests.get (Path, headers=head, timeout = 80)
    RecordData = json.loads(GetData.text)["value"]
    sQlLastSynch = cursor.execute ("SELECT MAX(SynchIn) AS LastSynch FROM "+Table_SQL)
    LastSynch = sQlLastSynch.fetchall()[0][0]
    LastSynch=str(LastSynch)[0:19]
    LastSynch = datetime.datetime.strptime(LastSynch, '%Y-%m-%d %H:%M:%S')
    n=0
    # Vérifer data et mettre à jour 
    for i in range(len(RecordData)):
        
        RecordDic = RecordData[i]
        LastModified = RecordDic['ModifiedDate']
        LastModified = str(LastModified)[0:19]
        LastModified = datetime.datetime.strptime(LastModified, '%Y-%m-%dT%H:%M:%S')
        
        if LastModified > LastSynch:
            RecordDic['SynchIn']=datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
            KeysTuple = tuple([*RecordDic.keys()])
            KeysText = str(KeysTuple).replace("'","")
            ValuesTuple= tuple([*RecordData[i].values()])
            ValuesText= str(ValuesTuple).replace('"',"'").replace("'","''").replace("(''","('").\
                        replace(", ''",", '").replace("'',","',").replace("'')","')").\
                        replace("None","Null").replace("False","0").replace("True","1")
            UpdateText = str(dict( zip(KeysTuple,KeysTuple) )).replace("', '",', TARGET.').replace("': '",'=SOURCE.').\
                     replace("{'",'').replace("'}",'')
            sQlMerge= "MERGE "+ Table_SQL +" AS TARGET"\
                      " USING (VALUES "+ValuesText+") AS SOURCE"+KeysText+\
                      "ON (TARGET.ID = SOURCE.ID)" +\
                      "WHEN NOT MATCHED THEN INSERT "+KeysText+" VALUES "+ValuesText+\
                      "WHEN MATCHED THEN UPDATE SET "+UpdateText+";"
            n=n+1
            print(n)
            cursor.execute(sQlMerge)
            conn.commit()
        
 
