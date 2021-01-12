# -*- coding: utf-8 -*-

from pathlib import Path


class NotEmailError(Exception):
    pass


class NotNameError(Exception):
    pass


def right_user_data(current_line):
    user_name, user_email, user_age = current_line.split(' ')
    user_age = int(user_age)

    if len(current_line.split()) != 3:
        raise ValueError('Не присутсвуют все три поля - ')
    elif not user_name.isalpha():
        raise NotNameError('Поле имени содержит не только буквы - ')
    elif '@' not in user_email:
        raise NotEmailError('Поле емейл не содержит @ - ')
    elif '.' not in user_email:
        raise NotEmailError('Поле емейл не содержит .(точку) - ')
    elif user_age not in range(10, 100):
        raise ValueError('Поле возраст не является числом от 10 до 99 - ')
    else:
        return current_line


analyze_file = Path('registrations.txt')
analyze_file.resolve()
with open(analyze_file, 'r', encoding='UTF-8') as file_source, \
        open('registrations_good.log.txt', mode='w', encoding='UTF-8') as good_log, \
        open('registrations_bad.log.txt', mode='w', encoding='UTF-8') as bad_log:
    for line in file_source:
        line = line[:-1]
        try:
            right_user_data(line)
            good_log.write(line + '\n')
        except ValueError as exc:
            bad_log.write(f'{exc}' + line + '\n')
        except NotEmailError as exc:
            bad_log.write(f'{exc}' + line + '\n')
        except NotNameError as exc:
            bad_log.write(f'{exc}' + line + '\n')

