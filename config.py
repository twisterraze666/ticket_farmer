ROOM_IDS = []  # Room ids (list[int,...])
FAMILY = ""  # Family (str) Example: Kakashkind
NAME = ""  # Name (str) Example: Garik
SECOND_NAME = ""  # Patronymic (str) Example: Gazarosovich
BIRTHDAY_DATE = ""  # Birthday date (str) Example: 09.09.1999
PHONE_NUMBER = "+375 ()"  # Phone number Example: +375 (29) 123-45-67
MEDIC_SERVICE_URL = "https://medic-service.by/BrestGDP1"  # Medic service url (str) Default: https://medic-service.by/BrestGDP1


COOKIES = {}  # Cookies

# May not be changed.
HEADERS = {
    "authority": "medic-service.by",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 9; TECNO KC2 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36",
}  # Headers
