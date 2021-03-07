Weekly Menu Manager
====================================

Weekly-Menu manager is the backend API service to manage all operations related to creating, updating, deleting & managing weekly menus.

Data Models:
=========

1. **category**: Category defines the categorization of the weekly menu like 'veggies', 'vegan', etc.
2. **weeklymenus**: A menu created weekly for each category consisting of x recipes.
3. **ingredients**: It defines various ingredients used across recipes.
4. **recipe**: It defines a recipe.
5. **recipe ingredients**: It defines the relationship between recipes and ingredients (the ingredients required to create a recipe).
6. **recipe nutritional values**: It defines the nutritional values like energy, fats, etch associated with a recipe.
4. **recipe steps**: This illustrates the steps required to create a recipe.
5. **user reviews**:  This describes the reviews submitted by the user for a menu/recipe.

![Alt text](erd.png?raw=true "ERD for Weekly Menu Manager")

API design:
===========
Endpoints and its major responsibilities below.
1. Recipes
    - **/api/v1/recipes/create** - creating & updating recipe
    - **/api/v1/recipes/delete/{id}** - deleting recipe by id
    - **/api/v1/recipes/list/{categoryId}** - listing all recipes by category
2. Ingredients
    - **/api/v1/ingredients/create** - creating ingredient
    - **/api/v1/ingredients/update** - updating ingredient
    - **/api/v1/ingredients/delete/{id}** - deleting ingredient by id
    - **/api/v1/ingredients/list/{category}** - listing all ingredients by category name
3. WeeklyMenus
    - **/api/v1/weeklymenus/create** - creating weekly menu
    - **/api/v1/weeklymenus/update** - updating weekly menu
    - **/api/v1/weeklymenus/delete/{id}** - deleting weekly menu by id
    - **/api/v1/weeklymenus/list/{categoryId}** - listing all weekly menus by category
4. User Reviews
    - **/api/v1/reviews/create** - creating and updating review
    - **/api/v1/reviews/delete/{id}** - deleting review by id
    - **/api/v1/reviews/menu/{menuId}** - listing all reviews for a menu
    - **/api/v1/reviews/recipe/{recipeId}** - listing all reviews for a recipe

To run locally:

```
1. Start a local instance of postgres server
2. Create tables and add test data - python setup.py
3. Run the command - env ENV=dev python app.py'
```

Or with docker:

```
1. docker build -t weekly-menu-manager .
2. docker run -p 8080:8080 -e ENV=dev weekly-menu-manager
```

To run tests:
==============
**Pre-requisites**
1. Python version 3.7+
2. pip3
```
- Navigate to the root folder of the project on the terminal
- Run -> sh scripts/activate.sh
- Once the venv is activated, Run -> sh scripts/run_tests.sh
```