from Models.charger import Charger
from Models.route import Route


def generate_train_routes():
    routes = []
    route = Route(1, 650)
    chargers = [Charger(1, 63),
                Charger(2, 120),
                Charger(3, 300),
                Charger(4, 327),
                Charger(5, 394),
                Charger(6, 445),
                Charger(7, 477),
                Charger(8, 512),
                Charger(9, 555),
                Charger(10, 620),
                Charger(11, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    route = Route(2, 1000)
    chargers = [Charger(1, 50),
                Charger(2, 120),
                Charger(3, 253),
                Charger(4, 311),
                Charger(5, 366),
                Charger(6, 402),
                Charger(7, 455),
                Charger(8, 511),
                Charger(9, 587),
                Charger(10, 657),
                Charger(11, 703),
                Charger(12, 789),
                Charger(13, 800),
                Charger(14, 907),
                Charger(15, 944),
                Charger(16, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    route = Route(3, 2105)
    chargers = [Charger(1, 150),
                Charger(2, 215),
                Charger(3, 343),
                Charger(4, 421),
                Charger(5, 531),
                Charger(6, 612),
                Charger(7, 731),
                Charger(8, 822),
                Charger(9, 889),
                Charger(10, 951),
                Charger(11, 1023),
                Charger(12, 1189),
                Charger(13, 1200),
                Charger(14, 1356),
                Charger(15, 1407),
                Charger(16, 1544),
                Charger(17, 1620),
                Charger(18, 1759),
                Charger(19, 1914),
                Charger(20, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    route = Route(4, 3222)
    chargers = [Charger(1, 70),
                Charger(2, 215),
                Charger(3, 343),
                Charger(4, 421),
                Charger(5, 531),
                Charger(6, 612),
                Charger(7, 731),
                Charger(8, 822),
                Charger(9, 889),
                Charger(10, 951),
                Charger(11, 1023),
                Charger(12, 1189),
                Charger(13, 1200),
                Charger(14, 1356),
                Charger(15, 1407),
                Charger(16, 1544),
                Charger(17, 1620),
                Charger(18, 1739),
                Charger(19, 1874),
                Charger(20, 1928),
                Charger(21, 2051),
                Charger(22, 2180),
                Charger(23, 2257),
                Charger(24, 2323),
                Charger(25, 2485),
                Charger(26, 2546),
                Charger(27, 2612),
                Charger(28, 2796),
                Charger(29, 2884),
                Charger(30, 2937),
                Charger(31, 3075),
                Charger(32, 3194),
                Charger(33, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    route = Route(5, 4152)
    chargers = [Charger(1, 91),
                Charger(2, 202),
                Charger(3, 354),
                Charger(4, 475),
                Charger(5, 526),
                Charger(6, 695),
                Charger(7, 736),
                Charger(8, 847),
                Charger(9, 922),
                Charger(10, 966),
                Charger(11, 1003),
                Charger(12, 1187),
                Charger(13, 1233),
                Charger(14, 1374),
                Charger(15, 1445),
                Charger(16, 1594),
                Charger(17, 1632),
                Charger(18, 1773),
                Charger(19, 1867),
                Charger(20, 1937),
                Charger(21, 2085),
                Charger(22, 2123),
                Charger(23, 2263),
                Charger(24, 2322),
                Charger(25, 2483),
                Charger(26, 2534),
                Charger(27, 2796),
                Charger(28, 2884),
                Charger(29, 2926),
                Charger(30, 3012),
                Charger(31, 3121),
                Charger(32, 3264),
                Charger(33, 3387),
                Charger(34, 3477),
                Charger(35, 3533),
                Charger(36, 3600),
                Charger(37, 3805),
                Charger(38, 3945),
                Charger(39, 4045),
                Charger(39, 4102),
                Charger(40, route.route_length)]
    route.add_chargers_manually(chargers)
    routes.append(route)

    return routes
