import json

output_file = "output.txt"

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as input:
		yomitan_dict = json.load(input)
	
	super_list = undict(yomitan_dict)

	with open(output_file, 'w', encoding='utf-8') as output:
		for i in super_list:
			for j in i:
				output.write(f"{j}\t")
			output.write("\n")

	print(f"Successfully wrote to file: {output_file}")

def undict(yomitan_dict):
	super_list = []

	def loop(data):
		if isinstance(data, dict):
			for i in data:
				loop(data[i])
		elif isinstance(data, list):
			for i in data:
				loop(i)
		else:
			sub_list.append(data)

	for i in yomitan_dict:
		sub_list = []
		loop(i)
		super_list.append(sub_list)

	usable_list = []

	for sub_list in super_list:
		term = []

		yoji = sub_list[0]
		image = get_image(sub_list)
		usage = get_usage(sub_list)

		term.append(yoji)
		term.append(image)
		term.append(usage)

		usable_list.append(term)
		
	return usable_list

def get_image(l):
	image = "\"<img src=\"\"" + l[l.index("img") + 1][4:] + "\"\">\""
	
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

def get_value_from_index(l, k, offset):
	i = l.index(k)
	v = l[i + offset]
	return v

#Make script runnable from terminal

if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))