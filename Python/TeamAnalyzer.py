import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    try: 
        pokedex_num = int(arg)
    except ValueError: 
        print(f"Error: Invalid pokedex number {arg}")
        sys.exit 
    

    #query returns the entire row where the pokedex_number matches
    conn = sqlite3.connect('pokemon.sqlite')
    c = conn.cursor()
    query = """
    SELECT *
    FROM pokemon 
    WHERE pokedex_number = ?
    """
    c.execute(query, (arg,))
    pokemon_name = c.fetchone()
    new_pokemon_name = pokemon_name[2]
    # print(new_pokemon_name)

    #query_1 gives type1 and type2 information from pokemon_Types_view
    query1 = """
    SELECT type1, type2
    FROM pokemon_types_view
    WHERE name = ?
    
    """
    c.execute(query1, (new_pokemon_name,))
    two_type_names = c.fetchone()

    #query2 gives information that matches up with pokemon type 1 and type 2
    query2 = """
    SELECT *
    FROM pokemon_types_battle_view 
    WHERE type1name = ? AND type2name = ?
    """
    c.execute(query2, (two_type_names[0], two_type_names[1]))
    type_id = c.fetchone()

    new_type = type_id[2:]
    pokemon_types = {}
    for v, k in zip(types, new_type): 
        pokemon_types[v] = k


    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1

    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    strength = []
    weakness = []
    for i in pokemon_types.keys():
        if pokemon_types[i]> 1:
            strength.append(i)
        elif pokemon_types[i] < 1:
            weakness.append(i)

    print(f"Analyzing {arg}")
    print(f"{new_pokemon_name} ({two_type_names[0]}{' '+ two_type_names[1] if two_type_names[1] else ''}) is strong against {strength} but weak against {weakness}")

    conn.close()

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

