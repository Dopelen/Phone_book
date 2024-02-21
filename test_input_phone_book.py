import chardet
import pytest

from phone_book import Phone_Book


@pytest.fixture
def phone_book():
    return Phone_Book(initialize=False)


@pytest.fixture(autouse=True)
def patch_input(monkeypatch):
    def mock_input(user_inputs):
        try:
            return next(user_inputs)
        except StopIteration:
            return ""

    monkeypatch.setattr('builtins.input', mock_input)


@pytest.fixture
def content():
    with open('test_file.txt', 'r') as file:
        content = file.read()
        content_strip = [elem.strip("\n") for elem in content]
        content_split = [elem.split("\t") for elem in content_strip]
        return content_split


def test_access_test_file():
    with open('test_file.txt', 'rb') as f:
        content_byt = f.read()
        encoding_info = chardet.detect(content_byt)
        file_encoding = encoding_info['encoding']


def test_input_and_output_0_digits(phone_book, monkeypatch, capsys):
    elements_for_check = 5
    user_inputs = iter(["1", "66", "513", "0", " ", "7"])
    expected_value = iter([1, 66, 513, 0, "Введенный", 7])
    for elem in range(elements_for_check):
        if elem == 4:
            phone_book.custom_input(user_inputs)
            if next(expected_value) in capsys.readouterr().out:
                assert "" in capsys.readouterr().out
        else:
            assert phone_book.custom_input(user_inputs) == next(expected_value)
            captured = capsys.readouterr()
            assert "" in captured.out
            assert captured.out.strip() == ""
            assert captured.err.strip() == ""


def test_input_and_output_1_titles(phone_book, monkeypatch, capsys):
    test_names = ["Ivanov_IV", "Petrov-Petrovich", "Sidorova&Co", "Johnson-Smith&Partners", "Ivanovа_Петровна",
                  "123_Name",
                  "Greg", "Company!", "Avangard", "$$organization", "Shreck", "Company Name", "Yurgov",
                  "Organization 123",
                  "Pobeda_corp"]
    expected_output = ["Ivanov_IV", "Petrov-Petrovich", "Sidorova&Co", "Johnson-Smith&Partners", "Ivanovа_Петровна",
                       "123_Name",
                       "Greg", "ERROR", "Avangard", "ERROR", "Shreck", "ERROR", "Yurgov", "ERROR",
                       "Pobeda_corp"]
    elements_for_check = len(test_names)
    for elem in range(elements_for_check):
        assert phone_book.custom_input("", 1, test_names[elem]) == expected_output[elem]
        captured = capsys.readouterr()


def test_input_and_output_2_numbers(phone_book, monkeypatch, capsys):
    test_names = ['+1234567890123456', '+1234567890', '1234567890abc', '+12345678901234567', '+1234', '123456789012345',
                  '123456789', '12345678901', '+123', '12345', '+12345678901234567890', '+12abc', '+1', '+abc',
                  '+1234567890abc', 'abc', '+', '+123456789012345678901', '+1a', '1234567890abc']

    expected_output = ['+1234567890123456', '+1234567890', 'ERROR', 'ERROR', '+1234', '123456789012345', '123456789',
                       '12345678901', '+123', '12345', 'ERROR', 'ERROR', '+1', 'ERROR', 'ERROR', 'ERROR', 'ERROR',
                       'ERROR',
                       'ERROR', 'ERROR']

    elements_for_check = len(test_names)
    for elem in range(elements_for_check):
        assert phone_book.custom_input("", 2, test_names[elem]) == expected_output[elem]
        captured = capsys.readouterr()


def test_input_and_output_3_digits_asterisk(phone_book, monkeypatch, capsys):
    test_names = ['*', '1', 'qLaUDZuHjLE', '9844980257685883758', 'PmkrHvfr',
                  '0429798822040984209', '7454203749887344015', '4', 'ZSbtrGrGTFQHzWfpxuj',
                  '7109783176163632612', '279932042']

    expected_output = ['*', '1', 'ERROR', '9844980257685883758',
                       'ERROR', '0429798822040984209', '7454203749887344015', '4',
                       'ERROR', '7109783176163632612', '279932042']

    elements_for_check = len(test_names)
    for elem in range(elements_for_check):
        assert phone_book.custom_input("", 3, test_names[elem]) == expected_output[elem]
        captured = capsys.readouterr()
