

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
# Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_image(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try: 
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None
    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None

# Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

# ## Mars Facts

def mars_facts():

    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.head()

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    df

    return df.to_html(classes='table table-striped table-hover', header = "true", justify = "center")
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


def hemisphere_image(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(0,4):
        hemispheres = {}
        #find the title in h3
        title = browser.find_by_tag('h3')[i].text
        #click the image
        to_url = browser.find_by_css('img.thumb')[i]
        to_url.click()

        #in new page
        html = browser.html
        img_soup = soup(html, 'html.parser')
        tmp_url = []
        # find the relative image url
        for a in img_soup.find_all('a', target='_blank', href=True):
            tmp_url.append(a['href'])
        #the url is always the 3rd element
        img_url_rel = tmp_url[2]
        # Use the base url to create an absolute url, and create the dictionary
        hemispheres['img_url']= f'https://marshemispheres.com/{img_url_rel}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

print("----done----")






