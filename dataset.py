import pandas as pd
import random

names = ["City Hospital","Apollo Hospital","AIIMS","Fortis Hospital","Sunrise Clinic"]
cities = ["Delhi","Mumbai","Pune","Bangalore"]

data = []

for i in range(300):
    name = random.choice(names)
    city = random.choice(cities)

    variation = random.randint(1,3)

    if variation == 1:
        new_name = name
    elif variation == 2:
        new_name = name.replace("Hospital","Hosp")
    else:
        new_name = name.lower()

    data.append({"name": new_name, "address": city})

df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

print("data.csv created")
