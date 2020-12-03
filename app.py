import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    snacks = mongo.db.recipes.find({"meal_type": "Snack"})
    mains = mongo.db.recipes.find({"meal_type": "Main"})
    desserts = mongo.db.recipes.find({"meal_type": "Dessert"})
    recipes = mongo.db.recipes.find()
    return render_template(
        "recipes.html", mains=mains, snacks=snacks, desserts=desserts,
         recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("recipes.html", recipes=recipes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username taken!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration complete!")
        return redirect(url_for("my_recipes", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                        "my_recipes", username=session["user"]))
            else:
                flash("Invalid username/password")
                return redirect(url_for("login"))
        else:
            flash("Invalid username/password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    myrecipes = {"created_by": session["user"]}

    ownrecipes = mongo.db.recipes.find(myrecipes)

    if session["user"]:
        return render_template(
            "my_recipes.html", username=username, myrecipes=myrecipes, 
            ownrecipes=ownrecipes)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "meal_type": request.form.get("meal_type"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "instructions": request.form.get("instructions"),
            "cookware": request.form.get("cookware"),
            "image_url": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe added!")
        return redirect("get_recipes")

    meal_type = mongo.db.types.find().sort("meal_type", 1)
    return render_template("add_recipe.html", meal_type=meal_type)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        submit = {
            "meal_type": request.form.get("meal_type"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "instructions": request.form.get("instructions"),
            "cookware": request.form.get("cookware"),
            "image_url": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe Updated!")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    meal_type = mongo.db.types.find().sort("meal_type", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, meal_type=meal_type)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Deleted!")
    return redirect("get_recipes")


# CHANGE DEBUG TO FALSE WHEN PROJECTS DONE
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
