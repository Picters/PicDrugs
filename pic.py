import requests
from bs4 import BeautifulSoup
import time

def main_menu():
    while True:
        print("1. Search")
        print("0. Exit\n")
        choice = input("Выберите опцию: ")

        if choice == "1":
            search_menu()
        elif choice == "0":
            print("Выход из программы.\n")
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

def search_menu():
    while True:
        print("\n1. WEB")
        print("2. IP-search")
        print("0. Back\n")
        choice = input("Выберите опцию: ")

        if choice == "1":
            web_search_menu()
        elif choice == "2":
            ip_search_menu()
        elif choice == "0":
            print()  # добавляет пустую строку перед возвратом в главное меню
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

def web_search_menu():
    while True:
        print("\nВыберите поисковую систему:")
        print("1. Google")
        print("2. Yandex")
        print("3. Bing")
        print("0. Back\n")
        choice = input("Ваш выбор: ")

        if choice in ["1", "2", "3"]:
            query = input("Введите поисковый запрос: ")
            count = int(input("Сколько результатов показать? "))
            print()  # Пустая строка перед результатами
            if choice == "1":
                google_search(query, count)
            elif choice == "2":
                yandex_search(query, count)
            elif choice == "3":
                bing_search(query, count)
        elif choice == "0":
            print()  # Пустая строка перед возвратом в меню
            break
        else:
            print("Неверный выбор. Попробуйте снова.\n")

def ip_search_menu():
    ip_address = input("Введите IP-адрес для поиска информации: ")
    print()  # Пустая строка перед результатами IP
    ip_info(ip_address)

def ip_info(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("\nИнформация о IP:")
        print(f"IP: {data.get('ip', 'Неизвестно')}")
        print(f"Город: {data.get('city', 'Неизвестно')}")
        print(f"Регион: {data.get('region', 'Неизвестно')}")
        print(f"Страна: {data.get('country', 'Неизвестно')}")
        print(f"Организация: {data.get('org', 'Неизвестно')}")
        print(f"Локация: {data.get('loc', 'Неизвестно')}")
        print(f"Почтовый индекс: {data.get('postal', 'Неизвестно')}\n")
    else:
        print("Не удалось получить информацию об IP-адресе.\n")

def google_search(query, count):
    print("\nРезультаты поиска Google:\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("div.g")
        for i, result in enumerate(results[:count], 1):
            title = result.select_one("h3")
            link = result.select_one("a")
            snippet = result.select_one(".VwiC3b")
            
            if title and link and snippet:
                print(f"{i}. {title.get_text()} - {link['href']}")
                print(f"   {snippet.get_text()}\n")
            time.sleep(1)
    else:
        print("Ошибка при выполнении запроса.\n")

def yandex_search(query, count):
    print("\nРезультаты поиска Yandex:\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    search_url = f"https://yandex.com/search/?text={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("li.serp-item")
        for i, result in enumerate(results[:count], 1):
            title = result.select_one("h2 a")
            snippet = result.select_one(".text-container")
            
            if title and snippet:
                print(f"{i}. {title.get_text()} - {title['href']}")
                print(f"   {snippet.get_text()}\n")
            time.sleep(1)
    else:
        print("Ошибка при выполнении запроса.\n")

def bing_search(query, count):
    print("\nРезультаты поиска Bing:\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    search_url = f"https://www.bing.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select("li.b_algo")
        for i, result in enumerate(results[:count], 1):
            title = result.select_one("h2 a")
            snippet = result.select_one(".b_caption p")
            
            if title and snippet:
                print(f"{i}. {title.get_text()} - {title['href']}")
                print(f"   {snippet.get_text()}\n")
            time.sleep(1)
    else:
        print("Ошибка при выполнении запроса.\n")

if __name__ == "__main__":
    main_menu()
