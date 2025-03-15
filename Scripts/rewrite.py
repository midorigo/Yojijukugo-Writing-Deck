import json

output_file = "rewrite_output.txt"

l = []

def run(input_file):
	print("Executing...")

	with open(input_file, 'r', encoding="utf-8") as f:
		data = json.load(f)
	
	loop(data)
	
	with open(output_file, 'w', encoding='utf-8') as o:
		for i in l:
			o.write(f"{i}\n") #TODO: There is likely a more idiomatic way to write lines to a file.

	print(f"Successfully wrote to file: {output_file}")

def loop(data):
	if isinstance(data, dict):
		for i in data:
			loop(data[i])
	elif isinstance(data, list):
		for i in data:
			loop(i)
	else:
		l.append(data)

if __name__ == "__main__":
	import sys
	run(str(sys.argv[1]))