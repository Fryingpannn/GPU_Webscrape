from urllib.request import urlopen as uReq # command to grab the page
from bs4 import BeautifulSoup as soup #command to parse the page
import re # regex

# the website page we are scraping
my_url = 'https://www.newegg.ca/p/pl?N=100007708%20600419577%20600536666%20601194948%20601202919%20601203901%20601203927%20601205646%20601294835%20601295933%20601296377%20601296379%20601301599%20601305993%20601321572%20601323902%20601326374%20601328427%20601331379%20601341679%204814&cm_sp=Cat_video-Cards_1-_-Visnav-_-Gaming-Video-Cards_1'

# opens up a connection, grab & downloads the page
uClient = uReq(my_url)
# read the html page and save it inside a var, if you don't store, the html is dumped
page_html = uClient.read()
# close the connection
uClient.close()

# html parser var: the html is a big jumble of text, we now need to parse it as html, and store it
page_soup = soup(page_html, "html.parser")

# we can now query specific tags: page_soup.h1
# in order to traverse the dom, we can use 'inspect element' to search for the tags we want to
# use. e.g.: a certain div class, then simply loop through the page to get all of them.

# find all divs with class 'item-container' (feeding this obj)
# 'containers' will be an array, you can see the div containers with containers[index]
containers = page_soup.findAll("div", {"class":"item-container"})

# open up a new csv file to write in
filename = "gpuinfo.csv"
f = open(filename, "w")

# first writing in the headers
headers = "brand, product_name, product_price, shipping_price\n" #csv are delimited by newlines
f.write(headers)

# at this point, you may want to use containers[0] in cmd to retrieve one container, beautify it
# using jsbeautifier, and paste in a separate file to read through it physically to see which part you need.

# if you scrape things that are not an element of all the items in the array, you may have to use
# an if-else or try-catch statement since we are looping through it.

# now, you would want to try scraping only one container before you even build the loop
# container = containers[0]

# looping (indented):
for container in containers:
	#get brand name
	product_brand = container.div.div.a.img['title'] # use array notation for attributes of tags

	# get product name
	# since we cannot reach the second <a> directly which contains the product name, we use findAll() 
	# function which returns an array. we can then index this array for its text
	title_name_container = container.findAll("a", {"class":"item-title"})
	product_name = title_name_container[0].text

	# get shipping cost
	shipping_container = container.findAll("li", {"class" : "price-ship"}) # returns html tag
	product_shipping = shipping_container[0].text.strip() # parsing the text and cleaning it's whitespace formatting with strip()

	# get product price: find > get text > clean text > retrieve text str
	price_container = container.findAll("li", {"class":"price-current"})
	price_str = price_container[0].text # return: '$299.99\xa0(4 Offers)–'
	cleaned_obj = re.search(r"\$[\d,.]*", price_str) # return: <re.Match object; span=(0, 7), match='$299.99'>
	cleaned_price_str = cleaned_obj.group() # extracts the string from obj; return: '$299.99'

	# print to console to see if works (ctrl+shift+L to edit many lines)
	print("product_brand: --- " + product_brand)
	print("product_name: --- " + product_name)
	print("product_shipping: --- " + product_shipping)
	print("cleaned_price_str: --- " + cleaned_price_str)

	# write to csv file: the product names/prices have commas in them which must be replaced, otherwise they'll be a new column in csv
	f.write(product_brand + "," + product_name.replace(",", "|") + "," + cleaned_price_str.replace(",", "") + "," + product_shipping + "\n")

# close file
f.close()