import os
import shutil
import time


class Sorter:
    """
    Небольшой код для сортировки фотографий или иных любых файлов по годам и месяцам.
    """

    def __init__(self, scan_directory):
        self.scan_directory = scan_directory
        self.stat = None

    def sort_file(self):
        for dirpath, dirnames, filenames in os.walk(self.scan_directory):
            for filename in filenames:
                full_file_path = os.path.join(dirpath, filename)
                secs = os.path.getmtime(full_file_path)
                file_time = time.gmtime(secs)
                new_icon_path = (os.path.dirname(__file__) + '/' + 'icons_by_year' + '/' + str(
                    file_time.tm_year) + '/' + str(file_time.tm_mon))
                new_icon_path = os.path.normpath(new_icon_path)
                os.makedirs(new_icon_path, exist_ok=True)
                shutil.copy2(src=full_file_path, dst=new_icon_path + '/' + filename)


scan = Sorter(scan_directory='icons')
scan.sort_file()
