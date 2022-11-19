# dowloadMangafreak.py - Downloads Manga as you want

import sys,os,requests #sys for read arguments || os for create directory || requests mainly to checkout connection
from selenium import webdriver
from selenium.webdriver.common.by import By

#Setting up webdriver
browser = webdriver.Chrome(executable_path=r'C:\Users\nvdun\Downloads\chromedriver_win32\chromedriver.exe')     # initiate 2 browser entities one for scraping number of chapters
mangaPage = webdriver.Chrome(executable_path=r'C:\Users\nvdun\Downloads\chromedriver_win32\chromedriver.exe')   # the other to scrape the images of each chapter

#Create the right name
mangaName = sys.argv[1:]                                                        # getting the arguments
for i in range(len(mangaName)):                                                 # forming the name in align with mangafreak name scheme 
    mangaName[i] = mangaName[i].capitalize()
    searchManga = '_'.join(mangaName)

#Create parent directory
directory = searchManga                                                         # initiate the parents directory
parent_dir = r'C:\Users\nvdun\OneDrive\Manga'
path = os.path.join(parent_dir, directory)
os.makedirs(path,exist_ok=True)

#TODO: Scoll through all the chapters

linkManga = ('https://w13.mangafreak.net/Read1_'+ searchManga +'_1')            # fed in the 1st chapter of the manga to get the list of manga
res = requests.get(linkManga)                                                   # checking the availibility of the linkManga
print(res.raise_for_status())
browser.get(linkManga) 
chapters = browser.find_elements(By.CSS_SELECTOR, 'select > option')            # get the list of chapters

for i in range(len(chapters)-1):                                                    #to change to len(chapters) to download the whole manga
    linkManga=('https://w13.mangafreak.net' + chapters[i].get_attribute('value'))   #loop through all chapters for download
    chapterPath = os.path.join(path,os.path.basename(linkManga))
    os.makedirs(chapterPath,exist_ok=True)                                          #Create the chapter directory
    print('Downloading ...' + chapterPath)
    mangaPage.get(linkManga)                                                        #Browse the chapter page

#TODO: Locate the image
    image = mangaPage.find_elements(By.ID, 'gohere')                                #Locate the element that holds pictures sources
#TODO: Download the image
    if image == []:                                                 
        print('Error')
    else:
        for a in range(len(image)):                     
            imageSrc = image[a].get_attribute('src')                                #Get sources link
            res = requests.get(imageSrc)
            res.raise_for_status
#TODO: Save the image to created directory
            imageFile = open(os.path.join(chapterPath,os.path.basename(imageSrc)),'wb') #Create file to save the pictures
            for chunk in res.iter_content(100000):                                          
                imageFile.write(chunk)
            imageFile.close()
browser.close()
print('Done')
