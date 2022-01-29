import re
import json


with open("kitap.txt",mode="r+") as k_list:
    data=k_list.readlines()



sahaf_dict={}

for i in data:
    name=i.replace("https://www.nadirkitap.com/","")
    s_id=re.search("f\d+",name).group().replace("f","")
    name=re.split("-sahaf\d+\w",name)
    sahaf_dict[s_id]=name[0]


with open('data.json', 'w') as fp:
    json.dump(sahaf_dict, fp)
