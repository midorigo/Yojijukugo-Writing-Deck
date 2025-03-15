import json

output_file = "rewrite_output.txt"
test_output = "rewrite_test.txt"

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as f:
		yomitan_dict = json.load(f)
	
	super_list = undict(yomitan_dict)
	super_dict = format_as_dict(super_list)

	with open(output_file, 'w', encoding='utf-8') as o:
		o.write(f"{super_dict}")

	print(f"Successfully wrote to file: {output_file}")

#<summary>
#Recursive function which loops through data formatted as nested lists and dictionaries (.json files) and appends values to list l = [].
#From our perspective, the keys don't tell us anything useful about their respective values, so we discard them and write our own parsing logic.
#</summary>

def undict(yomitan_dict):
	super_list = []
	
	for i in yomitan_dict:
		l = []
		l = loop(i, l)
		super_list.append(l)
	
	return super_list

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

def format_as_dict(super_list):
	super_dict = {}

	for i in super_list:
		yojijukugo = i[0]
		meaning = get_value_from_list(i, "意味", 3)
		usage = get_value_from_list(i, "使い方", 2)
		super_dict[yojijukugo] = {"意味": meaning, "使い方": usage}

	return super_dict

def get_value_from_list(l, k, offset):
	i = l.index(k)
	value = l[i + offset]
	return value

#Make script runnable from terminal

if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))