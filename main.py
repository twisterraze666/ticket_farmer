import asyncio
import os
import re
from datetime import datetime
from typing import Dict, List

from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from rich.console import Console
from rich.theme import Theme

from config import (BIRTHDAY_DATE, COOKIES, FAMILY, HEADERS, MEDIC_SERVICE_URL,
                    NAME, PHONE_NUMBER, ROOM_IDS, SECOND_NAME)
from medicservice.types import Info, Person, Ticket


custom_theme = Theme({
    "flower":"color(200)",
    "meadow":"#D59B2D b",
    "coffee":"#8D541E b",
    "status":"color(46) b",
    "reason":"color(9) b",
    "name":"color(220)",
    "family":"color(214)",
    "patronymic":"color(208)",
    "speciality":"color(196)"
})
console = Console(width=25, theme=custom_theme)

class MedicService:
    """MedicService."""

    def __init__(
        self, cookies: dict, headers: dict, medic_service_url: str, person: Person
    ) -> None:
        """__init__.

        Args:
            cookies (dict): cookies
            headers (dict): headers
            medic_service_url (str): medic_service_url
            person (Person): person

        Returns:
            None:
        """
        self.cookies = cookies
        self.headers = headers
        self.medic_service_url = medic_service_url
        self.person = person

    async def parse(self, json_ticket_object: Dict, room_id: int):
        id = json_ticket_object.get("id")
        date = datetime.strptime(
            f'{json_ticket_object.get("ticketdate")} {json_ticket_object.get("tickettime")}',
            "%Y-%m-%d %H:%M",
        )
        department = json_ticket_object.get("ticketdepartment")
        duration = json_ticket_object.get("ticketduration")
        graph = json_ticket_object.get("ticketgraph")
        hash = json_ticket_object.get("tickethash")
        cabinet = json_ticket_object.get("ticketcabinet")
        info = await self.get_info(room_id)

        return Ticket(
            date=date,
            department=department,
            cabinet=cabinet,
            graph=graph,
            duration=duration,
            hash=hash,
            id=id,
            info=info,
        )

    async def get_tickets(self, room_id: int) -> List:
        """Get tickets.

        Args:
            room_id (int): room_id

        Returns:
            List:
        """

        params = {"room_id": room_id}
        async with ClientSession() as session:
            response = await session.get(
                f"{self.medic_service_url}/ticketGet/",
                params=params,
                headers=self.headers,
                cookies=self.cookies,
            )
            soup = BeautifulSoup(await response.text(), "lxml")
            ticket_blocks = soup.find_all("div", class_="TimeItem")
            tickets_list = []
            for ticket_block in ticket_blocks:
                json_ticket_object = ticket_block.attrs
                ticket = await self.parse(json_ticket_object, room_id)
                tickets_list.append(ticket)
            return tickets_list

    async def get_ticket(self, room_id: int, json_ticket_object: dict) -> Ticket:
        """Get ticket.

        Args:
            room_id (int): room_id
            json_ticket_object (dict): json_ticket_object

        Returns:
            Ticket:
        """
        data = {
            "patient[family]": self.person.family,
            "patient[name]": self.person.name,
            "patient[secondname]": self.person.second_name,
            "patient[birthdayDate]": self.person.birthday_date,
            "patient[PhoneNumber]": self.person.phone_number,
            "Approve": "sendData",
        }

        params = {
            "TicketTime": json_ticket_object.get("tickettime"),
            "TicketDate": json_ticket_object.get("ticketdate"),
            "TicketDepartment": json_ticket_object.get("ticketdepartment"),
            "TicketGraph": json_ticket_object.get("ticketgraph"),
            "TicketHash": json_ticket_object.get("tickethash"),
            "TicketCabinet": json_ticket_object.get("ticketcabinet"),
            "TicketID": json_ticket_object.get("ticketid"),
            "TicketDuration": json_ticket_object.get("ticketduration"),
        }
        async with ClientSession() as session:
            response = await session.post(
                f"{self.medic_service_url}/ticketGet/views/DisplayTicket.php",
                headers=self.headers,
                cookies=self.cookies,
                data=data,
                params=params,
            )
            soup = BeautifulSoup(await response.text(), "lxml")
            ticket_result_block = soup.find("body", {"class": "ticket-getting__result"})
            alert_block = ticket_result_block.find("div", {"role": "alert"})

            status = alert_block.find("p")
            reason = status.find_next()

            ticket = await self.parse(json_ticket_object, room_id)
            ticket.status = status.text.strip()
            ticket.reason = reason.text.strip()

            return ticket

    async def get_info(self, room_id: int) -> Info:
        """Get info about room_id.

        Args:
            room_id (int): room_id

        Returns:
            Info:
        """
        params = {
            "room_id": room_id,
        }
        async with ClientSession() as session:
            response = await session.get(
                f"{self.medic_service_url}/ticketGet/", params=params
            )
            soup = BeautifulSoup(await response.text(), "lxml")
            header_block = soup.find("header", {"class": "page-head"})

            result = header_block.text.strip()

            cabinet_pattern = re.compile(r"\d{3}")

            speciality_pattern = re.compile(r"([А-Я]+){1,}")

            doctor_pattern = re.compile(
                r"(?P<family>[А-Я][а-я]+)\s(?P<name>[А-Я][а-я]+)\s(?P<patronymic>[А-Я][а-я]+)"
            )

            if doctor_pattern.search(result):
                doctor = doctor_pattern.search(result)
                family = doctor.group("family")
                name = doctor.group("name")
                patronymic = doctor.group("patronymic")

            else:
                family = None
                name = None
                patronymic = None

            if speciality_pattern.search(result):
                speciality = speciality_pattern.search(result).group()
            else:
                speciality = None

            if cabinet_pattern.search(result):
                cabinet = int(cabinet_pattern.search(result).group())

            else:
                cabinet = None

            return Info(
                name=name,
                family=family,
                patronymic=patronymic,
                speciality=speciality,
                cabinet=cabinet,
            )
    
    async def format_ticket(self, ticket: Ticket) -> None:
        info = ticket.info
        console.print(f"🎫 [meadow]Талон к [/meadow][u]{info.speciality}", justify="center")
        console.print(f"• 📅[flower] Дата[/flower]: {ticket.date}")
        console.print(f"• 🚪[coffee] Кабинет[/coffee]: {ticket.cabinet}")
        console.print(f"• 🔥[status] Статус[/status]: {ticket.status}")
        console.print(f"• 🚨[reason] Причина[/reason]: {ticket.reason}")
        print("")
        console.print(f"👩/👨 [b u]Информация о враче", justify="center")
        console.print(f"• 🎭[name] Имя[/name]: {info.name}")
        console.print(f"• 🎀[family] Фамилия[/family]: {info.family}")
        console.print(f"• 🍿[patronymic] Отчество[/patronymic]: {info.patronymic}")
        console.print(f"• 🔧[speciality] Специальность[/speciality]: {info.speciality}")  
         
        
    async def take_ticket(self, room_id: int) -> None:
        params = {"room_id": room_id}
        console.print("📨 Получение талонов...")
        async with ClientSession() as session:
            response = await session.get(
                f"{self.medic_service_url}/ticketGet/",
                params=params,
                headers=self.headers,
                cookies=self.cookies,
            )

            soup = BeautifulSoup(await response.text(), "lxml")

            ticket_blocks = soup.find_all("div", class_="TimeItem")

            if not ticket_blocks:
                console.print("❌ Не нашли талоны к данному врачу.")
                console.print("📌 Пробуем снова...")
                raise ValueError()

            for ticket in ticket_blocks:
                json_ticket_object = ticket.attrs
                console.print("[color(46)]Успех![/] Нашли талон 🎫")
                ticket = await self.get_ticket(
                    json_ticket_object=json_ticket_object, room_id=room_id
                )
                with open("tickets.log", "a") as file:
                    file.write(f"{ticket}\n\n")

                print("🎉 Взяли для тебя талон 🎫")
                print(f"👌 Держи -> ")
                await self.format_ticket(ticket)
                break


async def main():
    person = Person(
        birthday_date=BIRTHDAY_DATE,
        phone_number=PHONE_NUMBER,
        family=FAMILY,
        name=NAME,
        second_name=SECOND_NAME,
    )
    md = MedicService(
        cookies=COOKIES,
        headers=HEADERS,
        medic_service_url=MEDIC_SERVICE_URL,
        person=person,
    )
    UNIQUE_ROOM_IDS = list(set(ROOM_IDS))
    count = 1
    while True:     
        for room_id in UNIQUE_ROOM_IDS:
            console.print(f"📮 Иттерация: {count}")
            loop = asyncio.get_event_loop()
            task = loop.create_task(md.take_ticket(room_id))
            try:
                await task
                UNIQUE_ROOM_IDS.remove(room_id)
                
            except ValueError:
                continue

            else:
                continue

            finally:
                count += 1
        
        if not UNIQUE_ROOM_IDS:
            break

        else:
            continue



if __name__ == "__main__":
    asyncio.run(main())
