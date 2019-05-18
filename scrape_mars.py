from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "C:\chromedrv\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='content_title').find('a').text
    paragraph = soup.find('div', class_='article_teaser_body').text

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    articles = soup2.find('a', class_ = 'fancybox')
    href = articles['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + href

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')
    div = soup3.find('div', class_ = "js-tweet-text-container")
    mars_weather = div.find('p', "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather = mars_weather.replace('.twitter.com/qtElTnSRJj', '')

    url23 = "https://space-facts.com/mars/"
    table = pd.read_html(url23)
    mars_df = table[0]
    mars_df.columns =['Features', 'Measurement'] 
    mars_df.set_index("Features", inplace = True)
    mars_html = mars_df.to_html()
    mars_html = mars_html.replace('\n', '')

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html4 = browser.html
    soup4 = BeautifulSoup(html4, 'html.parser')
    links = []
    titles= []
    results = soup4.find_all('div', class_='item')
    for result in results:
        titles.append(result.find('h3').text)
        website = result.find('a', class_ = 'itemLink product-item')['href']
        url5 = "https://astrogeology.usgs.gov" + website
        browser.visit(url5)
        html5 = browser.html
        soup5 = BeautifulSoup(html5, 'html.parser')
        links.append('https://astrogeology.usgs.gov' + soup5.find('img', class_ = 'wide-image')['src'])
    hemisphere_image_urls = []    
    for x in range(4):
        hemisphere_image_urls.append({"title": titles[x], "image_url": links[x]})


    mars_data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_html": mars_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    browser.quit()

    return mars_data