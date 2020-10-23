import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib
import os


url = 'https://unsplash.com/search/photos/'

links = []
titles = []
credits_list = []

#----------------DOWNLOAD FUNCTION--------------


def download(links, keywords,titles):

    # creates a folder in the current directory with name as same as search input
    folder = os.path.join(os.getcwd(),keywords)
    if not os.path.exists(folder):
	    os.makedirs(folder)	
    
    # loop to download the photos
    i = 0 #iterator
    downloaded = 1 #downloads counter // set to 1 since to be subtracted
    for imgs in links:
        # creates name of photo
        img_path = str(i+1) + '- ' + titles[i] + '.jpg'
        name = os.path.join(folder,img_path)
        #download function using urllib.request
        urllib.request.urlretrieve(imgs, name)
        print('photo ' + str(i+1) + ' downloaded')
        print('no. of photo(s) remaining:' + str(len(links)-downloaded))
        downloaded += 1
        # adds "{authorname} : {link to the photo}" to a list
        credits_list.append(titles[i] + " : " + imgs.replace('download?force=true','') + '\n')
        
        i += 1

    # creates a credit file adding credits_list items to lines.
    credits = open(os.path.join(folder,'credits.txt'),'w')
    credits.writelines(credits_list)
    credits.close()


#---------------SCRAPER FUNCTION--------------

def scraper(url,keywords):
    
    # get the page as string
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print ('Error! \n More details:')
        print (e)
        exit()
    
    # html parser using bs4
    soup = BeautifulSoup(page.text, 'html.parser')
    

    # input for number of photos
    quantity = int(input('how many photos: '))

    # creates a list of links of photos to download
    img_list = soup.find_all('a', {'title': 'Download photo'}, limit = quantity)
    for i in range(0,len(img_list)):
        links.append(img_list[i].get('href'))

    # creates a list of links of authors of the photos to be downloaded
    author_list = soup.find_all('a', {'itemprop': 'contentUrl'}, limit = quantity)
    for i in range(0,len(author_list)):
        author_name = author_list[i].get('title')
        titles.append(author_name.replace('View the photo by ',''))


    download(links,keywords,titles)


#-----------SEARCH FUNCTION------------

def search():

    # take input of types of photos required
    keywords = input('enter search: ')
    link = url + keywords.replace(' ','-')


    scraper(link,keywords.replace(' ','-'))


if __name__ == "__main__":
    search()