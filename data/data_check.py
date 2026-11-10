import pandas as pd
import openpyxl as op

runef = pd.DataFrame(pd.read_excel("runef.xlsx", dtype=str)).fillna("")
cooking_table = pd.DataFrame(
    pd.read_excel("cooking_table.xlsx", header=None, dtype=str)
).fillna("")
frying_pan = pd.DataFrame(
    pd.read_excel("frying_pan.xlsx", header=None, dtype=str)
).fillna("")
knife = pd.DataFrame(pd.read_excel("knife.xlsx", header=None, dtype=str)).fillna("")
mixer = pd.DataFrame(pd.read_excel("mixer.xlsx", header=None, dtype=str)).fillna("")
oven = pd.DataFrame(pd.read_excel("oven.xlsx", header=None, dtype=str)).fillna("")
pot = pd.DataFrame(pd.read_excel("pot.xlsx", header=None, dtype=str)).fillna("")
steamer = pd.DataFrame(pd.read_excel("steamer.xlsx", header=None, dtype=str)).fillna("")

# make menus dataframe
equipments = ["cooking_table", "frying_pan", "knife", "mixer", "oven", "pot", "steamer"]

menus = pd.DataFrame(
    columns=["menu", "level", "sellprice", "rp", "equipment", "ingredients", "effects"]
)

for tool in equipments:
    tot_item = int(globals()[tool].shape[0] / 3)

    for _ in range(tot_item):
        # for _ in range(0, 2):

        name = globals()[tool][0][_ * 3].lower().strip().replace(" ", "_")
        level = int(globals()[tool][4][_ * 3])
        sellprice = int(globals()[tool][4][(_ * 3) + 1].replace("G", ""))

        ingredient = ""
        for __ in range(1, 7):
            if __ % 3 == 0:
                ing = (
                    globals()[tool][3][(_ * 3 + 1) if (__ > 3) else (_ * 3)]
                    .lower()
                    .strip()
                    .replace(" ", "_")
                )
            else:
                ing = (
                    globals()[tool][__ % 3][(_ * 3 + 1) if (__ > 3) else (_ * 3)]
                    .lower()
                    .strip()
                    .replace(" ", "_")
                )

            if len(ing) != 0:
                ingredient += (("+") if (__ != 1) else ("")) + ing

        effect = globals()[tool][1][_ * 3 + 2]

        menus.loc[len(menus)] = [name, level, sellprice, 0, tool, ingredient, effect]


runef["Name"] = runef["Name"].str.lower().str.strip().str.replace(" ", "_")

print(menus[0:11])

inventory = pd.DataFrame(columns=["ingredient", "quantity"])
crafting_recipe = pd.DataFrame(columns=["product", "ingredients"])

deleted_menu = []
inventory_list = []
fst = ["type:jam", "type:squid", "type:mushroom"]

for idx in range(0, len(menus)):
    recipe_list = menus["ingredients"][idx].split("+")

    for item in recipe_list:
        if menus["menu"].str.fullmatch(item, case=False, na=False).any():
            if item not in deleted_menu:
                deleted_menu.append(item)

                product = menus[
                    menus["menu"].str.fullmatch(item, case=False, na=False)
                ].reset_index(drop=True)

                crafting_recipe.loc[len(crafting_recipe)] = [
                    product["menu"][0],
                    product["ingredients"][0],
                ]

                craft_ing = product["ingredients"][0].split("+")
                for inge in craft_ing:
                    if (item in fst) or (inge in fst):
                        continue
                    else:
                        if inge not in inventory_list:
                            inventory_list.append(inge)
                            inventory.loc[len(inventory)] = [inge, 5]
        else:
            if item in fst:
                continue
            else:
                if item not in inventory_list:
                    inventory_list.append(item)
                    inventory.loc[len(inventory)] = [item, 5]


ingredient_types = pd.DataFrame()
ingredient_types["ingredient"] = [
    "lamp_squid",
    "squid",
    "sunsquid",
    "mushroom",
    "monarch_mushroom",
    "grape_jam",
    "apple_jam",
    "strawberry_jam",
]
ingredient_types["type"] = [
    "squid",
    "squid",
    "squid",
    "mushroom",
    "mushroom",
    "jam",
    "jam",
    "jam",
]

for item in ingredient_types["ingredient"]:
    if item not in inventory_list:
        inventory_list.append(item)
        inventory.loc[len(inventory)] = [item, 5]

spec = ["grape_jam", "apple_jam", "strawberry_jam"]
for item in spec:
    deleted_menu.append(item)
    product = menus[
        menus["menu"].str.fullmatch(item, case=False, na=False)
    ].reset_index(drop=True)

    crafting_recipe.loc[len(crafting_recipe)] = [
        product["menu"][0],
        product["ingredients"][0],
    ]

menus = menus[~menus["menu"].isin(deleted_menu)].reset_index(drop=True)

for i in range(0, len(inventory)):
    print(str(i) + " : " + inventory["ingredient"][i])

crafting_recipe.loc[len(crafting_recipe)] = ["mixed_herbs", "green_grass+toyherb"]
crafting_recipe.loc[len(crafting_recipe)] = ["sweet_powder", "apple"]
crafting_recipe.loc[len(crafting_recipe)] = ["sour_drop", "orange"]
crafting_recipe.loc[len(crafting_recipe)] = ["heavy_spice", "purple_grass"]

print(inventory)
print(crafting_recipe)
print(deleted_menu)

inventory.to_csv("inventory.csv", index=False)
inventory.to_excel("inventory.xlsx", index=False)
crafting_recipe.to_csv("crafting_recipes.csv", index=False)
crafting_recipe.to_excel("crafting_recipes.xlsx", index=False)
menus.to_csv("menus.csv", index=False)
menus.to_excel("menus.xlsx", index=False)
ingredient_types.to_csv("ingredient_types.csv", index=False)
ingredient_types.to_excel("ingredient_types.xlsx", index=False)
