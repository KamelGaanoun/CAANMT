import pandas as pd
import numpy as np
import re

DataPath="C:/Kamel/IslamicNLP/ContextAwareTranslationArabic/"



##Parallel Arabiv-English Quran (with 7 translations)
ParallelData=pd.read_csv(DataPath+"QuranCorpusEnglishFinal.csv")

##Saadi Data: Option1=Without joined tafssirs  Option2=including joined tafssirs
SaadiOption1=pd.read_csv(DataPath+"Saadi_cleaned2.tsv",sep='\t')
SaadiOption2=pd.read_csv(DataPath+"Saadi_cleaned1.tsv",sep='\t')


## Sourah name adaptation
ParallelData['Sourah']=ParallelData.Sourah_Ar.apply(lambda x: x.replace('سورة','').replace(' ',''))


#remove Sourah An'Nas as it is not including tafssir
SaadiOption1=SaadiOption1[SaadiOption1.Sourah!='الناس']
SaadiOption2=SaadiOption2[SaadiOption2.Sourah!='الناس']

#Rename bara'a to tawba in Saadi
SaadiOption1['Sourah']=SaadiOption1.Sourah.apply(lambda x: x.replace('براءة','التوبة'))
SaadiOption2['Sourah']=SaadiOption2.Sourah.apply(lambda x: x.replace('براءة','التوبة'))
## Get rid of hamza in Saadi Sourah names
SaadiOption1['Sourah']=SaadiOption1.Sourah.apply(lambda x: re.sub("[إأٱآا]", "ا", x))
SaadiOption2['Sourah']=SaadiOption2.Sourah.apply(lambda x: re.sub("[إأٱآا]", "ا", x))

#removing non scrapped Sourah from Parallel dataset

#Parallel Dataset Sourahs
ParallelSourahs=set(list(ParallelData.Sourah.unique()))
len(ParallelSourahs) #114
#Saadi Sourahs
SaadiSourahs=set(list(SaadiOption1.Sourah.unique()))
len(SaadiSourahs)   #37


#Check if we get the 114-37=  77 missing Sourahs 
MissingSourahs=ParallelSourahs-SaadiSourahs
len(MissingSourahs) #77  Bingo

ParallelData=ParallelData[ParallelData.Sourah.isin(SaadiSourahs)]

ParallelSourahs2=set(list(ParallelData.Sourah.unique()))
len(ParallelSourahs2) #37


#Number of verses 
SaadiOption1.shape[0]  # 2908 Verse
ParallelData.shape[0]  # 3970 Verse
##Only 3970 - 2908 =  1062 missing Verses (knowing that joined tafssirs are not included in SaadiOption1)

ParallelData.rename(columns={'Verse_number':'Verse_Number'},inplace=True)
SaadiOption1['Verse_Number']=SaadiOption1['Verse_Number'].astype(np.int64)


#Merge SaadiOption1 with ParallelData
SaadiParallel1=ParallelData.merge(SaadiOption1,how='right',on=['Sourah','Verse_Number'])
###SaadiParallel1 : Parallel Quran with translations and tafssirs, without joined verses/tafssirs


###Merge with SaadiOption2 (including joined tafssirs)###

#1. Detect joined verses on SaadiOption2
#2. Join them in the parallel Data
#3. Merge both


joinedVerses=SaadiOption2[SaadiOption2.Verse_Number.str.contains('-')]


ParallelDataJoin=ParallelData.copy()
JoinVersesDF=pd.DataFrame()

joinedVerses=joinedVerses[['Verse_Number','Sourah']]
joins=list(zip(joinedVerses.Verse_Number,joinedVerses.Sourah))


for elm in joins:
    #print(numbers_join,sourah)
    numbers_join=elm[0]
    numbers=[int(element) for element in numbers_join.split('-')]  
    sourah=elm[1]
    #Get current joined verses in Parallel Data and create a filter on them
    JoinFilter=ParallelDataJoin[(ParallelDataJoin.Verse_Number.isin(numbers) ) & (ParallelDataJoin.Sourah==sourah) ] 
    #Concat filtered Verses
    JoinVerses=JoinFilter.groupby(['Sourah','Sourah_number'],as_index=False)['Verse'].apply(' '.join)#.to_frame()
    JoinVersesSahih=JoinFilter.groupby(['Sourah'],as_index=False)['Sahih_int'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesPick=JoinFilter.groupby(['Sourah'],as_index=False)['Pickthall'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesYA=JoinFilter.groupby(['Sourah'],as_index=False)['YA'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesSh=JoinFilter.groupby(['Sourah'],as_index=False)['Shakir'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesMS=JoinFilter.groupby(['Sourah'],as_index=False)['MS'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesMK=JoinFilter.groupby(['Sourah'],as_index=False)['MK'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVersesAR=JoinFilter.groupby(['Sourah'],as_index=False)['Arberry'].apply(' '.join).drop(columns=['Sourah'])#.to_frame()
    JoinVerses=pd.concat([JoinVerses,JoinVersesSahih,JoinVersesPick,JoinVersesYA,JoinVersesSh,JoinVersesMS,JoinVersesMK,JoinVersesAR],axis=1)
    #Set Verse_Number to joined number
    JoinVerses['Verse_Number']=numbers_join
    #Append crated joined verses
    JoinVersesDF=JoinVersesDF.append(JoinVerses)
    #Remove joined rows from ParallelData
    ParallelDataJoin=ParallelDataJoin[ParallelDataJoin.apply(lambda x: (x['Verse_Number'] not in numbers) or (x.Sourah!=sourah) ,axis=1) ]


SaadiParallel2=ParallelDataJoin.append(JoinVersesDF)
###SaadiParallel2 : Parallel Quran with translations and tafssirs, With joined verses/tafssirs/Translations

SaadiParallel1.to_csv(DataPath+'SaadiParallelWithoutJoined.csv',sep='\t',index=None)
SaadiParallel2.to_csv(DataPath+'SaadiParallelWithJoined.csv',sep='\t',index=None)
