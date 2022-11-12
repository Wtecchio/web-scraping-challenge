#imports
#import splinter, soup and chrome driver
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


#scrape all function

def scrape_all():

    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False) #my path didn't work on here or on jupyter :/
    browser = Browser('chrome', headless=False)


    #return a json with all data to load to Mongo


    #get information from pages
    news_title, news_paragraph = scrape_news(browser)

    #build a dictionary using the infromatoin from the scrapes
    marsData = {
        "newsTitle" : news_title,
        "newsParagraph" : news_paragraph,
        "featuredImage" : scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres" : scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    #stop webdriver
    browser.quit()

    #display output
    return marsData





#scrape the mars news page
def scrape_news(browser):
    #go to mars news site first
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #delay
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    #get title
    news_title = slide_elem.find('div',class_='content_title').get_text()
    #get paragraph headline
    news_p = slide_elem.find('div',class_='article_teaser_body').get_text()

    #return the title and paragraph
    return news_title,news_p

#scrape through the featured image page
def scrape_feature_img(browser):
    #visit URL to website 
    url='https://spaceimages-mars.com'
    browser.visit(url)

    #find and locate the full image button to be able to scrape it
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    #Filter through the resulting html with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')

    #find image url
    image_url_rel = image_soup.find('img', class_='fancybox-image').get('src')

    #absolute url
    image_url = f'https://spaceimages-mars.com/{image_url_rel}'

    return image_url

#scrape through the facts page
def scrape_facts_page(browser):
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)

    #parse html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #find the facts location
    factsLocation = fact_soup.find('div',class_="diagram mt-4")
    factTable = factsLocation.find('table') #grab html code from the table

    #creat an empty string
    facts =""

    #add text to eht string then return

    facts += str(factTable)

    return facts #all I be returning honestly

#scrape through the hemisphere pages
def scrape_hemispheres(browser):
    #base url

    url = "https://marshemispheres.com/"
    browser.visit(url)

    #Create list to store images and titles
    hemisphere_image_urls = []

    #loop
    for i in range(4):
        #loops through all pages
        #hemisphere info dictionary
        hemisphereInfo = {}
    
    
        #find the elements on each loop to avoid a stale element
        browser.find_by_css('a.product-item img')[i].click()
    
        #find the image anchor tag and take href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']
    
        #Get Hemipshere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
    
    
     #Appened object to list
        hemisphere_image_urls.append(hemisphereInfo)
    
        #navigate back to the top to reset loop and get next data
        browser.back()

    #return the hemispheres urls with the titles
    return hemisphere_image_urls



#set up as a flask app

if __name__ == "__main__":
    print(scrape_all())