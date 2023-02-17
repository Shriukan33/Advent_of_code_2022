# Input
with open("aoc_01_input.txt") as f:
    data = f.read().splitlines()

# Part 1

# Recreate the inventories of the elves
# When encountering an empty string, sum the previous
# inputs and start a new inventory
current_calories_count = 0
all_inventories_totals = []
for snack in data:
    if snack == "":
        all_inventories_totals.append(current_calories_count)
        current_calories_count = 0
    else:
        current_calories_count += int(snack)

print("Highest number of calories :", max(all_inventories_totals))


# Part 2

# Get the 3 highest numbers of calories in all_inventories_totals
# and sum them

# Sort the list
all_inventories_totals.sort()

# Get the 3 highest numbers
highest_calories = all_inventories_totals[-3:]

# Sum them
print("Highest number of calories (sum top 3):", sum(highest_calories))
