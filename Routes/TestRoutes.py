from Models.charger import Charger
from Models.route import Route


def generate_test_routes():
    routes = []
    route = Route(1, 737)
    chargers = [Charger(1, 23),
                Charger(2, 216),
                Charger(3, 323),
                Charger(4, 363),
                Charger(5, 405),
                Charger(6, 478),
                Charger(7, 505),
                Charger(8, 544),
                Charger(9, 613),
                Charger(10, 679),
                Charger(11, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    route = Route(2, 1005)
    chargers = [Charger(1, 61),
                Charger(2, 88),
                Charger(3, 283),
                Charger(4, 351),
                Charger(5, 396),
                Charger(6, 434),
                Charger(7, 481),
                Charger(8, 563),
                Charger(9, 601),
                Charger(10, 691),
                Charger(11, 850),
                Charger(12, 932),
                Charger(13, 978),
                Charger(14, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    return routes
