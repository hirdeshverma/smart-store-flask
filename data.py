import json

def load_products():
    try:
        with open("products.json", "r") as file:
            products = json.load(file)
            return products
        
    except FileNotFoundError:
        products = []
        return products

def save_products(products):
    with open("products.json", "w") as file:
        json.dump(products, file)
