from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import string
import cgitb
cgitb.enable()

class item:
    title = ""
    link = ""
    image = ""
    def __init__(self, title, link, image):
        self.title = title
        self.link = link
        self.image = image

items = [item]
titles = []
links = []
images = {}

file = "movie.txt"
f = open(file, "w")

def setup():
    url = 'http://www.shaw.sg/sw_buytickets.aspx?CplexCode=&FilmCode=&date=11/6/2017'
    uClient = urlopen(url)
    pageHtml = uClient.read()
    uClient.close()

    page_soup = soup(pageHtml, "html.parser")

    dateList = page_soup.find("select", {"name" : "ctl00$Content$ddlShowDate"})

    dates = dateList.findAll("option")

    datesArr = []

    global titles
    global links

    for x in dates :
        datesArr += [x['value']]

    file = "movie.txt"
    f = open(file, "w")

    movies = page_soup.findAll("tr", {"class" : "NORM"})

    for m in movies :
        title = m.find("a", {"class" : "txtSchedule"}).text
        if title not in titles:
            titles += [title]
            link = m.find("a", {"class" : "txtSchedule"})['href']
            links += [link.replace(" ", "%")]

    f.close()
    return

def getImages():
    url = 'http://www.shaw.sg/sw_movie.aspx'
    uClient = urlopen(url)
    pageHtml = uClient.read()
    uClient.close()

    page_soup = soup(pageHtml, "html.parser")

    global images

    movies = page_soup.findAll("table", {"class" : "panelMovieListRow"})

    for m in movies :
        detail = m.findAll("td")
        images[detail[1].a.text] = detail[0].a.img['src']

def main(x):
    setup()
    getImages()
    for x in range(0, len(titles)):
        items += [item(titles[x], links[x], images[titles[x]])]

    for x in items:
        f.write(x.title + "\n" + x.link + "\n" + x.image + "\n\n")

    f.close()
    print(x)
    return x

if __name__ == "__main__":
    x = main(10)
    return x;
