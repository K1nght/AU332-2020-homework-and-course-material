# buyLotsOfFruit.py
"""
To run this script, type

  python buyLotsOfFruit.py

Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}


def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples

    Returns cost of order
    """
    totalCost = 0.0
    for (fruit, numPounds) in orderList:
        if fruit in fruitPrices:
            totalCost += fruitPrices[fruit] * numPounds
        else:
            print("ERROR: %s does not appear in fruitPrices!" % fruit)
            return None
    return totalCost


# Main Method
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList1 = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)]
    print('Test1: Cost of', orderList1, 'is', buyLotsOfFruit(orderList1))
    orderList2 = [('apples', 2.0), ('pears', 3.0), ('banana', 4.0)]
    print('Test2: Cost of', orderList2, 'is', buyLotsOfFruit(orderList2))
