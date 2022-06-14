""" Get day type - normal day, holiday, etc. Based on Warsaw Transport Authority timetable data, of all things """

import ftplib
import os
import datetime
import json
from pathlib import Path



def _get_file(today_obj=datetime.datetime.now()):
    """ Download timetable data from Warsaw Transport Authority """
    ftp = ftplib.FTP('rozklady.ztm.waw.pl')
    ftp.login()

    with open(Path(__file__).parent / 'data' / 'timetable.7z', 'wb') as fp:
        for i in range(-1, 7):
            try:
                # We try until we find any file near to todsays date
                today_obj += datetime.timedelta(days=i)
                today_str = today_obj.strftime('%y%m%d')
                ftp.retrbinary(f'RETR RA{today_str}.7z', fp.write)
                print('File found - ', today_str)
                break
            except ftplib.error_perm:
                print('File not found - ', today_str)

    ftp.quit()

    try:
        import py7zr
        with open(Path(__file__).parent / 'data' / 'timetable.7z', 'rb') as fp:
            with py7zr.SevenZipFile(fp) as archive:
                archive.extractall(path=Path(__file__).parent / 'data')
    except ImportError:
        print('py7zr not installed; Cannot unpack data')
        print('pip install py7zr')
        raise Exception('py7zr not installed')
    
    return today_str

def _get_calendar(f):
    days = {
        # 'timestamp': 'free|working',
    }

    mode = 'TY'  # or KA
    for line in f:
        if line.startswith('#KA'):
            break
        elif line.startswith('*KA'):
            mode = 'KA'
            continue

        if mode != 'KA':
            continue
        else:
            line = line.split()
            day = line[0]
            candidates = line[2:-1]
            if 'DP' in candidates:
                days[day] = 'working'
            elif 'DS' in candidates:
                days[day] = 'free'

    return days

def get_calendar(today_obj=datetime.datetime.now()):
    found = False
    files = os.listdir(Path(__file__).parent / 'data')
    # Try finding file in current directory
    for i in range(-1, 7):
        today_obj += datetime.timedelta(days=i)
        today_str = today_obj.strftime('%y%m%d')
        if f'RA{today_str}.TXT' in files:
            print('File found - ', today_str)
            found = today_str
            break

    if found:
        # src TXT file found, check if it was already parsed
        if f'days_{found}.json' in files:
            print('Calendar already parsed - ', found)
            with open(Path(__file__).parent / 'data' / f'days_{found}.json', 'r') as f:
                return json.load(f)
        else:
            print('Parsing calendar - ', found)
            with open(Path(__file__).parent / 'data' / f'RA{found}.TXT', 'r') as f:
                days = _get_calendar(f)
                with open(Path(__file__).parent / 'data' / f'days_{found}.json', 'w') as f:
                    json.dump(days, f)
                return days
    else: # File not found, download it
        print('File not found, downloading - ')
        today_str = _get_file()
        with open(Path(__file__).parent / 'data' / f'RA{today_str}.TXT', 'r') as f:
            days = _get_calendar(f)
            with open(Path(__file__).parent / 'data' / f'days_{today_str}.json', 'w') as f:
                json.dump(days, f)
            return days


if __name__ == '__main__':
    from rich import print
    print(get_calendar())
