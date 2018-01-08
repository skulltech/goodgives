import requests
from lxml import html



def enter_giveaway(identifier):
	page = session.get('https://www.goodreads.com/giveaway/enter_choose_address/{}'.format(identifier))
	tree = html.fromstring(page.content)
	address = int(tree.xpath('//a[@class="gr-button gr-button--small"]/@id')[0][13:])
	

	page = session.get('https://www.goodreads.com/giveaway/enter_print_giveaway/{}'.format(identifier), params={'address': address})
	tree = html.fromstring(page.content)
	authenticity_token = tree.xpath('//input[@name="authenticity_token"]/@value')[0]

	payload = {
		'authenticity_token': authenticity_token,
		'entry_terms': 1,
		'commit': 'Enter Giveaway'
	}
	response = session.post('https://www.goodreads.com/giveaway/enter_print_giveaway/{}'.format(identifier),
							params={'address': address}, data=payload)
	print(response.url)

	with open('dump.html', 'wb') as f:
		f.write(response.content)


session = requests.Session()

page = session.get('https://www.goodreads.com/')
tree = html.fromstring(page.content)
signInForm = tree.xpath('//div[@id="signInForm"]')[0]
authenticity_token = signInForm.xpath('.//input[@name="authenticity_token"]/@value')[0]
n = signInForm.xpath('.//input[@name="n"]/@value')[0]

print('authenticity_token: {0}\nn: {1}'.format(authenticity_token, n))

USERNAME = 'sumit.ghosh32@gmail.com'
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

with open('file.html', 'wb') as f:
	f.write(page.content)

tree = html.fromstring(page.content)
lis = tree.xpath('//li[@class="listElement giveawayListItem"]')


giveaways = []
print(len(lis))
for li in lis:
	ID = int(li.xpath('.//a[@class="actionLink detailsLink"]/@href')[0].rsplit('/', 1)[-1].split('-')[0])
	entered = not bool(li.xpath('.//a[@class="gr-button"]/@href'))
	giveaway = {
		'Name': li.xpath('.//a[@class="bookTitle"]/text()')[0],
		'URL': li.xpath('.//a[@class="bookTitle"]/@href')[0],
		'Entered': entered,
		'ID': ID
	}
	giveaways.append(giveaway)

for giveaway in giveaways:
	if not giveaway['Entered']:
		enter_giveaway(giveaway['ID'])
		print('Entered giveaway: {0}, {1}'.format(giveaway['Name'], giveaway['ID']))
		break

