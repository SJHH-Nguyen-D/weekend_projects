import pandas as pd 
import requests 
from bs4 import BeautifulSoup
import re


url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=CAD&To=USD"
tag = "div"
class_name = "sc-fzozJi dteCCc"
pattern = r'^.*\d+.*?$'
    
CONV_MAP = {
    "currencies": {"CAD":{"conversion_rate": 0.74}, 
                   "USD":{"conversion_rate": 1.36}
                  },
    "volume_unit": {"litre": {"conversion_rate": 0.264172 }, 
                    "gallon": {"conversion_rate": 3.785}},
}

def get_soup(url):
    url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=CAD&To=USD"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_conversion_rate(tag, class_name, pattern):
    soup = get_soup(url)
    txt = soup.find(tag, class_=class_name)
    try:
        conv_rate = re.search(pattern, txt).group(1)
    except AttributeError:
        conv_rate = ''
    return conv_rate


def gas_price_calc(original_currency, vol, ppu, vol_metric):
    assert original_currency in ["USD", "CAD"], "use CAD or USD"
    assert vol_metric in ["litre", "gallon"], "use litre or gallon as volume unit"
    if vol_metric == "litre":
        vol_litre = vol
        vol_gallon = vol * CONV_MAP["volume_unit"][vol_metric]["conversion_rate"]
    else:
        vol_litre = vol*CONV_MAP["volume_unit"][vol_metric]["conversion_rate"]
        vol_gallon = vol

    if original_currency == "CAD":
        price_cad = vol*ppu
        price_usd = vol*ppu*CONV_MAP["currencies"][original_currency]["conversion_rate"] 
    else:
        price_cad = vol*ppu*CONV_MAP["currencies"][original_currency]["conversion_rate"] 
        price_usd = vol*ppu

    print(f"\nVol: {vol_litre:.2f} litres | {vol_gallon:.2f} gallons\nPrice: ${price_cad:.2f}CAD | ${price_usd:.2f}USD\n")

if __name__ == "__main__":
    gas_price_calc("USD", 25, 1.5, "gallon")