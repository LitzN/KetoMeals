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
# Code to get evironment variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Code for function on Homepage - queries for meal type buttons and to get all recipes
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


# Code for function of search bar - queries needed for successful homepage function on reload after searching, search index input query and post method
@app.route("/search", methods=["GET", "POST"])
def search():
    snacks = mongo.db.recipes.find({"meal_type": "Snack"})
    mains = mongo.db.recipes.find({"meal_type": "Main"})
    desserts = mongo.db.recipes.find({"meal_type": "Dessert"})
    recipes = mongo.db.recipes.find()
    query = request.form.get("query")
    find_recipe = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("recipes.html", recipes=recipes, mains=mains,
                           snacks=snacks, desserts=desserts,
                           find_recipe=find_recipe)


# Code for function on Register page - prevent duplicate usernames, create hashed password and upload data to the users collection
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
            "password": generate_password_hash(request.form.get("password")),
            "favourites": []
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration complete!")
        return redirect(url_for("my_recipes", username=session["user"]))
    return render_template("register.html")


# Code for function on Login Page - checks user input for match on database and display flash messages if input doesn't match
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


# Code for function on My Recipes Page - queries to get specific users created recipes and favourites, code to unpack recipe ids from their favourites.
@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    myrecipes = {"created_by": session["user"]}

    user = mongo.db.users.find_one({"username": session["user"]})

    favourites = user['favourites']
    results = []
    for fav in favourites:
        results.append(mongo.db.recipes.find_one({"_id": ObjectId(fav)}))

    ownrecipes = mongo.db.recipes.find(myrecipes)

    if session["user"]:
        return render_template(
            "my_recipes.html", username=username, favourites=favourites,
            myrecipes=myrecipes, ownrecipes=ownrecipes, results=results)

    return redirect(url_for("login"))


# Code for function of Logout button on navigation - removes session cookie to log out user and flash message to alert them.
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Code for function on Add recipe page - Post method uses inputs from form to create dictionary to submit to database. Displays flash message on completion.
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


# Code for function of favourite button - Adds recipe id to user's favourites array
@app.route("/add_favourite/<recipe_id>", methods=["GET", "POST"])
def add_favourite(recipe_id):
    mongo.db.users.update_one(
        {"username": session["user"].lower()},
        {"$push": {"favourites": ObjectId(recipe_id)}})
    flash("Favourite saved")
    return redirect(url_for("get_recipes"))


# Code for function of remove favourite buttons - Removes recipe id from users favourites array
@app.route("/remove_favourite/<recipe_id>", methods=["GET", "POST"])
def remove_favourite(recipe_id):
    mongo.db.users.find_one_and_update(
        {"username": session["user"].lower()},
        {"$pull": {"favourites": ObjectId(recipe_id)}})
    flash("Favourite saved")
    return redirect(url_for("get_recipes"))

# Code for function of Edit recipe Page - pulls recipe data from database for field population and submits updated dictionary to update database.
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


# Code for function of delete recipe buttons - removes recipe from the database
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
