#<summary>
#This script targets a specific Yomitan dictionary: "四字熟語の百科事典 rev.2024-06-30" with data taken from 四字熟語の百科事典 (https://idiom-encyclopedia.com/).
#It takes a .json as input and outputs a .txt which can be dropped directly into Anki to augment an existing deck.
#</summary>

import json

output_file = "hyakka_output.txt"

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as input:
		yomitan_dict = json.load(input)
	
	usable_list = undict(yomitan_dict)

	write_to_file(usable_list)

	print(f"Successfully wrote to file: {output_file}")

def undict(yomitan_dict):
	super_list = []
	usable_list = []

	#Recursively loop over nested dictionary, ignoring keys while appending values to a sub-list
	def loop(data):
		if isinstance(data, dict):
			for i in data:
				loop(data[i])
		elif isinstance(data, list):
			for i in data:
				loop(i)
		else:
			sub_list.append(data)
	
	#Append sub-lists to a super-list
	for i in yomitan_dict:
		sub_list = []
		loop(i)
		super_list.append(sub_list)

	#Format relevant data
	for sub_list in super_list:
		term = []

		yoji = get_yoji(sub_list) 
		image = get_image(sub_list)
		usage = get_usage(sub_list)

		term.append(yoji)
		term.append(image)
		term.append(usage)

		usable_list.append(term)
		
	return usable_list

def get_yoji(sub_list):
	#Yojijukugo is always at index 0
	yoji = sub_list[0]

	return yoji

def get_image(sub_list):
	#Image path is identified by the "img" tag directly above it, and is formatted as "img/image.png"
	image = "\"<img src=\"\"" + sub_list[sub_list.index("img") + 1][4:] + "\"\">\""
	
	return image

def get_usage(sub_list):
	#Usage is identified by "使い方" content. Each example has "span" tag directly above it. First example is 12 lines below, then repeating every 3 lines.
	examples_list = []
	examples_str = ""
	yojijukugo = sub_list[0]

	i = 0

	while sub_list[sub_list.index("使い方") + 11 + i * 3] == "span":
		examples_list.append(get_value_from_index(sub_list, "使い方", 12 + i * 3))
		i += 1

	for example in examples_list:
		examples_str += "<li>" + example.replace(yojijukugo, f"<span style=\"\"color: rgb(25, 150, 250);\"\"><b>{yojijukugo}</b></span>") + "</li>"

	examples_str = "\"<ul>" + examples_str + "</ul>\""

	return examples_str

def get_value_from_index(sub_list, key, offset):
	index = sub_list.index(key)
	value = sub_list[index + offset]
	return value

def write_to_file(usable_list):
	with open(output_file, 'w', encoding='utf-8') as output:
		for i in usable_list:
			output.write("\t".join(i) + "\n")

#Make script runnable from terminal
if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))