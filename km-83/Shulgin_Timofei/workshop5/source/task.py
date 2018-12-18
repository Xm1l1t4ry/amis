import plotly
import plotly.graph_objs as go
from data.dataset import dataset

# Які продукти купляли усі покупці?
def getProductsSet(dataset):
    all_prod = []
    for client in dataset.values():
        for date in client.values():
            all_prod.extend(list(date.keys()))
    return set(all_prod)

# Як змінювалась ціна на яблука? (графік)
def getApplePrice(dataset):
    apple_dict = dict()
    for client in dataset:
        for date in dataset[client]:
            for prod in dataset[client][date]:
                if prod == 'apple':
                    price = float(dataset[client][date][prod]['price'])/float(dataset[client][date][prod]['quantity'])
                    apple_dict[date] = price
    keys = list(apple_dict.keys())
    keys.sort()
    sorted_dict = dict()
    for key in keys:
        for date in apple_dict:
            if date == key:
                sorted_dict[date] = apple_dict[date]
    plotly.offline.plot([go.Scatter(x=list(sorted_dict.keys()),y=list(sorted_dict.values()))], filename='appleprice.html')

# Скільки грошей витрачає кожний покупець на покупки? (графік)
def buyerExpenditure(dataset):
    expend = dict()
    for client in dataset:
        if client not in expend:
            expend[client] = 0
        for date in dataset[client]:
            for prod in dataset[client][date]:
                expend[client] += float(dataset[client][date][prod]['price'])
    plotly.offline.plot([go.Bar(x=list(expend.keys()), y=list(expend.values()))], filename='expenditure.html')

# Який найпопулярніший товар? Якого товару було куплено найменше?
def getPopularProd(dataset):
    popular_prod = {}
    for client in dataset:
        for date in dataset[client]:
            for product in dataset[client][date]:
                if product in popular_prod:
                    popular_prod[product] += float(dataset[client][date][product]['quantity'])
                else:
                    popular_prod[product] = float(dataset[client][date][product]['quantity'])

    cnt_max, cnt_min = 0, list(popular_prod.values())[0]
    most_popular, least_popular = None, None
    for product in popular_prod:
        if popular_prod[product] > cnt_max:
            cnt_max = popular_prod[product]
            most_popular = product
        elif popular_prod[product] < cnt_min:
            cnt_min = popular_prod[product]
            least_popular = product
    return '''Найпопулярніший продукт - {0}
Товару, якого було куплено найменше - {1}'''.format(most_popular, least_popular)

# Який найдорожчий товар?
def getMostExpensive(dataset):
    max_cnt, most_expensive = 0, None
    for client in dataset:
        for date in dataset[client]:
            for product in dataset[client][date]:
                price = float(dataset[client][date][product]['price'])/float(dataset[client][date][product]['quantity'])
                if price > max_cnt:
                    most_expensive = product
                    max_cnt = price
    return most_expensive

# Якого товару, скільки покупців купляє? (графік)
def getBoughtByAmount(dataset):
    counter = dict()
    for client in dataset:
        bought = set()
        for date in dataset[client]:
            for prod in dataset[client][date]:
                bought.add(prod)
        for buy in bought:
            if buy not in counter:
                counter[buy] = 0
            counter[buy] += 1
    plotly.offline.plot([go.Pie(labels=list(counter.keys()),values=list(counter.values()))], filename='bought.html')

# Написати функціонал для додавання нових даних
def addData(dataset):

    def addProd(prod=dict()):
        decision = input('Додати куплений продукт? y/n\n')
        if decision == 'y':
            title, price, quan = map(input, ('Назва продукту: ',
                                             'Ціна: ',
                                             'Кількість: '))
            prod[title] = {'price': price, 'quantity': quan}
            return addProd(prod)
        elif decision == 'n':
            return prod
        else:
            print('Невірна команда')
            return addProd(prod)

    client, date = map(input, ('Ім\'я покупця: ',
                               'Дата покупки: '))
    products = addProd()
    if client in dataset:
        if date in dataset[client]:
            for prod in products:
                dataset[client][date][prod] = products[prod]
        else:
            for prod in products:
                dataset[client][date] = products[prod]
    else:
        dataset[client] = {date: products}