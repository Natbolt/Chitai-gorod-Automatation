from Chitai_Gorod.Pages.Shop_API import ShopAPI
import allure

api = ShopAPI('https://web-gate.chitai-gorod.ru/api/')


@allure.id("SKYPRO-1")
@allure.epic("Корзина Читай-город. API")
@allure.feature("ADD")
@allure.title("Добавление одного товара в корзину")
@allure.severity("blocker")
@allure.suite("API тесты на работу с корзиной")
def test_1():
    id = api.find_good('Идеальный Че, Интуиция и новые беспринцыпные истории')["id"]
    api.add_to_cart(id)
    id_added = api.get_short_cart()["items"][0]
    with allure.step("Очистка тестового пространства: Удаление товара из корзины"):
        delid = api.get_cart()["products"][0]["id"]
        api.delete_goods(delid)
    with allure.step("Проверить, что id товара в корзине совпадает с id выбранного для добавления в корзину товара"):
        assert id == id_added

@allure.id ("SKYPRO-2")
@allure.epic("Корзина Читай-город. АРТ")
@allure.story ("Изменение количества товаров в корзине")
@allure.feature("UPDATE")
@allure.title("увеличение количества единиц одного товара в корзине")
@allure.severity("critical")
@allure. suite("API тесты на работу с корзиной")
def test_2():
    id = api.find_good('Идеальный Че, Интуиция и новые беспринцыпные истории')["id"]
    api.add_to_cart(id)
    cart_id = api.get_cart()["products"][0]["id"]
    new_q = 4
    q_in_cart = api.change_quantity_of_goods(cart_id, new_q)
    with allure.step("Очистка тестового пространства: удаление товара из корзины"):
        api.delete_goods(cart_id)
    with allure.step("Проверить, что число единиц товаров изменилось в соответствии в установленным значением"):
        assert new_q == q_in_cart

@allure.id ("SKYPRO-3")
@allure.epic("Корзина Читай-город. АРІ")
@allure.story("Удаление товара из корзины")
@allure.feature("DELETE")
@allure.title("Удаление одного товара из корзины")
@allure.severity("blocker")
@allure. suite("API тесты на работу с корзиной")
def test_3():
    id = api.find_good('Идеальный Че, Интуиция и новые беспринцыпные истории')["id"]
    api.add_to_cart(id)
    del_id = api.get_cart ()["products"][0]["id"]
    result = api.delete_goods(del_id)
    null_cart = api.get_short_cart()["quantity"]
    with allure.step("Проверить, что список товаров в корзине после удаления пуст"):
        assert len(api.get_short_cart()["items"]) == 0
    with allure.step("Проверить, что количество товаров равно нулю"):
        assert null_cart == 0
    with allure.step("Проверить, статус-код ответа - 204"):
        assert result == 204

@allure.id("SKYPRO-4")
@allure.epic("Корзина Читай-город. АРІ")
@allure. story ("Добавление нескольких товаров в корзину")
@allure.feature("ADD")
@allure.title("Добавление 3 товаров в корзину")
@allure.severity("critical")
@allure.suite("API тесты на работу с корзиной")
def test_4():
    with allure.step("Добавить в корзину все товары из списка"):
        goods = ['Пазл Premium "Искусство орнамента", 4000 элементов', 'Мягкая игрушка "Корги", 60 см', 'Акриловая краска орхидея olki, 100 мл']
        total_cost = 0
        for i in goods:
            id = api.find_good(i)["id"]
            price = api.find_good(i)["price"]
            total_cost += api.find_good(i)["price"]
            api.add_to_cart(id)
    api.get_short_cart()
    with allure.step("Посчитать количество товаров в корзине"):
        count = len(api.get_short_cart()["items"])
    with allure.step("Посчитать общую сумму товаров в корзине"):
        total_sum = api.get_cart()["costWithSale"]
    api.delete_all()
    with allure.step("Проверить, что общая сумма покупки совпадает общей стоимостью трех добавленных товаров"):
        assert total_sum == total_cost
    with allure.step("Проверить, что количество товаров в корзине совпадает в количеством добавленных товаров"):
        assert count == len(goods)

@allure.id("SKYPRO-5")
@allure.epic("Корзина Читай-город. АРІ")
@allure. story ("Добавление нескольких товаров в корзину с последующим удалением нескольких")
@allure.feature("ADD")
@allure.title("Добавление 3 товаров в корзину и Удаление двух из них")
@allure.severity("critical")
@allure.suite("API тесты на работу с корзиной")
def test_5():
    with allure.step("Добавить в корзину все товары из списка"):
        goods = ['Пазл Premium "Искусство орнамента", 4000 элементов', 'Мягкая игрушка "Корги", 60 см', 'Акриловая краска орхидея olki, 100 мл']
        total_cost = 0
        for i in goods:
            id = api.find_good(i)["id"]
            price = api.find_good(i)["price"]
            total_cost += api.find_good(i)["price"]
            api.add_to_cart(id)
    api.get_cart()
    with allure.step("Посчитать количество товаров в корзине"):
        count = len(api.get_short_cart()["items"])
    with allure.step("Удалить первые два добавленных товара по id"):
        del_goods_by_id = []
        del_goods_by_id.append(api.get_cart()["products"][0]["id"])
        del_goods_by_id.append(api.get_cart()["products"][1]["id"])
        for id in del_goods_by_id:
            result = api.delete_goods(id)
        deleted_cart = api.get_short_cart()["quantity"]
    with allure.step("Проверить, что список товаров в корзине после удаления равен 1"):
        assert len(api.get_short_cart()["items"]) == 1
    with allure.step("Проверить, что количество товаров равно 1"):
        assert deleted_cart == 1
    with allure.step("Проверить, статус-код ответа - 204"):
        assert result == 204
    with allure.step("Очистка тестового пространства: удаление товара из корзины"):
        api.delete_goods(deleted_cart)
