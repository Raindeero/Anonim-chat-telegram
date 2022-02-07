from enum import Enum


class Sexes(Enum):
    MALE = 1
    FEMALE = 2
    ALL = 3


class UserTempData:
    def __init__(self, uid: int, sex: Sexes):
        self.uid = uid
        self.sex = sex

        self.age = None
        self.name = None
        self.age_partner = None
        self.sex_partner = None


class TempCash:
    cash = {}

    @classmethod
    def insert(cls, uid: int, data: UserTempData):
        cls.cash[uid] = data

    @classmethod
    def add_age(cls, uid: int, age: int):
        cls.cash.get(uid).age = age

    @classmethod
    def add_name(cls, uid: int, name: str):
        cls.cash.get(uid).name = name

    @classmethod
    def get_and_add_age_partner(cls, uid: int, age: tuple) -> UserTempData:
        cls.cash.get(uid).age_partner = age
        return cls.get(uid)

    @classmethod
    def add_sex_partner(cls, uid: int, sex: Sexes):
        cls.cash.get(uid).sex_partner = sex

    @classmethod
    def get(cls, uid: int):
        return cls.cash.get(uid)

    @classmethod
    def delete(cls, uid: int):
        cls.cash.pop(uid)


SEX_DICT = {'male': Sexes.MALE, 'female': Sexes.FEMALE, 'all': Sexes.ALL}
#
# TempCash.insert(uid, UserData(uid, sex))
#
# TempCash.add_age(uid, age)
#
# TempCash.add_name(uid, name)
#
# fu = TempCash.get(uid)
# 'INSERT INTO user (id, sex, name, age) VALUES (?, ?, ?, ?)', [fu.uid, fu.sex, fu.name, fu.age]
# await mes.answer('Вы успешно зарегались!')
