# **KetoMeals**

Keto meals is a site for a cookbook database which allows users to find recipes they can use when following a ketogenic diet. The website informs visitors of the benefits of this type of diet as well as allowing them to build their own personalised cookbook to make their lifestyle change easier. The website also allows users to view cookware products they may need from a promoted brand.

The project consists of 5 pages. When a user first visits the site, the pages available to them will be the homepage and register/login page. On registering/logging in they will gain access to the my recipes, add recipe and logout button.
 The homepage gives the user the chance to understand the types of recipes available and the aim of the ketogenic diet. The search capabilities are flexible allowing users to search either by meal type or by recipe or ingredient name. 
 The register page allows users to create an account for the site. After registering the user is directed to their profile page (my recipes), here they are invited to add a recipe, which will become available for all users to view. 
 Only the user is able to edit or delete the recipe. When browsing recipes, users can decide to add their favourites to their personal page for easy viewing. 

## **User Stories & UX**

### **Overall design**
1. Viewing several popular recipe sites gave me an idea of the styling conventions for online cookbooks.
 It is clear users only want to see an image of the recipe and name while searching. When a recipe is selected ingredients and steps are presented simply, making the recipe easy to follow. 
 Colours are minimal with most focus on the recipe images.
 Websites used for inspiration:
[BBC good food](https://www.bbcgoodfood.com/recipes), [Delicious magazine](https://www.deliciousmagazine.co.uk/recipes/), [All recipes](http://allrecipes.co.uk/recipes/)

2. The color palette was created with [coolors](https://coolors.co/), I chose this palette as the lighter colours will ensure focus remains on the images. The brighter colours draw attention to important parts of the page for easy navigation and give the page more vibrancy.
[Palette Used](https://coolors.co/274c77-af3b6e-d8ddef-60992d-ffffff)

### **User Stories**
1. I am new to keto lifestyle and want to know why I should follow this and what would be available to me.
2. I am following a keto diet and need ideas on what to cook which I can access quickly and easily
3. I am following a keto diet and want to see if the site has recipes for a specific ingredient I want to use
4. I am a follower of the keto diet and want to share my recipes and update them if I’ve found a better way to make them
5. I am the site owner and would like to promote Haden cookware

### **Wireframes**

Wireframes created for this project:
* [Homepage](static/images/wireframes/home.png)
* [Add Recipe and Edit Recipe pages](static/images/wireframes/add_edit.png)
* [Register and Login pages](static/images/wireframes/register_login.png)
* [My recipes page](static/images/wireframes/user_recipes.png)

## **Features**

### **Sitewide Features**

* __Navigation bar__ is dark to compliment both the lighter site colour theme and image backgrounds.
Bar is collapsible and appears as a bar icon on smaller screen sizes.
* __Cookware promotion__ 

### **Homepage**

* __Header image__ is a simple colourful image of keto food. The image is overlayed with a black translucent cover featuring the brand name appearing in a large white font. 
The header introduces the site and gives the user an idea of what to expect.
* __Introduction text__ welcomes the user to start creating their cookbook. The benefits of the keto way of eating is described briefly and users are invited to view the recipes.
The text is intended to inform users who are not familiar with the keto diet and entice them to explore further.
* __Meal Type selector buttons__ are the first method of exploring the recipes. Buttons for each meal type allow the user to select the meal type they want to explore
and view relevant recipes. The buttons are made up of a large image, showing an example of the meal type and a heading. Background color is dark to draw attention against the lighter
colour scheme and keep the main focus on the images.
* __Meal Type results__ are displayed below the buttons, in the form of cards. Cards show the recipe image and title only until selected,
once clicked on an overlay containing the recipe and ingredients appears. This allows users to view more than one recipe at a time.
* __Search bar__ allows users to search for recipes by ingredient or recipe name. 
* __Search results__ are displayed as a list of collapsibles with the recipe name and image appearing side by side. Once 
recipe is selected the drop down reveals the recipe and relevant cookware promotion. This section also contains different buttons 
depending on the identity of the user. If the user is the recipe owner, they have the option of "Edit" or "Delete"; while other users
will see a "favourite" button, used to add the recipe to their personal page.

### **Register/Login Pages**
* __Image background__ 
* __Form__


### **My Recipes** 
* __User Header__ is styled with site theme colours.
* __Own Recipes__ are each displayed along with relevant cookware promotion and edit and delete buttons.
* __Favourite Recipes__ are displayed along with relevant cookware promotion and unfavourite button.

### **Add Recipe**
* __Image Background__
* __Form__ is used to add a recipe to the database and is styled using site theme colours. Form contains a field for each recipe requirement in the database. For longer input, such as in ingredients or instructions, expected input 
is explained through helper text below the input field. All fields must be filled out for the recipe to be submitted and incorrectly filled fields will be highlighted in red.

### **Edit Recipe**
* __Image Background__
* __Form__ is used to update a recipe in the database and is styled using site theme colours. The form's input fields are prefilled with current recipe data, allowing the user
to easily make adjustments to the recipe. 