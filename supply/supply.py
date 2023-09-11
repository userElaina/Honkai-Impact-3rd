from copy import deepcopy as dcp

DELTA = 0.0000000001
NORMAL_S = 40
EFC_LOW_CHIP = 150
ELFC_LOW_CHIP = 98
SPC_LOW_CHIP = 60

TYPE = '_type'

CRYSTAL = '水晶'
CHIP = '礼包币'
L_S_R = ''

CARD = 'Supply-Card'

COST = '_cost'
DESC = '_description'

ITEM = '_item'
VALK = '_valkyrie'

types = [ITEM, CARD, VALK]

cost_desc = [
    ('标价', CRYSTAL),
    ('限量礼包', CHIP),
    ('身边统计学', CRYSTAL),
]


class Item:
    def __init__(
        self,
        _cost: tuple | float | int,
        _type: str = ITEM,
        _desc: str = '物品',
        auto_reg_type: bool = False,
    ) -> None:
        if isinstance(_cost, (float, int)):
            _cost = [_cost,]
        self.cost = dcp(_cost)
        if _type not in types:
            if auto_reg_type:
                types.append(_type)
            else:
                raise ValueError(_type)
        self.type = _type
        self.desc = _desc


class Card(Item):
    def __init__(
        self,
        _cost: tuple | float | int,
        _desc: str = '补给卡',
    ) -> None:
        super().__init__(_cost, CARD, _desc, False)


class EFCard(Card):
    def __init__(self,) -> None:
        super().__init__([280, EFC_LOW_CHIP], '普通补给卡')


class ELFCard(Card):
    def __init__(self,) -> None:
        super().__init__([150, ELFC_LOW_CHIP], '人偶补给卡')


class SPCard(Card):
    def __init__(self,) -> None:
        super().__init__([120, SPC_LOW_CHIP], 'SP 补给卡')


class Valkyrie(Item):
    def __init__(
        self,
        _card: type | Card,
        standard: float,
        cost10: float | int = 0,
        normal: float = 0.,
        duplicate: int = 30,
        _desc: str = '女武神',
    ) -> None:
        if isinstance(_card, type):
            _card = _card()
        _card = _card.cost[0]
        standard = 100. / standard * _card
        cost10 *= duplicate / 10

        if normal > DELTA:
            normal = 100. / normal * _card
            _cost = [standard, cost10, normal]
        elif cost10 > DELTA:
            _cost = [standard, cost10]
        else:
            _cost = [standard,]

        super().__init__(_cost, VALK, _desc, False)


class NorS(Valkyrie):
    def __init__(
        self,
        standard: float,
        cost10: float | int = 0,
        _desc: str = '普通初始 S 女武神'
    ) -> None:
        super().__init__(EFCard, standard, cost10, 100. / NORMAL_S, 30, _desc)


class Supply:
    def __init__(
        self,
        _card: type,
        standard: list[tuple[type, float, int] | tuple[type, float]],
        _desc: str = '补给',
    ) -> None:
        self.card = _card
        self.desc = _desc
        self.d, ans = cost_sum(standard)
        self.ans = [i/100. for i in ans]

        self.cycle = 0.
        for i in self.d:
            if i == _card:
                self.cycle = self.d.pop(i) / 100.
                break

    def prt1(self) -> None:
        prt_ans(self.ans, '单次期望')

    def prt_standard(self) -> None:
        print('每次补给概率表:')
        for i in self.d:
            print('%s: %.2lf%s' % (i().desc, self.d[i], '%'))
        print()

    def prt_cycle(self) -> None:
        if self.cycle > DELTA:
            print('每次有 %.2lf%s 获得原补给卡, 因此相当于每次消耗 %.3lf 张祈愿卡' %
                  (self.cycle, '%', 1.-self.cycle))


class Before:
    def __init__(
        self,
        card_num: int,
        cost_num: int,
        cost_type: str,
    ) -> None:
        self.card_num = card_num
        self.cost_num = cost_num
        assert cost_type in [CHIP, CRYSTAL]
        self.cost_type = cost_type

    def prt_num(self) -> None:
        print('本次有 %d 张补给卡, 共花费 %d %s' %
              (self.card_num, self.cost_num, self.cost_type))


class Analyzer:
    def __init__(
        self,
        _supply: Supply,
    ) -> None:
        self.supply = _supply

    def analyze(self, before: Before = None, result: list[tuple[type, float]] = None) -> None:
        self.supply.prt_standard()
        self.supply.prt1()

        self.supply.prt_cycle()
        if before is None:
            return
        before.prt_num()
        real_card_num = before.card_num
        if self.supply.cycle > DELTA:
            real_card_num /= 1.-self.supply.cycle
            print('期望抽取补给次数为 %.3lf' % real_card_num)
        print()

        print('本次期望抽到:')
        for i in self.supply.d:
            print('%s: %.3lf' %
                  (i().desc, self.supply.d[i]*real_card_num/100.))
        print()
        prt_ans([i*real_card_num for i in self.supply.ans], '本次期望折合')

        if result is None:
            return
        d, ans = cost_sum(result)
        print('本次实际抽到:')
        for i in d:
            print('%s: %d' % (i().desc, d[i]))
        print()
        prt_ans(ans, '本次实际折合')


def cost_sum(standard: list) -> tuple:
    d = dict()
    checksum = 0.
    for i in standard:
        assert len(i) == 2 or len(i) == 3
        if len(i) == 2:
            i, j = i
        else:
            i, j, k = i
            j *= k

        assert isinstance(i, type)
        assert isinstance(i(), Item)
        assert isinstance(j, (float, int))

        d.setdefault(i, 0.)
        d[i] += j
        checksum += j

    assert checksum < 100. + DELTA

    channels = range(len(cost_desc))
    ans = [0.] * len(cost_desc)
    for i in d:
        j = d[i]
        i = i()

        for k in channels:
            kk = k
            while kk >= len(i.cost) or cost_desc[kk][1] != cost_desc[k][1]:
                kk -= 1
            # print('[%d] + %.2lf*%.2lf' % (k, i.cost[kk] , j))
            ans[k] += i.cost[kk] * j
    return d, ans


def prt_ans(ans: list, title: str = '数学期望') -> None:
    print('%s:' % title)
    for i in range(len(cost_desc)):
        print('%s: %.3lf %s%s' %
              (cost_desc[i][0], ans[i], cost_desc[i][1], L_S_R))
    print()


def prt_sum(standard: list) -> None:
    print('You get')
    for i, j in standard:
        if isinstance(i, type):
            i = i()
        print('%s: %d' % (i.desc, j))
    print()
    print('It equals')
    prt_ans(cost_sum(standard)[1])
