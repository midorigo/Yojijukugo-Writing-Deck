import json

all_yojijukugo = {}

test_list = [
	["空前絶後", "alah", "blah", "clah", "意味", "stuff", "more stuff", "This is the meaning of this Yojijukugo", "even more stuff", "使い方", 0, "This is how you use this Yojijukugo"],
	["前代未聞", "alah", "blah", "clah", "意味", "stuff", "more stuff", "This is the meaning of this Yojijukugo", "even more stuff", "使い方", 0, "This is how you use this Yojijukugo"],
	["国士無双", "alah", "blah", "clah", "意味", "stuff", "more stuff", "This is the meaning of this Yojijukugo", "even more stuff", "使い方", 0, "This is how you use this Yojijukugo"]
	]

def get_value_from_list(l, k, offset):
	i = l.index(k)
	value = l[i + offset]
	return value

for i in test_list:
	yojijukugo = i[0]
	meaning = get_value_from_list(i, "意味", 3)
	usage = get_value_from_list(i, "使い方", 2)
	all_yojijukugo[yojijukugo] = {"意味": meaning, "使い方": usage}

print(all_yojijukugo)

