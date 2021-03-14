import os
import pymysql
#import MySQLdb
import mysql.connector
from datetime import date
from datetime import datetime

import dbcofig

print("==========  Temperatury  ==========")


# Read from 1-wire files

def operationOnMySQL(tempInside, tempOutside):
    mydb = mysql.connector.connect(

            host = dbcofig.dbhost,
            user = dbcofig.dbuser,
            password = dbcofig.dbpass,
            database = dbcofig.dbname,
            )
    #print(mydb)
    mycursor =  mydb.cursor()
    #today  = date.today()
    #clock = datetime.now()
    #print today+" "+clock

    fulldate = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    # Create a new record

    sql = "INSERT INTO `temperatury` ( `Data`, `temp_inside`, `temp_outside`) VALUES ( %s, %s, %s);"
    val =  (fulldate,  tempInside, tempOutside)
    mycursor.execute(sql,val)

    #output = cur.fetchall()
    mydb.commit()
    print (mycursor.rowcount, "test")

def readTempInside():
    file = open("/sys/bus/w1/devices/28-051693eb15ff/w1_slave")
    print('Domek:')
    for line in file:
        temp = line.partition("t=")[2]
    print (float(temp)/1000)
    return float(temp)/1000

def readTempOutside():

    file = open("/sys/bus/w1/devices/28-051693eb6aff/w1_slave")
    print('Na dworze:')
    for line in file:
        temp =  line.partition("t=")[2]
    if((float(temp)/1000) > 4000):
        temp = 4096-(float(temp)/1000)
    print(float(temp)/1000)
    return float(temp)/1000

def main():
    readTempInside()
    readTempOutside()
    operationOnMySQL(readTempInside(), readTempOutside())





main()


