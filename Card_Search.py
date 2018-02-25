# Calls needed libraries
import json
import requests
import csv


query = input("Welcome to MTG Management.\n"
	      "Please choose the cooresponding number from the options below.\n"
	      "   1) Search for a card or group of cards.\n"
	      "   2) Build or modify a Decklist.\n"
	      "   3) Manage your collection.\n")

# Defines Card_Search function
def Card_Search():
	# Requests query information from User, NEED TO ADD FORMATTING AND INSTRUCTIONS TO MATCH SCRYFALL API
	query = input("\nInput requested search words.\n")

	# search_cards :: string -> [dataObjs]
	def search_cards(query):
		url = "https://api.scryfall.com/cards/search?q=%s" % (query)
		response = requests.get(url).json()["data"]
		return response

	# return_card_names :: [dataObj] -> [string]
	def return_card_names(card_list):
		return list(map(lambda x: x["name"], card_list))

	# get_card_data :: string -> string -> object
	#def get_card_data(set, id):
	#	url = "https://api.scryfall.com/cards/%s/%s?format=json" % (set,str(id))
	#	response = requests.get(url).json()
	#	return response

	search_results = search_cards(query)
	names = return_card_names(search_results)

	# loop through return_card_names to make a numbered list
	x = 0
	for x in range(len(names)):
		print("%d) %s" % (x+1,names[x])) 

	# result input for user to choose from numbered list
	number_choice_array = input("\nChoose a number or numbers from the list above.\nSeparate multiples using commas (no spaces)\n").split(",")

	# Prints the names of the cards chosen in the previous input function
	for x in number_choice_array:
		print(names[int(x)-1])

	selected_card_array = []

	# Inserts the chosen cards into selected_card_array
	for x in number_choice_array:
		selected_card_array = selected_card_array + [search_results[int(x)-1]]

	# Saves card info into .csv named by file_name
	file_name = "selected_card_info.csv"
	with open(file_name, 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
				    quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for item in selected_card_array:
			spamwriter.writerow([item["name"]])
			if 'mana_cost' in item:
				spamwriter.writerow([item["cmc"],item["mana_cost"]])
			else:
				spamwriter.writerow([item["cmc"]])
			spamwriter.writerow([item["type_line"]])
			spamwriter.writerow([item["oracle_text"]])
			if 'power' in item:
				spamwriter.writerow([item["power"],item["toughness"]])
			if 'colors' in item:
				spamwriter.writerow([item["colors"]])
			if 'flavor_text' in item:
				spamwriter.writerow([item["flavor_text"]])
			spamwriter.writerow([item["set_name"],item["set"],item["collector_number"]])
			if 'usd' in item:
				spamwriter.writerow(["$%s" % (item["usd"])])
			spamwriter.writerow([""])
	
	# Ask user if they need to change a set on a chosen card
	query = input("\nDo you need a specific printing of any card? Y/N \n")
	
	if query == "Y" or "y" and len(selected_card_array) > 1:
		selected_card_names = return_card_names(selected_card_array)	
		
		print("Your chosen cards are as follows:")	
		x = 0
		for x in range(len(selected_card_names)):
			print("%d) %s" % (x+1,selected_card_names[x])) 

		number_choice = input("\nChoose one number from the list above.\n").split(",")
		
	
	return

if query == "1":
	Card_Search()
quit()
