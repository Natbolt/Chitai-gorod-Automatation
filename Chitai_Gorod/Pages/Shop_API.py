import requests
import allure

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjE4OTkyOTksImlhdCI6MTcyMTczMTI5OSwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6Ijk1MDYzYzNkN2ZlYWVmMzEzZTRjOTE1ZThjYzFmYjM4OWU1YTdlMjM0NTVmNmNiMzM5MzA5OGU4YjlkZDNhYmQiLCJ0eXBlIjoxMH0.Nc9WPfOvtJuUAog2NOpEvOsVyDPSOdnpXBipdPFucog'
class ShopAPI:
    def __init__(self, url):
        self.url = url

    @allure.step("Найти товары по названию {phrase}")
    def find_good(self, phrase):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+f'v2/search/product?customerCityId=2&phrase={phrase}&products%5Bpage%5D=1&products%5Bper-page%5D=48&sortPreset=relevance', headers=my_headers)
        id = resp.json()["included"][0]["attributes"]["id"]
        price = resp.json()["included"][0]["attributes"]["price"]
        return {"id": id, "price": price}

    @allure.step("Добавить первый товар по id {id} в корзину")
    def add_to_cart(self, id):
        body = {
            "id": id,
            "adData": {"item_list_name": "product-page"}
        }
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        requests.post(self.url+'v1/cart/product/', json = body, headers=my_headers)

    @allure.step("Получить список id товаров в корзине")
    def get_short_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/short', headers=my_headers)
        return resp.json()["data"]

    @allure.step("Получить список товаров в корзине с подробной информацией")
    def get_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/', headers=my_headers)
        return resp.json()

    @allure.step("Изменить количество экземпляров {number} товара по id {id}")
    def change_quantity_of_goods(self, id, number):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        body = [
             {
                 "id": id,
                 "quantity": number
             }
        ]
        resp = requests.put(self.url+'v1/cart/', json = body, headers=my_headers)
        return resp.json()["products"][0]["quantity"]

    @allure.step("Удалить товар по id {id} из корзины")
    def delete_goods(self, id):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/product/{id}', headers=my_headers)
        return resp.status_code

    @allure.step("Очистить корзину")
    def delete_all(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/', headers=my_headers)
