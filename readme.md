# PolDataGenerator

PolDataGenerator is a Python package for generating synthetic Polish personal data. It provides functionality to generate random names, addresses, and personal information in either string or dictionary format.

## Installation

Before using PolDataGenerator, you need to install the required dependencies. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Getting Started
To begin using **PolDataGenerator**, follow these steps:

1. Import the **PolDataGenerator** class from the package:
```
from src.PolDataGenerator import PolDataGenerator
```
2. Initialize a **PolDataGenerator** instance with optional parameters:
```
gen = PolDataGenerator(seed=42, output='str')
```
* seed (optional): Seed for random number generation. Defaults to None.
* output: Specifies the output format, which can be either 'str' or 'dict'. The default is 'str'.

3. You can generate synthetic data using the available methods:

* `generate_sex()`: Generates a random gender ('M' or 'F').
* `generate_name(name_type='full', sex=None)`: Generates a random name based on Polish population data. You can specify the name_type ('first', 'last', or 'full') and sex ('M' or 'F').
* `generate_city(extended=False)`: Generates a random city or city details based on the population of cities in Poland. If extended is set to True, it returns detailed city information.
* `generate_postal_code(**kwargs)`: Generates a random postal code with optional filtering conditions.
* `generate_street()`: Generates a random street name based on occurrences in Poland.
* `generate_street_number()`: Generates a random street number following an exponential distribution.
* `generate_address()`: Generates a random address by concatenating city, postal code, street, and street number.
* `generate_person(sex=None)`: Generates random personal data by concatenating name and address.
4. You can specify the desired output format as either a string or a dictionary by setting the output attribute of the PolDataGenerator instance:
```
gen.set_output('dict')
```

## Example
Here's an example of how to use PolDataGenerator to generate a random person in dictionary format:

```
from PolDataGenerator import PolDataGenerator

gen = PolDataGenerator(seed=42, output='dict')

# Generate a random person in dictionary format
person = gen.generate_person(sex='M')

print(person)
```


## License
This package is released under the MIT License. 