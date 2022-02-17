import random
from multiprocessing import Pool
from flask import Flask, request, render_template
import requests
import json
import time
import math


def BvToAv(Bv):
    # 1.去除Bv号前的"Bv"字符
    print(Bv)
    BvNo1 = Bv[2:]
    keys = {
        '1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
        'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38', 'K': '51',
        'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50', 'U': '10', 'V': '44',
        'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
        'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41',
        'k': '16', 'm': '11', 'n': '37', 'o': '2',
        'p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14',
        'z': '19'
        }
    # 2. 将key对应的value存入一个列表
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))

    # 3. 对列表中不同位置的数进行*58的x次方的操作

    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6));
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2));
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4));
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8));
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5));
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9));
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3));
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7));
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1));
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0));

    # 4.求出这10个数的合
    sum = 0
    for i in BvNo2:
        sum += i
    # 5. 将和减去100618342136696320
    sum -= 100618342136696320
    # 6. 将sum 与177451812进行异或
    temp = 177451812

    return sum ^ temp


def blbl():
    av = BvToAv(str(bv))
    list1 = []
    dict2 = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Referer': 'https://www.bilibili.com/video/BV1ES4y197vN?spm_id_from=333.851.b_7265636f6d6d656e64.2'
    }
    p = 1
    while True:
        page = requests.get(f'https://api.bilibili.com/x/v2/reply?pn={p}&type=1&oid={av}&sort=2', headers=headers)
        a = 0
        time.sleep(random.random() * 3)
        while True:
            if page.text[a] == '{':
                break
            else:
                a = a + 1
        results = json.loads(page.text[a:len(page.text)])
        replies = results.get('data')['replies']
        if replies == []:
            break
        p = p + 1
        for i in replies:
            dict1 = {}
            name = i['member']['uname']
            comment = i['content']['message']
            dict1['name'] = name
            dict1['comment'] = comment.replace('\n', '')
            list1.append(dict1)
        dict2['data'] = list1
    return dict2


def bl(url):
    list1 = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Referer': 'https://www.bilibili.com/video/BV1ES4y197vN?spm_id_from=333.851.b_7265636f6d6d656e64.2'
    }
    time.sleep(random.random() * 3)
    page = requests.get(url, headers=headers)
    a = 0
    while True:
        if page.text[a] == '{':
            break
        else:
            a = a + 1
    results = json.loads(page.text[a:len(page.text)])
    replies = results.get('data')['replies']
    for i in replies:
        dict1 = {}
        name = i['member']['uname']
        comment = i['content']['message']
        dict1['name'] = name
        dict1['comment'] = comment.replace('\n', '')
        list1.append(dict1)
    return list1


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('blbl.html')
    if request.method == 'POST':
        f = request.files.get('img_file')
        basedir = 'E:/Python项目/a试用/api/static/images'
        f_name = f.filename
        f_path = basedir + f_name
        f.save(f_path)
        return render_template('blbl.html', f_name=f_name)


@app.route('/names/')
def names():
    global bv
    bv = request.args.get('bv')
    name = []
    na = {}
    dict3 = blbl()
    for i in dict3['data']:
        name.append(i['name'])
    na['data'] = json.dumps(name, ensure_ascii=False)
    return '{}'.format(na)


@app.route('/comments/')
def comments():
    global bv
    bv = request.args.get('bv')
    comment = []
    com = {}
    dict3 = blbl()
    for i in dict3['data']:
        comment.append(i['comment'])
    com['data'] = json.dumps(comment, ensure_ascii=False)
    return '{}'.format(com)


@app.route('/name_comments/', methods=['GET', 'POST'])
def avnum():
    if request.method == 'GET':
        return render_template('mulwin.html')
    if request.method == 'POST':
        global bv
        bv = request.form.get('bv')
        time1 = time.time()
        ab = blbl()
        time2 = time.time()
        print(f'单线程爬取用时{time2-time1}秒')
        num = 1
        for i in ab['data']:
            i['num'] = num
            num = num + 1
        abc = {'num': '序号', 'name': '用户名', 'comment': '评论内容'}
        ab['data'].insert(0, abc)
        return render_template('mulwin.html', list=ab['data'])


@app.route('/mul/', methods=['GET', 'POST'])
def mul():
    print(request.method)
    if request.method == 'GET':
        UA = request.user_agent
        print(str(UA))
        if ('Windows' or 'Macintosh') in str(UA):
            return render_template('mulwin.html')
        # if ('Android' or 'HarmonyOS' or 'iPhone' or 'iPod' or 'iPad' or 'SymbianOS') in str(UA)
        else:
            return render_template('muland.html')
    if request.method == 'POST':
        global bv
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'Referer': 'https://www.bilibili.com/video/BV1ES4y197vN?spm_id_from=333.851.b_7265636f6d6d656e64.2'
        }
        p = 1
        url_list = []
        bv = request.form.get('bv')
        bv = bv.replace('\n', '').replace(' ', '')
        if len(str(bv)) != 12:
            return '''
            <html>
            <head lang="en">
                <meta charset="UTF-8">
                <title>错误页面</title>
            </head>
            <body style="text-align: center;">
                <h1>输入的BV号格式不正确<h1>
                <a href="http://t4y6207815.qicp.vip/mul/">点击此处回到主页</a>
            </body>
            </html>'''
        av = BvToAv(str(bv))
        response = requests.get(f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next=0&type=1&oid={av}&mode=3&plat=1', headers=headers)
        re = json.loads(response.text)
        try:
            page_number = int(re['data']['cursor']['all_count']) // 15 + 1
        except TypeError:
            return '''
            <html>
            <head lang="en">
                <meta charset="UTF-8">
                <title>错误页面</title>
            </head>
            <body style="text-align: center;">
                <h1>请求被B站拦截，请五分钟后再试<h1>
                <a href="http://t4y6207815.qicp.vip/mul/">点击此处回到主页</a>
            </body>
            </html>'''
        print(page_number)
        while p <= page_number:
            url = f'https://api.bilibili.com/x/v2/reply?pn={p}&type=1&oid={av}&sort=2'
            url_list.append(url)
            p = p + 1
        pool = Pool(8)
        ab = {}
        name_comments = []
        time1 = time.time()
        res = pool.map(bl, url_list)
        for i in res:
            for j in i:
                name_comments.append(j)
        time2 = time.time()
        print(f'多线程爬取用时{time2-time1}秒')
        ab['data'] = name_comments
        num = 1
        for i in ab['data']:
            i['num'] = num
            num = num + 1
        abc = {'num': '序号', 'name': '用户名', 'comment': '评论内容'}
        ab['data'].insert(0, abc)
        return render_template('response.html', list=ab['data'])


@app.route('/image/', methods=['POST'])
def image():
    basedir = 'C:/Users/29865/Desktop/POST图片/'
    f = request.files.get('img')
    fname = f.filename
    fpath = basedir + fname
    f.save(fpath)
    return f'''
                <html>
                <body>
                <center>
                <h1>您上传的图像为</h1>
                <img src="{fpath}"/>
                </center>
                </body>
                </html>
           '''


@app.route('/chengxin/', methods=['GET'])
def cx():
    if request.method == 'GET':
        UA = request.user_agent
        print(str(UA))
        if ('Windows' or 'Macintosh') in str(UA):
            return render_template('cxwin.html')
        if ('Android' or 'HarmonyOS' or 'iPhone' or 'iPod' or 'iPad' or 'SymbianOS') in str(UA):
            return render_template('cxand.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('E:/haoea.xyz_nginx/haoea.xyz_nginx/haoea.xyz_bundle.crt','E:/haoea.xyz_nginx/haoea.xyz_nginx/haoea.xyz.key'))

