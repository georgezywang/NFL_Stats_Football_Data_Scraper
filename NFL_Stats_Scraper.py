#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:52:17 2019

@author: wzy
"""

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np

def getdataNFLStats(url, ODtype):
    #obtain raw data
    req=Request(url, headers={'User-Agent': 'Chrome/11.0'})
    page = urlopen(req).read()
    page_soup = soup(page, 'html.parser')
    odd=page_soup.find_all('tr',{'class':'odd'})
    even=page_soup.find_all('tr',{'class':'even'})
    
    rows = odd + even
    alldata=[]
    if ODtype == 'D':
        length = 20
    else:
        length = 21
    for i in range(length):
        alldata.append([])
    
    for row in rows:
        data=row.find_all('td')
        alldata[0].append(re.search(r"[-+]?\d*\.?\d+|\d+", str(data[0])).group())
        alldata[1].append(str(data[1]).split(">")[2].split("<")[0])
        for i in range(2,length):
            alldata[i].append(str(data[i]).replace("\t","").replace("\n","").split('>')[1].split('<')[0])
    return alldata

def generalNFLyearrange(startyear,endyear,place):
    if place!='D'and place!='O':
        print('error input type')
        return(0)
    alldat=[]
    for i in range(startyear,endyear+1):
        if place == 'D':
            print("---------"+"retrieving defense data of year " + str(i)+'---------')
            url='http://www.nfl.com/stats/categorystats?archive=true&conference=null&role='\
            +'OPP&offensiveStatisticCategory=null&defensiveStatisticCategory=GAME_STATS&season='\
            +str(i)+'&seasonType=REG&tabSeq=2&qualified=false&Submit=Go'
            dat=getdataNFLStats(url,'D')
        else:
            print("---------"+"retrieving offense data of year " + str(i)+'---------')
            url='http://www.nfl.com/stats/categorystats?archive=true&conference=null&role='\
            +'TM&offensiveStatisticCategory=GAME_STATS&defensiveStatisticCategory=null&season='\
            +str(i)+'&seasonType=REG&tabSeq=2&qualified=false&Submit=Go' 
            dat=getdataNFLStats(url,'O')
        alldat.append(dat)
    return alldat

def sortNFLdata(startyear,endyear,place):
    #reshape the data
    alldat=generalNFLyearrange(startyear,endyear,place)
    years=endyear-startyear+1
    sorteddata=[]
    for i in range (len(alldat[0])):
        sorteddata.append([])
        
    for i in range(years):
        data_year=alldat[i]
        for j in range(len(alldat[0])):
            for k in range(len(alldat[0][0])):
                sorteddata[j].append(data_year[j][k])
    return sorteddata

def NFL2df(sorteddata, place):
    if place!='D'and place!='O':
        print('error input type')
        return(0)
    if place == 'O':
        df=pd.DataFrame(np.array(sorteddata).transpose(), columns=['Rank','Team','Games','ptsPg',\
                        'totalpt','Scrm Plys','yds/g','yds/p','1st/G','3rd MD', '3rd Att','3rd Pct'\
                        '4rd MD', '4rd Att','4rd Pct','Pen','Pen Yds	','ToP/G','Fum','Lost','TO'])
    else :
        df=pd.DataFrame(np.array(sorteddata).transpose(), columns=['Rank','Team','Games','ptsPg',\
                        'totalpt','Scrm Plys','yds/g','yds/p','1st/G','3rd MD', '3rd Att','3rd Pct'\
                        '4rd MD', '4rd Att','4rd Pct','Pen','Pen Yds	','ToP/G','Fum','Lost'])
    return df

def writefile(data,filename):
    print('Writing file: '+filename)
    data.to_csv(filename+'.csv',index=False)
    
sorteddataO=sortNFLdata(2005,2019,'O')
writefile(NFL2df(sorteddataO,'O'),'NFL_Stats_fifteen_yearsO')
sorteddataD=sortNFLdata(2005,2019,'D')
writefile(NFL2df(sorteddataD,'D'),'NFL_Stats_fifteen_yearsD')