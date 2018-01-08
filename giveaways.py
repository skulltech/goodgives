import requests
from getpass import getpass
from lxml import html



def login(session, username, password):
	page = session.get('https://www.goodreads.com/')
	tree = html.fromstring(page.content)
	form = tree.xpath('//div[@id="signInForm"]')[0]
	authenticity_token = form.xpath('.//input[@name="authenticity_token"]/@value')[0]
	n = form.xpath('.//input[@name="n"]/@value')[0]

	payload = {
		'user[email]': username,
		'user[password]': password,
		'remember_me': 'on',
		'authenticity_token': authenticity_token,
		'n': n
	}
	response = session.post('https://www.goodreads.com/user/sign_in?source=home', data=payload)
	print('[*] Successfully logged in to Goodreads!')


def scrape_giveaways(session):
	giveaways = []
	count = 1

	while True:
		page = session.get('https://www.goodreads.com/giveaway', params={'page': count})
		tree = html.fromstring(page.content)
		lis = tree.xpath('//li[@class="listElement giveawayListItem"]')

		if not lis: break

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
		
		count = count + 1

	print('[*] {} giveaways scraped.'.format(len(giveaways)))
	return giveaways


def enter_giveaway(session, identifier):
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


def main():	
	session = requests.Session()
	username = input('[?] Enter your Goodreads username: ')
	password = getpass('[?] Enter your Goodreads password: ')
	login(session, username, password)
	giveaways = scrape_giveaways(session)
	print()

	for giveaway in giveaways:
		if not giveaway['Entered']:
			enter_giveaway(session, giveaway['ID'])
			print('[*] Entered giveaway for: {0} - {1}'.format(giveaway['Name'], giveaway['ID']))



if __name__=='__main__':
	main()
