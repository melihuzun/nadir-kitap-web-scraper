import json
with open("result.json",encoding='utf8') as fp:
    data=json.load(fp)

for i in data:
    print(i," - ",data[i])