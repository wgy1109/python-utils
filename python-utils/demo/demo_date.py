import datetime

if __name__ == '__main__':
    devid = '0012345678910'
    today = datetime.date.today()
    dt_start = datetime.datetime(today.year, today.month, today.day)
    dt_day = datetime.date.today()
    print(dt_start, dt_day)
    print("反序字符串：",devid[::-1])
    # datetime.strftime(str(dt_day), '%Y%m%d' )
    start_row = '{}P0000001{}'.format(devid[::-1], int(dt_start.timestamp()) * 1000)
    print(start_row)