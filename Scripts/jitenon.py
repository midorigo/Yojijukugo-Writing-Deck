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
		reading = get_reading(sub_list)
		meaning = get_meaning(sub_list)
		level = get_level(sub_list)
		source = get_source(sub_list)
		context = get_context(sub_list)
		synonyms = get_synonyms(sub_list)
		variants = get_variants(sub_list)

		term.extend([yoji, reading, level, meaning, source, context, synonyms, variants])

		usable_list.append(term)
		
	return usable_list

def get_yoji(sub_list):
	#Yojijukugo is always at index 0
	yoji = sub_list[0]

	return yoji

def get_reading(sub_list):
	#Reading is always at index 1
	reading = sub_list[1]

	return reading

def get_meaning(sub_list):
	meaning_list = []
	meaning_str = ""
	
	i = 0

	while sub_list[sub_list.index("div") + (i + 1) * 2] == "br":
		meaning_list.append(sub_list[sub_list.index("div") + (i + 1) * 2 - 1])

		i += 1

	meaning_str = "\n".join(meaning_list)

	return meaning_str

def get_level(sub_list):
	if "漢検級" in sub_list:
		level = get_value_from_index(sub_list, "漢検級", 4)
	else:
		level = None

	return level

def get_source(sub_list):
	if "出典" in sub_list:
		source = get_value_from_index(sub_list, "出典", 2)
	else:
		source = None

	return source

def get_context(sub_list):
	context_list = []
	context_str = ""

	if "場面用途" in sub_list:
		i = 0

		while sub_list[sub_list.index("場面用途") + i * 4 + 2] == "a":
			context_list.append(sub_list[sub_list.index("場面用途")] + i * 4 + 4)

		i += 1
	else:
		context_list = None

	context_str = "・".join(context_list)

	return context_str

def get_synonyms(sub_list):
	synonym_list = []

	if "類義語" in sub_list:
		for i in sub_list[sub_list.index("類義語"):]:
			if i[0] == "t" or "a" or "?":
				continue
			elif sub_list[sub_list.index(i) + 1][0] == "t" or "a" or "?":
				synonym_list.append(i)
				continue
			else:
				break
	else:
		synonym_list = None

	synonym_str = "\n".join(synonym_list)

	return synonym_str

def get_variants(sub_list):
	variant_list = []

	if "異形" in sub_list:
		for i in sub_list[sub_list.index("異形"):]:
			if i == "td" or "tr":
				continue
			elif sub_list[sub_list.index(i) + 2] == "td":
				variant_list.append(i)
				continue
			else:
				break
	else:
		variant_list = None

	variant_str = "\n".join(variant_list)

	return variant_str


def get_value_from_index(sub_list, key, offset):
	index = sub_list.index(key)
	value = sub_list[index + offset]
	return value

def write_to_file(file, nested_list):
	with open(file, 'w', encoding='utf-8') as output:
		for i in nested_list:
			output.write("\t".join(map(str, i)) + "\n")

#Make script runnable from terminal
if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))