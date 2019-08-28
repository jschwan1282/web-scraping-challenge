#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":r"C:\Users\Jay\Desktop\personal\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    #set url to NASA Mars news
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape site for title and paragraph
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_ ="article_teaser_body").text
    print(news_title)
    print(news_p)

    #set url to JPL NASA images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape site for image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)

    #set url to Twitter
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape site for weather data
    tweet_xpath = '//*[@id="stream-item-tweet-1164580812664332289"]/div[1]/div[2]/div[2]/p'
    mars_weather = browser.find_by_xpath(tweet_xpath).text
    print(mars_weather)

    #set url to Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html
    soup = bs(html, "html.parser")

    #scrape site for Mars Facts
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    print(mars_facts)

    #Set url to Astrogeology site
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")

    #Create empty dictionary
    hemisphere_image_urls  = []

    #Point to hamisphere product block
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    #loop through each of the hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    #Close the browser after scraping
    browser.quit()

    #Return data
    return mars_data