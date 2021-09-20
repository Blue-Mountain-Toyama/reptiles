import random
path = 'D:/repositories/made_by_nakayama/text_generator/'

def make_list(name): #name must be char
	with open(path + name + '.txt', 'r', encoding='UTF-8') as f:
	    contents = [x.strip() for x in f.readlines()]
	return(contents)

person = make_list('person')
where = make_list('where')
go = make_list('go')
do = make_list('do')

cats = {
	0: 'no',
	1: 'go',
	2: 'do',
}

def go_random():
	return(print(random.choice(person)+'と'+random.choice(where)+'に'+random.choice(go)))
def go_specific(place): #place must be char
	return(print(random.choice(person)+'と'+ place +'に'+random.choice(go)))
def do_random():
	return(print(random.choice(person)+'と'+random.choice(where)+'で'+random.choice(do)))
def rand_generation():
	i = random.getrandbits(1)
	if i == 0:
		return(go_random())
	else:
		return(do_random())

#go_specific('京都')
print(rand_generation())
"""
for i in cats:
	print(i)
"""