from __future__ import print_function
import numpy as np


class Star(object):
    def __init__(self, natural_resource, owner=None):
        self.nat_resource = natural_resource
        self.owner = owner
        self.economy = 0
        self.industry = 0
        self.science = 0
        self.name = None

    def __repr__(self):
        return "Star: {}. Infrastructure: econ_{}, industry_{}, science_{}. Owned by {}".format(self.name, self.economy, self.industry, self.science, self.owner.name)

    def get_infrastructure(self):
        return self.economy, self.industry, self.science

    def set_infrastructure(self, econ, industry, science):
        self.economy = econ
        self.industry = industry
        self.science = science

    def get_production_per_day(self):
        money = self.economy * 10
        ships = self.industry * (self.owner.manufacturing + 5)
        science = self.science * 24
        return money, ships, science

    def set_effective_resources(self):
        self.terraformed_resources = self.nat_resource+(self.owner.terraforming*5)

    def get_upgrade_prices(self):
        econ_price = int( 500 * (1+self.economy) / self.terraformed_resources )
        industry_price = int(1000 * (1+self.industry)/self.terraformed_resources)
        science_price = int( 4000 * (1+self.science) / self.terraformed_resources )
        return econ_price, industry_price, science_price

    def update(self):
        self.set_effective_resources()

    def buy_upgrade(self, upgrade_idx):
        prices = self.get_upgrade_prices()
        price = prices[upgrade_idx]
        levels = list(self.get_infrastructure())
        if self.owner.money - price >= 0:
            self.owner.money -= price
            levels[upgrade_idx] += 1
            self.set_infrastructure(*levels)
            return True
        else:
            return False


class Player(object):
    def __init__(self, name, money=500):
        self.name = name
        self.scanning = 1
        self.hyperspace = 1
        self.terraforming = 1
        self.experimentation = 1
        self.weapons = 1
        self.banking = 1
        self.manufacturing = 1
        self.stars = []
        self.money = money
        self.ships = 60
        self.science = 0

    def __repr__(self):
        return "Player: {}, money: {}, ships: {}".format(self.name, self.money,
                                                         self.ships)

    def add_star(self, natural_resources, name=None, infrastructure=None):
        star = Star(natural_resources, self)
        star.name = name
        if infrastructure is not None:
            star.economy, star.industry, star.science = infrastructure
        star.update()
        self.stars.append(star)

    def get_total_production(self):
        money, ships, science = 0, 0, 0
        for star in self.stars:
            mo, sh, sc = star.get_production_per_day()
            ships += sh
            money += mo
            science += sc
        money += 75 * self.banking

        return money, ships, science

    def update_day(self):
        """One day passes"""
        money, ships, science = self.get_total_production()
        self.money += money
        self.ships += ships
        self.science += science
        # Check if we have upgraded manufacturing
        if self.science >= self.manufacturing * 144:
            self.science -= self.manufacturing * 144
            self.manufacturing += 1
        for star in self.stars:
            star.update()

    def get_cheapest_upgrades(self):
        prices = []
        for star in self.stars:
            prices.append(list(star.get_upgrade_prices()))

        prices = np.array(prices)
        cheapest_star_idx = np.argmin(prices, axis=0)
        return [(star_idx, prices[star_idx, ii])
                for ii, star_idx in enumerate(cheapest_star_idx)]

    def get_star_by_name(self, name):
        for star in self.stars:
            if star.name.lower() == name.lower():
                return star
        else:
            print("No star by that name")
            return None
