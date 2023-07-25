import datetime
import re
import typing
from dataclasses import dataclass


class Person:
    def __init__(
        self,
        name: typing.Text,
        family: typing.Text,
        second_name: typing.Text,
        birthday_date: datetime.datetime | typing.Text,
        phone_number: typing.Text,
    ) -> None:
        self.name = name
        self.family = family
        self.second_name = second_name
        self.birthday_date = birthday_date
        self.phone_number = phone_number

    @staticmethod
    def check(value: typing.Text):
        if re.match(r"[А-Я][а-я]+", value):
            return True
        else:
            return False

    @staticmethod
    def format_str(value: typing.Text):
        return f"{value} must match the format Xxxx..."

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: typing.Text):
        if self.check(value):
            self.__name = value
            return
        else:
            raise ValueError(self.format_str("Name"))

    @property
    def family(self):
        return self.__family

    @family.setter
    def family(self, value: typing.Text):
        if self.check(value):
            self.__family = value
            return

        else:
            raise ValueError(self.format_str("Family"))

    @property
    def second_name(self):
        return self.__second_name

    @second_name.setter
    def second_name(self, value: typing.Text):
        if self.check(value):
            self.__second_name = value
        else:
            raise ValueError(self.format_str("Second name"))

    @property
    def birthday_date(self):
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, date: typing.Text):
        try:
            valid_date = datetime.datetime.strptime(date, "%d.%m.%Y")
            self.__birthday_date = valid_date

        except ValueError:
            raise ValueError("The date format must match dd.mm.yy")

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: typing.Text):
        self.__phone_number = value


@dataclass
class Info:
    """Info."""

    name: typing.Text | None = None
    family: typing.Text | None = None
    patronymic: typing.Text | None = None
    speciality: typing.Text | None = None
    cabinet: int | None = None


@dataclass
class Ticket:
    """Ticket."""

    date: datetime.date
    cabinet: int
    department: int
    graph: int
    duration: int
    hash: typing.Text
    info: Info
    id: int | None = None
    status: typing.Text | None = None
    reason: typing.Text | None = None
