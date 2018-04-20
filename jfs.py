from lxml import html, etree
import requests
import re
import csv

r = requests.get("https://www.apartmentfinder.com/Florida/Tampa-Apartments")

tree = html.fromstring(r.content)

buyer = tree.xpath('//*[@id="listingContainer"]/div')
atos = re.compile('data-pn="(.*?)"')
pr = re.compile('data-pr="(.*?)"')
ad = re.compile('<span title="(.*?)"')

letters_only = re.compile('[^a-zA-Z|\s]')
class appt:
    def __init__(self, n, p, a):
        self.name = n
        self.price = p
        self.address = a



rows = {}
li = []
for x in buyer:
    z = etree.tostring(x)
    name = atos.findall(str(z))
    price = pr.findall(str(z))
    address = ad.findall(str(z))
    if name and price and address:
        sep_add = address[0].split(',')

        new = sep_add[-1].split()
        sep_add.remove(sep_add[-1])
        sep_add.append(new[0])
        sep_add.append(new[1])
        print(sep_add)

        li.append([letters_only.sub('', name[0]), price[0], *sep_add])
        rows[letters_only.sub('', name[0])] = appt(name[0], price[0], address[0])

for ap in rows.keys():
    print("name: %s\n\tprice: %s\n\taddress: %s\n\n" %(ap, rows[ap].price, rows[ap].address))


with open('csv_scrape.csv', 'w+') as out:
    wr = csv.writer(out)
    wr.writerow(["Listing", "Price", "Street", "City", "State","Zip"])
    for ad in li:
        wr.writerow(ad)