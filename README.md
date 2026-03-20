# pricerush-bot
Developed a promotional bot project in Python using Selenium, aimed at enhancing my knowledge of Java and related libraries.

PriceRush Bot

A Discord bot that scans for good deals and posts them automatically so you don’t have to keep checking websites all the time.

The idea is simple. It goes into a promotions page, looks for products with high discounts (50% or more), and sends them to a Discord channel with price, link and image.

What it does

Monitors promotions automatically

Filters only high discounts

Sends embed messages to Discord

Avoids sending the same link twice

Includes a button to go directly to the product

Tech stack

Python

Selenium

discord.py

asyncio

How it works

It opens the promotions page, collects the products, filters the ones with more than 50 percent discount, formats the data and sends it to Discord. This runs every 10 minutes.

How to run

Clone the repository

git clone https://github.com/caioNox/pricerush-bot.git

cd pricerush-bot

Install dependencies

pip install -r requirements.txt

Download ChromeDriver compatible with your Chrome version and place it in the project folder.

Notes

If you leak your Discord token, regenerate it immediately.

If the website changes its structure, the bot will likely break.

Future ideas

Support more stores, better filtering, custom alerts, maybe a web dashboard, maybe deploy it somewhere instead of running locally.

About

Built to stop manually hunting for deals like a maniac. If you want to improve it, go ahead.
