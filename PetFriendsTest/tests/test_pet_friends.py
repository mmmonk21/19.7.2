
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_pets_with_valid_data_without_photo(name = 'Не знаю', animal_tipe = 'Котя', age = '4'):
    """ Проверка на добавление питомца без фото"""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_tipe, age)
    assert status == 200
    assert result['name'] == name

def test_get_api_key_for_non_correct_email(email = 'yanichegoneponimau@mail.ru', password = valid_password):
    """ Негативное тестирование на ввод неверного e-mail """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_for_no_valid_email(email = 'невалидный@mail.ru', password = valid_password):
    """Негативное тестирование на ввод невалидного e-mail, то есть с запрещенными символами"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_no_valid_password(email=valid_email, password='88005553535'):
    """ Негативное тестирование на ввод неправильного пароля """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_no_valid_age_str(name = 'Козлик', animal_type = 'барашка', age = 'старец', pet_photo = 'images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с вводом нечисловой переменной в поле возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert age not in result['age']

def test_add_new_pet_with_four_age_number(name = 'Мурзик', animal_type = 'Барсук', age = '1234', pet_photo = 'images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование, добавление питомца с четырехзначным числом в поле возраст """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert len(result['age']) < 4, 'Питомец добавлен на сайт с четырехзначным числом в поле возраст!'

def test_add_pet_with_value_in_variable_name(name='', animal_type='кот', age='2', pet_photo='images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование,  возможности добавления питомца без имени """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Питомец добавлен на сайт с пустым значением в имени'

def test_add_pet_with_a_lot_of_variable_name(animal_type='Нихуахуа', age='6', pet_photo='images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с именем состоящим более 5 слов """

    name = 'На самом деле это был милый Ежик'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    assert status == 200
    assert len(list_name) < 5, 'Питомец добавлен с именем более 5 слов'

def test_add_new_pet_with_no_valid_tipe_int(name = 'Числа', animal_type = '12348', age = '12', pet_photo = 'images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с вводом числа в поле порода"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type not in result['animal_type'], 'Нельзя указывать числа в названии породы!'

def test_add_pet_with_a_lot_of_variable_tipe(name ='Биба', age='25', pet_photo='images/9c944406a89a61d775c41652fcc7b2a5.jpg'):
    """ Проверка, негативное тестирование, добавления питомца с названием породы состоящим более 5 слов """

    animal_type = 'Этой очень милый Ежик к Вам пришел'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['animal_type'].split()
    assert status == 200
    assert len(list_name) < 5, 'Питомец добавлен с названием породы более 5 слов'