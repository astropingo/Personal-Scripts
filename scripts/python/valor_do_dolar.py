'''
Receives a float value as argument and returns the value converted to USD and BRL.
The script uses the API from https://economia.awesomeapi.com.br/ to get the current currency exchange rate.
It also uses the rich library to display the results in a table.
'''

import requests
import json
import argparse
from rich.console import Console
from rich.table import Table
from rich import box

def main():
    def float_or_default(value):
        value = value.replace(",", ".")
        if value == "":
            return 1.0
        try:
            return float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid float type: {value}.")
    parser = argparse.ArgumentParser(description="Currency converter script")
    parser.add_argument("amount", type=float_or_default, help="Amount to convert")
    args = parser.parse_args()

    api_endpoint = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.request("Get", api_endpoint)
    result = response.text
    result = json.loads(result)
    display(result, args.amount)

def display(api_response, amount):
    USDBRL = float(api_response["USDBRL"]["bid"])
    table = Table(title="Valor do dólar", box=None)
    table.add_column("Valor", justify="center", style="cyan", no_wrap=True)
    table.add_column("USD -> BRL", justify="center", style="cyan", no_wrap=True)
    table.add_column("BRL -> USD", justify="center", style="cyan", no_wrap=True)
    table.add_row(f"{amount:.2f}", f"BRL {round(USDBRL * amount,2):.2f}", f"USD {round(amount / USDBRL,2):.2f}")
    table.box = box.SIMPLE_HEAD
    console = Console()
    console.print(table)

if __name__ == '__main__':
    main()