# Chicken Breeding Simulation - Project Overview
This project is a Python script to simulate a chicken breeding environment. This repository was created to allow our players to understand, review, and contribute to the simulation that shapes the in-game mechanics of our game. We highly value your feedback, suggestions and contributions!

## How the Simulation Works
The simulation begins with an initial population of chickens. Each chicken has certain attributes like gender, age, remaining eggs (for hens), and remaining fertility (for roosters). Each day, these chickens age, consume food and water, lay eggs, and may produce new chickens. If a chicken reaches the end of its fertility or egg-laying capacity, it is turned into meat.

This simulation emphasizes the interplay between the size of the population and the availability of resources. A careful balance is maintained to ensure that the population does not grow unbounded, as roosters will eventually run out of fertility and hens will run out of eggs. In our tests, we've noticed that the initial population of 1200 chickens usually dies out by day 810.

## Running the Simulation
You can run the simulation by calling the script from the command line and passing the desired parameters. For example:

```bash
python3 chickens.py --days=365 --food=2 --water=3`
```

This will run a simulation for 365 days, with each chicken consuming 2 units of food and 3 units of water per day.

### Sample Output
Here's a sample output from the simulation going on for many days (until the flock dies out):

```bash
All chickens are gone. Stopping simulation.
Simulation Complete!
Last day: 810
Total eggs produced: 110727
Total chicken meat produced: 2193
Total Dusk awarded: 282048
Total Glitter awarded: 28371
Total water used: 136811
Total food used: 410433
```

## Notes on Balancing
All of the values used in the simulation are placeholders and are subject to change as we continue to balance the game. We can tune parameters such as the initial population, the ratio of hens to roosters, the amount of food and water each chicken consumes, and more.

Please note that the cost of "food" in this simulation refers to "chicken food". We can tune the cost of this resource to be as expensive or cheap as needed, allowing us to further adjust the balance of the game.

## Simulation Variables and Balance
The following variables influence the simulation and can be adjusted for game balance:

- eggs per hen: This determines how many eggs each hen lays. Increasing this value will result in more eggs being produced.
- fertility per rooster: This controls how many times a rooster can fertilize eggs. Adjusting this value will affect the population growth of the flock.
- breed rarity: The chance of a rare breed being born. Higher values will lead to a more diverse flock.
- dusk award and glitter award: These are special rewards given when rare breeds are born. The values can be adjusted to control the rate of reward generation.
- Note: Dusk and Glitter awards are given only once in a chicken's lifetime when the chicken is of rare or better reproductivity.

## Note on Rooster Fertility
The mechanic of rooster fertility is key to keeping the flock population under control. With a starting flock of 1200 chickens, a typical simulation sees the flock completely dying out by around day 810.

## Note on Food Consumption
The food_per_chicken value represents the consumption of chicken food. This is an important balancing variable and can be adjusted to make the simulation more or less challenging. Higher food requirements will put more pressure on resource management.

## Contributing
We welcome feedback, suggestions, and contributions from our player community! Feel free to fork this repository, make changes, and submit a pull request. If you have any questions or ideas, please open an issue to discuss them.