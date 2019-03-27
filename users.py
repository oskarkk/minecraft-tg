filename = 'users.csv'

def get():
    try:
        with open(filename, 'r+') as f:
            return f.read().replace('\n','').split(',')
    except FileNotFoundError:
        return []

def save(x):
    with open(filename, 'w') as f:
        f.write(','.join(x))

def add(name):
    namesList = get()
    if name in namesList: return
    namesList.append(name)
    save(namesList)