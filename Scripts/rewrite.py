import json

output_file = "rewrite_output.txt"
test_output = "rewrite_test.txt"

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as f:
		yomitan_dict = json.load(f)
	
	super_list = undict(yomitan_dict)

	with open(output_file, 'w', encoding='utf-8') as o:
		for i in super_list:
			for j in i:
				o.write(f"{j}\t")
			o.write("\n")

	print(f"Successfully wrote to file: {output_file}")

def undict(yomitan_dict):
	super_list = []
	
	for i in yomitan_dict:
		l = []
		l = loop(i, l)
		super_list.append(l)
	
	usable_list = []

	for i in super_list:
		term = []

		term.append(i[0]) #yoji
		#term.append(i[1]) #reading
		term.append(get_image(i))
		#term.append(get_value_from_index(i, "意味", 10).replace("\n", "")) #meaning
		term.append(get_usage(i)) #usage

		usable_list.append(term)
		
	return usable_list

#<summary>
#Recursive function which loops through data formatted as nested lists and dictionaries (.json files) and appends values to list l = [].
#From our perspective, the keys don't tell us anything useful about their respective values, so we discard them and write our own parsing logic.
#</summary>

def loop(data, l):
	if isinstance(data, dict):
		for i in data:
			loop(data[i], l)
	elif isinstance(data, list):
		for i in data:
			loop(i, l)
	else:
		l.append(data)

	return l

def get_value_from_index(l, k, offset):
	i = l.index(k)
	value = l[i + offset]
	return value

def get_image(my_list):
	image = my_list[my_list.index("img") + 1][4:]

	image = "\"<img src=\"\"" + image + "\"\">\""

	return image

def get_usage(my_list):
	examples_list = []
	examples_str = ""
	yojijukugo = my_list[0]

	i = 0

	while my_list[my_list.index("使い方") + 11 + i * 3] == "span":
		examples_list.append(get_value_from_index(my_list, "使い方", 12 + i * 3))
		i += 1

	for example in examples_list:
		examples_str += "<li>" + example.replace(yojijukugo, f"<span style=\"\"color: rgb(25, 150, 250);\"\"><b>{yojijukugo}</b></span>") + "</li>"

	examples_str = "\"<ul>" + examples_str + "</ul>\""

	return examples_str

#Make script runnable from terminal

if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))