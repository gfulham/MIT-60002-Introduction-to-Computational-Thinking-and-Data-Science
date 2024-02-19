class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w

    def getValue(self):
        return self.value

    def getCost(self):
        return self.calories

    def density(self):
        return self.getValue()/self.getCost()

    def __str__(self):
        return f"{self.name}: < {self.value}, {self.calories} >"

    def buildMenu(names, values, calories):
        """names, values, calories lists of same length.
        name a list of strings
        values and calories lists of numbers
        returns list of Foods"""
        menu = []
        for i in range(len(values)):
            menu.append(Food(names[i], values[i], calories[i]))
        return menu

    def greedy(items, maxCost, keyFunction):
        """Assumes item a list, maxCost >= 0,
        keyFcuntion maps elementns of items to numbers"""
        itemsCopy = sorted(items, key = keyFunction, reverse = True) # keyfunction can be changed

        result = []
        totalValue, totalCost = 0.0 , 0.0

        for i in range(len(itemsCopy)):
            if (totalCost + itemsCopy[i].getCost()) <= maxCost:
                result.append(itemsCopy[i])
                totalCost += itemsCopy[i].getCost()
                totalValue += itemsCopy[i].getValue()
        return (result, totalValue)

    def testGreedy(items, constraint, keyFunction):
        taken, val = greedy(items, constraint, keyFunction)
        print('Total value of items taken =', val)
        for item in taken:
            print(' ', item)

    def testGreedys(foods, maxUnits):
        print('Use greedy by value to allocate', maxUnits, 'calories')
        testGreedy(foods, maxUnits, lambda x: x.getValue())
        print('\nUse greedy by cost to allocate', maxUnits, 'calories')
        testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x))
        print('\nUse greedy by density to allocate', maxUnits, 'calories')
        testGreedy(foods, maxUnits, lambda x: x.density())

    def maxVal(toConsider, avail):
        """Assumes toConsider a list of items, avail a weight
        Returns a tuple of the total value of a solution to the
            0/1 knapsack problem and the items of that solution"""
        if toConsider == [] or avail == 0:
            result = (0, ())
        elif toConsider[0].getCost() > avail:
            #Weight of first item is greater than availble weight
            #Explore right branch only
            #Call function recursivly with remaining items and same available weight
            result = maxVal(toConsider[1:], avail)
        else:
            #Explore both brances
            nextItem = toConsider[0]
            #Explore left branch
            withVal, withToTake = maxVal(toConsider[1:], avail - nextItem.getCost())
            #Increase the value of the backpack
            withVal += nextItem.getValue()
            
            #Explore right branch
            withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
            
            #Choose better branch
            if withVal > withoutVal:
                result = (withVal, withToTake + (nextItem,))
            else:
                result = (withoutVal, withoutToTake)
        return result
