import requests 
from bs4 import BeautifulSoup
import json

python_data = {"quotes" : [] ,"authors" : []}

def get_quote_details(quote_container):
    quote_dict = dict()
   
    quote_element = quote_container.find("span" , class_ = "text") 
    quote_text = quote_element.string 
    
    author_element = quote_container.find("small" , class_ = "author")
    author_name = author_element.string
    
    tags_container = quote_container.find("div" , class_ = "tags")
    tag_elements = tags_container.find_all("a" , class_ = "tag")
    tags_list = []
    for tag_element in tag_elements:
        tags_list.append(tag_element.string)
 
    quote_dict["quote"] = quote_text
    quote_dict["author"] = author_name
    quote_dict["tags"] = tags_list 
    
    return quote_dict

def get_author_details(quote_container):
    author_dict = dict()
    
    author_element = quote_container.find("small" , class_ = "author")
    author_name = author_element.string

    about_author_element = quote_container.find("a" ,text = "(about)") 
    about_author_url = about_author_element["href"]
    reference = "http://quotes.toscrape.com" + about_author_url
    
    author_result = requests.get(reference) 
    author_doc = BeautifulSoup(author_result.text , "html.parser")
    
    born_date_element = author_doc.find("span" ,class_="author-born-date") 
    born_date = born_date_element.string 
    born_place_element = author_doc.find("span" ,class_="author-born-location") 
    born_place = born_place_element.string 
    born_date_location = born_date + " " +  born_place 

    author_dict["name"] = author_name 
    author_dict["born"] = born_date_location 
    author_dict["reference"] = reference 
    
    return author_dict

def get_url_of_next_page(doc):
    next_button_element = doc.find("li" , class_ = "next")
    if next_button_element == None:
        return None
    anchor_element = next_button_element.find("a") 
    url = "http://quotes.toscrape.com" + anchor_element["href"]
    return url

def get_data_from_page(python_data ,url):
    quotes_list = python_data.get("quotes")
    authors_list = python_data.get("authors")
    
    result = requests.get(url) 
    doc = BeautifulSoup(result.text , "html.parser")
    quotes_containers = doc.find_all("div" , class_ ="quote")

    for quote_container in quotes_containers:
        quote_details = get_quote_details(quote_container)
        author_details = get_author_details(quote_container)

        quotes_list.append(quote_details)
        if author_details not in authors_list:
            authors_list.append(author_details)   
    
    new_python_data = { "quotes" : quotes_list , "authors" : authors_list}
    next_page_url = get_url_of_next_page(doc)
    
    return (new_python_data,next_page_url)


first_page_url = "http://quotes.toscrape.com/"
python_data , url = get_data_from_page(python_data , first_page_url) 

for _ in range(9): #Since page contains 10 pages
   python_data , url = get_data_from_page(python_data , url)

json_data = json.dumps(python_data)
with open("quotes.json" , "w") as f:
    f.write(json_data) 

