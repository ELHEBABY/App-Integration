import json
import  pyodbc 
import datetime
import os


def synchSage(head, conn):
    try:
        # Ouvrir fichier log
        old_filename = 'data.txt'
        timeNow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = "%s%s" % (timeNow, old_filename)
        LogPath = os.path.join('./core/media', filename)
        Log = open(LogPath,'a')
        Log.write("Début de traitement : " + str(datetime.datetime.now())+"\n")

        # Variables environementales

        Y=1

        # Récupérer l'enregistrement invoice
        while Y==1:
            sqlInvoice ="SELECT * FROM VANTAGE.dbo.VantageInvoice2Integer"
            cursor.execute(sqlInvoice)
            recordsInvoice = cursor.fetchall()
            ChampsInvoice = [column[0] for column in cursor.description]
            ResInvoice = dict( zip( ChampsInvoice , recordsInvoice[0] ) )
            CodeClient= ResInvoice['DO_Tiers']
            InvoiceId = ResInvoice ['DO_Coord01']
            Nfacture = ResInvoice ['DO_Piece']
            print(len(recordsInvoice))
            if len(recordsInvoice)==0:
                Log.write("Fin de traitement : " + str(datetime.datetime.now())+"\n")
                #Log.close()
                #conn.close()
                #exit()
            else:
                # Vérifier si client existe
                sqlClt= "SELECT * FROM ARKEOS_ERP_TEST.dbo.DP_CLIENTS WHERE (CLI_NUM = '"+CodeClient+"')"
                cursor.execute(sqlClt)
                recordsClt = cursor.fetchall()
                print(len(recordsClt))
                if len(recordsClt)== 0:
                    Log.write("Err : Client inexistant : " + str(CodeClient)+" : " +str(datetime.datetime.now())+"\n")
                    #Log.close()
                    #conn.close()
                    #exit()
                else:
                    sqlInvoiceLine ="SELECT * FROM VANTAGE.dbo.VantageInvoiceLines2Integer"
                    cursor.execute(sqlInvoiceLine)
                    recordsInvoiceLine = cursor.fetchall()
                    ChampsInvoiceLine = [column[0] for column in cursor.description]
                    for recordInvoiceLine in recordsInvoiceLine:
                        ResInvoiceLine = dict( zip( ChampsInvoiceLine , recordInvoiceLine ) )            
                        CodeArticle= ResInvoiceLine['AR_Ref']
                        # Vérifier si Article existe
                        sqlArt= "SELECT * FROM ARKEOS_ERP_TEST.dbo.DP_ARTICLES WHERE (ART_NUM = '"+CodeArticle+"')"
                        cursor.execute(sqlArt)
                        recordsArt = cursor.fetchall()
                        ChampsArt = [column[0] for column in cursor.description]
                        ResArt = dict( zip( ChampsArt , recordsArt[0] ) )
                        if len(recordsArt)== 0:
                            Log.write("Err : Article inexistant : " + str(CodeArticle)+" : " +str(datetime.datetime.now())+"\n")
                            #Log.close()
                            #conn.close()
                            #exit()
                            st.resultat = 'Err : Article inexistant'
                        else:
                            SuiviStock = ResArt['ART_SUIVISTOCK']
                            # Vérifier si Stock suffisant
                            if SuiviStock != 'Aucun':
                                sqlStock= "SELECT * FROM VANTAGE.dbo.VantageInvoiceCheckDispo WHERE (AR_Ref = '"+CodeArticle+"')"
                                cursor.execute(sqlStock)
                                recordsStock = cursor.fetchall()
                                if len(recordsStock)==0:
                                    Log.write("Err : Stock insuffisant : " + str(CodeArticle)+" : " +str(datetime.datetime.now())+"\n")
                                    #Log.close()
                                    #conn.close()
                                    #exit()
                                    st.resultat = 'Err : Stock insuffisant'
                                else:
                                    ChampsStock = [column[0] for column in cursor.description]
                                    ResStock = dict( zip( ChampsStock , recordsStock[0] ) )
                                    DispoStock = ResStock['QteDispo']
                                    if DispoStock < 0:
                                        Log.write("Err : Stock insuffisant : " + str(CodeArticle)+" : " +str(datetime.datetime.now())+"\n")
                                        #Log.close()
                                        #conn.close()
                                        #exit()
                                        st.resultat = 'Err : Stock insuffisant'
                                        
                
                sqlInvoice2Integer = "INSERT INTO ARKEOS_ERP_TEST.dbo.F_DOCENTETE ("+str(ChampsInvoice).replace("'","").replace("[","").replace("]","")+") VALUES"+str(recordsInvoice).replace("[","").replace("]","").replace("Decimal('","").replace("')","").replace('"',"'").replace("'","''").replace("(''","('").replace(", ''",", '").replace("'',","',").replace("'')","')").replace("None","Null").replace("False","0").replace("True","1")
                print(sqlInvoice2Integer)
                cursor.execute(sqlInvoice2Integer)
                conn.commit()
                
                for i in range (len(recordsInvoiceLine)):
                    sqlInvoiceLines2Integer = "INSERT INTO ARKEOS_ERP_TEST.dbo.F_DOCLIGNE ("+str(ChampsInvoiceLine).replace("'","").replace("[","").replace("]","")+") VALUES"+str(recordsInvoiceLine[i]).replace("[","").replace("]","").replace("Decimal('","").replace("')","").replace('"',"'").replace("'","''").replace("(''","('").replace(", ''",", '").replace("'',","',").replace("'')","')").replace("None","Null").replace("False","0").replace("True","1")
                    print(sqlInvoiceLines2Integer)
                    cursor.execute(sqlInvoiceLines2Integer)
                    conn.commit()


                sqlUpdateInvoice = "UPDATE VANTAGE.dbo.VantageInvoice SET  SynchOut = "+str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))+" WHERE (Id = "+str(InvoiceId)+")"
                cursor.execute(sqlUpdateInvoice)
                conn.commit()
                
                sqlUpdateInvoiceLine = "UPDATE VANTAGE.dbo.VantageInvoice SET  SynchOut = "+str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))+" WHERE (InvoiceId = "+str(InvoiceId)+")"
                cursor.execute(sqlUpdateInvoiceLine)
                conn.commit()

                Path = 'https://api.vantage.online/Invoice('+InvoiceId+')'
                requests.patch(Path,headers=head, json = {'ExportedDate' : str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))+"+01:00"})
                
                Log.write("Succès : Facture : " + str(Nfacture)+" : " +str(datetime.datetime.now())+"\n")
        conn.close()
        Log.close()
        # exit()
    except Exception as err:
        Log = open('data.txt','a')
        #print(sqlInvoice2Integer)
        #print(sqlInvoiceLines2Integer)
        print(err)
        Log.write("Err : Erreur Sys : " + str(err)+" : " +str(datetime.datetime.now())+"\n")
        conn.close()
        Log.close()
        # exit()

        

