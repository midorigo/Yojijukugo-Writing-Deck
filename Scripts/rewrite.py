import json

output_file = "rewrite_output.txt"

l = []

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as f:
		data = json.load(f)
	
	undict(data)
	
	with open(output_file, 'w', encoding='utf-8') as o:
		for i in l:
			o.write(f"{i}\n") #TODO: There is likely a more idiomatic way to write lines to a file.

	print(f"Successfully wrote to file: {output_file}")

#<summary>
#Recursive function which loops through data formatted as nested lists and dictionaries (.json files) and appends values to list l = [], which we will then write unique parsing logic for.
#The key idea is that Yomitan dictionaries are undescriptive yet repetitive, so we can get the information we want without knowing every value's corresponding key.
#</summary>

def undict(data):
	if isinstance(data, dict):
		for i in data:
			undict(data[i])
	elif isinstance(data, list):
		for i in data:
			undict(i)
	else:
		l.append(data)

#Make script runnable from terminal

if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))