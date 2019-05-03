#! /usr/bin/python


def index(filename): 
    global lines, dict, posting_list
    f = open(filename, 'r')
    lines = f.readlines()
	# {str: [int, int]}
	# {token: [freq, pointer]}
    dict = {}
    pointer = 0
    line_no = 0
    posting_list = []
    # Populate the dictionary.
    for line in lines:
        line = line.rstrip().split('\t')[-1]
        # Cut the line into tokens and put into a set
        token_set = set(line.split())
        # Put the token into dictionary and count the frequency
        for token in token_set:
            # If token exists in dictionary add frequency by one
            # and update the posting list,
            # if not create a new entry with a pointer to a list.
            if dict.get(token.lower()): 
                dict[token.lower()][0] += 1
                posting_list[dict[token.lower()][1]].append(line_no)
            else:
                dict[token.lower()] = [1, pointer]
                posting_list.append([line_no])
                pointer += 1
        # Count the lines
        line_no += 1

def query1(term):
    return posting_list[dict[term][1]]

def query2(term1, term2):
    listiter1 = iter(query1(term1))
    listiter2 = iter(query1(term2))
    ans = []
    p1 = next(listiter1)
    p2 = next(listiter2)
    while True:
        try:
            if p1 == p2:
                ans.append(p1)
                p1 = next(listiter1)
                p2 = next(listiter2)
            elif p1 < p2:
                p1 = next(listiter1)
            else:
                p2 = next(listiter2)
        except StopIteration:
            break
    return ans

index("data")
for i in query2("stuttgart", "bahn"):
    print("Tweet id: ", lines[i].split("\t")[1])
    print("Text: ", lines[i].rstrip().split("\t")[-1])
