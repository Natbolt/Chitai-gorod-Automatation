from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Chitai_Gorod.Pages.Main_Page import MainPage
import allure


cookie = {
    'name': 'access-token',
    'value': 'Bearer%20eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE4OTkyOTksImlhdCI6MTcyMTczMTI5OSwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6Ijk1MDYzYzNkN2ZlYWVmMzEzZTRjOTE1ZThjYzFmYjM4OWU1YTdlMjM0NTVmNmNiMzM5MzA5OGU4YjlkZDNhYmQiLCJ0eXBlIjoxMH0.Nc9WPfOvtJuUAog2NOpEvOsVyDPSOdnpXBipdPFucog'
}

@allure.id("SKYPRO-6")
@allure.epic("Поиск Читай-город. UI")
@allure.story("Поиск товара")
@allure.feature("Find")
@allure.title("Поиск товара через поисковую стороку")
@allure.description("Поиск товара по артикулу через строку поиска")
@allure.severity("critical")
@allure.suite("UI тесты на работу с поиском")
def test_find_book():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    main_page = MainPage(driver)
    book = main_page.enter_values("2824689")
    assert book == 'Идеальный Че, Интуиция и новые беспринцыпные истории'


@allure.id("SKYPRO-7")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Добавление в корзину")
@allure.feature("ADD")
@allure.title("Добавление 1 книги в корзину")
@allure.description("Добавление 1 книги в корзину")
@allure.severity("blocker")
@allure.suite("UI тесты на работу с корзиной")
def test_add_book_to_cart():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
        # main_page.cookies(cookie) кукисы не пробрасывались, добавлялся почему-то второй ключ в Application, по факту авторизации нет
    main_page.enter_values("Идеальный Че, Интуиция и новые беспринцыпные истории")
    with allure.step("Добавить первую книгу из поисковой выдачи в корзину"):
        dct = main_page.add_to_cart()
    main_page.go_cart()
    book = main_page.check_book()
    with allure.step("Проверить, что в корзину добавилась нужная книга"):
        assert book == dct["title"]


@allure.id("SKYPRO-8")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Удаление товара из корзины")
@allure.feature("DEL")
@allure.title("Удаление товара из корзины")
@allure.description("Добавление в корзину 1 книги и последующее ее удаление из корзины")
@allure.severity("critical")
@allure.suite("UI тесты на работу с корзиной")
def test_del_book():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
    main_page.enter_values("Идеальный Че, Интуиция и новые беспринцыпные истории")
    with allure.step("Добавить первую книгу из поисковой выдачи в корзину"):
        main_page.add_to_cart()
    main_page.go_cart()
    main_page.del_book()
    clear_cart = main_page.check_quantity('0 товаров')
    with allure.step("Проверить, книга удалилась из корзины"):
        assert clear_cart == '0'


@allure.id("SKYPRO-9")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Добавление одного товара в корзину")
@allure.feature("ADD")
@allure.title("Добавление одной книги в корзину и изменение количества экземляров")
@allure.description("Добавление 1 книги в корзину с последующим изменением количества ее экземпляров и удалением из корзины")
@allure.severity("critical")
@allure.suite("UI тесты на работу с корзиной")
def test_add_book():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
        # main_page.cookies(cookie) кукисы не пробрасывались, добавлялся почему-то второй ключ в Application, по факту авторизации нет
    main_page.enter_values("Идеальный Че, Интуиция и новые беспринцыпные истории")
    with allure.step("Добавить первую книгу из поисковой выдачи в корзину"):
        dct = main_page.add_to_cart()
    main_page.go_cart()
    book = main_page.check_book()
    new_q = '8'
    main_page.change_quantity(new_q)
    cart_q = main_page.check_quantity('8 товаров')
    main_page.del_book()
    clear_cart = main_page.check_quantity('0 товаров')
    with allure.step("Проверить, что в корзину добавилась нужная книга"):
        assert book == dct["title"]
    with allure.step("Проверить, что число экземпляров книги увеличилось в соответствии с выставленным значением"):
        assert cart_q == new_q
    with allure.step("Проверить, книга удалилась из корзины"):
        assert clear_cart == '0'


@allure.id("SKYPRO-10")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Добавление нескольких товаров в корзину")
@allure.feature("ADD")
@allure.title("Добавление 3 книг в корзину")
@allure.description("Добавление книг из списка и подсчет общей стоимости покупки")
@allure.severity("critical")
@allure.suite("UI тесты на работу с корзиной")
def test_add_three_books():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
        # main_page.cookies(cookie)
    with allure.step("Добаввить по очереди 3 книги в корзину через поиск"):
        total_sum = 0
        with allure.step("Выполнить цикл для поиска каждой книги по названию и последующего добавления в корзину первой книги из поисковой выдачи"):
            for i in ["1984", "Сумерки", "Цветы для Элджернона"]:
                main_page.enter_values(i)
                dct1 = main_page.add_to_cart()
                total_sum += int(dct1["price"])
    with allure.step("Перейти в корзину"):
        main_page.go_cart()
        with allure.step("Записать в переменную общую стоимость покупки"):
            cart_total = main_page.check_total()
    with allure.step("Проверить, что сумма покупки совпадает с общей суммой трех добавленных книг"):
        assert total_sum >= int(cart_total)