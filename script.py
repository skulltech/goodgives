import requests
from lxml import html



session = requests.Session()

page = session.get('https://www.goodreads.com/')
tree = html.fromstring(page.content)
signInForm = tree.xpath('//div[@id="signInForm"]')[0]
authenticity_token = signInForm.xpath('//input[@name="authenticity_token"]/@value')[0]
n = signInForm.xpath('///input[@name="n"]/@value')[0]

print('authenticity_token: {0}\nn: {1}'.format(authenticity_token, n))

USERNAME = 'sample@gmail.com'
PASSWORD = 'pw'

payload = {
	'user[email]': USERNAME,
	'user[password]': PASSWORD,
	'remember_me': 'on',
	'authenticity_token': authenticity_token,
	'n': n
}
response = session.post('https://www.goodreads.com/user/sign_in?source=home', data=payload)
with open('file.html', 'wb') as f:
	f.write(response.content)

cookies = {
	'_session_id2': '443ba8de2c43d28203a7dd6cf5105fe1',
	'csid': 'BAhJIhgwODMtNzQ3NDg1Ny01MDk1OTQ1BjoGRVQ',
	'locale': 'en'
}	 