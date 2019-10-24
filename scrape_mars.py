
import pandas as pd
import numpy as np
import requests as req
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def scrape():

    executable_path = {"executable_path": 'C:/chromedriver/chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)

# Nasa Mars News

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = req.get(url)
    soup = bs(html.text, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text

# JPL Mars Spage Images - Featured Image

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html2 = browser.html
    soup2 = bs(html2, "html.parser")
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    img_path = soup3.find('img', class_='main_image')
    img_path = img_path.get('src')
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + img_path

# Mars Weather

    t_html = req.get("https://twitter.com/marswxreport?lang=en")
    t_soup = bs(t_html.text, 'html.parser')
    t_weather = t_soup.find_all('div', class_="js-tweet-text-container")
    mars_weather = t_weather[0].text

# Mars Facts

    mars_facts = req.get("https://space-facts.com/mars/")
    mars_facts_html = pd.read_html(mars_facts.text)
    #mars_html_table = mars_facts_html[1].to_html(header=False, index=False)
    mars_html_table = mars_facts_html[1].set_index(0).to_html()
    mars_html_table = mars_html_table.replace('\n', '')

# Mars Hemispheres

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_req = req.get(usgs_url)
    browser.visit(usgs_url)
    soup = bs(usgs_req.text, "html.parser")
    hemisphere_list = soup.find_all('a', class_="itemLink product-item")


# list to keep the dictionaries that have title and image url
    hemi_links = []
    titles = []
    img_urls = []
    hemisphere_image_urls = []

    base_url = "https://astrogeology.usgs.gov"
    x = 0
    for hemi in hemisphere_list:
        time.sleep(2)
        titles.append(hemi.find('h3').text)
        hemi_links.append(base_url + hemi['href'])
        browser.visit(base_url + hemi['href'])
        img_req = req.get(base_url + hemi['href'])
        soup = bs(img_req.text, 'html.parser')
        img_div = soup.find('div', class_='downloads')
        img_url = img_div.find('a')['href']
        img_urls.append(img_url)
        hemisphere_image_urls.append(
            {"title": titles[x], "image_url": img_urls[x]})
        x += 1
        time.sleep(2)
        browser.back()

    mars_data = {
        "News_Title": news_title,
        "Paragraph_Text": news_p,
        "Mars_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts": mars_html_table,
        "Mars_Hemisphere": hemisphere_image_urls
    }

    return mars_data
