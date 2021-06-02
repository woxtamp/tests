import pytest
import app
import unittest.mock as mock
import allure

TEST_DOC_NUM = 'test-1234-12'
TEST_DOC_TYPE = 'test-passport'
TEST_OWNER_NAME = 'test-owner-name'
TEST_SHELF_NUM = '101'


class TestApp:

    # Перед запуском каждого теста очищаем список документов и полок
    def setup(self):
        app.directories = {}
        app.documents = []

    @allure.feature('Документы')
    @allure.story('Отсутствие документа')
    def test_check_documents_not_exist(self):
        with allure.step('Проверим, что метод вернёт False'):
            assert app.check_document_existance('77777') is False

    @allure.feature('Документы')
    @allure.story('Наличие документа')
    def test_check_documents_exist(self):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with allure.step('Проверим, что метод вернёт True'):
            assert app.check_document_existance(TEST_DOC_NUM) is True

    @allure.feature('Документы')
    @allure.story('Имя владельца документа')
    @pytest.mark.parametrize('doc_num, return_value', [(TEST_DOC_NUM, TEST_OWNER_NAME), ('77777', None)])
    def test_get_doc_owner_name(self, doc_num, return_value):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with allure.step('Проверим, что метод вернёт имя владельца документа или None'):
            with mock.patch('app.input', return_value=doc_num):
                assert app.get_doc_owner_name() == return_value

    @allure.feature('Полки')
    @allure.story('Удаление документа из полки')
    def test_remove_doc_from_shelf(self):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with allure.step('Проверим, что метод вернёт None'):
            assert app.remove_doc_from_shelf(TEST_DOC_NUM) is None
        with allure.step('Проверим, что удалённого документа нет на полке'):
            assert app.directories.get(TEST_SHELF_NUM) == []

    @allure.feature('Полки')
    @allure.story('Номер полки')
    @pytest.mark.parametrize('shelf_num, return_value', [('77777', ('77777', True)),
                                                         (TEST_SHELF_NUM, (TEST_SHELF_NUM, False))])
    def test_add_new_shelf(self, shelf_num, return_value):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: []
            }
        with allure.step('Проверим, что метод вернёт номер полки и True/False в зависимости от наличия документа'):
            with mock.patch('app.input', return_value=return_value):
                assert app.add_new_shelf(shelf_num) == return_value

    @allure.feature('Документы')
    @allure.story('Добавление нового документа на полку')
    @pytest.mark.parametrize('doc_num, shelf_num', [('77777', '12')])
    def test_append_new_doc_to_shelf(self, doc_num, shelf_num):
        with allure.step('Добавляем документ на полку полку, проверяем что метод вернул None'):
            assert app.append_doc_to_shelf(doc_num, shelf_num) is None
        with allure.step('Проверяем, что документ добавлен на полку'):
            assert app.directories.get(shelf_num) == [doc_num]

    @allure.feature('Документы')
    @allure.story('Добавление уже существующего документа на полку')
    @pytest.mark.parametrize('doc_num, shelf_num', [(TEST_DOC_NUM, TEST_SHELF_NUM)])
    def test_append_exist_doc_to_shelf(self, doc_num, shelf_num):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with allure.step('Добавляем документ на полку полку, проверяем что метод вернул None'):
            assert app.append_doc_to_shelf(doc_num, shelf_num) is None
        with allure.step('Проверяем, что на полке два одинаковых документа'):
            assert app.directories.get(shelf_num) == [doc_num, doc_num]

    @allure.feature('Документы')
    @allure.story('Удаление существующего документа')
    @pytest.mark.parametrize('return_value, return_bool', [(TEST_DOC_NUM, True)])
    def test_delete_exist_doc(self, return_value, return_bool):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with mock.patch('app.input', return_value=return_value):
            with allure.step('Проверяем, метод вернёт номер документа и True'):
                assert app.delete_doc() == (return_value, return_bool)
            assert app.directories.get(TEST_SHELF_NUM) == []
            with allure.step('Проверяем, что документ удалён из хранилища'):
                assert {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME} not in app.documents

    @allure.feature('Документы')
    @allure.story('Попытка удаления несуществующего документа')
    @pytest.mark.parametrize('return_value, return_none', [(TEST_DOC_NUM, None)])
    def test_delete_non_exist_doc(self, return_value, return_none):
        with mock.patch('app.input', return_value=return_value):
            with allure.step('Проверяем, метод вернёт None'):
                assert app.delete_doc() == return_none

    @allure.feature('Полки')
    @allure.story('Получение номера полки по номеру документа')
    @pytest.mark.parametrize('doc_num, shelf_num', [(TEST_DOC_NUM, TEST_SHELF_NUM), ('77777', None)])
    def test_get_doc_shelf(self, doc_num, shelf_num):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        with mock.patch('app.input', return_value=doc_num):
            with allure.step('Проверим, что метод вернул корректный номер полки'):
                assert app.get_doc_shelf() == shelf_num

    @allure.feature('Документы')
    @allure.story('Перемещение документа на другую полку')
    @pytest.mark.parametrize('mock_args', [[TEST_DOC_NUM, TEST_SHELF_NUM], [TEST_DOC_NUM, '2']])
    @mock.patch('app.print')
    @mock.patch('app.input', create=True)
    def test_move_doc_to_shelf_with_print(self, mock_input, mock_print, mock_args):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        mock_input.side_effect = [mock_args[0], mock_args[1]]
        app.move_doc_to_shelf()
        with allure.step('Проверим текст сообщения об успешности перемещения документа'):
            mock_print.assert_called_with(f'Документ номер "{mock_args[0]}" был перемещен на полку '
                                          f'номер "{mock_args[1]}"')
        with allure.step('Проверим, что документ перемещён на указанную полку'):
            assert app.directories.get(mock_args[1]) == [mock_args[0]]

    @allure.feature('Документы')
    @allure.story('Получение информации о документе')
    @pytest.mark.parametrize('mock_args', [[TEST_DOC_TYPE, TEST_DOC_NUM, TEST_OWNER_NAME]])
    @mock.patch('app.print')
    def test_show_document_info(self, mock_print, mock_args):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        document = {"type": mock_args[0], "number": mock_args[1], "name": mock_args[2]}
        app.show_document_info(document)
        with allure.step('Проверим корректность отображения текста с информацией о документе'):
            mock_print.assert_called_with(f'{mock_args[0]} "{mock_args[1]}" "{mock_args[2]}"')

    @allure.feature('Документы')
    @allure.story('Получение информации о всех документах')
    @pytest.mark.parametrize('mock_args', [[TEST_DOC_TYPE, TEST_DOC_NUM, TEST_OWNER_NAME]])
    @mock.patch('app.print')
    def test_show_all_docs_info(self, mock_print, mock_args):
        with allure.step('Создадим документ и полку'):
            app.documents = [
                {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME}
            ]
            app.directories = {
                TEST_SHELF_NUM: [TEST_DOC_NUM]
            }
        app.show_all_docs_info()
        with allure.step('Проверим корректность отображения текста с информацией о документах'):
            mock_print.assert_called_with(f'{mock_args[0]} "{mock_args[1]}" "{mock_args[2]}"')

    @allure.feature('Документы')
    @allure.story('Создание документа')
    @pytest.mark.parametrize('directories', [{TEST_SHELF_NUM: []}, {}])
    def test_add_new_doc(self, directories):
        app.directories = directories
        mock_args = [TEST_DOC_NUM, TEST_DOC_TYPE, TEST_OWNER_NAME, TEST_SHELF_NUM]
        with mock.patch('app.input') as mocked_input:
            mocked_input.side_effect = mock_args
            with allure.step('Проверим, что метод вернул номер полки на которую добавлен документ'):
                assert app.add_new_doc() == TEST_SHELF_NUM
        with allure.step('Проверим, что данные добавлены в хранилище'):
            assert app.directories.get(TEST_SHELF_NUM) == [TEST_DOC_NUM]
            assert {"type": TEST_DOC_TYPE, "number": TEST_DOC_NUM, "name": TEST_OWNER_NAME} in app.documents

    def teardown(self):
        # Перед завершением каждого теста очищаем список документов и полок
        app.directories = {}
        app.documents = []
