from bs4 import BeautifulSoup
from unidecode import unidecode
import urllib2


def ikea_scrape():

	base_url = "http://www.ikea.com/us/en/catalog/productsaz/"
	products = {}

	for i in range(0, 26):
		url = base_url + str(i) + "/"
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read(), 'html.parser')
		letter_products = soup.findAll("span", {"class": "productsAzLink"})
		for product in letter_products:
			string = product.get_text()
			products[string] ={
				"name": string.split(' ')[0].lower().capitalize(),
				"desc": ' '.join(string.split(' ')[1:]).capitalize(),
				"url": "http://www.ikea.com" + product.a.get('href')
			}

	return products

if __name__ == '__main__':
	products = ikea_scrape()
	f = open('scrape_ikea.txt', 'w')
	for p_key, p in products.iteritems():
		f.write((p["url"] + '\t' + p["name"] + '\t' + p["desc"] + '\n').encode('utf8'))
	f.close

