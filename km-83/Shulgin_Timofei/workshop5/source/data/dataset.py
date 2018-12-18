file = open('data/orders.csv')
lines = file.read().splitlines()
reqData = [i.split(', ') for i in lines[1:]]
dataset = dict()
for buy in reqData:
    client, date, prod, quan, price = [i for i in buy]
    if client in dataset.keys():
        if date in dataset[client].keys():
            dataset[client][date][prod] = {'price': price, 'quantity': quan}
        else:
            dataset[client][date] = {prod: {'price': price, 'quantity': quan}}
    else:
        dataset[client] = {date: {prod: {'price': price, 'quantity': quan}}}
file.close()