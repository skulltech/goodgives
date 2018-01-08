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


page = session.get('https://www.goodreads.com/giveaway')
tree = html.fromstring(page.content)
lis = tree.xpath('//li[@class="giveawayListItem"]')


giveaways = []
for li in lis:
	giveaway = {
		'Name': li.xpath('//a[@class="bookTitle"]/text()'),
		'URL': li.xpath('//a[@class="bookTitle"]/@href'),
		'GiveawayURL': li.xpath('//a[@class="gr-button"]/@href')
	}


def enter_giveaway(session, id=261589, address=3334069, ):
	response = session.post('https://www.goodreads.com/giveaway/enter_print_giveaway/{}'.format(id), params={'address': address})