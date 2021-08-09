import requests
from nsepy import get_history
from datetime import date


def main():
    nifty_opt = get_history(symbol="NIFTY",
                            start=date(2021, 7, 1),
                            end=date(2021, 7, 15),
                            index=True,
                            option_type='CE',
                            strike_price=16000,
                            expiry_date=date(2021, 7, 22))

if __name__ == '__main__':
    main()
