from flask import Flask, render_template, request, redirect
from data import load_products, save_products

app = Flask(__name__)

products = load_products()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def view_products():
    return render_template("products.html", products = products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"].capitalize().strip()
        price = request.form["price"]
  
        if not name:
            error = "Product Name Can Not Be Empty.."
            return render_template("add_product.html", error = error, name = name, price = price)
        elif not price:
            error = "Invalid Product Price.."
            return render_template("add_product.html", error = error, name = name, price = price)
        elif int(price) < 0:
            error = "Product Price Can Not Be Negetive.."
            return render_template("add_product.html", error = error, name = name, price = price)
        else:
            for product in products:
                if product["name"] == name:
                    error = "Product Already Exists.."
                    return render_template("add_product.html", error=error, name = name, price = price)
            new_product = {"name" : name, "price" : int(price)}
            products.append(new_product)
            save_products(products)
            return redirect("/products")
    return render_template("add_product.html")

@app.route("/delete", methods = ["POST"])
def delete_product():
    if request.method == "POST":
        name = request.form["name"]
        for product in products:
            if product["name"] == name:
                products.remove(product)
                save_products(products)
                break
        return redirect("/products")
    return render_template("products.html")

@app.route("/edit", methods = ["GET", "POST"])
def edit_product():
    if request.method == "GET":
        name = request.args["name"]
        for product in products:
            if product["name"] == name:
                price = product["price"]
                return render_template("add_product.html", old_name = name, name = name, price = price)
    elif request.method == "POST":
        old_name = request.form["old_name"]
        name = request.form["name"].capitalize().strip()
        price = request.form["price"]
        print("old_name", old_name)
        print("new_name", name)

        if not name:
            error = "Product Name Can Not Be Empty.."
            return render_template("add_product.html", error = error, name = name, old_name = old_name, price = price)
        elif price == "" or int(price) < 0:
            error = "Invali Price.."
            return render_template("add_product.html", error = error, name = name, old_name = old_name, price = price)

    
        for product in products:
            if product["name"] == name and product["name"] != old_name:
                error = "Product Already Exists.."
                return render_template("add_product.html", error = error, name = name, old_name = old_name, price = price)
            
        for product in products:
            if product["name"] == old_name:
                product["name"] = name
                product["price"] = int(price)
                save_products(products)
                return redirect("/products")
            

@app.route("/search")
def search():
    search_text = request.args.get("name","").strip()
    results = []

    if search_text:
        for product in products:
            if search_text.lower() in product["name"].lower():
                results.append(product)

    return render_template("search_product.html", results = results, search_text = search_text)
            



if __name__ == "__main__":
    app.run(debug=True)