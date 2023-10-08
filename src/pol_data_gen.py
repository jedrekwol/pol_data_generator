from typing import Optional, Union, Dict
import random
from src.output_formatter import OutputFormatter
from src.data_loader import DataLoader

class PolDataGenerator(DataLoader, OutputFormatter):

    def __init__(
            self,
            seed: Optional[int] = None,
            output: str = 'str'
    ):
        super().__init__()
        self.output = output
        self.set_seed(seed)

    def set_seed(
            self,
            seed: Optional[int]
    ):
        """
        Set the seed for random number generation.

        Args:
            seed (int, optional): Seed for random number generation. Defaults to None.

        Returns:
            None
        """

        self.seed = seed
        random.seed(seed)

    def _generate_random_item(
            self,
            key_name: str,
            item_name: str,
            weights_colname: Optional[str] = None,
            **kwargs
    ) -> Union[str, Dict[str, str]]:
        """
        Get a random item from a DataFrame based on specified conditions.

        Args:
            key_name (str): Key name to identify the data.
            item_name (str): Name of the item to retrieve.
            weights_colname (str, optional): Name of the column
                containing weights for random choice. Defaults to None.
            **kwargs: Additional conditions to filter the DataFrame.

        Returns:
            Union[str, pd.Series]: Randomly selected item.
        """

        dataframe = self.data_dict[key_name].copy()
        for column, condition in kwargs.items():
            dataframe = dataframe[dataframe[column] == condition]
        weights_column = None if weights_colname is None else dataframe[weights_colname]
        dataframe.reset_index(drop=True, inplace=True)
        index = random.choices(dataframe.index, weights=weights_column)[0]
        item = dataframe.loc[index, item_name]
        return item

    def generate_sex(self) -> str:
        """
        Generate a random gender ('M' or 'F').

        Returns:
            str: Randomly generated gender.
        """

        genders = ['M', 'F']
        return random.choices(genders)[0]

    def generate_name(
            self,
            name_type: str = 'full',
            sex: Optional[str] = None
    ) -> Union[str, Dict[str, str]]:
        """
        Generate a random name based on the distribution of names in Polish population.

        Args:
            name_type (str): Type of name to generate ('first', 'last', or 'full').
            sex (str, optional): Gender for name generation ('M' or 'F'). Defaults to None.

        Returns:
            Union[str, Dict[str, str]]: Randomly generated name.

        Raises:
            ValueError: If name_type is not 'first', 'last', or 'full'.
            ValueError: If sex is provided but not 'M' or 'F'.
        """

        if sex is None:
            sex = self.generate_sex()
        elif sex not in ['M', 'F']:
            raise ValueError("Sex must be 'M' or 'F'")

        if name_type in ['first', 'last']:
            key_name = f'{name_type}_names'
            item_name = f'{name_type}_name'
            self._load_data(key_name)
            name = self._generate_random_item(
                key_name=key_name,
                item_name=item_name,
                weights_colname='occurrences',
                sex=sex
            )
            return self.format_output(item_name=item_name, item=name)

        elif name_type == 'full':
            first_name = self.generate_name(name_type='first', sex=sex)
            last_name = self.generate_name(name_type='last', sex=sex)
            output_list = [first_name, last_name]
            return self.contantenate_outputs(output_list)
        else:
            raise ValueError("name_type must be 'first', 'last' or 'full'")


    def generate_city(
            self,
            extended: bool = False
    ) -> Union[str, Dict[str, str]]:
        """
        Generate a random city or city details based on population of cities in Poland.

        Args:
            extended (bool, optional): If True, return extended city details. Defaults to False.

        Returns:
            Union[str, Dict[str, str]]: Randomly generated city or details.
        """

        key_name = 'cities'
        item_name = ['voivodeship', 'city', 'county'] if extended else 'city'

        self._load_data(key_name)
        city = self._generate_random_item(
            key_name=key_name,
            item_name=item_name,
            weights_colname='population'
        )
        if extended:
            return city.to_dict()
        return self.format_output(item_name=item_name, item=city)

    def generate_postal_code(
            self,
            **kwargs
    ) -> Union[str, Dict[str, str]]:
        """
        Generate a random postal code.

        Args:
            **kwargs: Additional conditions to filter postal codes.

        Returns:
            Union[str, Dict[str, str]]: Randomly generated postal code.
        """

        key_name = 'postal_codes'
        item_name = 'postal_code'
        self._load_data(key_name)

        postal_code = self._generate_random_item(
            key_name=key_name,
            item_name=item_name,
            **kwargs
        )

        return self.format_output(item_name=item_name, item=postal_code)


    def generate_street(self) -> Union[str, Dict[str, str]]:
        """
        Generate a random street name based on occurrences of streets in Poland.

        Returns:
            Union[str, Dict[str, str]]: The generated street name, either as a string or a dictionary.
        """

        key_name = 'streets'
        item_name = 'street'
        self._load_data(key_name)

        street = self._generate_random_item(
            key_name=key_name,
            item_name=item_name,
            weights_colname='occurrences'
        )

        return self.format_output(item_name=item_name, item=street)


    def generate_street_number(self) -> Union[int, Dict[int, str]]:
        """
        Generate a random street number. The generator uses an exponential distribution - the
        lower the number is, the greater the probability of picking it

        Returns:
            Union[int, Dict[int, str]]: The generated street number.
        """

        item_name = 'street_number'
        street_number = round(random.expovariate(1/50) + 1)
        return self.format_output(item_name=item_name, item=street_number)


    def generate_address(self) -> Union[str, Dict[str, str]]:
        """
        Generate a random address by concatenating city, postal code, street and street number

        Returns:
            Union[str, Dict[str, str]]: The generated address, either as a string or a dictionary.
        """

        geo_info = self.generate_city(extended=True)
        if self.output == 'str':
            city = geo_info['city']
        elif self.output == 'dict':
            city = {'city': geo_info['city']}
        postal_code = self.generate_postal_code(**geo_info)
        street = self.generate_street()
        street_number = self.generate_street_number()

        output_list = [street, street_number, city, postal_code]

        return self.contantenate_outputs(output_list, breaking_indices=[1])

    def generate_person(self, sex: Optional[str] = None):
        """
        Generate a random personal data by concantenating name and address

        Arguments:
            sex (str, optional): Gender for name generation ('M' or 'F'). Defaults to None.

        Returns:
            Union[str, Dict[str, str]]: The generated address, either as a string or a dictionary.
        """

        full_name = self.generate_name(sex=sex, name_type='full',)
        address = self.generate_address()
        output_list = [full_name, address]
        return self.contantenate_outputs(output_list, breaking_indices=[0])
    