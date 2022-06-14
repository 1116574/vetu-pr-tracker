""" Get day type - normal day, holiday, etc. Based on Warsaw Transport Authority timetable data, of all things """

import ftplib
import datetime


def get_file():
    """ Download timetable data from Warsaw Transport Authority """
    today = datetime.datetime.now()
    today = today.strftime('%y%m%d')

    ftp = ftplib.FTP('rozklady.ztm.waw.pl')
    ftp.login()

    with open('timetable.7z', 'wb') as fp:
        ftp.retrbinary(f'RETR RA{today}.7z', fp.write)

    ftp.quit()

    try:
        import py7zr
        with py7zr.SevenZipFile("timetable.7z", 'r') as archive:
            archive.extractall()
    except ImportError:
        print('py7zr not installed; Cannot unpack data')
        print('pip install py7zr')
        raise Exception('py7zr not installed')

def get_day_type(f):
    """ Weekday, Weekend, or Holiday. If 2 types are possible, returns in this order: weekend > holiday > weekday """
    mode = 'TY'  # or KA
    days = {
        'timestamp': 'weekday|weekend|holiday',
    }

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
                return 'working'
            elif 'DS' in candidates:
                return 'free'