import requests
from bs4 import BeautifulSoup as bs
import json

#constants
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open("data.json","r") as fp:
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
    url=f"https://nadirkitap.com/kitapara.php?satici={seller_id}&ara=aramayap&tip={tip}&kitap_Adi={book_name}"
    result = requests.get(url, headers=headers)

    soup=bs(result.text,"html.parser")
    pages=soup.find("div",class_="pagination-product-bottom")
    if pages !=None:
        page_count=int(pages.strong.text.split("/")[1])
        for i in range(1,page_count+1):
            res = requests.get(f"{url}+&page={i}", headers=headers)
            soup_page=bs(res.text,"html.parser")
            product_list=soup.find("ul",class_="product-list")
            for i in product_list:
                books_dict[i.span.text]=i.find("div",class_="product-list-price").text
    else:
        print(data[seller_id])
        res = requests.get(f"{url}", headers=headers)
        soup_page=bs(res.text,"html.parser")
        product_list=soup.find("ul",class_="product-list")
        try:
            for i in product_list:
                books_dict[i.span.text]=i.find("div",class_="product-list-price").text
        except TypeError:
            continue


with open('result.json', 'w') as fp:
    json.dump(books_dict, fp)