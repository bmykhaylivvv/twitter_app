"""
Module for searching through the JSON file
"""

import json
import sys
from typing import Union, List, Dict, Any, Callable


def user_choice() -> str:
    """
    Functioт get the user`s value and return it.
    If the input == "exit()", the program execution will stop.
    """
    inputted_value = input("Enter the value: ")
    if inputted_value == "exit":
        sys.exit()
    return inputted_value


def read_json(path: str) -> Union[Dict, List]:
    """
    Function return .json file depending on inputted by user value.
    """

    with open(path, "r") as json_file:
        json_data = json.load(json_file)
    return json_data


def json_parser(data) -> Union[Callable, List]:
    """
    Function provide you an opportunity to search through the json file.
    If you enter "return" you`ll get the whole file.
    If you enter "exit()" you will stop program executing.
    """
    if isinstance(data, dict):
        print("It`s a dictionary, choose criterion from available keys,\
        or enter RETURN to return values on this level. You can enter \"exit()\" to stop\
                program execution")
        available_values = list(data.keys())
        print(available_values)
        while True:
            choice = user_choice()
            if choice not in available_values and choice != "return":
                print("Choose a value from the list")
            elif choice == "return":
                return data
            else:
                break

        if choice != "return":
            return json_parser(data[choice])

        return data

    if isinstance(data, list):
        print(f"It`s a list, choose the index from 0 to {len(data)-1},\
            or enter RETURN to return values on this level. You can enter \"exit()\" to stop\
                program execution")
        while True:
            choice = user_choice()
            if choice not in [str(num) for num in range(len(data))] and choice != "return":
                print("Choose a value from the list")
            elif choice == "return":
                return data
            else:
                break

        if choice != "return":
            return json_parser(data[int(choice)])
        return data

    return data


def main():
    """
    Main function of main.py module
    """
    PATH = "friends.json"
    initial_data = read_json(PATH)
    print(json_parser(initial_data))


if __name__ == "__main__":
    main()
