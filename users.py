filename = 'data/users.csv'

def get():
    try:
        with open(filename, 'r+') as f:
            # remove newlines just in case
            x = f.read().replace('\n','')
            # if empty file return empty list, 
            # not list with an empty string
            if not x: return []
            
            return x.split(',')
    # return empty list if file doesn't exist yet
    except FileNotFoundError:
        return []

def save(x):
    with open(filename, 'w') as f:
        f.write(','.join(x))

def add(id):
    id = str(id)
    idList = get()
    # in user is on the list already, do nothing
    if id in idList: return
    idList.append(id)
    save(idList)

def remove(id):
    id = str(id)
    idList = get()
    # do antyhing only if user is on the list
    if id in idList:
        idList.remove(id)
        save(idList)
