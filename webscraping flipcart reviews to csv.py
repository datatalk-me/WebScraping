from re import search
from bs4 import BeautifulSoup as bs
import requests
import csv
from urllib.request import urlopen as uReq



class flipkart_scraping():
    def __init__(self):
        self.search_term = input("Enter search term: ").replace(" ", "")
        self.flipkart_url = "https://www.flipkart.com/search?q=" + self.search_term + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    def flipkart_scraping(self):
        uClient = uReq(self.flipkart_url)
        flipkart_page = uClient.read()
        uClient.close()
        flipkart_soup = bs(flipkart_page, "html.parser")
        return flipkart_soup

    def product_info(self, flipkart_soup):
        products = flipkart_soup.findAll("div", {"class": "_1AtVbE col-12-12"})
        for product in products:
            if product.find("div", {"class":"_4rR01T"}) is not None:
                product_url = self.flipkart_url + product.find("a")["href"]
                product = requests.get(product_url)
                product.encoding = 'utf-8'
                product_soup = bs(product.text, "html.parser")
                product_reviews = product_soup.findAll("div", {"class":"_16PBlm"})
                for review in product_reviews:
                    if review.find("div", {"class":"col _2wzgFH"}) is not None:
                        product_review_head = review.div.div.div.p.text
                        product_review_rating = review.find("div", {"class":"_3LWZlK _1BLPMq"}).text
                        product_review_body = review.find("div", {"class":""}).text
                        reviewer_name = review.find("p", {"class":"_2sc7ZR _2V5EHH"}).text
                        review_date = review.find("p", {"class":"_2sc7ZR"}).text
                        with open(self.search_term + '.csv', 'a') as csvfile:
                            fieldnames = ['product_review_head', 'product_review_rating', 'product_review_body', 'reviewer_name', 'review_date']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow({'product_review_head': product_review_head, 'product_review_rating': product_review_rating, 'product_review_body': product_review_body, 'reviewer_name': reviewer_name, 'review_date': review_date})
                            csvfile.close()
                    else:
                        print("No reviews found")
            else:
                print("No products found")
                

obj = flipkart_scraping()
flipkart_soup = obj.flipkart_scraping()
obj.product_info(flipkart_soup)


