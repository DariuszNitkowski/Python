class Cake:
    bakery_offer = []

    def __init__(self, name, kind, taste, additives, filling):

        self.name = name
        self.kind = kind
        self.taste = taste
        self.additives = additives.copy()
        self.filling = filling
        self.bakery_offer.append(self)

    def show_info(self):
        print("{}".format(self.name.upper()))
        print("Kind:        {}".format(self.kind))
        print("Taste:       {}".format(self.taste))
        if len(self.additives) > 0:
            print("Additives:")
            for a in self.additives:
                print("\t\t{}".format(a))
        if len(self.filling) > 0:
            print("Filling:     {}".format(self.filling))
        print('-' * 20)

    def add_additives(self, additives):
        self.additives.extend(additives)

    def __str__(self):# to jest do printu instancji
        return "ciastko {} typu:{} o smaku{}. Składniki to:{}".format(self.name, self.kind, self.taste, self.additives)
    def __iadd__(self, other): # to wbudowana funkcja do dodawania w instacji wybranych cech
        self.additives.append(other)
        return self

cake01 = Cake('Vanilla Cake','cake', 'vanilla', ['chocolade', 'nuts'], 'cream')
cake01 += "milk" # tak dodaje i wykorzystuje iadd!!!
print(cake01)
"""
class NoDuplicates:
    def __init__(self, funct):
        self.funct=funct
    def __call__(self, cake, additives):
        no_duplicate_list=[]
        for i in additives:
            if i not in cake.additives:
                no_duplicate_list.append(i)
        self.funct(cake, no_duplicate_list)


@NoDuplicates
def add_extra_additives(cake, additives):
    cake.add_additives(additives)


add_extra_additives(cake01, ['strawberries', 'sugar-flowers'])
cake01.show_info()

add_extra_additives(cake01, ['strawberries', 'sugar-flowers', 'chocolade', 'nuts'])
cake01.show_info()
"""