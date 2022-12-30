from rswiki_wrapper import Latest


if __name__ == "__main__":
    latest_prices = Latest()

    for item_id, values in latest_prices.content.items():
        print(f"ID: {item_id}, high: {values['high']}, low: {values['low']}")
