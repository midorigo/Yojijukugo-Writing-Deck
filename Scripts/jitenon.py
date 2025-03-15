import json

output_file = "jitenon_output.txt"
test_file = "jitenon_testing.txt"

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding='utf-8') as input:
		yomitan_dict = json.load(input)
	
	usable_list = undict(yomitan_dict)

	write_to_file(output_file, usable_list)

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
	
	write_to_file(test_file, super_list)

	#Format relevant data
	for sub_list in super_list:
		term = []

		yoji = get_yoji(sub_list) 

		term.append(yoji)

		usable_list.append(term)
		
	return usable_list

def get_yoji(sub_list):
	#Yojijukugo is always at index 0
	yoji = sub_list[0]

	return yoji

def write_to_file(file, nested_list):
	with open(file, 'w', encoding='utf-8') as output:
		for i in nested_list:
			output.write("\t".join(map(str, i)) + "\n")

#Make script runnable from terminal
if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))