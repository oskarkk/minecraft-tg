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

def add(id):
    id = str(id)
    idList = get()
    if id in idList: return
    idList.append(id)
    save(idList)

def remove(id):
    id = str(id)
    idList = get()
    if id in idList:
        idList.remove(id)
        save(idList)