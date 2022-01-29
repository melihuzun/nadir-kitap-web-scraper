import requests
from bs4 import BeautifulSoup as bs
import json
from flask import Flask,jsonify

#constants
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open("sellers.json","r") as fp:
    data=json.load(fp)

keys=list(data.keys())

books_dict={}




print("""
1.yayinevi
2.kitap_adi
""")
tip=input(">: ")
book_name=input("name: ")

for seller_id in keys:
    seller_name=data[seller_id]
    print(f"serching thru {seller_name}")
    my_dict={}
    url=f"https://nadirkitap.com/kitapara.php?satici={seller_id}&ara=aramayap&tip={tip}&kitap_Adi={book_name}"
    result = requests.get(url, headers=headers)

    soup=bs(result.text,"html.parser")
    pages=soup.find("div",class_="pagination-product-bottom")
   
    if pages !=None:
        try:    
            page_count=int(pages.strong.text.split("/")[1])
        except AttributeError:
            pages=soup.find("input",attrs={"type":"text","name":"page"})
            page_count=int(pages["value"])

        for i in range(1,page_count+1):
            request_url=f"{url}&page={i}"
            print(request_url)
            res = requests.get(request_url, headers=headers)
            soup_page=bs(res.text,"html.parser")
            product_list=soup_page.find("ul",class_="product-list")
            for book in product_list:
                my_dict[book.span.text]=book.find("div",class_="product-list-price").text
    else:
        res = requests.get(f"{url}", headers=headers)
        soup_page=bs(res.text,"html.parser")
        product_list=soup_page.find("ul",class_="product-list")
        my_dict[book.span.text]=book.find("div",class_="product-list-price").text

    books_dict[seller_name]=my_dict


with open('result.json', 'w') as fp:
    json.dump(books_dict, fp)


with open("result.json",encoding='utf8') as fp:
    data=json.load(fp)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def hello_world():
    return jsonify(data)

if __name__ == '__main__':
    app.run()