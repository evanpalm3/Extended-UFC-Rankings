import requests
from bs4 import BeautifulSoup

page_to_scrape = requests.get("http://www.ufcstats.com/statistics/events/completed?page=all")
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

links=[]
for link in soup.findAll("a", attrs={"class":"b-link b-link_style_black"}):
    links.append(link.get("href"))

fights=[]
num=0
for link in links:
    num+=1
    print(str(num)+" of "+str(len(links)))
    page_to_scrape = requests.get(link)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    date = soup.find("div", attrs={"class":"b-list__info-box b-list__info-box_style_large-width"}).text.split('\n')[6].strip()
    rows = soup.findAll("tr", attrs={"class":"b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"})
    for row in rows:
        parts = row.findAll("p", attrs={"class":"b-fight-details__table-text"})
        text=[]
        for part in parts:
            text.append(part.text)
        result="win"
        if(len(text)==17):
            result="draw"
            text.remove(text[0])
        fighter1=text[1].strip()
        fighter2=text[2].strip()
        weightclass=text[11].strip()
        entry=[fighter1,fighter2,weightclass,result,date]
        fights.append(entry)
        
file = open('fights.txt', mode='w')
for fight in fights:
    for part in fight:
        file.write(part+"*")
    file.write("\n")
file.close()
print("done")

