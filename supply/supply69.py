from supply import Card, EFCard, ELFCard, SPCard
from supply import NorS, Before, Supply, Analyzer
from supply import CHIP


class ChaseLightCard(Card):
    def __init__(self,) -> None:
        super().__init__([0, 0], '逐光祈愿补给卡')


class NorS69(NorS):
    def __init__(
        self,
        _desc: str = '6.9 版本普通初始 S 女武神'
    ) -> None:
        super().__init__(1.5, 440, _desc)


class Mei(NorS69):
    def __init__(
        self,
        _desc: str = '始源芽衣'
    ) -> None:
        super().__init__(_desc)


class V2v(NorS69):
    def __init__(
        self,
        _desc: str = '维尔薇'
    ) -> None:
        super().__init__(_desc)


class ChaseLightSupply(Supply):
    def __init__(self, _desc: str = 'Chase the Light Supply') -> None:
        standard = [
            (Mei, 0.1),
            (V2v, 0.1),
            (EFCard, 0.25, 2),
            (EFCard, 0.25, 2),
            (EFCard, 1.6),
            (EFCard, 1.6),
            (ELFCard, 1.6),
            (SPCard, 1.6),
            (ChaseLightCard, 10),
        ]
        super().__init__(ChaseLightCard, standard, _desc)


a = Analyzer(ChaseLightSupply())

a.analyze(Before(
    437,
    7280,
    CHIP
), [
    (Mei, 1),
    (V2v, 1),
    (EFCard, 12),
    (ELFCard, 9),
    (SPCard, 5)
])
