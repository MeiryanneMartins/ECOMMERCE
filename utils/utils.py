def format_price(val):
    return f'$ {val:.2f}'.replace('.', ',')


def cart_total_qtd(car):
    return sum([item['amount'] for item in car.values()])


def cart_totals(car):
    return sum(
        [
            item.get('price_amount_promotional')
            if item.get('price_amount_promotional')
            else item.get('price_amount')
            for item
            in car.values()
        ]
    )
