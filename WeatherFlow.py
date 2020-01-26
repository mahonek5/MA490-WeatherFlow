# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:26:36 2020

@author: Kade Mahoney
"""
import csv
import os.path
from os import path
import pandas as pd

#Max station number used for the upper bound in searching for valid station ID's
MaxStationID = 20000

#Used In Counting the number of valid files
NumberOfFiles=0

#Imports the file with station metadata into a tuple then converts to a pandas dataframe
with open("station_metadata.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file)
    station_metadata=map(tuple,csv_reader)
    
    station_metadata_df=pd.DataFrame(station_metadata, columns=["Station_ID","Latitude","Longitude","Timezone","Elevation","Device_Serial_Number","Device_ID","Device_AGL"])
    #print(station_metadata_df)
    MetaDataIDs=station_metadata_df["Device_ID"]

#Loops through all possible device ID's searching for valid stations
for fileNum in range(MaxStationID):
    
    #Makes the file names in a format usable by the exists() function ("XXX.csv")
    fileName=str(fileNum)+".csv"
    
    #Checks possible stations against actual stations going further only if a station is real
    if(path.exists(fileName)):
        #print ("file exist:"+str(path.exists(fileName))+" " +fileName)
        NumberOfFiles+=1
      
        #checks the device's ID against metadata to determine if it is an air or sky
        #i"m sure there's a better way to do this than iteratively but i'm not a CS major so this is what I know and I couldn't find an easier way in my 10 minute search
        numberofItems=station_metadata_df.count()
        for IDIndex in range(1,numberofItems[0]):
            
            if(int(MetaDataIDs[IDIndex])==fileNum):
                DeviceType=(station_metadata_df['Device_Serial_Number'].values[IDIndex])
                DeviceType=DeviceType[:2]
                
                with open(fileName,"r") as csv_file:
                    csv_reader=csv.reader(csv_file)
                    stationData=map(tuple,csv_reader)
                
                    #Splits the data input by the type of device SK or AR
                    if (DeviceType == "SK"):
                        #Time is in UTC, Lux in lx, 1 min precipitation in mm, wind in m/s, wind direction in degrees, solar radiation in W m^-2, local day precipitation accumulation in mm
                        stationDatadf=pd.DataFrame(stationData,columns=["Time","Lux","UV","1MinPrecip","WindLull","WindAvg","WindGust","WindDir","SolarRadiation","LocalDayPrecipAccum"])
                    elif(DeviceType == "AR"):
                        #Time is in UTC, pressure in mb, temp in C, rh, strike count, strike distance in km
                        stationDatadf=pd.DataFrame(stationData,columns=["Time","Pressure","Temp","rh","StrikeCount","StrikeDistance"])

                for time in range(1,stationDatadf["Time"].count()):
                    g=5 #here just to stop the ide from freaking out about my empty loop
                    #add up each column
                    #if first char in time is different print the sums and reset the adding variables
                    #i've been coding for a while and can;t really think anymore so I stop here for today
        print(stationDatadf)
                
print("There are " + str(NumberOfFiles) + " valid files")