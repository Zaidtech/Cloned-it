# from pywebcopy import save_webpage
import requests
import os
from flask import Flask , render_template, request
from selenium import webdriver
import time
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import re
import datetime
import random


PATH = '/home/zaid/Desktop/WatsApp-Predictor/WatsApp Project/geckodriver-v0.27.0-linux64/geckodriver'

path = os.path.dirname(__file__)
print(path)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/main" ,methods=["POST"])
def main():
    fox = webdriver.Firefox(executable_path=PATH)
    url = request.form.get("url")
    fox.get(url)
    # try to find a way to hide the above open window
    time.sleep(10)
    i = 0
    while True:
        page = fox.page_source
        with open(f"./templates/cloned0.html", 'w') as f:
            f.write(page)
        # the above page is the source of html 
        # parsing thos page into the bs4obj
        # print(page)
        random.seed(datetime.datetime.now())
        internalLinks = []
        externalLinks = []
        
        #Retrieves a list of all Internal links found on a page
        def getInternalLinks(bsObj, includeUrl):
            random.seed(datetime.datetime.now())    
        #Finds all links that begin with a "/" ie the internal links 
            for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
                if link.attrs['href'] is not None:
                    # if link.attrs['href'] not in internalLinks:
                    internalLinks.append(link.attrs['href'])
                    fox.get(link.attrs['href'])
                    page = fox.page_source
                    time.sleep(5)
                    with open(f"./templates/{ link.attrs['href'] }.html", 'w') as f:
                        f.write(page)
            # return internalLinks
        
        #Retrieves a list of all external links found on a page
        def getExternalLinks(bsObj, excludeUrl): 
        #Finds all links that start with "http" or "www" that do
        #not contain the current URL
            for link in bsObj.findAll("a",href=re.compile("^(http|https|www)((?!"+excludeUrl+").)*$")):
                if link.attrs['href'] is not None:
                    # if link.attrs['href'] not in externalLinks:
                    #     # print(f"Adding {link.attrs['href']}  to externalLinks")
                    # externalLinks.append(link.attrs["href"])
                    fox.get(link.attrs['href'])
                    page = fox.page_source
                    time.sleep(5)
                    with open(f"./templates/{link.attrs['href']}.html", 'w') as f:
                        f.write(page)
                            # print(res.cookies)
            # return externalLinks
        
        
        def splitAddress(address):
            addressParts = address.replace("https://", "").split("/")
            return addressParts
        #  for eg if adddress is http://www.google.com   addressparts = ['www.google.com']
        
        def getLinks(startingPage):
            # parsinng and creating objects of page
            html = urlopen(startingPage)
            bsObj = BeautifulSoup(html, 'html.parser')
            # searching for external links on this page
            externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
            if len(externalLinks) == 0:
                internalLinks = getInternalLinks(bsObj, startingPage)
                print("An internal link")
                try:
                    return internalLinks[random.randint(0, len(externalLinks)-1)]
                except:
                    return externalLinks[0]
                    
                    
            else:
                print("found an external link")
                try:
                    return externalLinks[random.randint(0, len(externalLinks)-1)]
                except:
                    externalLinks[0]    
        
        def followExternalOnly(startingSite):
            link_internal_external = getLinks(startingSite) 
            html = urlopen(link_internal_external)
            bsObj = BeautifulSoup(html, 'html.parser')
            tags = bsObj.find_all('div')
            # imgs = bsObj.find_all('img')
        #    specifically for watsAPP  
        # imgs = bsObj.find_all("img",{"class":"_2goTk _1Jdop _3Whw5"})
            for tag in tags:
                print(link_internal_external)
                # print(tag.text)
                # print("\n \n \n ")
            # try:
            #     for img in imgs:
            #         imgUrl = img['src']
            #         print(imgUrl)
            #         print("downloading ....")
            #         name = random.randrange(1,1000)
            #         fullname = str(name)+".jpg"
            #         urllib.request.urlretrieve(imgUrl,fullname)     
        
            # except:
            #     pass
            # print(link_internal_external)
            try:
                followExternalOnly(link_internal_external)
            except:
                print("Unable to acess")
                followExternalOnly(externalLinks[0])
        i = i+1
        followExternalOnly(url)
        # url = input("Enter the base Url to start with : ")
        # this is a base url to start with...
        
        

    


