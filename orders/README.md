#### Краткая документация

REST API для управления заказами ИМ (интернет-магазина). API позволяет пользователям и администраторам создавать заказы, подтверждать и отменять их, добавлять и удалять товары, а также получать детали и список заказов по дате.

#### Функции:

* Создание заказов с товарами.
* Подтверждение и отмена заказов.
* Добавление и удаление товаров из заказа.
* Получение списка заказов по дате.
* Получение деталей конкретного заказа.
* Импорт товаров.
* Уведомление о подтверждении/отмене заказов по email.
* Регистрация и авторизация пользователя, а также смена пароля; получение токена.

Когда пользователь/администратор авторизуется - ему выдаётся токен, который тесно взаимосвязан с манипуляциями заказов, адресов, подтверждением и прочее. Токен действителен 1 час (по желанию можно увеличить или вовсе убрать время). По истечении срока действия токена, необходимо будет получить новый посредством повторной авторизации. В противном случае, нельзя будет ничего сделать.

---------------------------


Для начала нужно активировать виртуальное окружение и установить зависимости (**pip install -r requirements.txt**).
 
После чего - создать папку в **orders** (где расположен **manage.py**). Внутри этой папки создать файл **api_requests.rest** и вставить следующее:


### Регистрация пользователя
POST http://127.0.0.1:8000/api/users/register/
Content-Type: application/json

{
    "username": "....",
    "password": "....",
    "email": "y@example.com"
}


### Получение токена
POST http://127.0.0.1:8000/api/users/login/
Content-Type: application/json

{
  "username": "user1",
  "password": "...."
}


### Подтверждение
GET http://127.0.0.1:8000/api/users/protected/
Authorization: Bearer YOUR TOKEN


### Верификация
POST http://127.0.0.1:8000/api/users/token/verify/
Content-Type: application/json

{
    "token": "YOUR TOKEN"

}


### Сброс пароля и создание нового

POST http://127.0.0.1:8000/api/users/password-reset/
Content-Type: application/json
Authorization: Bearer YOUR TOKEN

{
    "old_password": "....",
    "new_password": "...."
}


### Создание продукта

POST http://127.0.0.1:8000/api/products/
Content-Type: application/json
Authorization: Bearer YOUR TOKEN

{
    "name": "Honor X7C",
    "description": "........",
    "price": "16990",
    "stock": 7,
    "is_available": true,
    "supplier_name": "МегаФон",
    "color": "Green",
    "specifications": [
        {
            "spec_name": "Category",
            "spec_value": "Smartphone"
        },
        {
            "spec_name": "Material",
            "spec_value": "Plastic"
        }
    ]
}


### Создание заказа
POST http://localhost:8000/api/order/ 
Content-Type: application/json
Authorization: Bearer YOUR TOKEN

[
  {
    "customer": 8,
    "items": [
      {
        "name": "Iphone 16 4/128",
        "supplier_id": 2,
        "quantity": 1,
        "specification": ["Smartphone", "Plastic, metall"]
      }
    ],
    "shipping_address": {
      "address_line1": "Tokyo ken",
      "city": "Tokyo",
      "postal_code": "12345",
      "country": "Japan",
      "phone": "+814783456789",
      "is_primary": true
    }
  }
]

### Импорт продуктов
GET http://localhost:8000/api/order/import-products/
Authorization: Bearer YOUR TOKEN

{

  "user": "user1"

}

### Удаление товара

DELETE http://localhost:8000/api/order/38/remove-product/
Authorization: Bearer YOUR TOKEN
Content-Type: application/json

{
  "product_id": 26
}

### Удаление адреса

DELETE http://localhost:8000/api/order/39/remove-shipping-address/
Authorization: Bearer YOUR TOKEN
Content-Type: application/json


### Подтверждение заказа и отправка на почту

POST http://localhost:8000/api/order/37/confirm/
Authorization: Bearer YOUR TOKEN



### Отправка отмены заказа на почту
POST http://localhost:8000/api/order/40/cancel-confirmation/
Authorization: Bearer YOUR TOKEN


### Получение списка заказов по дате

Здесь можно менять период дат в пути

GET http://localhost:8000/api/order/filter-by-date/?start_date=2024-12-01&end_date=2024-12-02
Authorization: Bearer YOUR TOKEN


### получение деталей заказа
GET http://localhost:8000/api/order/37/
Authorization: Bearer YOUR TOKEN