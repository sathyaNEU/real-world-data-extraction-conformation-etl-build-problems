"""The assortment's product texture: what each family is (brand, product, size), its varieties and its regular price.

world.items() draws the family structure (department, family size, popularity, UPCs) from the master stream; this
module dresses every family as a real product line on its own stream, so the structure the rest of the world is
drawn on never moves. A family is one brand's product in one size; its varieties are the flavours, scents, cuts or
sizes a shopper picks between. (brand, product, size) is unique across the assortment, and so is its POS short form.
"""
import re

import numpy as np

import params as P

# product: (varieties, [(size, price factor)], regular price at factor 1.0, weight in its department)
SPECS = {
    "GROCERY": {
        "Pasta": (["Spaghetti", "Penne", "Rotini", "Fusilli", "Linguine", "Macaroni", "Fettuccine", "Rigatoni"],
                  [("450 g", 0.6), ("900 g", 1.0)], 2.79, 1.6),
        "Pasta Sauce": (["Tomato Basil", "Marinara", "Four Cheese", "Roasted Garlic", "Mushroom", "Arrabbiata",
                         "Bolognese"], [("410 mL", 0.65), ("650 mL", 1.0)], 3.49, 1.3),
        "Rice": (["Long Grain", "Basmati", "Jasmine", "Brown", "Parboiled", "Arborio"],
                 [("900 g", 0.45), ("2 kg", 1.0), ("8 kg", 3.1)], 6.49, 1.0),
        "Cereal": (["Honey Oat", "Bran Flakes", "Corn Flakes", "Multigrain", "Frosted Wheat", "Raisin Bran",
                    "Crispy Rice"], [("350 g", 0.75), ("525 g", 1.0), ("750 g", 1.3)], 5.49, 1.6),
        "Peanut Butter": (["Smooth", "Crunchy", "Natural Smooth", "Natural Crunchy", "Light", "Honey"],
                          [("500 g", 0.6), ("1 kg", 1.0), ("2 kg", 1.75)], 6.99, 1.0),
        "Soup": (["Chicken Noodle", "Tomato", "Cream of Mushroom", "Vegetable", "Beef Barley", "Minestrone",
                  "Clam Chowder"], [("284 mL", 0.45), ("540 mL", 1.0), ("900 mL", 1.5)], 2.49, 1.4),
        "Canned Tomatoes": (["Diced", "Whole", "Crushed", "Stewed", "Diced No Salt Added", "Diced Italian"],
                            [("398 mL", 0.6), ("796 mL", 1.0)], 1.99, 0.9),
        "Coffee": (["Medium Roast", "Dark Roast", "Decaf", "Original Roast", "Breakfast Blend", "Colombian",
                    "French Roast"], [("300 g", 0.55), ("640 g", 1.0), ("920 g", 1.35)], 11.49, 1.3),
        "Tea": (["Orange Pekoe", "Green", "Earl Grey", "Chamomile", "Peppermint", "English Breakfast"],
                [("20 bags", 0.45), ("72 bags", 1.0), ("144 bags", 1.7)], 5.49, 0.9),
        "Flour": (["All Purpose", "Whole Wheat", "Unbleached", "Bread", "Cake and Pastry"],
                  [("1 kg", 0.55), ("2.5 kg", 1.0), ("10 kg", 2.7)], 5.29, 0.6),
        "Sugar": (["Granulated", "Golden Yellow", "Dark Brown", "Icing", "Berry"],
                  [("1 kg", 0.6), ("2 kg", 1.0), ("4 kg", 1.8)], 3.99, 0.6),
        "Jam": (["Strawberry", "Raspberry", "Wild Blueberry", "Apricot", "Mixed Fruit", "Peach", "Black Currant"],
                [("250 mL", 0.6), ("500 mL", 1.0), ("1 L", 1.65)], 4.79, 0.8),
        "Crackers": (["Original", "Whole Wheat", "Cheddar", "Rosemary", "Sea Salt", "Multigrain", "Rice"],
                     [("200 g", 1.0), ("400 g", 1.6)], 3.49, 1.2),
        "Oatmeal": (["Quick Oats", "Large Flake", "Steel Cut", "Maple Brown Sugar", "Apple Cinnamon"],
                    [("430 g", 0.75), ("1 kg", 1.0), ("2.25 kg", 1.8)], 4.49, 0.7),
        "Salsa": (["Mild", "Medium", "Hot", "Chunky Mild", "Black Bean and Corn", "Peach Mango"],
                  [("430 mL", 0.75), ("650 mL", 1.0)], 4.29, 0.7),
        "Olive Oil": (["Extra Virgin", "Pure", "Light Tasting", "Organic Extra Virgin", "Cold Pressed"],
                      [("500 mL", 0.55), ("1 L", 1.0), ("3 L", 2.6)], 12.99, 0.7),
        "Ketchup": (["Original", "Less Sugar", "Organic", "No Salt Added", "Spicy"],
                    [("750 mL", 0.8), ("1 L", 1.0), ("1.25 L", 1.2)], 4.49, 0.8),
        "Mustard": (["Yellow", "Dijon", "Honey", "Grainy", "Spicy Brown"],
                    [("250 mL", 0.7), ("400 mL", 1.0), ("800 mL", 1.6)], 2.69, 0.6),
        "Mayonnaise": (["Real", "Light", "Olive Oil", "Avocado Oil", "Garlic Aioli"],
                       [("445 mL", 0.65), ("890 mL", 1.0)], 6.29, 0.7),
        "Salad Dressing": (["Ranch", "Caesar", "Italian", "Balsamic", "Greek", "Thousand Island",
                            "Raspberry Vinaigrette"], [("475 mL", 1.0), ("950 mL", 1.7)], 3.99, 0.9),
        "Canned Tuna": (["Flaked Light", "Chunk Light", "Solid White", "Light in Olive Oil", "Lemon Pepper"],
                        [("85 g", 0.45), ("170 g", 1.0), ("4 x 85 g", 1.6)], 2.29, 0.8),
        "Beans": (["Baked in Tomato Sauce", "Maple Baked", "Red Kidney", "Chickpeas", "Black Beans", "Romano"],
                  [("398 mL", 1.0), ("540 mL", 1.3)], 1.79, 0.8),
        "Maple Syrup": (["Amber Rich", "Golden Delicate", "Dark Robust", "Very Dark", "Organic Amber"],
                        [("250 mL", 0.5), ("540 mL", 1.0), ("1 L", 1.75)], 11.99, 0.5),
        "Honey": (["Liquid Clover", "Creamed", "Wildflower", "Buckwheat", "Blueberry Blossom"],
                  [("500 g", 0.6), ("1 kg", 1.0)], 9.99, 0.5),
        "Granola": (["Maple Almond", "Vanilla", "Honey Oat", "Fruit and Nut", "Cranberry"],
                    [("450 g", 0.6), ("750 g", 1.0)], 6.49, 0.6),
        "Instant Noodles": (["Chicken", "Beef", "Shrimp", "Spicy", "Vegetable"],
                            [("85 g", 0.12), ("12 x 85 g", 1.0)], 5.99, 0.6),
        "Vegetable Oil": (["Canola", "Vegetable", "Sunflower", "Corn", "Blended"],
                          [("946 mL", 0.5), ("1.89 L", 1.0), ("3 L", 1.45)], 6.99, 0.6),
        "Chocolate Chips": (["Semi-Sweet", "Milk", "Dark", "White", "Mini Semi-Sweet"],
                            [("270 g", 0.6), ("600 g", 1.0)], 4.99, 0.5),
        "Stock": (["Chicken", "Beef", "Vegetable", "Low Sodium Chicken", "Mushroom"],
                  [("500 mL", 0.65), ("900 mL", 1.0)], 3.29, 0.7),
        "Pickles": (["Dill", "Bread and Butter", "Garlic Dill", "Sweet Mixed", "Baby Dill"],
                    [("500 mL", 0.65), ("1 L", 1.0)], 4.49, 0.6),
    },
    "DAIRY": {
        "Yogurt": (["Vanilla", "Strawberry", "Plain", "Blueberry", "Peach", "Mixed Berry", "Raspberry"],
                   [("650 g", 1.0), ("750 g", 1.15), ("16 x 100 g", 1.7)], 4.49, 1.6),
        "Greek Yogurt": (["Plain", "Vanilla", "Honey", "Strawberry", "Coconut", "Blueberry"],
                         [("4 x 100 g", 0.5), ("500 g", 0.75), ("750 g", 1.0)], 6.49, 1.2),
        "Cheddar": (["Mild", "Medium", "Old", "Extra Old", "Marble", "Light"],
                    [("200 g", 0.5), ("400 g", 1.0), ("700 g", 1.65)], 7.99, 1.5),
        "Mozzarella": (["Part Skim", "Whole Milk", "Light", "Fior di Latte", "Bocconcini"],
                       [("340 g", 0.85), ("400 g", 1.0), ("600 g", 1.4)], 6.99, 1.0),
        "Shredded Cheese": (["Tex Mex", "Pizza Mozzarella", "Marble Cheddar", "Italiano", "Old Cheddar"],
                            [("320 g", 1.0), ("640 g", 1.85)], 7.49, 1.0),
        "Cheese Slices": (["Cheddar", "Swiss", "Marble", "Light", "Havarti"],
                          [("16 slices", 0.75), ("22 slices", 1.0)], 5.49, 0.8),
        "Cream Cheese": (["Original", "Light", "Herb and Garlic", "Chive and Onion", "Strawberry",
                          "Spicy Jalapeno"], [("227 g", 0.85), ("250 g", 1.0), ("500 g", 1.8)], 4.49, 0.9),
        "Cottage Cheese": (["2%", "1%", "4%", "Lactose Free 2%", "Fat Free"],
                           [("500 g", 0.7), ("750 g", 1.0)], 5.49, 0.6),
        "Butter": (["Salted", "Unsalted", "Spreadable", "Garlic", "Cultured Salted"],
                   [("250 g", 0.6), ("454 g", 1.0)], 7.29, 1.1),
        "Margarine": (["Original", "Light", "Olive Oil", "Non-Hydrogenated", "Plant Butter"],
                      [("427 g", 0.55), ("850 g", 1.0), ("1.36 kg", 1.5)], 6.49, 0.7),
        "Milk": (["2%", "1%", "Skim", "Homogenized", "Lactose Free 2%", "Organic 2%"],
                 [("1 L", 0.36), ("2 L", 0.58), ("4 L", 1.0)], 6.49, 1.6),
        "Flavoured Milk": (["Chocolate", "Strawberry", "Vanilla", "Dark Chocolate", "Lactose Free Chocolate"],
                           [("473 mL", 0.4), ("1 L", 0.6), ("2 L", 1.0)], 4.99, 0.7),
        "Cream": (["10% Half and Half", "18% Table", "35% Whipping", "5% Cereal", "Lactose Free 10%"],
                  [("237 mL", 0.4), ("473 mL", 0.65), ("1 L", 1.0)], 4.99, 0.9),
        "Sour Cream": (["14%", "Light 7%", "Fat Free", "Lactose Free", "Organic 14%"],
                       [("250 mL", 0.6), ("500 mL", 1.0), ("750 mL", 1.3)], 3.49, 0.7),
        "Eggs": (["Large White", "Large Brown", "Extra Large", "Free Run Large", "Omega-3 Large", "Organic Large"],
                 [("12 pk", 1.0), ("18 pk", 1.45), ("30 pk", 2.3)], 4.69, 1.2),
        "Plant Beverage": (["Oat Original", "Almond Unsweetened", "Soy Original", "Oat Barista", "Almond Vanilla",
                            "Coconut"], [("946 mL", 0.55), ("1.89 L", 1.0)], 5.99, 0.8),
        "Kefir": (["Plain", "Strawberry", "Blueberry", "Vanilla", "Peach"],
                  [("500 mL", 0.6), ("1 L", 1.0)], 6.29, 0.4),
        "Feta": (["Classic", "Light", "Crumbled", "Herb", "Goat"],
                 [("200 g", 0.6), ("400 g", 1.0)], 7.49, 0.5),
        "Parmesan": (["Grated", "Shredded", "Wedge", "Light Grated", "Romano Blend"],
                     [("125 g", 0.5), ("250 g", 1.0)], 6.99, 0.6),
        "Havarti": (["Plain", "Dill", "Jalapeno", "Light", "Caraway"],
                    [("200 g", 0.55), ("400 g", 1.0)], 8.49, 0.4),
        "Swiss": (["Classic", "Light", "Emmental", "Baby Swiss", "Smoked"],
                  [("200 g", 0.55), ("400 g", 1.0)], 8.49, 0.4),
        "String Cheese": (["Mozzarella", "Marble", "Cheddar", "Light Mozzarella", "Twists"],
                          [("8 pk", 0.6), ("16 pk", 1.0)], 8.99, 0.5),
        "Whipped Cream": (["Original", "Light", "French Vanilla", "Lactose Free", "Coconut"],
                          [("225 g", 1.0), ("400 g", 1.6)], 4.29, 0.4),
        "Yogurt Drink": (["Strawberry", "Blueberry", "Peach", "Vanilla", "Raspberry"],
                         [("6 x 93 mL", 0.7), ("1 L", 1.0)], 4.49, 0.5),
    },
    "FROZEN": {
        "Pizza": (["Pepperoni", "Deluxe", "Three Cheese", "Hawaiian", "Margherita", "Meat Lovers", "Vegetarian"],
                  [("450 g", 0.65), ("780 g", 1.0), ("1.3 kg", 1.5)], 7.49, 1.5),
        "French Fries": (["Straight Cut", "Crinkle Cut", "Shoestring", "Seasoned", "Sweet Potato", "Steak Cut"],
                         [("650 g", 0.75), ("1 kg", 1.0), ("2 kg", 1.7)], 3.99, 1.1),
        "Ice Cream": (["Vanilla", "Chocolate", "Neapolitan", "Cookies and Cream", "Maple Walnut", "Strawberry",
                       "Mint Chip"], [("500 mL", 0.8), ("1.5 L", 1.0), ("2 L", 1.25)], 6.49, 1.4),
        "Mixed Vegetables": (["Classic Mix", "California Blend", "Peas and Carrots", "Stir Fry Blend",
                              "Corn and Peas", "Broccoli Medley"], [("750 g", 1.0), ("1 kg", 1.25), ("2 kg", 2.1)],
                             3.49, 1.0),
        "Fish Fillets": (["Haddock Battered", "Cod Breaded", "Sole", "Pollock Crispy", "Salmon Portions",
                          "Haddock Lemon Pepper"], [("400 g", 1.0), ("700 g", 1.6)], 9.49, 0.9),
        "Waffles": (["Original", "Buttermilk", "Blueberry", "Whole Grain", "Chocolate Chip"],
                    [("280 g", 1.0), ("560 g", 1.7)], 3.79, 0.7),
        "Perogies": (["Cheddar", "Potato and Onion", "Bacon and Cheddar", "Cottage Cheese", "Jalapeno Cheddar"],
                     [("907 g", 1.0), ("2 kg", 1.8)], 5.29, 0.7),
        "Frozen Berries": (["Wild Blueberries", "Strawberries", "Raspberries", "Mixed Berries", "Cherries"],
                           [("600 g", 1.0), ("1.5 kg", 2.0)], 6.49, 0.8),
        "Chicken Nuggets": (["Original", "Breaded", "Spicy", "Whole Grain", "Popcorn"],
                            [("700 g", 0.75), ("907 g", 1.0), ("1.6 kg", 1.6)], 10.99, 0.8),
        "Burgers": (["Beef", "Angus Beef", "Chicken", "Turkey", "Plant Based"],
                    [("1.13 kg", 1.0), ("2.27 kg", 1.85)], 15.99, 0.6),
        "Pot Pies": (["Chicken", "Beef", "Turkey", "Vegetable", "Steak and Mushroom"],
                     [("200 g", 0.3), ("4 x 200 g", 1.0)], 7.99, 0.5),
        "Entrees": (["Lasagna", "Chicken Alfredo", "Mac and Cheese", "Beef Stroganoff", "Shepherd's Pie",
                     "Butter Chicken"], [("283 g", 0.5), ("907 g", 1.0)], 8.99, 0.8),
        "Frozen Treats": (["Vanilla Fudge Bars", "Strawberry Fruit Bars", "Ice Cream Sandwiches", "Mango Bars",
                           "Chocolate Cones"], [("6 pk", 1.0), ("12 pk", 1.7)], 6.49, 0.7),
        "Garlic Bread": (["Classic", "Cheese", "Texas Toast", "Whole Wheat", "Herb"],
                         [("400 g", 1.0), ("675 g", 1.5)], 4.49, 0.5),
        "Shrimp": (["Cooked Medium", "Raw Large", "Cooked Jumbo", "Breaded", "Raw Peeled"],
                   [("340 g", 0.5), ("680 g", 1.0)], 15.99, 0.5),
    },
    "BAKERY": {
        "Bagels": (["Plain", "Sesame", "Everything", "Cinnamon Raisin", "Whole Wheat", "Blueberry", "Multigrain"],
                   [("6 pk", 1.0), ("12 pk", 1.8)], 4.29, 1.3),
        "Sliced Bread": (["White", "60% Whole Wheat", "100% Whole Wheat", "Multigrain", "Rye", "Sourdough",
                          "Oatmeal"], [("570 g", 0.9), ("675 g", 1.0)], 3.99, 1.8),
        "Muffins": (["Blueberry", "Banana Nut", "Chocolate Chip", "Bran", "Lemon Poppyseed", "Carrot",
                     "Cranberry Orange"], [("4 pk", 0.75), ("6 pk", 1.0), ("12 pk", 1.8)], 5.99, 1.0),
        "Tortillas": (["Original", "Whole Wheat", "Multigrain", "Spinach", "Corn", "Ancient Grain"],
                      [("6 pk", 0.7), ("10 pk", 1.0), ("20 pk", 1.7)], 4.29, 0.9),
        "Dinner Rolls": (["White", "Whole Wheat", "Multigrain", "Ciabatta", "Potato", "Brioche"],
                         [("6 pk", 0.6), ("12 pk", 1.0), ("24 pk", 1.7)], 4.29, 0.9),
        "English Muffins": (["Original", "Whole Wheat", "Multigrain", "Sourdough", "Cinnamon Raisin"],
                            [("6 pk", 1.0), ("12 pk", 1.8)], 3.49, 0.8),
        "Hamburger Buns": (["White", "Whole Wheat", "Sesame", "Brioche", "Potato"],
                           [("8 pk", 1.0), ("12 pk", 1.4)], 3.79, 0.7),
        "Hot Dog Buns": (["White", "Whole Wheat", "Top Sliced", "Brioche", "Multigrain"],
                         [("8 pk", 1.0), ("12 pk", 1.4)], 3.79, 0.6),
        "Croissants": (["Butter", "Mini Butter", "Chocolate", "Almond", "Whole Wheat"],
                       [("6 pk", 1.0), ("12 pk", 1.8)], 5.49, 0.7),
        "Pita": (["White", "Whole Wheat", "Multigrain", "Greek Style", "Pocket"],
                 [("6 pk", 1.0), ("12 pk", 1.7)], 3.29, 0.6),
        "Loaf Cake": (["Lemon", "Banana", "Marble", "Carrot", "Chocolate"],
                      [("400 g", 0.8), ("500 g", 1.0)], 5.99, 0.5),
        "Cinnamon Buns": (["Classic", "Cream Cheese Iced", "Raisin", "Caramel Pecan", "Maple"],
                          [("4 pk", 0.7), ("6 pk", 1.0)], 6.49, 0.5),
        "Naan": (["Original", "Garlic", "Whole Wheat", "Butter", "Mini"],
                 [("5 pk", 1.0), ("10 pk", 1.8)], 4.29, 0.5),
    },
    "MEAT": {
        "Bacon": (["Original", "Thick Cut", "Maple", "Low Sodium", "Fully Cooked", "Applewood Smoked"],
                  [("375 g", 0.75), ("500 g", 1.0), ("1 kg", 1.85)], 7.49, 1.5),
        "Sausages": (["Mild Italian", "Hot Italian", "Breakfast", "Honey Garlic", "Bratwurst", "Maple"],
                     [("375 g", 0.8), ("500 g", 1.0), ("1 kg", 1.8)], 6.99, 1.2),
        "Ground Beef": (["Lean", "Extra Lean", "Medium", "Sirloin Extra Lean", "Regular"],
                        [("450 g", 1.0), ("900 g", 1.9), ("1.36 kg", 2.75)], 7.49, 1.3),
        "Chicken Breasts": (["Boneless Skinless", "Bone-In", "Air Chilled", "Lemon Pepper", "Organic Boneless"],
                            [("600 g", 0.65), ("1 kg", 1.0), ("2 kg", 1.9)], 15.99, 1.3),
        "Ham": (["Black Forest", "Honey", "Smoked", "Maple", "Old Fashioned"],
                [("175 g", 1.0), ("375 g", 1.9)], 4.99, 0.9),
        "Pork Chops": (["Boneless Centre Cut", "Bone-In Rib End", "Butterfly", "Thin Cut", "Garlic Seasoned"],
                       [("500 g", 0.6), ("800 g", 1.0), ("1.5 kg", 1.8)], 10.99, 0.9),
        "Chicken Thighs": (["Boneless Skinless", "Bone-In", "Teriyaki", "Air Chilled", "Skin-On"],
                           [("700 g", 0.7), ("1 kg", 1.0), ("2 kg", 1.85)], 11.99, 0.9),
        "Chicken Wings": (["Plain", "Honey Garlic", "Buffalo", "Salt and Pepper", "BBQ"],
                          [("800 g", 0.8), ("1 kg", 1.0), ("2 kg", 1.9)], 13.99, 0.8),
        "Pork Tenderloin": (["Plain", "Garlic and Herb", "Peppercorn", "Teriyaki", "Maple"],
                            [("500 g", 0.6), ("1 kg", 1.0)], 12.99, 0.6),
        "Beef Steak": (["Striploin", "Sirloin", "Ribeye", "Top Sirloin", "Flank"],
                       [("300 g", 0.6), ("500 g", 1.0)], 15.99, 0.8),
        "Meatballs": (["Italian Style", "Swedish", "Turkey", "Homestyle", "Cocktail"],
                      [("907 g", 1.0), ("1.8 kg", 1.8)], 10.99, 0.6),
        "Wieners": (["Original", "All Beef", "Chicken", "Jumbo", "Cheese"],
                    [("450 g", 1.0), ("900 g", 1.8)], 4.99, 0.8),
        "Ground Turkey": (["Lean", "Extra Lean", "Italian Seasoned", "Taco Seasoned", "Regular"],
                          [("450 g", 1.0), ("900 g", 1.85)], 7.99, 0.5),
    },
    "DELI PACKAGED": {
        "Hummus": (["Original", "Roasted Red Pepper", "Garlic", "Spicy", "Lemon", "Pine Nut"],
                   [("227 g", 1.0), ("454 g", 1.7)], 4.29, 1.3),
        "Salami": (["Genoa", "Hungarian", "Calabrese", "Light", "Milano"],
                   [("150 g", 1.0), ("300 g", 1.8)], 5.49, 1.0),
        "Turkey Breast": (["Oven Roasted", "Smoked", "Honey", "Peppered", "Low Sodium"],
                          [("175 g", 1.0), ("375 g", 1.9)], 5.49, 1.1),
        "Dip": (["French Onion", "Spinach", "Ranch", "Tzatziki", "Jalapeno Cheddar", "Dill Pickle"],
                [("227 g", 0.75), ("340 g", 1.0), ("454 g", 1.25)], 3.79, 1.0),
        "Coleslaw": (["Creamy", "Tangy", "Classic", "Light", "Broccoli"],
                     [("454 g", 1.0), ("908 g", 1.7)], 4.29, 0.7),
        "Potato Salad": (["Classic", "Mustard", "Egg", "Dill", "Bacon Ranch"],
                         [("454 g", 1.0), ("908 g", 1.7)], 4.29, 0.7),
        "Pepperoni Sticks": (["Mild", "Hot", "Honey Garlic", "Turkey", "Original"],
                             [("150 g", 0.65), ("350 g", 1.0)], 7.99, 0.8),
        "Roast Beef": (["Shaved", "Rare", "Peppered", "Italian", "Low Sodium"],
                       [("175 g", 1.0), ("300 g", 1.6)], 6.99, 0.7),
        "Pasta Salad": (["Italian", "Greek", "Pesto", "Caesar", "Macaroni"],
                        [("454 g", 1.0), ("908 g", 1.7)], 4.99, 0.6),
        "Guacamole": (["Classic", "Spicy", "Mild", "Chunky", "Lime"],
                      [("227 g", 0.6), ("454 g", 1.0)], 6.99, 0.5),
        "Smoked Salmon": (["Atlantic", "Sockeye", "Peppered", "Maple", "Dill"],
                          [("120 g", 0.6), ("200 g", 1.0)], 11.99, 0.5),
        "Prosciutto": (["Classic", "Thinly Sliced", "Smoked", "Herb", "Spicy"],
                       [("80 g", 0.5), ("150 g", 1.0)], 7.99, 0.4),
    },
    "SNACKS": {
        "Potato Chips": (["Original", "Salt and Vinegar", "BBQ", "Sour Cream and Onion", "Ketchup", "Dill Pickle",
                          "All Dressed", "Lightly Salted"], [("40 g", 0.35), ("200 g", 1.0), ("235 g", 1.1)],
                         4.29, 1.8),
        "Tortilla Chips": (["Restaurant Style", "Lime", "Nacho Cheese", "Multigrain", "Scoops", "Blue Corn"],
                           [("300 g", 1.0), ("500 g", 1.5)], 4.49, 1.1),
        "Cookies": (["Chocolate Chip", "Oatmeal Raisin", "Double Chocolate", "Shortbread", "Ginger Snap",
                     "Fudge Striped", "Peanut Butter"], [("300 g", 1.0), ("350 g", 1.1), ("600 g", 1.8)], 3.99, 1.5),
        "Granola Bars": (["Chocolate Chip", "Peanut Butter", "Oats and Honey", "Mixed Berry", "Dipped Chocolate",
                          "Peanut Free"], [("6 pk", 0.75), ("8 pk", 1.0), ("16 pk", 1.8)], 4.29, 1.0),
        "Microwave Popcorn": (["Butter", "Light Butter", "Kettle Corn", "Natural", "Extra Butter"],
                              [("3 pk", 0.6), ("6 pk", 1.0), ("12 pk", 1.75)], 4.49, 0.7),
        "Pretzels": (["Mini Twists", "Rods", "Sticks", "Thins", "Unsalted Twists"],
                     [("300 g", 0.8), ("400 g", 1.0), ("750 g", 1.6)], 3.69, 0.6),
        "Chocolate Bar": (["Milk", "Dark 70%", "Caramel", "Almond", "Mint", "Crispy", "Hazelnut"],
                          [("100 g", 1.0), ("170 g", 1.5), ("4 x 45 g", 1.7)], 2.79, 1.1),
        "Nuts": (["Salted Peanuts", "Deluxe Mixed", "Roasted Almonds", "Cashews", "Unsalted Mixed", "Pistachios",
                  "Honey Roasted Peanuts"], [("275 g", 0.5), ("600 g", 1.0), ("1 kg", 1.6)], 9.49, 0.9),
        "Rice Cakes": (["Lightly Salted", "Unsalted", "Caramel", "Apple Cinnamon", "Multigrain"],
                       [("150 g", 1.0), ("300 g", 1.8)], 2.99, 0.4),
        "Cheese Puffs": (["Original", "Crunchy", "Baked", "Spicy", "Jalapeno"],
                         [("200 g", 1.0), ("310 g", 1.4)], 3.99, 0.6),
        "Gummies": (["Fruit", "Sour", "Bears", "Worms", "Peach Rings"],
                    [("180 g", 0.6), ("350 g", 1.0)], 3.49, 0.6),
        "Trail Mix": (["Classic", "Tropical", "Chocolate", "Cranberry", "Energy"],
                      [("300 g", 0.45), ("800 g", 1.0)], 9.99, 0.4),
        "Licorice": (["Red", "Black", "Strawberry", "Cherry", "Raspberry"],
                     [("250 g", 0.55), ("454 g", 1.0)], 3.49, 0.4),
        "Fruit Snacks": (["Mixed Berry", "Strawberry", "Tropical", "Sour", "Peach"],
                         [("10 pk", 0.5), ("22 pk", 1.0)], 6.49, 0.5),
        "Pita Chips": (["Sea Salt", "Garlic", "Cinnamon Sugar", "Everything", "Multigrain"],
                       [("227 g", 1.0), ("400 g", 1.6)], 4.49, 0.4),
    },
    "BEVERAGES": {
        "Orange Juice": (["Original", "No Pulp", "Some Pulp", "Calcium Added", "Low Acid"],
                         [("1 L", 0.55), ("1.75 L", 1.0), ("2.63 L", 1.4)], 5.49, 1.5),
        "Apple Juice": (["Unsweetened", "Clear", "Cloudy", "McIntosh", "Honeycrisp"],
                        [("1 L", 0.55), ("1.89 L", 1.0), ("8 x 200 mL", 0.9)], 3.79, 1.1),
        "Cranberry Cocktail": (["Original", "Light", "Raspberry", "Grape", "Pomegranate"],
                               [("1 L", 0.6), ("1.89 L", 1.0)], 4.79, 0.7),
        "Sparkling Water": (["Lime", "Lemon", "Natural", "Grapefruit", "Mixed Berry", "Raspberry", "Orange"],
                            [("1 L", 0.25), ("12 x 355 mL", 1.0), ("24 x 355 mL", 1.75)], 6.49, 1.2),
        "Spring Water": (["Natural", "Alkaline", "Electrolyte", "Sport Cap", "Glacier"],
                         [("4 L", 0.5), ("12 x 500 mL", 0.6), ("24 x 500 mL", 1.0)], 4.99, 1.0),
        "Cola": (["Regular", "Diet", "Zero Sugar", "Caffeine Free", "Cherry"],
                 [("2 L", 0.45), ("6 x 710 mL", 0.85), ("12 x 355 mL", 1.0)], 8.49, 1.3),
        "Ginger Ale": (["Regular", "Diet", "Zero Sugar", "Cranberry", "Golden"],
                       [("2 L", 0.45), ("6 x 710 mL", 0.85), ("12 x 355 mL", 1.0)], 8.49, 0.9),
        "Root Beer": (["Regular", "Diet", "Zero Sugar", "Cream Soda", "Vanilla"],
                      [("2 L", 0.45), ("12 x 355 mL", 1.0)], 8.49, 0.6),
        "Iced Tea": (["Lemon", "Peach", "Raspberry", "Green Tea", "Half and Half", "Unsweetened"],
                     [("500 mL", 0.3), ("1.89 L", 0.55), ("12 x 341 mL", 1.0)], 6.99, 0.9),
        "Sports Drink": (["Fruit Punch", "Lemon Lime", "Orange", "Blue Raspberry", "Grape", "Cool Blue"],
                         [("710 mL", 0.17), ("946 mL", 0.2), ("12 x 591 mL", 1.0)], 13.99, 0.8),
        "Energy Drink": (["Original", "Sugar Free", "Tropical", "Berry", "Mango"],
                         [("473 mL", 0.3), ("4 x 473 mL", 1.0)], 10.49, 0.6),
        "Coffee Pods": (["Medium Roast", "Dark Roast", "Decaf", "Breakfast Blend", "French Vanilla", "Colombian"],
                        [("12 pk", 0.5), ("30 pk", 1.0), ("72 pk", 2.1)], 16.99, 0.9),
        "Lemonade": (["Original", "Pink", "Raspberry", "Strawberry", "Light"],
                     [("1.75 L", 1.0), ("2.63 L", 1.35)], 4.49, 0.6),
        "Tomato Juice": (["Original", "Low Sodium", "Spicy", "Garden Vegetable", "Organic"],
                         [("946 mL", 0.6), ("1.89 L", 1.0)], 3.99, 0.4),
        "Juice Boxes": (["Apple", "Fruit Punch", "Grape", "Orange", "Tropical"],
                        [("8 x 200 mL", 0.85), ("10 x 200 mL", 1.0), ("32 x 200 mL", 2.7)], 4.49, 0.8),
        "Kombucha": (["Ginger", "Raspberry", "Original", "Lemon", "Hibiscus"],
                     [("355 mL", 0.3), ("4 x 355 mL", 1.0)], 11.99, 0.4),
        "Hot Chocolate": (["Original", "Milk Chocolate", "Dark Chocolate", "Salted Caramel", "Light"],
                          [("8 x 28 g", 0.55), ("450 g", 1.0)], 5.49, 0.6),
    },
    "HOUSEHOLD": {
        "Paper Towels": (["Select-A-Size", "Regular", "Double Roll", "Triple Roll", "Strong"],
                         [("2 rolls", 0.4), ("6 rolls", 1.0), ("12 rolls", 1.8)], 10.99, 1.3),
        "Bathroom Tissue": (["Double Roll", "Ultra Soft", "Strong", "Triple Roll", "Septic Safe", "Comfort"],
                            [("6 rolls", 0.55), ("12 rolls", 1.0), ("24 rolls", 1.85)], 10.49, 1.4),
        "Dish Soap": (["Original", "Lemon", "Free and Clear", "Antibacterial", "Lavender", "Apple"],
                      [("473 mL", 0.75), ("739 mL", 1.0), ("1.2 L", 1.4)], 4.29, 1.0),
        "Laundry Detergent": (["Original", "Free and Clear", "Spring Fresh", "Cold Water", "Lavender",
                               "Mountain Fresh"], [("1.47 L", 0.65), ("2.03 L", 1.0), ("4.43 L", 1.85)], 13.99, 1.2),
        "Garbage Bags": (["Kitchen Drawstring", "Large Black", "Lawn and Leaf", "Scented Kitchen",
                          "Clear Recycling"], [("20 bags", 0.6), ("40 bags", 1.0), ("80 bags", 1.75)], 9.99, 0.9),
        "Aluminum Foil": (["Regular", "Heavy Duty", "Non-Stick", "Extra Wide", "BBQ"],
                          [("15 m", 0.6), ("30 m", 1.0), ("60 m", 1.7)], 5.99, 0.6),
        "Food Wrap": (["Clear", "Press and Seal", "Microwave Safe", "Heavy Duty", "Cling"],
                      [("30 m", 0.6), ("60 m", 1.0)], 4.99, 0.5),
        "Storage Bags": (["Large Freezer", "Medium Freezer", "Sandwich", "Snack", "Large Slider"],
                         [("25 bags", 0.7), ("50 bags", 1.0)], 5.49, 0.6),
        "Dishwasher Detergent": (["Original", "Lemon", "Free and Clear", "Power", "Fresh Scent"],
                                 [("25 pods", 0.6), ("60 pods", 1.0)], 14.99, 0.7),
        "All Purpose Cleaner": (["Lemon", "Original", "Lavender", "Unscented", "Disinfecting"],
                                [("650 mL", 0.6), ("950 mL", 1.0), ("2.84 L", 1.9)], 4.99, 0.7),
        "Fabric Softener": (["Original", "Unscented", "Lavender", "Fresh", "Spring"],
                            [("1.53 L", 0.6), ("2.95 L", 1.0)], 9.99, 0.6),
        "Facial Tissue": (["Ultra Soft", "Lotion", "Everyday", "Cube", "Hypoallergenic"],
                          [("3 pk", 0.55), ("6 pk", 1.0)], 8.99, 0.7),
        "Light Bulbs": (["LED Soft White", "LED Daylight", "LED Warm White", "Dimmable", "Candelabra"],
                        [("2 pk", 0.5), ("4 pk", 1.0)], 9.99, 0.4),
        "Batteries": (["AA", "AAA", "C", "D", "9V"], [("4 pk", 0.55), ("8 pk", 1.0)], 11.99, 0.6),
        "Bleach": (["Regular", "Splash Free", "Lemon", "Lavender", "Gel"],
                   [("1.89 L", 0.6), ("3.57 L", 1.0)], 4.49, 0.5),
    },
    "HEALTH BEAUTY": {
        "Shampoo": (["Moisturizing", "Volumizing", "Anti-Dandruff", "Clarifying", "2 in 1", "Colour Care"],
                    [("250 mL", 0.7), ("400 mL", 1.0), ("750 mL", 1.6)], 7.99, 1.4),
        "Conditioner": (["Moisturizing", "Volumizing", "Smooth", "Colour Care", "Repair"],
                        [("250 mL", 0.7), ("400 mL", 1.0), ("750 mL", 1.6)], 7.99, 1.0),
        "Toothpaste": (["Whitening", "Cavity Protection", "Sensitive", "Fresh Mint", "Tartar Control", "Kids"],
                       [("75 mL", 0.8), ("100 mL", 1.0), ("2 x 100 mL", 1.8)], 4.29, 1.3),
        "Body Wash": (["Original", "Sensitive", "Sport", "Shea Butter", "Coconut", "Charcoal"],
                      [("355 mL", 0.75), ("532 mL", 1.0), ("1 L", 1.6)], 8.49, 1.0),
        "Deodorant": (["Unscented", "Fresh Scent", "Sport", "Powder", "Clinical"],
                      [("48 g", 0.7), ("85 g", 1.0), ("2 x 85 g", 1.8)], 6.49, 1.0),
        "Body Lotion": (["Unscented", "Daily Moisture", "Aloe", "Shea", "Intensive Repair"],
                        [("200 mL", 0.65), ("400 mL", 1.0), ("600 mL", 1.35)], 8.99, 0.7),
        "Bar Soap": (["Original", "Moisturizing", "Unscented", "Oatmeal", "Aloe"],
                     [("4 x 90 g", 0.6), ("8 x 90 g", 1.0)], 7.99, 0.6),
        "Mouthwash": (["Fresh Mint", "Cool Mint", "Alcohol Free", "Whitening", "Total Care"],
                      [("500 mL", 0.6), ("1 L", 1.0), ("1.5 L", 1.35)], 7.49, 0.7),
        "Hand Soap": (["Original", "Aloe", "Lavender", "Antibacterial", "Unscented"],
                      [("250 mL", 0.4), ("1 L", 1.0)], 7.99, 0.6),
        "Razors": (["Twin Blade", "Triple Blade", "Sensitive Triple", "Smooth Triple", "Five Blade"],
                   [("4 pk", 0.6), ("10 pk", 1.0)], 12.99, 0.5),
        "Cotton Swabs": (["Original", "Organic", "Precision", "Baby", "Antibacterial"],
                         [("300 pk", 0.65), ("500 pk", 1.0)], 4.99, 0.4),
        "Lip Balm": (["Original", "Medicated", "Cherry", "Mint", "Vanilla"],
                     [("2 pk", 0.6), ("4 pk", 1.0)], 5.99, 0.4),
    },
    "PET": {
        "Dry Dog Food": (["Chicken and Rice", "Beef", "Lamb and Rice", "Small Breed", "Senior", "Puppy", "Salmon"],
                         [("2 kg", 0.3), ("8 kg", 1.0), ("15 kg", 1.65)], 32.99, 1.4),
        "Dry Cat Food": (["Chicken", "Salmon", "Indoor", "Seafood", "Kitten", "Turkey"],
                         [("1.4 kg", 0.35), ("3.2 kg", 0.7), ("7 kg", 1.0)], 27.99, 1.2),
        "Wet Cat Food": (["Chicken Pate", "Salmon Pate", "Turkey Chunks", "Tuna Flakes", "Mixed Grill"],
                         [("12 x 85 g", 1.0), ("24 x 85 g", 1.85)], 12.99, 1.1),
        "Cat Litter": (["Unscented Clumping", "Scented Clumping", "Multi-Cat", "Lightweight", "Non-Clumping"],
                       [("5 kg", 0.6), ("9 kg", 1.0), ("14 kg", 1.4)], 13.99, 1.0),
        "Dog Treats": (["Chicken Jerky", "Beef Biscuits", "Dental Chews", "Peanut Butter Biscuits",
                        "Bacon Strips"], [("200 g", 0.55), ("500 g", 1.0), ("1 kg", 1.7)], 8.99, 1.0),
        "Wet Dog Food": (["Beef Stew", "Chicken Dinner", "Lamb", "Turkey", "Puppy"],
                         [("374 g", 0.11), ("12 x 374 g", 1.0)], 24.99, 0.7),
        "Cat Treats": (["Chicken", "Salmon", "Catnip", "Dental", "Tuna"],
                       [("85 g", 0.6), ("170 g", 1.0)], 4.99, 0.6),
        "Bird Seed": (["Wild Bird Mix", "Sunflower", "Nyjer", "Finch", "Cardinal"],
                      [("3.5 kg", 0.45), ("9 kg", 1.0)], 16.99, 0.4),
    },
    "BABY": {
        "Diapers": (["Newborn", "Size 1", "Size 2", "Size 3", "Size 4", "Size 5", "Size 6"],
                    [("30 pk", 0.55), ("56 pk", 1.0), ("120 pk", 1.85)], 26.99, 1.5),
        "Baby Wipes": (["Unscented", "Sensitive", "Fresh Scent", "Water Based", "Aloe"],
                       [("72 pk", 0.35), ("216 pk", 1.0), ("504 pk", 1.95)], 10.99, 1.2),
        "Baby Food": (["Apple", "Pear", "Sweet Potato", "Banana", "Carrot", "Peas", "Mixed Fruit"],
                      [("128 mL", 1.0), ("4 x 128 mL", 3.3)], 1.39, 1.2),
        "Infant Formula": (["Iron Fortified", "Sensitive", "Gentle", "Soy", "Lactose Free"],
                           [("658 g", 1.0), ("915 g", 1.3)], 39.99, 0.8),
        "Training Pants": (["Size 2T-3T", "Size 3T-4T", "Size 4T-5T", "Night 3T-4T", "Night 4T-5T"],
                           [("22 pk", 0.55), ("46 pk", 1.0)], 23.99, 0.6),
        "Baby Cereal": (["Rice", "Oat", "Mixed Grain", "Barley", "Multigrain with Fruit"],
                        [("227 g", 1.0), ("454 g", 1.8)], 4.49, 0.5),
        "Teething Biscuits": (["Original", "Banana", "Apple", "Blueberry", "Sweet Potato"],
                              [("12 pk", 0.6), ("24 pk", 1.0)], 5.49, 0.4),
    },
}

# brand names: a place or nature word, then a word that says what the brand makes
PREFIX = ["Harvest", "Northcove", "Ridgeway", "Maple Crest", "Bay Ridge", "Fundy", "Clearwater", "Old Mill",
          "Brightfield", "Tidewell", "Sunnyhill", "Cobequid", "Lunenburg", "Atlantic", "Valley", "Highland",
          "Kingsport", "Seaside", "Annapolis", "Minas", "Sable", "Acadia", "Shoreline", "Harbourside", "Pinecrest",
          "Cedar Point", "Birchwood", "Stonebridge", "Meadowvale", "Willow Creek", "Silver Birch", "Bluenose",
          "Greenfield", "Redcliff", "Saltwater", "Sandy Cove", "Wildrose", "Grand Pre", "Port Royal", "Riverbend",
          "Brookside", "Oakhill", "Island Light", "Schooner", "Lighthouse", "Anchor", "Compass Rose", "Puffin",
          "Heron", "Bayview", "Seabright", "Windsor", "Wolfville", "Chester", "Baddeck", "Margaree",
          "Tatamagouche", "Parrsboro", "Granville", "Pictou", "Mahone Bay", "Cape North", "Glen Haven", "Hubbards"]
SUFFIX = {
    "GROCERY": ["Pantry", "Kitchen", "Provisions", "Foods", "Table", "Harvest", "Select", "Naturals", "Gold"],
    "DAIRY": ["Dairy", "Creamery", "Farms", "Pastures", "Meadows"],
    "FROZEN": ["Kitchen", "Foods", "Farms", "Frozen Foods", "Table"],
    "BAKERY": ["Bakery", "Bakehouse", "Oven", "Mill", "Hearth"],
    "MEAT": ["Meats", "Smokehouse", "Butchers", "Farms", "Provisions"],
    "DELI PACKAGED": ["Deli", "Charcuterie", "Kitchen", "Fine Foods", "Smokehouse"],
    "SNACKS": ["Snacks", "Snack Co.", "Confections", "Kettle", "Treats"],
    "BEVERAGES": ["Springs", "Beverages", "Orchards", "Soda Works", "Drinks"],
    "HOUSEHOLD": ["Home", "Essentials", "Clean", "Household", "Basics"],
    "HEALTH BEAUTY": ["Naturals", "Botanicals", "Care", "Labs", "Apothecary"],
    "PET": ["Pet", "Pet Co.", "Pet Foods", "Pet Supply", "Animal Care"],
    "BABY": ["Baby", "Baby Care", "Infant Care", "Nursery", "Kids"],
}
PRIVATE_LABEL = "Saltmarsh"
ENDINGS = [0.99, 0.49, 0.79, 0.29, 0.69]
ENDING_W = np.array([0.42, 0.22, 0.14, 0.10, 0.12])
VOWELS = set("AEIOU")


def squeeze(word, n):
    """the pricing system's short form of one description part (the same rule world.abbrev applies)"""
    w = re.sub(r"[^A-Z0-9]", "", word.upper())
    if len(w) <= n:
        return w
    keep = w[0] + "".join(ch for ch in w[1:] if ch not in VOWELS)
    return (keep if len(keep) >= 3 else w)[:n]


def short_key(brand, noun, size):
    return (squeeze(brand, 6), squeeze(noun, 6), size.upper().replace(" ", ""))


def brands_for(dept, rng, need, taken, taken_short):
    """brands for one department, each with its own product line, until the lines hold `need` brand-product-size
    combinations; the chain's own label carries every product the department sells"""
    spec = SPECS[dept]
    nouns = list(spec)
    w = np.array([spec[n][3] for n in nouns])
    brands = [(PRIVATE_LABEL, nouns)]
    room = sum(len(spec[n][1]) for n in nouns)
    names = [p + " " + s for p in PREFIX for s in SUFFIX[dept]]
    order = rng.permutation(len(names))
    for j in order:
        if room >= need:
            break
        name = names[j]
        if name in taken or squeeze(name, 6) in taken_short:
            continue
        taken.add(name)
        taken_short.add(squeeze(name, 6))
        k = int(np.clip(round(len(nouns) * rng.uniform(0.25, 0.7)), 2, len(nouns)))
        line = [nouns[i] for i in sorted(rng.choice(len(nouns), size=k, replace=False, p=w / w.sum()))]
        brands.append((name, line))
        room += sum(len(spec[n][1]) for n in line)
    if room < need:
        raise RuntimeError("catalogue: %s needs %d brand-product-size combinations, only %d" % (dept, need, room))
    return brands


def retexture(w):
    """dress every family drawn by world.items() as one brand's product in one size, with its varieties and its
    regular price; rewrites w.desc, w.parts, w.famname and w.reg in place, drawing on its own stream"""
    rng = np.random.default_rng([P.SEED, 41])
    fam_ids = sorted(set(int(f) for f in w.fam))
    members = {f: [] for f in fam_ids}
    for i, f in enumerate(w.fam):
        members[int(f)].append(i)
    dept_of = {f: str(w.dept[members[f][0]]) for f in fam_ids}
    need = {}
    for f in fam_ids:
        need[dept_of[f]] = need.get(dept_of[f], 0) + 1
    taken, taken_short = {PRIVATE_LABEL}, {squeeze(PRIVATE_LABEL, 6)}
    universe = {}
    for dept in SPECS:
        if dept not in need:
            continue
        spec = SPECS[dept]
        combos, wts = [], []
        for brand, line in brands_for(dept, rng, int(need[dept] * 1.5) + 20, taken, taken_short):
            for noun in line:
                sizes = spec[noun][1]
                for size, _ in sizes:
                    combos.append((brand, noun, size))
                    wts.append(spec[noun][3] / len(sizes) * (2.5 if brand == PRIVATE_LABEL else 1.0))
        keys = rng.random(len(combos)) ** (1.0 / np.array(wts))
        universe[dept] = [combos[i] for i in np.argsort(-keys)]
    pointer = {d: 0 for d in universe}
    used_short = set()
    desc = list(w.desc)
    parts = list(w.parts)
    reg = np.array(w.reg, dtype=float)
    famname = {}
    for f in fam_ids:
        d = dept_of[f]
        mem = members[f]
        lst = universe[d]
        while True:
            if pointer[d] >= len(lst):
                raise RuntimeError("catalogue: %s ran out of brand-product-size combinations" % d)
            brand, noun, size = lst[pointer[d]]
            pointer[d] += 1
            sk = short_key(brand, noun, size)
            if sk not in used_short:
                used_short.add(sk)
                break
        vars_, sizes, base, _ = SPECS[d][noun]
        factor = dict(sizes)[size]
        if len(mem) == 1:
            vs = [""]
        else:
            vs, seen = [], set()
            for j in rng.permutation(len(vars_)):
                v = vars_[int(j)]
                if squeeze(v, 5) in seen:
                    continue
                seen.add(squeeze(v, 5))
                vs.append(v)
                if len(vs) == len(mem):
                    break
        if len(vs) < len(mem):
            raise RuntimeError("catalogue: %s has fewer distinct varieties than family %d needs" % (noun, f))
        p = base * factor * float(np.exp(rng.normal(0.0, 0.10)))
        end = ENDINGS[int(rng.choice(len(ENDINGS), p=ENDING_W / ENDING_W.sum()))]
        price = round(float(np.floor(p)) + end, 2) if p >= 1.0 else 0.99
        famname[f] = "%s %s %s" % (brand, noun, size)
        for i, v in zip(mem, vs):
            parts[i] = (brand, noun, v, size)
            desc[i] = " ".join(x for x in (brand, noun, v, size) if x)
            reg[i] = price
    w.desc = np.array(desc)
    w.parts = parts
    w.famname = famname
    w.reg = reg
