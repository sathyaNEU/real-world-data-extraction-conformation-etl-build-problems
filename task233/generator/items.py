"""The field-collected item list: code, group, description, unit, base price (dollars)."""

ITEMS = [
    # Fresh fruit and vegetables
    ("011601", "FV", "Apples, loose", "per kg", 4.49), ("011602", "FV", "Bananas, loose", "per kg", 3.49),
    ("011603", "FV", "Oranges, loose", "per kg", 3.99), ("011604", "FV", "Pears, loose", "per kg", 4.29),
    ("011605", "FV", "Kiwifruit, green", "per kg", 5.49), ("011606", "FV", "Avocado, medium", "each", 2.29),
    ("011607", "FV", "Grapes, green seedless", "per kg", 8.99), ("011608", "FV", "Strawberries", "250 g punnet", 4.99),
    ("011701", "FV", "Potatoes, washed", "per kg", 2.79), ("011702", "FV", "Carrots, loose", "per kg", 2.49),
    ("011703", "FV", "Onions, brown", "per kg", 2.69), ("011704", "FV", "Tomatoes, loose", "per kg", 6.99),
    ("011705", "FV", "Lettuce, iceberg", "each", 3.49), ("011706", "FV", "Broccoli", "each", 2.99),
    ("011707", "FV", "Cabbage, half", "each", 3.29), ("011708", "FV", "Capsicum, red", "per kg", 9.99),
    ("011709", "FV", "Cucumber, telegraph", "each", 2.79), ("011710", "FV", "Mushrooms, button", "per kg", 12.99),
    ("011711", "FV", "Pumpkin, crown", "per kg", 2.19), ("011712", "FV", "Sweet potato, orange", "per kg", 4.99),
    # Meat, fish and poultry
    ("011201", "MF", "Beef mince, regular", "per kg", 14.99), ("011202", "MF", "Beef sirloin steak", "per kg", 32.99),
    ("011203", "MF", "Lamb loin chops", "per kg", 27.99), ("011204", "MF", "Pork shoulder chops", "per kg", 15.99),
    ("011205", "MF", "Chicken breast, skinless", "per kg", 16.99), ("011206", "MF", "Chicken, whole fresh", "per kg", 8.49),
    ("011207", "MF", "Sausages, beef", "per kg", 11.99), ("011208", "MF", "Bacon, middle rashers", "per kg", 19.99),
    ("011209", "MF", "Ham, sliced champagne", "per kg", 21.99), ("011301", "MF", "Fish fillets, fresh hoki", "per kg", 22.99),
    ("011302", "MF", "Tuna in springwater", "185 g can", 2.99),
    # Bread and cereals
    ("011101", "BC", "Bread, white toast", "600 g loaf", 3.29), ("011102", "BC", "Bread, wholemeal", "700 g loaf", 4.19),
    ("011103", "BC", "Bread rolls, white", "6 pack", 3.79), ("011104", "BC", "Breakfast cereal, wheat biscuits", "750 g box", 5.99),
    ("011105", "BC", "Rolled oats", "750 g bag", 3.49), ("011106", "BC", "Rice, long grain", "1 kg bag", 3.19),
    ("011107", "BC", "Pasta, spaghetti", "500 g packet", 1.99), ("011108", "BC", "Flour, plain", "1.5 kg bag", 2.89),
    ("011109", "BC", "Biscuits, chocolate chip", "250 g packet", 3.59),
    # Milk, cheese and eggs
    ("011401", "DE", "Milk, standard", "2 litre bottle", 4.39), ("011402", "DE", "Milk, trim", "1 litre bottle", 2.59),
    ("011403", "DE", "Cheese, mild block", "1 kg block", 13.49), ("011404", "DE", "Butter, salted", "500 g block", 7.99),
    ("011405", "DE", "Yoghurt, plain", "1 kg pottle", 5.49), ("011406", "DE", "Eggs, size 7 barn", "dozen", 8.99),
    ("011407", "DE", "Cream, fresh", "300 ml bottle", 3.29),
    # Other food and non-alcoholic drinks
    ("011901", "OF", "Coffee, instant", "200 g jar", 9.99), ("011902", "OF", "Tea bags", "100 pack", 5.49),
    ("011903", "OF", "Sugar, white", "1.5 kg bag", 3.39), ("011904", "OF", "Jam, strawberry", "500 g jar", 4.29),
    ("011905", "OF", "Peanut butter, smooth", "375 g jar", 4.79), ("011906", "OF", "Tomato sauce", "560 ml bottle", 3.19),
    ("011907", "OF", "Baked beans", "420 g can", 1.89), ("011908", "OF", "Potato chips", "150 g bag", 3.29),
    ("011909", "OF", "Chocolate block", "200 g block", 4.49), ("011910", "OF", "Ice cream, vanilla", "2 litre tub", 6.99),
    ("011911", "OF", "Frozen peas", "1 kg bag", 3.99), ("011912", "OF", "Cooking oil, canola", "1 litre bottle", 5.99),
    ("012101", "OF", "Soft drink, cola", "1.5 litre bottle", 3.29), ("012102", "OF", "Orange juice", "2 litre bottle", 5.49),
    ("012103", "OF", "Water, still", "1.5 litre bottle", 1.79),
    # Household supplies
    ("056101", "HS", "Dishwashing liquid", "1 litre bottle", 4.49), ("056102", "HS", "Laundry powder", "1 kg box", 8.99),
    ("056103", "HS", "Toilet paper", "12 roll pack", 9.49), ("056104", "HS", "Paper towels", "2 roll pack", 4.29),
    ("056105", "HS", "Rubbish bags", "20 pack", 4.99), ("056106", "HS", "Light bulb, LED 9W", "each", 4.99),
    ("056107", "HS", "Batteries, AA alkaline", "4 pack", 7.99), ("056108", "HS", "Surface cleaning spray", "500 ml bottle", 5.29),
    ("056109", "HS", "Aluminium foil", "10 m roll", 3.99),
    # Personal care
    ("121301", "PC", "Toothpaste", "110 g tube", 3.49), ("121302", "PC", "Shampoo", "400 ml bottle", 6.99),
    ("121303", "PC", "Conditioner", "400 ml bottle", 6.99), ("121304", "PC", "Soap, bar", "4 pack", 4.49),
    ("121305", "PC", "Deodorant, roll-on", "50 ml", 5.99), ("121306", "PC", "Sunscreen SPF50", "200 ml tube", 14.99),
    ("121307", "PC", "Paracetamol tablets", "20 pack", 3.99), ("121308", "PC", "Razor cartridges", "4 pack", 17.99),
    ("121309", "PC", "Facial tissues", "180 pack", 3.29), ("121310", "PC", "Multivitamin tablets", "60 pack", 16.99),
    ("121311", "PC", "Sanitary pads", "14 pack", 5.49), ("121312", "PC", "Nappies, disposable", "40 pack", 24.99),
    # Clothing and footwear
    ("031201", "CF", "Jeans, men's", "each", 69.99), ("031202", "CF", "Jeans, women's", "each", 74.99),
    ("031203", "CF", "T-shirt, men's cotton", "each", 24.99), ("031204", "CF", "Top, women's knit", "each", 39.99),
    ("031205", "CF", "Jacket, children's", "each", 49.99), ("031206", "CF", "Socks, men's", "3 pack", 14.99),
    ("031207", "CF", "Briefs, women's", "3 pack", 19.99), ("032101", "CF", "Running shoes, adult", "pair", 119.99),
    ("032102", "CF", "School shoes, children's", "pair", 89.99), ("031208", "CF", "Dress, women's", "each", 89.99),
]

# items an outlet kind can carry (by code); kinds not listed take every item of their groups
KIND_ITEMS = {
    "convenience": ["011401", "011402", "011404", "011406", "011101", "011103", "011907", "011908", "011909",
                    "012101", "012103", "011902", "011903", "056103", "056101", "011910"],
    "hardware": ["056106", "056107", "056108", "056105", "056109", "056101"],
    "pharmacy_chain": ["121301", "121302", "121303", "121304", "121305", "121306", "121307", "121308", "121309",
                       "121310", "121311", "121312", "056107"],
    "pharmacy": ["121301", "121302", "121304", "121305", "121306", "121307", "121309", "121310", "121311"],
    "bakery": ["011101", "011102", "011103", "011109"],
}
