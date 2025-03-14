#<summary>
#This script was designed to target a specific Yomitan dictionary, namely "四字熟語の百科事典 rev.2024-06-30", with data taken from 四字熟語の百科事典 (https://idiom-encyclopedia.com/).
#From the .json, it extracts the relevant information and turns it into a usable format which can be dropped straight into Anki to augment our existing deck, created by another user from 四字熟語辞典オンライン (https://yoji.jitenon.jp/).
#It first iterates over the .json to produce a more usable format in get_content.
#Then, it obtains the relevant fields, namely the image and example fields, which are what we want to add to our deck.
#Finally, it formats those fields into a .txt file that can be imported directly into Anki, adding these fields for each Yojijukugo in our existing deck.
#</summary>

import json

input_file = 'term_bank_1.json'
output_file = 'output.txt'
test_file = 'test.txt'

#Iterates through .json string composed of dictionaries and lists.
#Output is an array of indefinite length, composed of arrays of length 2.
#In the case that the entry is in a dict, appends [key, value].
#In the case that the entry is in a list, appends [index, value]...
#...Where index is the index of the entire array thus far.
def get_content(entry, content):
	if isinstance(entry, dict):
		for item in entry:
			if isinstance(entry.get(item), dict) or isinstance(entry.get(item), list):
				get_content(entry.get(item), content)
			else:
				content.append([item, entry.get(item)])
	elif isinstance(entry, list):
		for item in entry:
			get_content(item, content)
	elif entry:
		content.append([len(content), entry])
    
	return content

# /!\ Hardcoded logic unique to my purposes /!\

def get_image(content):
	image = ""
	
	for item in content:
		if item[0] == "path":
			image = item[1][4:];

	image = "\"<img src=\"\"" + image + "\"\">\""

	return image

def get_examples(content):
	array = []
	
	for item in content:
		if item[0] == "content":
			array.append(item[1])
	
	array = array[array.index("使い方") + 1:]
	yoji = content[0][1]
	examples = ""
	
	for i in array:
		examples += "<li>" + i.replace(yoji, f"<span style=\"\"color: rgb(25, 150, 250);\"\"><b>{yoji}</b></span>") + "</li>"
	
	examples = "\"<ul>" + examples + "</ul>\""

	return examples

def run():
	with open(input_file, 'r', encoding='utf-8') as file:
		data = json.load(file)

	with open(output_file, 'w', encoding='utf-8') as out:
		for entry in data:
			content = get_content(entry, [])
			
			yoji = content[0][1]
			image = get_image(content)
			examples = get_examples(content)
			
			out.write(f"{yoji}\t{image}\t{examples}\n")

			'''print(len(content))
			for item in content:
				print(f"{item[0]}\t{item[1]}")'''

	with open(test_file, 'w', encoding='utf-8') as test:
		for entry in data[:10]:
			content = get_content(entry, [])		
			for item in content:
				test.write(f"{item[0]}\t{item[1]}\n")

	print(f"Successfully wrote to file: {output_file}.")

run()