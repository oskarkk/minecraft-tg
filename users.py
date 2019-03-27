def get():
    with open('users.csv', 'r+') as f:
        return f.read().split(',')
    return []

def add(name)
    namesList = get()
    if name in namesList: return
    namesList.append(name)
    with open('users.csv', 'w') as f:
        f.write(','.join(namesList))