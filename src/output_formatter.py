from typing import List, Union, Dict

class OutputFormatter:

    def __init__(
            self,
            output: str = 'str'
    ):
        self.output = output

    def contantenate_outputs(
            self,
            args: List[str],
            breaking_indices: List[int] = []
    ):
        """
        Format the input arguments as a string with optional line breaks.

        Args:
            args (List[Union[str, int]]): The list of arguments to be formatted.
            breaking_indices (List[int], optional): A list of indices where line breaks
                should be inserted.Default is an empty list.

        Returns:
            str: The formatted string with optional line breaks.
        """

        if self.output == 'str':
            result = ''
            for i, arg in enumerate(args):
                result += str(arg)
                if i in breaking_indices:
                    result += '\n'
                else:
                    result += ' '
            return result.strip()
        elif self.output == 'dict':
            result = {}
            for dictionary in args:
                result |= dictionary
            return result

    def format_output(
            self,
            item_name: str,
            item: str
    ) -> Union[str, Dict[str, str]]:
        """
        Get the output in the specified format.

        Args:
            item_name (str): Name of the item.
            item (str): Item to format.

        Returns:
            Union[str, Dict[str, str]]: Formatted output.
        """

        if self.output == 'str':
            return item
        elif self.output == 'dict':
            return {item_name: item}
