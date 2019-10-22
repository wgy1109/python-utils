import logging
import datetime


def initLogging():
    fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    today = datetime.date.today()

    filenameurl = 'D:/Code/svnPyCharm/pythonTest/logs-{0}.log'.format(str(today))
    print(filenameurl)
    logging.basicConfig(
                        level=logging.INFO,
                        format=fmt,
                        filename=filenameurl,
                        filemode='a',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    console.setFormatter(formatter);
    logging.getLogger('').addHandler(console);



initLogging()

def loggingWrite():
    logging.debug('this is a debug level message')
    logging.info("this is a info level message")
    logging.warning("this is a warning level message")
    logging.error("this is a error level message")
    logging.critical("this is a critical level message")
    logging.info("设备不在线： {}{}{}".format("1", "2", "2"))

if __name__ == '__main__':
    loggingWrite()