import requests
from bs4 import BeautifulSoup as bs
import json
from urllib.parse import quote


with open("data.json","r") as fp:
    data=json.load(fp)

keys=list(data.keys())



print("""
1.yayinevi
2.kitap_adi
""")
tip=input(">: ")
book_name=input("name: ")
seller=keys[0]


books_dict={}

url=f"https://nadirkitap.com/kitapara.php?satici={seller}&ara=aramayap&tip={tip}&kitap_Adi={book_name}"#&page={page}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

result = requests.get(url, headers=headers)
print(result.status_code)
soup=bs(result.text,"html.parser")

pages=soup.find("div",class_="pagination-product-bottom")
page_count=int(pages.strong.text.split("/")[1])



for i in range(1,page_count+1):
    res = requests.get(f"{url}+&page={i}", headers=headers)
    soup_page=bs(res.text,"html.parser")
    product_list=soup.find("ul",class_="product-list")
    for i in product_list:
        books_dict[i.span.text]=i.find("div",class_="product-list-price").text

sort_books = sorted(books_dict.items(), key=lambda x: x[1])
print(sort_books)