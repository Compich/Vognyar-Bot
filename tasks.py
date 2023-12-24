import asyncio

import aiohttp
from database import models as dbm
from aiogram import Bot
import logging
from bs4 import BeautifulSoup
import re
import utils

async def check_sauces(bot: Bot):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url='https://vognyar.com/ru/ekstragostra-serija/'
        )
        if response.status != 200:
            logging.error(f'[Check Task] Failed to get sauces list: {response.status}')
            return

        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find_all('div', class_='product__card')

        sauces = {}

        for product in products:
            name = product.find(
                'div',
                class_='product__card-title'
            ).text
            scoville_heat_units_str = product.find(
                'div',
                class_='product__card-shu'
            ).text
            res = re.search(
                '(?P<scoville_heat_units>[\d\s]+)',
                scoville_heat_units_str
            )
            if res is None:
                continue

            scoville_heat_units = int(res.group(1).replace(' ', ''))

            in_stock = product.find('div', class_='text_no_product') is None

            price_str = product.find('div', class_='price__curent').text.strip()

            res = re.search(
                '(?P<price>[\d\s]+)',
                price_str
            )

            if res is None:
                logging.error(f'[Check Task] Failed to parse price for {name}: {price_str}')
                continue

            price = int(res.group(1).replace(' ', ''))

            anchor = product.find('a')

            img = product.find('img')

            new_sauce = {
                'scoville_heat_units': scoville_heat_units,
                'in_stock': in_stock,
                'price': price,
                'link': anchor['href'],
                'img_url': img['src']
            }

            if (
                name in sauces and not sauces[name]['in_stock'] and in_stock
            ):
                sauces[name] = new_sauce
            elif name not in sauces:
                sauces[name] = new_sauce

        for name, sauce_info in sauces.items():
            sauce = dbm.Sauce.get(dbm.Sauce.name == name)
            if sauce is None:
                sauce = dbm.Sauce.add_new(
                    name=name,
                    **sauce_info
                )
                await utils.send_new_sauce(bot=bot, sauce=sauce)
            elif sauce.in_stock != sauce_info['in_stock']:
                sauce = sauce.update(
                    **sauce_info
                )
                await utils.send_stock_status_change(bot=bot, sauce=sauce)
