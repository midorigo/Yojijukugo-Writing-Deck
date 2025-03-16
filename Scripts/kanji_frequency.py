#Step 1: Export Anki deck as .txt   DONE
#Step 2: Parse .txt to list of all yojijukugo   DONE
#Step 3: From list, create dictionary of format (kanji): (frequency)
#Step 4: From kanji frequency dictionary, create dictionary of format (yoji): (least common kanji)
#Step 5: Export final dictionary as .txt

input_file = 'Yojijukugo (四字熟語) Writing.txt'
freq_file = 'frequency.txt'
output_file = 'output.txt'

def parse(file):
    raw_data = file.readlines()
    term_list = []
    for line in raw_data:
        #Ignore line if it starts with a # (first two lines)
        if line[0] == "#":
            continue
        term_list.append(line[0:4])
    return term_list

def get_freq_dict(term_list):
    concatinated_list = ""
    freq_dict = {}
    for term in term_list:
        concatinated_list += term
    for char in concatinated_list:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    return freq_dict

def get_uncommon_dict(term_list, freq_dict):
    uncommon_dict = {}
    for term in term_list:
        yoji_dict = {}
        for char in term:
            yoji_dict[char] = freq_dict.get(char)
        #GPT-4o taught me this trick
        uncommon_dict[term] = min(yoji_dict, key=yoji_dict.get)
    return uncommon_dict

def run():
    with open(input_file, 'r', encoding='utf-8') as file:
        term_list = parse(file)
        freq_dict = get_freq_dict(term_list)
        uncommon_dict = get_uncommon_dict(term_list, freq_dict)

    with open(freq_file, 'w', encoding = 'utf-8') as frequency:
        frequency.write(f"{freq_dict}")

    with open(output_file, 'w', encoding='utf-8') as output:
        for term in term_list:
            output.write(f"{term}\t{uncommon_dict[term]}\t{freq_dict[uncommon_dict[term]]}\n")

run()

