import pandas as pd

class DataLoader:

    def __init__(self):
        self.data_dict = {}

    def _load_data(
            self,
            key_name: str
    ):
        """
        Load data from a CSV file into a pandas DataFrame and store it in the data_dict
            under key_name. If data with the same key_name has already been loaded, it
            will not be loaded again to prevent overwriting.

        Args:
            key_name (str): Key name to identify the data.

        Returns:
            None
        """

        if self.data_dict.get(key_name) is None:
            self.data_dict[key_name] = pd.read_csv(f'data/{key_name}.csv')
    