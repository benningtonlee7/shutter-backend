import csv
from application.resources.BrandResource import Brand
from application import db

set_name = set()
set_i = set()
with open('brand_list.csv', 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    my_reader = list(my_reader)
    for idx, row in enumerate(my_reader):
        if idx == 0:
            continue
        _, name = row[0], row[1]
        if name.lower() not in set_name:
            set_name.add(name.lower())
            set_i.add(idx)
    l = []
    for i in set_i:
        row = my_reader[i]
        _, name = row[0], row[1]
        l.append(name)

    l2 = sorted(l)
    l3 = []
    for i, item in enumerate(l2):
        if i not in set([1, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]):
            l3.append(item)


    for name in l3:
        new_brand = Brand(brand_name=name)
        db.session.add(new_brand)

    db.session.commit()


