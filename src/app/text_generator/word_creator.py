import random, os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/text_generator/'


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
	person = make_list('person')
	where = make_list('where')
	go = make_list('go')
	do = make_list('do')
	return random.choice(person)+'と'+random.choice(where)+'に'+random.choice(go)
def go_specific(place): #place must be char
	person = make_list('person')
	where = make_list('where')
	go = make_list('go')
	do = make_list('do')
	return random.choice(person)+'と'+ place +'に'+random.choice(go)
def do_random():
	person = make_list('person')
	where = make_list('where')
	go = make_list('go')
	do = make_list('do')
	return random.choice(person)+'と'+random.choice(where)+'で'+random.choice(do)
def do_specific(event):
	person = make_list('person')
	where = make_list('where')
	go = make_list('go')
	do = make_list('do')
	return random.choice(person)+'と'+random.choice(where)+'で'+str(event)+'した。'
def rand_generation():
	person = make_list('person')
	where = make_list('where')
	event = make_list('event')
	go = make_list('go')
	do = make_list('do')

	i = random.getrandbits(1)
	if i == 0:
		place_key = random.choice(where)
		return {'text': go_specific(place_key), 'keyword': place_key}
	else:
		event_key = random.choice(event)
		return {'text': do_specific(event_key), 'keyword': event_key}

