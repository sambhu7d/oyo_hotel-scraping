#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 00:39:30 2020
@author: sambhu7
"""

from selenium import webdriver
import pandas as pd
import time
import bs4

list_=[]

page=input('Input Number of Page ')


for o in range(1,int(page)+1):
    
    path='/Users/sambhu7/Downloads/chromedriver'
    url='https://www.oyorooms.com/hotels-in-goa/?page='+str(o)
    
    driver=webdriver.Chrome(executable_path=path)
    driver.maximize_window()
    time.sleep(2)
    driver.get(url)
    ps=driver.page_source
    soup=bs4.BeautifulSoup(ps,'html.parser')
    
   
    
    hotel=soup.select('div.oyo-row.oyo-row--no-spacing.listingHotelDescription>div.oyo-cell--12-col.listingHotelDescription__content>div.listingHotelDescription__contentWrapper')#'>div.listingHotelDescription__contentWrapper--left.u-fullWidth')#'>a.link.u-width100')
    rating=soup.select('div.oyo-row.oyo-row--no-spacing.listingHotelDescription>div.oyo-cell--12-col.listingHotelDescription__content>div.hotelRating')#'>div.hotelRating__wrapper')
    price=soup.select('div.oyo-row.oyo-row--no-spacing.listingHotelDescription>div.oyo-cell--12-col.listingHotelDescription__priceBtn>div.oyo-row.oyo-row--no-spacing>div.oyo-cell--5-col>div.listingPrice>div.listingPrice__numbers>span.listingPrice__finalPrice')
    
    ls=[]
    
    for i in range(len(hotel)): 
        rate=rating[i].get_text()[:3]
        try:
            rate=float(rate)
            ls.append([rate, rating[i].get_text(),hotel[i].get_text(),price[i].get_text()])
        except:
            pass
                  
    
    for i in ls:
        data=i[1]
        people=data[5:10]
        p=''
        for j in people:
            if ord(j)==32:
                break
            else:
                p+=j
                
        i.insert(1,int(p))
        
    for i in ls:
        data=i[2]
        review=data
        l=len(review)
        p=''
        for j in range(l):
            if ord(review[j])==41:
                p=review[j+2:]
                break
        
                
        i.insert(2,p)
        del i[3]
        
    for i in ls:
        list_.append(i)
    driver.close()
       
             
df=pd.DataFrame(list_, columns =['Rating', 'People', 'Review','Name','Price']) 
df=df.sort_values(by=['Rating', 'Price' ,'People',],ascending=False)
df = df.reset_index(drop=True)
df.index+= 1  
df.to_csv('result.csv', index_label='Event_id')