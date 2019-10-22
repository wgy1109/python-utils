import requests

_BASE_URL = 'http://localhost:5555/api_cloud/api'

def getSiteList():
    url = _BASE_URL + '/ebc/hw/siteListByNameV2'
    data = {
        'siteName': "",
        'siteType': "3"
    }

    result = requests.post(url=url, json=data).text
    print("getSiteList : "+result)
    return result


if __name__ == '__main__':
    getSiteList()
