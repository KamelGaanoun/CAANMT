# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:59:22 2023

@author: kamel
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

import re
import pandas as pd




driver=uc.Chrome(use_subprocess=True)#Launch the browser
wait=WebDriverWait(driver,20) #define the wait


pgbd='//*[@id="pagebody"]'
Sourah='/html/body/div[2]/div[2]/section/div[1]/div/div[2]/a'


#URL example
url="https://www.islamweb.net/ar/library/index.php?page=bookcontents&idfrom=450&idto=496&bk_no=209&ID=457"


#Lists initialisation
Verses_Numbers,Verses_Tafssirs,Sourah_Names=[],[],[]


##Lopping over the pages and getting elements
for seq in range(1,1748):
    url="https://www.islamweb.net/ar/library/index.php?page=bookcontents&ID="+str(seq)+"&bk_no=209&flag=1"   
    driver.get(url) 
    sleep(1)
    try:
        test=driver.find_element(By.XPATH,pgbd).text
    except:
        print('sleeping')
        sleep(2)
        driver.get(url) 
        test=driver.find_element(By.XPATH,pgbd).text
    test=test.replace('(و )','(و)')
    # define a regular expression that matches parentheses without digits
    pattern = re.compile(r'\((?![0-9])|(?<!\d)\)')
    # use sub() method to remove the matched patterns from the text
    test = pattern.sub('', test)
    test=test.replace('\n',' ')
    test=test.replace('–','-')
    sourah_name=driver.find_element(By.XPATH,Sourah).text ##Getting sourah name
    if len(Sourah_Names)==0:
        print(sourah_name)
    elif Sourah_Names[-1]!=sourah_name:
        print(sourah_name)
    
    
    #Getting verse numbers
    
    #Numbers=re.findall(r"\([\d\\)]*\)",test)
    #Numbers=re.findall(r"\([\d\\)]*\)|[\d] -|\([\d]",test)
    #Numbers=re.findall(r"[ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} -",test)
    #Numbers=re.findall(r"[ ]{0,1}\([\d \- \d\\)]* | [ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} -",test)
    Numbers=re.findall(r"[ ]{0,1}\([\d \- \d\\)]* | [ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} - \d{1,3}| \d{1,3} -",test)

    #Getting corresponding explanations
    
    #Tafssirs=re.split(r"\([\d\\)]*\)",test)[1:]
    #Tafssirs=re.split(r"\([\d\\)]*\)|[\d] -|\([\d]",test)[1:]
    #Tafssirs=re.split(r"[ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} -",test)[1:]
    Tafssirs=re.split(r"[ ]{0,1}\([\d \- \d\\)]* | [ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} -",test)[1:]
    Tafssirs=re.split(r"[ ]{0,1}\([\d \- \d\\)]* | [ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} - \d{1,3}| \d{1,3} -",test)[1:]

    Verses_Numbers.extend(Numbers)
    Verses_Tafssirs.extend(Tafssirs)
    Sourah_Names.extend([sourah_name]*len(Tafssirs))
    
  
    
  
###Some tests to recognize patterns    
test=' (8-9) very (9 is then (3 - 4) not ( 56 - 57 )  is (1 - 2   or by 10 - while the other  وأما  فلا يخلو إما أن يكون sdsd (8 - 10) also (38) and then (4 and the 168 - 170 ) while (و ) is (3 - 4  last one  '.replace('(و )','(و)') 
test=test.replace('–','-')
re.findall(r"[ ]{0,1}\([\d \- \d\\)]* | [ ]{0,1}\([\d \- \d\\)]*\) | [ ]{0,1}[\d \- \d\\)]*\) | \([\d\\)]*\) | \(\d{1,3} | \d{1,3} - \d{1,3}| \d{1,3} -",test)

re.findall(r"[ ]{0,1}\([\d \- \d\\)]*",test)
   
           
SaadiDf8=pd.DataFrame({'Verse_Number':Verses_Numbers,'Verse_Tafssir':Verses_Tafssirs,'Sourah':Sourah_Names})


SaadiDf8_1=SaadiDf8.copy()
SaadiDf8_1['Verse_Number']=SaadiDf8.Verse_Number.apply(lambda x: re.sub('[()]', '', x).replace(' ',''))
SaadiDf8_1['Sourah']=SaadiDf8_1.Sourah.apply(lambda x: x.replace('تفسير سورة','').replace(' ',''))


SaadiDf8_1['duplicated'] = SaadiDf8_1.duplicated(subset=['Verse_Number','Sourah'],keep=False)

###################################################################################################################
#Manually changed 1- and 2- for surah Youssouf 

#Duplicated verse numbers analysis:
## Baqara, 143 : it is the same verse continued  --> to join the Tafssirs
## Youssouf, 78: the second one is actually 79   --> to correct     
## Kahf, 8: the second one is actually  9        --> to correct  
## Kahf, 34 : it is the same verse continued     --> to join the Tafssirs
## Kahf, 99 : it is the same verse continued     --> to join the Tafssirs  
## Maryam, 8: the second one is actually  9      --> to correct  
## Anbia, 27: the first one is actually  26      --> to correct  
## Hajj, 8: the second one is actually  9        --> to correct  
## Hajj, 70: the second one is actually  71      --> to correct 
## Mouminoun, 8: the second one is actually  9   --> to correct  
## Mouminoun, 70: the second one is actually  71 --> to correct 
## Ashouara, 8: the second one is actually  9    --> to correct  
## An-naml, 6: the second one is actually  16    --> to correct  
## An-naml, 8: the second one is actually  9    --> to correct  

SaadiDf8_2=SaadiDf8_1.copy()
SaadiDf8_2 = SaadiDf8_2.drop_duplicates(subset=['Verse_Number','Sourah'],keep='first').sort_index().drop(columns=['duplicated'])




SaadiDf8_3=SaadiDf8_2.copy()


filter = SaadiDf8_3['Verse_Number'].str.contains("-")

SaadiDf8_3=SaadiDf8_3[~filter]

#Corrected duplicated verse numbers: example 8 twice on sourah  --> second 8 is actually Verse number 9

#Remains joined tafssirs like 8-9, 100-102, etc. :
## Option1 : Remove all joined tafssirs (Saadi_cleaned2)
## Option2 : Keep them and join Verses from the Verses dataset and consider joined tafssirs for joined verses (Saadi_cleaned1)   

## Adopt sourah names to comply to parallel dataset---> Example : sourah Moahammad = Sourah al9ital
##########################################################################################################################


SaadiDf8_3.to_csv('C:/Kamel/IslamicNLP/ContextAwareTranslationArabic/Saadi_cleaned2.tsv',sep='\t',index=None)


SaadiDf6=pd.read_csv('C:/Kamel/IslamicNLP/ContextAwareTranslationArabic/Saadi.tsv',sep='\t')



