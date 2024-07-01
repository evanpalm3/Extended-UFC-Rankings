import requests
from bs4 import BeautifulSoup

fighters=[]
for i in range(ord('a'), ord('z')+1):
    print("loading names and DOB for "+chr(i))
    page_to_scrape = requests.get("http://www.ufcstats.com/statistics/fighters?char="+chr(i)+"&page=all")
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    rows = soup.findAll("tr", attrs={"class":"b-statistics__table-row"})
    num=0
    for row in rows:
        if(num<2):
            num+=1
            continue
        parts = row.text.split('\n')
        name = (parts[2]+" "+parts[5]).strip()
        link = row.find("a", attrs={"class":"b-link b-link_style_black"}).get("href")
        fightPage = requests.get(link)
        soup2 = BeautifulSoup(fightPage.text, "html.parser")
        info = soup2.find("div", attrs={"class":"b-list__info-box b-list__info-box_style_small-width js-guide"})
        parts = info.text.split('\n')
        k=len(parts)==36
        dob=parts[30+k].strip()
        fighters.append([name,dob])
        
file = open('fighters.txt', mode='w')
for fighter in fighters:
    for part in fighter:
        file.write(part+"*")
    file.write("\n")
file.close()
print("done")
