from datetime import date

#number of days away from sport to be considered retired and removed from rankings
retirement=800

divisions = ['Flyweight','Bantamweight','Featherweight','Lightweight','Welterweight','Middleweight','Light Heavyweight','Heavyweight',     
              "Women's Strawweight","Women's Flyweight",  "Women's Bantamweight", "Women's Featherweight", 'Super Heavyweight', 'Open Weight', 'Catch Weight']
months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#datetime.date(year, month, day)
getMonth={}
for i in range(12):
    getMonth[months[i]]=i+1
    getMonth[months[i][0:3]]=i+1

def convertDate(d):
    parts=d.split(' ')
    parts[1] = parts[1].replace(',','')
    return date(int(parts[2]),getMonth[parts[0]],int(parts[1]))

fights={}
for d in divisions:
    fights[d]=[]

lines = open('fighters.txt', 'r').readlines()
dob = {}
for line in lines:
    parts = line.split('*')
    if(parts[1]!='--'):
        parts[1]=convertDate(parts[1])
    dob[parts[0]]=parts[1]

def getAge(fighter,fightNight):
    return int((fightNight-dob[fighter]).days/365.25)

activity={}
lines = open('fights.txt', 'r').readlines()
fightList=[]
for line in lines:
    parts = line.split('*')
    parts.remove(parts[5])
    parts[4]=convertDate(parts[4])
    fightList.append(parts)
    for p in [parts[0],parts[1]]:
        if p not in activity:
            activity[p]=[parts[4],parts[4]]
        else:
            a=activity[p]
            if(parts[4]<a[0]):
                a[0]=parts[4]
            elif(parts[4]>a[1]):
                a[1]=parts[4]
lastUpdated = fightList[0][4]

def getDivision(name, index):
    for i in range(index, len(fightList)):
        fight = fightList[i]
        if((fight[0]==name or fight[1]==name) and fight[2]!='Catch Weight'):
            return fight[2]
    return 'Catch Weight'

num=0
for fight in fightList:
    if(fight[2]=='Super Heavyweight'):
        fight[2]='Heavyweight'
    elif(fight[2]=='Catch Weight'):
        fight[2] = getDivision(fight[0],num)
        if(fight[2]=='Catch Weight'):
            fight[2] = getDivision(fight[1],num)
            if(fight[2]=='Catch Weight' and num-600>-1):
                fight[2] = getDivision(fight[0],num-600)
    fights[fight[2]].append(fight)
    num+=1

divisions.remove('Catch Weight')
divisions.remove('Super Heavyweight')
divisions.remove('Open Weight')
divisions.remove("Women's Featherweight")

rankings={}
for d in divisions:
    fights[d].reverse()
    ranking=[]
    lastDate=fights[d][0][4]
    for fight in fights[d]:
        if(lastDate!=fight[4]):
            lastDate=fight[4]
            for p in ranking:
                if((fight[4]-activity[p][1]).days>=retirement):
                    ranking.remove(p)
        for p in [fight[0],fight[1]]:
            if p not in ranking:
                ranking.append(p)
        if(fight[3]=='draw'):
            continue
        if(ranking.index(fight[0])>ranking.index(fight[1])):
            ranking.remove(fight[0])
            ranking.insert(ranking.index(fight[1]), fight[0])
    rankings[d]=ranking

file=open('rankings.csv','w')
length=0
for d in divisions:
    length=max(length,len(rankings[d]))
    file.write(d+',')
file.write('\n')
for k in range(length):
    for d in divisions:
        if(k<len(rankings[d])):
            file.write(rankings[d][k])
        file.write(',')
    file.write('\n')
file.close()

