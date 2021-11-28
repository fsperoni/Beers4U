# Beers4U

## Purpose
The main purpose of this website is to be a reference guide for amateur homebrewers (like me) who like to experiment with new beer recipes, and are looking for new ideas. 

A secondary purpose is to provide pairing ideas between beer and food. The pairing would work both ways: given a beer, the website would make suggestions on food pairing; given a food, the website would make suggestions on beer pairing.

Registered users have the option to leave feedback on recipes or beer they've tried. Feedback is visible to registered users that can upvote (thumbs up) or down vote (thumbs down) a feedback.  

## Audience
The website can potentially be visited by homebrewers who are looking for new recipe ideas for their next beer. Other potential visitors include people looking for beer pairing information based on what they will be cooking; or perhaps they have this specific beer at home and are curious about what food would be a good pair to try the beer with. Registered users might also be looking for feedback/reviews (or leaving feedback) on beer recipes.

## Data / API
Making use of the [Punk API](https://punkapi.com/), the website can provide a huge variety/amount of data on beer recipes including, but not limited to: 

* Type of beer (included in the beer name):
	* Pale Ale;
	* Lager; 
	* Pilsner;
* Bitterness Level (measured in IBU);
* Alcohol Level (measured in ABV);
* Image (if available);
* Ingredients used:
	* Hops;
	* Malts;
	* Yeast;
* Food Pairing

Here's an example of what a JSON response from the API looks like: 
![Example JSON response](static/example.png)

## Aproach

### Database Schema
The application will make use of two databases: a User and a Favorite database, according to the schema below. The recipeID column in the Favorite database will be an integer that references the beer recipe ID obtained from the API.

![Database Schema](static/database_schema.png)
### Potential issues
Because the database will not store any beer recipe information directly (except for the recipe Id), the website will completely rely on the API availability to be able to display information to users and ultimately work properly.

### Sensitive information
The database will store user password that will be encrypted with bcrypt before it's stored in the database.

### Functionality
The application will allow any user to view basic/advanced information on beer recipes, such as:

* Name;
* Tags;
* Image (if available);
* Alcohol volume (percentage);
* Bitterness;
* Food pairing;
* Ingredients required to brew the beer;
* Brewer's tips

In addition to all the above mentioned functionalities, all registered/logged in users will be able to mark recipes as favorites, and add their own notes on each of these recipes for future reference. Feedback will be displayed by beer recipe and can be sorted by date, number of likes, or dislikes (either ascending or descending order).

### User Flow / UX
Once in the home page, users will have the option to register, log in, or use the website without the extra features that are only available to registered/logged in users. Regardless of their choice, they will be presented with a basic search interface allowing them to perform searches based on the beer name (the name includes the type of beer - lager, pilsner, pale ale, etc.), bitterness (since the search is made using IBU - an integer - the website will have dropdowns with ranges for better experience), alcohol volume, and food pairing. If the user chooses to perform an *advanced search* (more directed towards homebrewers), the search can then also be performed based on the ingredients (malt, hop, and yeast). If the user is registered/logged in, they will be presented with the option to mark beer recipes as favorite, add, edit, or delete feedback, and like or dislike feedback. 

### More than just CRUD
The website will offer a customized experience not only for users who are curious about different types of beer (looking for new beers to buy), but also for users who are interested in better matching their meal to the beer they already have, not to mention homebrewers willing to explore new recipes, and users interested in learning which beers would be a good match for the food being served. Because the website will have a section for feedback on recipes, users can refer to previous comments before deciding on brewing a new beer recipe, or buying/trying a new beer for pleasure or food pairing.

### Technologies used

* Ajax;
* Bootstrap;
* HTML;
* JavaScript
 * jQuery;
* PostgreSQL;
* Python
 * Flask;
 * WTForms;
* SQLAlchemy

#### Live App:
