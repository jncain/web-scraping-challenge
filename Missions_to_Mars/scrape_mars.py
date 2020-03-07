# Import dependencies
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/bin/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### 
    # NASA Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(5)
    news_html = browser.html
    # Parse site with beautifulsoup
    news_soup = bs(news_html, 'html.parser')
    # Find the latests News Title and paragraph text and save as variable
    article = news_soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text
    ###

    ### 
    # JPL Images
    jpl_mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_mars_url)
    time.sleep(2)
    # Click 'full image' button to go to image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    # Click 'more info' button to go to full size image
    browser.click_link_by_partial_text('more info')
    # Parse html via Beautiful Soup
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    #Saving image source
    image_path = image_soup.find_all('img', class_="main_image")[0]["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{image_path}'
    ###

    ###
    # Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(8)
    weather_html = browser.html
    # Parse html with BS
    weather_soup = bs(weather_html, 'html.parser')
    # Extract tweet
    tweet_container = weather_soup.find(attrs={"data-testid": "tweet"})
    tweets = tweet_container.text
    # Saving tweet as variable
    weather_tweets = tweets.split("InSight ")
    mars_weather = weather_tweets[1]
    ###

    ###
    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    # Extract table
    table = pd.read_html(facts_url)
    mars_facts = table[0]
    mars_facts.columns = ["Fact", "Value"]
    # Convert to HTML table string
    mars_facts = mars_facts.to_html(index=False, classes="table table-striped", justify="left")
    ###

    ###
    # Mars Hemispheres
    mars_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_url)
    mars_hemi_html = browser.html
    # Parser HTML with BS
    mars_hemispheres_soup = bs(mars_hemi_html, 'html.parser')
    # Creating list to store data
    hemisphere_image_urls = []
    # Getting all elements
    results = mars_hemispheres_soup.find_all('div', class_="item")
    for result in results:
        # saving image title
        title = result.find('h3').text
        title = title.replace("Enhanced", '')
        # navigating for full image and setting up HTML parser
        click_link = result.find('a')['href']
        image_link = "https://astrogeology.usgs.gov" + click_link
        browser.visit(image_link)
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, 'html.parser')
        # saving image urls
        links = hemi_soup.find('div', class_="downloads")
        img_url = links.find('a')['href']
        # appending list
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    ###

    ###
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "mars_hemispheres": hemisphere_image_urls 
    }

    # close browser
    browser.quit()
    # return results
    return mars_data


