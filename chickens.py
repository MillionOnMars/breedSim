import random
import uuid
import argparse
import math

egg_rarity_data = {
    "Common": {"chance": 0.3, "eggs": 30},
    "Uncommon": {"chance": 0.4, "eggs": 60},
    "Rare": {"chance": 0.2, "eggs": 120},
    "Epic": {"chance": 0.06, "eggs": 180},
    "Legendary": {"chance": 0.03, "eggs": 360},
    "Mythic": {"chance": 0.01, "eggs": 720},
}

fertility_rarity_data = {
    "Common": {"chance": 0.3, "min": 0, "max": 1},
    "Uncommon": {"chance": 0.4, "min": 0, "max": 2},
    "Rare": {"chance": 0.2, "min": 1, "max": 2},
    "Epic": {"chance": 0.06, "min": 1, "max": 3},
    "Legendary": {"chance": 0.03, "min": 2, "max": 4},
    "Mythic": {"chance": 0.01, "min": 3, "max": 4},
}

breed_data = {
    "Dominique": {"rarity": 0.1},
    "Jersey Giant": {"rarity": 0.15},
    "Leghorn": {"rarity": 0.2},
    "Brahma": {"rarity": 0.1},
    "Australorp": {"rarity": 0.15},
    "Sussex": {"rarity": 0.1},
    "Plymouth Rock": {"rarity": 0.1},
    "Rhode Island Red": {"rarity": 0.1},
}

class Chicken:
    def __init__(self, breed, gender, eggs, fertility, mature=False):
        self.id = str(uuid.uuid4())
        self.breed = breed
        self.gender = gender
        if (mature):
            self.status = "mature"
            self.days_until_mature = 0
        else:
            self.status = "chick"
            self.days_until_mature = 30
        self.eggs_remaining = eggs
        self.fertility_remaining = fertility
        self.eggs_produced = 0

    def is_eligible_for_blue_ribbon(self):
        return (self.gender == "hen" and self.eggs_remaining >= 120) or \
               (self.gender == "rooster" and self.fertility_remaining >= 1)

    @classmethod
    def generate_eggs(cls):
        rarities = list(egg_rarity_data.keys())
        rarity_chances = [egg_rarity_data[rarity]["chance"] for rarity in rarities]
        rarity = random.choices(rarities, weights=rarity_chances)[0]
        return egg_rarity_data[rarity]["eggs"]

    @classmethod
    def generate_fertility(cls):
        rarities = list(fertility_rarity_data.keys())
        rarity_chances = [fertility_rarity_data[rarity]["chance"] for rarity in rarities]
        rarity = random.choices(rarities, weights=rarity_chances)[0]
        return random.randint(fertility_rarity_data[rarity]["min"], fertility_rarity_data[rarity]["max"])

    @classmethod
    def hatch(cls, female_ratio, mature=False):
        breeds = list(breed_data.keys())
        breed_probabilities = [breed_data[breed]["rarity"] for breed in breeds]
        breed = random.choices(breeds, weights=breed_probabilities)[0]
        gender = "hen" if random.random() < female_ratio else "rooster"
        eggs = cls.generate_eggs() if gender == "hen" else 0
        fertility = cls.generate_fertility() if gender == "rooster" else 0
        new_chick = cls(breed, gender, eggs, fertility, mature=mature)
        if new_chick.is_eligible_for_blue_ribbon():
            new_chick.award_blue_ribbon()
        else:
            new_chick.dusk_award = 0
            new_chick.glitter_award = 0
        return new_chick

    def __str__(self):
        return f"ID: {self.id}, Breed: {self.breed}, Gender: {self.gender}, Eggs Remaining: {self.eggs_remaining}, Fertility Remaining: {self.fertility_remaining}, Status: {self.status}"

    def award_blue_ribbon(self):
        award_categories = [
            {"name": "Green", "chance": 0.30, "min_dusk": 100, "max_dusk": 200, "min_glitter": 10, "max_glitter": 20},
            {"name": "Yellow", "chance": 0.40, "min_dusk": 200, "max_dusk": 500, "min_glitter": 20, "max_glitter": 50},
            {"name": "White", "chance": 0.20, "min_dusk": 500, "max_dusk": 1000, "min_glitter": 50, "max_glitter": 100},
            {"name": "Red", "chance": 0.06, "min_dusk": 1000, "max_dusk": 2500, "min_glitter": 100, "max_glitter": 250},
            {"name": "Blue", "chance": 0.03, "min_dusk": 2500, "max_dusk": 5000, "min_glitter": 250, "max_glitter": 500},
            {"name": "Purple", "chance": 0.01, "min_dusk": 5000, "max_dusk": 10000, "min_glitter": 500, "max_glitter": 1000},
        ]
        category = random.choices(award_categories, weights=[cat["chance"] for cat in award_categories])[0]
        self.dusk_award = random.randint(category["min_dusk"], category["max_dusk"])
        self.glitter_award = random.randint(category["min_glitter"], category["max_glitter"])
        # print(f"Chicken {self.id} won a {category['name']} Ribbon! Dusk: {self.dusk_award}, Glitter: {self.glitter_award}")

    def age(self):
        if self.days_until_mature > 0:
            self.days_until_mature -= 1
            if self.days_until_mature == 0:
                self.status = "mature"

    def lay_egg(self):
        if self.gender == "hen" and self.status == "mature" and self.eggs_remaining > 0:
            self.eggs_remaining -= 1
            self.eggs_produced += 1
            return 1
        return 0
    
    def mate(self, flock, female_ratio):
        if self.gender == "rooster" and self.status == "mature" and self.fertility_remaining > 0:
            potential_mate = next((chicken for chicken in flock if chicken.gender == "hen" and chicken.status == "mature" and chicken.eggs_remaining > 0), None)
            if potential_mate:
                self.fertility_remaining -= 1
                potential_mate.eggs_remaining -= 1
                new_chick = Chicken.hatch(female_ratio=female_ratio, mature=False)
                return new_chick, new_chick.dusk_award, new_chick.glitter_award
        return None, 0, 0



class Simulation:
    def __init__(self, starting_population=1200, female_ratio=0.55, days_to_simulate=365, food_per_chicken=1, water_per_chicken=3):
        self.starting_population = starting_population
        self.female_ratio = female_ratio
        self.days_to_simulate = days_to_simulate
        self.food_per_chicken = food_per_chicken
        self.water_per_chicken = water_per_chicken

        self.total_eggs = 0
        self.total_meat = 0
        self.total_dusk = 0
        self.total_glitter = 0
        self.total_food = 0
        self.total_water = 0

    def flock_summary(self, day, eggs_produced_today=0, chicken_meat_today=0):
        print(f"Day {day}:")
        print(f"Total chickens: {len(self.flock)}")
        print(f"Hens: {sum(chick.gender == 'hen' for chick in self.flock)}")
        print(f"Roosters: {sum(chick.gender == 'rooster' for chick in self.flock)}")
        print(f"Chicks: {sum(chick.status == 'chick' for chick in self.flock)}")
        print(f"Mature: {sum(chick.status == 'mature' for chick in self.flock)}")
        print(f"Eggs harvested today: {eggs_produced_today}")
        print(f"Chicken Meat Harvested today: {chicken_meat_today}")
        print(f"Water used: {len(self.flock) * self.water_per_chicken}")
        print(f"Food used: {len(self.flock) * self.food_per_chicken}")
        print()

    def simulate_day(self):
        new_flock = []
        eggs_produced_today = 0
        chicken_meat_today = 0

        for chicken in self.flock:
            chicken.age()

            new_chick, dusk_award, glitter_award = chicken.mate(self.flock, self.female_ratio)
            if new_chick:
                new_flock.append(new_chick)
                self.total_dusk += dusk_award
                self.total_glitter += glitter_award

            eggs_produced_today += chicken.lay_egg()

            if (chicken.gender == "rooster" and chicken.fertility_remaining == 0) or \
            (chicken.gender == "hen" and chicken.eggs_remaining == 0):
                chicken_meat_today += 1
                continue

            new_flock.append(chicken)

        self.total_food += len(self.flock) * self.food_per_chicken
        self.total_water += len(self.flock) * self.water_per_chicken

        return new_flock, eggs_produced_today, chicken_meat_today


    def print_starting_variables(self):
            print("----------------------")
            print("Simulation Starting Variables:")
            print(f"Starting Population: {self.starting_population}")
            print(f"Female Ratio: {self.female_ratio}")
            print(f"Days to Simulate: {self.days_to_simulate}")
            print(f"Food per Chicken: {self.food_per_chicken}")
            print(f"Water per Chicken: {self.water_per_chicken}")
            print("----------------------")

    def run(self):

        self.print_starting_variables()

        # Create initial population
        self.flock = [Chicken.hatch(female_ratio=self.female_ratio, mature=True) for _ in range(self.starting_population)]
        self.flock_summary(0)

        # Determine the frequency of printout based on total days
        print_frequency = max(1, int(math.sqrt(self.days_to_simulate)))

        # Simulate for specified number of days
        for day in range(self.days_to_simulate):
            self.flock, eggs_produced_today, chicken_meat_today = self.simulate_day()        
            self.total_eggs += eggs_produced_today
            self.total_meat += chicken_meat_today

            # Break the simulation if all chickens are gone
            if len(self.flock) == 0:
                print("All chickens are gone. Stopping simulation.")
                break

            # Print every print_frequency days
            if day % print_frequency == 0:
                self.flock_summary(day, eggs_produced_today, chicken_meat_today)

        print("Simulation Complete!")
        print(f"Last day: {day}")
        print(f"Total eggs produced: {self.total_eggs}")
        print(f"Total chicken meat produced: {self.total_meat}")
        print(f"Total Dusk awarded: {self.total_dusk}")
        print(f"Total Glitter awarded: {self.total_glitter}")
        print(f"Total water used: {self.total_water}")
        print(f"Total food used: {self.total_food}")



def main(days, water, food):
    sim = Simulation(1200, 0.55, days, food, water)
    sim.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a chicken farm simulation.')
    parser.add_argument('--days', type=int, default=365, help='The number of days to run the simulation.')
    parser.add_argument('--water', type=int, default=3, help='The amount of water per chicken.')
    parser.add_argument('--food', type=int, default=1, help='The amount of food per chicken.')
    args = parser.parse_args()

    main(args.days, args.water, args.food)





