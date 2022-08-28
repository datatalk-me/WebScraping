from re import search
from bs4 import BeautifulSoup as bs
import requests
import csv
from urllib.request import urlopen as uReq




def flipkart_scraping():
    search_term = input("Enter search term: ").replace(" ", "")
    pages = int(input("Enter number of pages: "))
    flipkart_url = "https://www.flipkart.com/search?q=" + search_term + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    uClient = uReq(flipkart_url)
    flipkart_page = uClient.read()
    uClient.close()
    flipkart_soup = bs(flipkart_page, "html.parser")
    return flipkart_soup


def product_info(flipkart_soup):
    products = flipkart_soup.findAll("div", {"class": "_1AtVbE col-12-12"})
    for product in products:
        if product.find("div", {"class":"_4rR01T"}) is not None:
            product_name = product.find("div", {"class":"_4rR01T"}).text
            product_price = product.find("div", {"class":"_30jeq3 _1_WHN1"}).text
            product_rating = product.find("div", {"class":"_3LWZlK"}).text
            print(product_name,product_price,product_rating)
            with open('flipkart.csv', 'a') as csvfile:
                fieldnames = ['product_name', 'product_price', 'product_rating']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'product_name': product_name, 'product_price': product_price, 'product_rating': product_rating})
                csvfile.close()
            

def main():
    flipkart_soup = flipkart_scraping()
    product_info(flipkart_soup)



if __name__ == "__main__":
    main()
