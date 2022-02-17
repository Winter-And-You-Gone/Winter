from flask import Flask, request, render_template
import requests
import base64
n = 0


app = Flask(__name__)


@app.route('/sb/', methods=['GET', 'POST'])
def sb():
    UA = request.user_agent
    global n
    print(n)
    n = n + 1
    print(str(UA))
    if request.method == 'GET':
        if ('Windows' or 'Macintosh') in str(UA):
            return render_template('sbapiwin.html')
        # if ('Android' or 'HarmonyOS' or 'iPhone' or 'iPod' or 'iPad' or 'SymbianOS') in str(UA)
        else:
            return render_template('sbapi.html')
    if request.method == 'POST':
        f = request.files.get('img_file')
        basedir = './static/images'
        f_name = f.filename
        f_path = basedir + '/' + f_name
        print(f_path, f_name)
        f.save(f_path)
        '''
        通用物体和场景识别
        '''

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
        # 二进制方式打开图片文件
        f = open('./static/images/' + f_name, 'rb')
        img = base64.b64encode(f.read())

        params = {"image": img, 'baike_num': 1}
        access_token = '24.f67d9dfa558ec3f8d9e74ec032c1756d.2592000.1647412979.282335-25607057'
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        res = response.json()
        print(res)
        # resp = json.loads(response.text)
        # res = json.dumps(resp, ensure_ascii=False)
        # re = json.loads(res)
        q = 0
        baike_url = 'https://baike.baidu.com'
        if 'baike_url' in res['result'][0]['baike_info']:
            baike_url = res['result'][0]['baike_info']['baike_url']
        baike = res['result'][0]['keyword']
        abc = {'num': '序号', 'keyword': '图片可能含有', 'root': '分类'}
        res['result'].insert(0, abc)
        for i in res['result']:
            if q == 0:
                q = q + 1
                continue
            i['num'] = q
            q = q + 1
        return render_template('baiduapi.html', list=res['result'], f_name=f_name, baike_url=baike_url, baike=baike)
        # return render_template('sbapi.html', f_name=f_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
