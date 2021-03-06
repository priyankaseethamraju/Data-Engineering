import pandas as pd
import psycopg2
import argparse
import re
import csv
import json
import time
import datetime
from sqlalchemy import create_engine
DBname = "ctran"
DBuser = "priya"
DBpwd = "priya"

TableName = 'trip'
TableName = 'breadcrumb'
Datafile = "filedoesnotexist"  # name of the data file to be loaded
CreateDB = False  # indicates whether the DB table should be (re)-created



def createTable(conn):






















                






        with conn.cursor() as cursor:
                cursor.execute(f"""
                DROP TABLE IF EXISTS trip;


                CREATE UNLOGGED TABLE trip(


                trip_id         INTEGER ,


                route_id        INTEGER  ,
                vehicle_id      INTEGER ,

                service_key     VARCHAR,
                direction        INTEGER 
                       
               
                );






        """)

                print(f"Created {TableName}")





        with conn.cursor() as cursor:
                cursor.execute(f"""

                DROP TABLE IF EXISTS breadcrumb ;
                CREATE UNLOGGED TABLE breadcrumb(

                tstamp        INTEGER,


                latitude          FLOAT ,
                longitude        FLOAT,

                direction        INTEGER,
                speed            FLOAT,
                trip_id          INTEGER
                );







        """)






















 










                















































def dbconnect():
        connection = psycopg2.connect(


        host="127.0.0.1",
        database=DBname,
        user=DBuser,
        password=DBpwd,
        )
        connection.autocommit = True
        return connection

def serviceKey(df,i):

  for i in range(len(df['OPD_DATE'])):



   day_of_week = datetime.datetime.strptime(df['OPD_DATE'][i],'%d-%b-%y').weekday()

   if day_of_week <= 4:
     return 'weekday'
   if day_of_week ==5 :
     return 'saturday'
   if day_of_week == 6:

     return 'sunday'

def validate_breadcrumb_df(df):
 

 try:

  eve_not_null = pd.notnull(df["EVENT_NO_TRIP"])



  assert eve_not_null.all() == True
 except AssertionError:
  print("Assertion Error")


 for i in range(len(df)):

  if not df['ACT_TIME'][i]:
   df['ACT_TIME'][i] = None 

  if not df['GPS_LATITUDE'][i]:

   df['GPS_LATITUDE'][i] = None
  if not df['GPS_LONGITUDE'][i]:
   df['GPS_LONGITUDE'][i] = None
  if not df['DIRECTION'][i]:
   df['DIRECTION'][i]=None
  if not df['VELOCITY'][i]:
   df['VELOCITY'][i] = None
  if not df['EVENT_NO_TRIP'][i]:

   df['EVENT_NO_TRIP'][i] = None 


def validate_trip_df(df):
 try:

  assert(df["VEHICLE_ID"].astype(str).str.isnumeric().all()) == True
 except ValueError:

  print("value error")


 for i in range(len(df)):
  if not df['EVENT_NO_TRIP'][i]:
   df['EVENT_NO_TRIP'][i] = None
  if not df['ROUTE_ID'][i]:
   df['ROUTE_ID'][i]= None 
  if not df['VEHICLE_ID'][i]:
   df['VEHICLE_ID'][i] = None
  if not df['SERVICE_KEY'][i]:

   df['SERVICE_KEY'][i] = None
  if not df['DIRECTION'][i]:

   df['DIRECTION'][i] = None

def load(input):




  with open('a.json','w') as file:
    json.dump(input,file)

  df = pd.read_json('a.json') 
  

  conn = dbconnect()




  createTable(conn)



















  service_key = []
  for i in range(len(df)):


   service_key.append(serviceKey(df,i))



















  
  route_id = 0

  df["ROUTE_ID"] = route_id
  df['SERVICE_KEY'] = service_key


  columns_1 = df[["ACT_TIME","GPS_LATITUDE","GPS_LONGITUDE","DIRECTION","VELOCITY","EVENT_NO_TRIP"]]





  columns_2 = df[["EVENT_NO_TRIP","ROUTE_ID","VEHICLE_ID","SERVICE_KEY","DIRECTION"]]


  breadcrumb_df = columns_1.copy()
  print(breadcrumb_df.head(10))
  trip_df = columns_2.copy()
  print(trip_df.head(10))

  engine = create_engine('postgresql://priya:priya@127.0.0.1/ctran')

  validate_breadcrumb_df(breadcrumb_df)

  validate_trip_df(trip_df) 







  breadcrumb_df.rename(columns = {'ACT_TIME':'tstamp','GPS_LATITUDE':'latitude','GPS_LONGITUDE':'longitude','DIRECTION':'direction','VELOCITY':'speed','EVENT_NO_TRIP':'trip_id'},inplace=True)



  trip_df.rename(columns = {'EVENT_NO_TRIP':'trip_id','ROUTE_ID':'route_id','VEHICLE_ID':'vehicle_id','SERVICE_KEY':'service_key','DIRECTION':'direction'},inplace=True)
  
  print(trip_df.head(10))



  breadcrumb_df.to_sql('breadcrumb',engine,if_exists='append',index=False)

  trip_df.to_sql('trip',engine,if_exists='append',index=False)



  cursorObj = conn.cursor()


  cursorObj.execute('select * from breadcrumb;')

  print('Total insertions in breadcrumb table:',len(cursorObj.fetchall()))


  cursorObj.execute('select * from trip;')

  print('Total insertions in trip table:',len(cursorObj.fetchall()))

  


















  


















  






  









   


















 



 












