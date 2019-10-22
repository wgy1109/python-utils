import hbase
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import StringIO
import matplotlib.pyplot as plt

zk = '192.168.1.19:2181,192.168.1.20:2181,192.168.1.21:2181'


def timespan(series):
    return series[-1] - series[0]


def lastele(series):
    return series[-1] if not series.empty else None


if __name__ == '__main__':
    with hbase.ConnectionPool(zk).connect() as conn:
        dfs = []

        # filter conditions
        devids = []
        dt_start = datetime(2019, 1, 10)
        # dt_end = dt_start + timedelta(1)
        dt_end = datetime(2019, 1, 15)

        # Get data from hbase
        table = conn['default']['iot-anlyz']
        #         # filter
        filterlist = [f"PrefixFilter(=, 'substring:{reversed(devid)}')" for devid in devids]
        filter = None
        if filterlist:
            filter = ' AND '.join(filterlist)
        # scan
        for row in table.scan(filter_=filter if filter else None):
            if not row.get('cf:devid'):
                continue
            devid = str(row.get('cf:devid'), encoding='utf8')
            # print(f'devid={devid}')

            ts = np.int64(row.get('cf:start')) / 1000
            valid_ts = dt_start.timestamp() < ts and ts < dt_end.timestamp()
            # print(f'dt_start={dt_start.timestamp()}, ts={ts/1000}, dt_end={dt_end.timestamp()}')
            if not valid_ts:
                continue

            # startts = row['cf:startts']
            if not row.get('cf:positions'):
                continue
            moves = str(row.get('cf:positions'), encoding='utf8')

            df = pd.read_csv(StringIO(moves.replace(';', '\n')),
                             header=None,
                             names=['Timestamp', 'Lon', 'Lat', 'Distance'])
            df = df.dropna(how='all')
            df = df.fillna(0.0)

            df['Devid'] = devid
            # df['Vel'] = df['Distance'] / (df['Timestamp'] - df['Timestamp'].shift(1)) * 1000 * 60
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(
                'Asia/Shanghai')
            df['Date'] = df['Timestamp'].dt.date
            df['Time'] = df['Timestamp'].dt.time
            df = df.set_index('Timestamp')
            # print(df.rolling('5min')['Distance'].agg(np.sum))
            df2 = df.resample('5T').agg({'Devid': lastele, 'Lon': lastele, 'Lat': lastele,
                                         'Date': lastele, 'Time': lastele, 'Distance': np.sum})
            df2['Vel'] = df2['Distance'] / 5
            df2 = df2.ffill()
            print(df2)
            dfs.append(df2)

        # ######
        if dfs:
            final_df = pd.concat(dfs)

            fig, ax = plt.subplots(figsize=(15, 7))
            # final_df.groupby(['Devid', 'Date']).plot(x='Time', y='Vel', ax=ax, legend=True)
            # final_df.groupby(['Devid', 'Date'])['Vel'].plot(ax=ax, legend=True)
            final_df.groupby(['Devid', 'Date']).plot.bar(x='Time', y='Vel', alpha=0.3)
            plt.show()

    # with hbase.ConnectionPool(zk).connect() as conn:
    #     table = conn['default']['iot-anlyz']
    #     table.put(hbase.Row(
    #         '00001', {
    #             'cf:name': b'fcx',
    #             'cf:home': b'HLD, Liaoning'
    #         }
    #     ))

    exit()
# 在线次数，在线时长，速度，位置，里程，