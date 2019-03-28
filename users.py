filename = 'users.csv'

def get():
    try:
        with open(filename, 'r+') as f:
            x = f.read().replace('\n','')
            if not x: return []
            return x.split(',')
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

def remove(name):
    namesList = get()
    if name in namesList:
        namesList.remove(name)
        save(namesList)