import sys

sys.path.append('../')

from lib import *

@singleton
class markath01(Room):

    def __init__(self):

        super().__init__()

        self.setDescription( {
            "de": "Du befindest dich im Startraum.",
            "en": "You're in the starting room."
        } )

        self.addDetail("startraum", "Du befindest dich mitten drin.")

        self.addDirection("osten", "world.markath.kraemer01")

        banana = Banane()

        messer = Knife()

        messer.setDescription("Ein Messer.")

        messer.setShortDescription("Ein Messer.")

        messer.setGender(NEUTER)

        self.addItem(banana)

        box = Box()

        box.setName('kiste')

        box.setGender(FEMALE)

        box.setDescription("Eine hölzerne Kiste mit silbernen Beschlägen.")

        box.setShortDescription("Eine hölzerne Kiste")

        box.addItem(messer)

        self.addItem(box)

@singleton
class kraemer01(Room):

    def __init__(self):

        super().__init__()

        self.addProperty("__is_shop__", True)

        self.setDescription("Dies ist ein ganz gewöhnlicher Laden. Hier kannst Du allen möglichen Kram kaufen und verkaufen.")

        self.addDetail("laden", "Hier gibt es Kram zu kaufen.")

        self.addDetail("kram", "Kram von überall her. Du kannst ihn kaufen.")

        self.addDirection("westen", "world.markath.markath01")

        #banana = Banane()

        #banana.setDescription("Diese Banane ist schon ganz matschig.")
        
        #banana.setShortDescription("Eine faule Banane.")
        
        #banana.addIdentity("faule banane")
        
        #banana.setHealthiness(0)

        #seller = Seller("verkäufer", MALE)
        
        #seller.setDescription("Ein Verkäufer. Er schaut dich mit einem wissendem Lächeln an. Du kannst bei ihm kaufen und verkaufen.")
        
        #seller.setShortDescription("Ein Verkäufer.")
        
        #seller.addItem(banana)
        
        #seller.addMoney(1000)

        #self.addCreature(seller)
