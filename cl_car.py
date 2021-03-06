#!/usr/bin/env python
# coding: utf-8

# In[29]:


#import get to call a get request on the site
from requests import get

#get the first page of the east bay cars+truck for sale by owner
response = get('https://sfbay.craigslist.org/search/eby/cto?hasPic=1') 
#URL is including post with images and sold by owner

from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')

#get the macro-container for the car cost
posts = html_soup.find_all('li', class_= 'result-row')
print(type(posts)) #to double check that I got a ResultSet
print(len(posts)) #to double check I got 120 (elements/page)


# In[30]:


#grab the first post
post_one = posts[0]


# In[31]:


#grab the price of the first post
post_one_price = post_one.a.text
post_one_price.strip()


# In[32]:


#grab the time and datetime it was posted
post_one_time = post_one.find('time', class_= 'result-date')
post_one_datetime = post_one_time['datetime']

print (post_one_time['datetime'])


# In[33]:


#title is a and that class, link is grabbing the href attribute of that variable
post_one_title = post_one.find('a', class_='result-title hdrlnk')
post_one_link = post_one_title['href']

#easy to grab the post title by taking the text element of the title variable
post_one_title_text = post_one_title.text

title_split = post_one_title_text.split() # split title by space makes in list


# In[34]:


import car_make

#removes any numbers and capitalizes first letter in each string of the title
title_holder = title_split
title_holder = [x for x in title_holder if not(x.isdigit() or x[0] == '-' and x[1:].isdigit())]
title_holder = [p.capitalize() for p in title_holder]

print (title_split)
print (title_holder)

#check car make
make_of_car_in_title = car_make.check_make(title_holder)

print (make_of_car_in_title)

import car_year_extract

#check for car year in title
car_year = car_year_extract.car_year_extractor(title_split)

print(car_year)


# In[51]:


#build out the loop for each page 
from time import sleep
import re
from random import randint #avoid throttling by not sending too many requests one after the other
from warnings import warn
from time import time
from IPython.core.display import clear_output
import numpy as np

#find the total number of posts to find the limit of the pagination
results_num = html_soup.find('div', class_= 'search-legend')
results_total = int(results_num.find('span', class_='totalcount').text) #pulled the total count of posts as the upper bound of the pages array

#each page has 119 posts so each new page is defined as follows: s=120, s=240, s=360, and so on. So we need to step in size 120 in the np.arange function
pages = np.arange(0, results_total+1, 120)

iterations = 0

post_timing = []
post_hoods = []
post_title_texts = []
car_makes = []
car_years = []
post_links = []
post_prices = []


for page in pages:
    
    #get request from pages
    response = get("https://sfbay.craigslist.org/search/eby/cto?" 
                   + "s=" #the parameter for defining the page number 
                   + str(page) #the page number in the pages array from earlier
                   + "&hasPic=1")

    sleep(randint(1,5))
     
    #throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
        
    #define the html text
    page_html = BeautifulSoup(response.text, 'html.parser')
    
    #define the posts
    posts = page_html.find_all('li', class_= 'result-row')
        
    #extract data item-wise
    for post in posts:

        if post.find('span', class_ = 'result-hood') is not None:

            #posting date
            #grab the datetime element 0 for date and 1 for time
            post_datetime = post.find('time', class_= 'result-date')['datetime']
            post_timing.append(post_datetime)

            #neighborhoods
            post_hood = post.find('span', class_= 'result-hood').text
            post_hoods.append(post_hood)

            #title text
            post_title = post.find('a', class_='result-title hdrlnk')
            post_title_text = post_title.text
            post_title_texts.append(post_title_text)
       
            splits = post_title.text.split()  
        
            #car make 
            import car_make
            parser = splits
            parser = [x for x in parser if not(x.isdigit() or x[0] == '-' and x[1:].isdigit())]
            parser = [p.capitalize() for p in parser]
            
            make_of_car_in_title = str(car_make.check_make(parser))
            car_makes.append(make_of_car_in_title)   
            
            #car year
            import car_year_extract
            
            car_year_post = car_year_extract.car_year_extractor(splits)
            car_years.append(car_year_post)
            
            #post link
            post_link = post_title['href']
            post_links.append(post_link)
            
            #removes the \n whitespace from each side, removes the currency symbol, and turns it into an int
            post_price = int(post.a.text.strip().replace("$", "").replace(",","")) 
            post_prices.append(post_price)
                  
    iterations += 1
    print("Page " + str(iterations) + " scraped successfully!")

print("\n")

print("Scrape complete!")


# In[55]:


import pandas as pd

eb_autos = pd.DataFrame({'posted': post_timing,
                       'neighborhood': post_hoods,
                       'post title': post_title_texts,
                        'Year' : car_years,
                        'Make' : car_makes,
                       'Price': post_prices,
                       'URL': post_links})

eb_autos['Make'].fillna(0)

eb_autos.head(2)


# In[82]:


#first things first, drop duplicate URLs because people are spammy on Craigslist. 
#Let's see how many uniqe posts we really have.
eb_autos = eb_autos.drop_duplicates(subset='URL')
len(eb_autos.drop_duplicates(subset='URL'))

from datetime import datetime

#convert datetime string into datetime object to be able to work with it
eb_autos['posted'] = pd.to_datetime(eb_autos['posted'])

#titlecase them
eb_autos['neighborhood'] = eb_autos['neighborhood'].str.title()

#just take the first name of the neighborhood list, splitting on the '/' delimiter
eb_autos['neighborhood'] = eb_autos['neighborhood'].apply(lambda x: x.split('/')[0])

#remove whitespaces
eb_autos['neighborhood'] = eb_autos['neighborhood'].apply(lambda x: x.strip())

#remove the parenthesis from the left and right of the neighborhoods
eb_autos['neighborhood'] = eb_autos['neighborhood'].map(lambda x: x.lstrip('(').rstrip(')'))

#saves 1st page to .csv file for review or confirmation

eb_autos.replace(to_replace='None', value=np.nan).dropna().to_csv('eb_cars_info.csv')


eb_auto_cleaned = pd.read_csv("eb_cars_info.csv")

eb_auto_cleaned.head(5)


# In[88]:


import pandas as pd, numpy as np
from matplotlib import figure
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.figure(figsize=(30, 10))
plt.hist(eb_auto_cleaned['Make'], edgecolor='white');
plt.xlabel("Make")
plt.ylabel('# of Cars')
plt.title("Distribution of Makes");

