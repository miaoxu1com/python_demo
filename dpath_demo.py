import json

import dpath

x = {
    "a": {
        "b": {
            "3": 2,
            "43": 30,
            "c": [],
            "d": ['red', 'buggy', 'bumpers'],
        }
    }
}
result = dpath.search(x, "a/b/[cd]")
print(result)

# Setting existing keys
dpath.set(x, 'a/b/[cd]', 'Waffles')
print(json.dumps(x, indent=4, sort_keys=True))

# Adding new keys
dpath.new(x, 'a/b/e/f/g', "Roffle")
print(json.dumps(x, indent=4, sort_keys=True))
# Deleting Existing Keys
dpath.delete(x, 'a/b/c', separator='/', afilter=None)
print(json.dumps(x, indent=4, sort_keys=True))

# Merging
y = {'a': {'b': {'e': {'f': {'h': [None, 0, 1, None, 13, 14]}}}, 'c': 'RoffleWaffles'}}

dpath.merge(x, y)
print(json.dumps(x, indent=4, sort_keys=True))
