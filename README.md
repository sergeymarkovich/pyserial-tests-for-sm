# Скрипт для тестирования сервисного маршрутизатора

Скрипт написан на языке python, с использованием библиотеки pyserial, для тестирования сервисного маршрутизатора путем подключения через консольный кабель.

Функция ***enter_bmc*** -  при чтении из последовательного порта строки `Hit any key to stop autoboot` передает символы: три стрелки вниз и enter для вхождения в BMC console. 

Функция ***send_commands*** - считывает команды по одной из текстового файла `input.txt`. Для реализации последовательного выполнения строк из файла добавлено условие на проверку содержания символа `#`. Так же фунция выводит результат работы команд в консоль и сохраняет весь вывод из консоли подключенного устройства в генерируемый файл `output.txt`. Название файла сопоставлено времени создания файла.

 Функция ***send_command*** отправляет команды в консоль маршрутизатора.

Фунция ***parse_output*** парсит данные из `#Serial number#_output.txt` файла и записывает ошибоки в файл `#Serial number#_errors.txt`



## Для запуска
Необходимо наличия на пк python 3.10 `sudo apt-get install python3` и библиотеки pyserial `pip install serial`

 Подключить консольный кабель. Из склонированной папки в терминале - `sudo python3 main.py`. Затем подать питание на устройство.

 Список тестируемых команд можно изменить в файле `input.txt`. 
 
 Выходные логи хранятся в папке `output`. Файл `#Serial number#_output.txt` - весь лог. `#Serial number#_errors.txt` - список ошибок.