from names_generator import generate_name
from random import randint
import pandas as pd
import uuid

data_raw = pd.read_excel(r"data.xlsx")
#process input

data = {}
for col in data_raw.keys():
    data[col] = []
    for row in range(len(data_raw[col])):
        data[col].append(data_raw[col][row])

d = ["TB1", "TB2", "VB1", "VB2", "U"]
for dp in d:    
    for i, e in enumerate(data[dp]):
        if e == "X":
            data[dp][i] = True
        else:
            data[dp][i] = False

for i, s in enumerate(data["Fractions"]):
    data["Fractions"][i] = s.split(",")

cumulative = {}
c = 0
for i, e in enumerate(data["Regions"]):
    cumulative[(c,c+data["Probability"][i])] = e
    c += data["Probability"][i]

# print(cumulative)

# index_number = 0
# def get_id():
#     x = index_number
#     index_number += 1
#     return x

def generate_type():
    x = randint(1,100)
    for k in reversed(cumulative.keys()):
        if (x > k[0] and x <= k[1]):
            return cumulative[k]
        
def generate_fraction(type):
    k = data["Regions"].index(type)
    r = randint(0,len(data["Fractions"][k])-1)
    return data["Fractions"][k][r]

def generate_time(type):
    k = data["Regions"].index(type)
    return data["Time"][k]

used_ids = []

class patient:
    def __init__(self, name, type, fraction, time):
        self.name = name
        # self.id = get_id()
        self.id = uuid.uuid1()
        self.type = type
        self.fraction = fraction
        self.time = time

    def __init__(self):
        self.name = generate_name(style='capital')
        # self.id = uuid.uuid1()
        nr = 0
        while nr == 0 and not (nr in used_ids):
            nr = randint(100000000, 999999999)
        used_ids.append(nr)
        self.id = nr
        self.type = generate_type()
        self.fraction = int(generate_fraction(self.type))
        self.time = int(generate_time(self.type))

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Type: {self.type}, Fraction: {self.fraction}, Time: {self.time}"

def generate_patients(n):
    pats = []
    for i in range(n):
        pats.append(patient())

    # for e in pats:
    #     print(e)
    return pats

# generate_patients()
# print(data_raw)
# print(data)