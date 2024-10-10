
import requests
from bs4 import BeautifulSoup
import json

url = "https://stephene369.github.io/exemple/"
response = requests.get(url)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_elements = soup.find_all(class_='title')
    
    for element in title_elements:
        print(element.text.strip())
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")




##############################
## First exercice  :

## GEtting the html code and the content div code
url_ = "https://www.jebosseengrandedistribution.fr/2020/04/14/voici-la-liste-des-rayons-quon-trouve-en-grande-distribution/?srsltid=AfmBOooak7kkzniP0a2veGYmU5VTJTseh3MR_lb8eC8HllV50yvuwmuJ"
res = requests.get(url_)

sp = BeautifulSoup(res.text, "html.parser")
div = sp.find('div', class_='post-content')


### getting all the children
children = div.find_all()


data = { }
for i , child in enumerate(children) : 
    if child.name in 'h3' : 
        
        if children[i+1].name == 'ul' : 
            data[child.text] = []
            for produit in children[i+1].find_all('li') : 
                # print(produit.text)
                data[child.text].append( produit.text )

                
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)





## Data injection in SQL database  
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        age INTEGER
    )
''')

# Insert some sample data
sample_data = [
    ('John', 'Doe', 30),
    ('Jane', 'Smith', 25),
    ('Mike', 'Johnson', 35)
]

cursor.executemany('INSERT INTO persons (first_name, last_name, age) VALUES (?, ?, ?)', sample_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

# Reopen the connection to fetch and display data
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Fetch all data and print it
print("All data in the database:")
cursor.execute('SELECT * FROM persons')
for row in cursor.fetchall():
    print(row)

# Perform some simple queries
print("\nPeople older than 30:")
cursor.execute('SELECT * FROM persons WHERE age > 30')
for row in cursor.fetchall():
    print(row)

print("\nPeople with last name 'Smith':")
cursor.execute("SELECT * FROM persons WHERE last_name = 'Smith'")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()



















import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('grande_distribution.db')
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rayons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rayon TEXT,
        produits TEXT
    )
''')


for rayon, produits in data.items():
    cursor.execute('''
        INSERT INTO rayons (rayon, produits)
        VALUES (?, ?)
    ''', (rayon, json.dumps(produits)))


conn.commit()
conn.close()











#################

import requests

barcode = "3017624010701"  # Nutella Ferrero barcode
url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"

response = requests.get(url)

if response.status_code == 200:
    product_data = response.json()
    print(product_data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")



