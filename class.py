import requests
import re
import time

# 两次爬虫之间的间隔，建议>=3，如果不怕出问题可以设2
INTV = 3

# 要选的课程，格式为 '学期;课程号;课序号;'
# 按照round-robin依次尝试，直至选上或报错
CLASS = [
'2022-2023-1;60680021;1;',
'2022-2023-1;60680021;2;',
'2022-2023-1;60680021;5;',
'2022-2023-1;60680021;6;',
]


URL = 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do'

GET_URL = 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do?m=xwkSearch&p_xnxq=2022-2023-1&tokenPriFlag=xwk'

GET_HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Cookie': 'serverid=1325456; JSESSIONID=bhfEWzILh-ho05_8DBrmy',
'Pragma': 'no-cache',
'Referer': 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

HEADERS = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': 'serverid=1325456; JSESSIONID=bhfEWzILh-ho05_8DBrmy',
'Origin': 'http://zhjwxk.cic.tsinghua.edu.cn',
'Pragma': 'no-cache',
'Referer': 'http://zhjwxk.cic.tsinghua.edu.cn/xkYjs.vxkYjsXkbBs.do',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

PAYLOAD = {
'm': 'saveXwKc',
#'token': '',
'p_xnxq': '2022-2023-1',
'tokenPriFlag': 'xwk',
'tabType': '',
'page': '',
'p_kch': '',
'p_kcm': '',
#'p_xwk_id': '2022-2023-1;60230014;202;',
}

TOKEN = ''

def log(txt):
	with open('1.txt', 'w', encoding = 'utf-8') as f:
		print(txt, file = f)


def apply(cl):
	global TOKEN
	PAYLOAD['token'] = TOKEN
	PAYLOAD['p_xwk_id'] = cl
	#print(TOKEN)
	res = requests.post(URL, headers = HEADERS, data = PAYLOAD)
	m = re.search(r'showMsg\("(.*?)"\);', res.text)
	assert m is not None, log(res.text)
	msg = m[1]
	print(msg)

	'''
	m = re.search(r'<input\s+type="hidden"\s+name="token"\s+value="([0-9a-z]+)">', res.text)
	assert m is not None, log(res.text)
	TOKEN = m[1]
	'''

	res = requests.get(GET_URL, headers = GET_HEADERS)
	m = re.search(r'<input\s+type="hidden"\s+name="token"\s+value="([0-9a-z]+)">', res.text)
	assert m is not None, log(res.text)
	TOKEN = m[1]
	if msg == '提交选课成功;':
		return True
	elif msg.find('课余量已无,不能再选,不能提交 !') != -1:
		return False
	else:
		raise ValueError(msg)

def main():
	global TOKEN
	cl_id = 0
	t = time.time() + INTV
	res = requests.get(GET_URL, headers = GET_HEADERS)
	m = re.search(r'<input\s+type="hidden"\s+name="token"\s+value="([0-9a-z]+)">', res.text)
	assert m is not None, log(res.text)
	TOKEN = m[1]
	while not apply(CLASS[cl_id]):
		cl_id = 0 if cl_id >= len(CLASS)-1 else cl_id + 1
		t -= time.time()
		if t > 0:
			time.sleep(t)
		t = time.time() + INTV

if __name__ == '__main__':
	main()