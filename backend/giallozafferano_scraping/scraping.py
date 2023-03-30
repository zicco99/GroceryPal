from backend.controllers.recipe import InsertRecipe
from backend.database.bootstrapDB import *
import re
from bs4 import BeautifulSoup
import requests

debug = False


def findTitle(soup):
    titleRecipe = ""
    for title in soup.find_all(attrs={'class': 'gz-title-recipe gz-mBottom2x'}):
        titleRecipe = title.text
    return titleRecipe


def findIngredients(soup):
    allIngredients = []
    for tag in soup.find_all(attrs={'class': 'gz-ingredient'}):
        nameIngredient = tag.a.string
        contents = tag.span.contents[0]
        quantityProduct = re.sub(r"\s+", " ",  contents).strip()
        allIngredients.append([nameIngredient, quantityProduct])
    return allIngredients


def findCategory(soup):
    for tag in soup.find_all(attrs={'class': 'gz-breadcrumb'}):
        category = tag.li.a.string
        return category


def findImage(soup):
    pictures = soup.find('picture', attrs={'class': 'gz-featured-image'})
    if pictures is None:
        pictures = soup.find(
            'div', attrs={'class': 'gz-featured-image-video gz-type-photo'})
    imageSource = pictures.find('img')
    imageURL = imageSource.get('data-src')

    if imageURL is not None:
        return imageURL
    else:
        return None


def findSteps(soup):
    steps = []
    for step_tag in soup.find_all(attrs={'class': 'gz-content-recipe-step'}):
        step = ("https://ricette.giallozafferano.it" +
                step_tag.find('img').get('data-src'), step_tag.find('p').text)
        steps.append(step)
    return steps


def scrap():
    # TODO Choose a way to choose when to refresh recipes (last update on a .txt)

    while (True):
        # Check number of pages
        numberOfPages = 0
        linkList = 'https://www.giallozafferano.it/ricette-cat'
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all(attrs={'class': 'disabled total-pages'}):
            numberOfPages = int(tag.text)

        # Scrap
        for pageNumber in range(1, numberOfPages + 1):  # numberOfPages
            linkList = 'https://www.giallozafferano.it/ricette-cat/page' + \
                str(pageNumber)
            response = requests.get(linkList)
            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup.find_all(attrs={'class': 'gz-title'}):
                link = tag.a.get('href')
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    InsertRecipe(title=findTitle(soup), category=findCategory(soup), ingredients=findIngredients(soup),
                                 steps=findSteps(soup), image_url=findImage(soup))
                except:
                    continue

        # Wait 24 and repeat (Naive solution)
        time.sleep(24 * 60 * 60)
