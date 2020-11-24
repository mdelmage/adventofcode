TARGET = 909441
recipes = '37'
elf1 = 0
elf2 = 1

while True:
    if len(recipes) % 1000000 == 0:
        index = recipes.find(str(TARGET))
        if index > 0:
            print 'Recipes: ' + recipes[TARGET:TARGET+10]
            print 'Index: %d' % recipes.find(str(TARGET))
            break

    new_recipe = int(recipes[elf1]) + int(recipes[elf2])
    if new_recipe > 9:
        recipes += str(new_recipe / 10)
        recipes += str(new_recipe % 10)
    else:
        recipes += str(new_recipe)

    elf1 = (elf1 + int(recipes[elf1]) + 1) % len(recipes)
    elf2 = (elf2 + int(recipes[elf2]) + 1) % len(recipes)
