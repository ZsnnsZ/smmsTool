import imghdr
import requests
import sys

uploadUrl = "https://sm.ms/api/upload"
historyUrl = "https://sm.ms/api/list"
clearUrl = "https://sm.ms/api/clear"

allowSuffix = ['jpeg', 'png', 'gif']
results = []

def upload(args):
    files = []
    for arg in args:
        file = open(arg, 'rb')
        fileName = arg.split('/')[-1]
        imgType = imghdr.what(file)
        if imgType in allowSuffix:
            files.append({'smfile': (fileName, file, 'image/jpeg')})
    data = {
        'ssl': True
    }
    # edit the file path as you want
    with open('/Users/macbookair/Desktop/smmsTool/photoUrls.txt', 'at+') as f:
        for file in files:
            response = requests.post(uploadUrl, data=data, files=file)
            json = response.json()
            if json['code'] == 'success':
                # result = '''![%s](%s)''' % (json['data']['filename'], json['data']['url'])
                # f.write(result)
                result = '%s' % (json['data']['url']) + '\n'
                results.append(result)
                f.write(result)
            else:
                results.append(response.json())
    print(results)

def history():
    data = {
        'ssl': True
    }
    response = requests.get(historyUrl, data=data)
    urls = response.json()['data']
    for i in range(len(urls)):
        results.append(urls[i]['url'])
    print(results)

def clear():
    data = {
        'ssl': True
    }
    response = requests.get(clearUrl, data=data)
    json = response.json()
    print(json)

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        print("Usage: getUrls.py imagePath or options(history/clear)")
    elif args[1] == 'history':
        history()
    elif args[1] == 'clear':
        clear()
    else:
        upload(args)

