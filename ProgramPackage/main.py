from pathlib import Path

from main import BOT_TOKEN
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import discord
from discord.ext import tasks
import time
import os
import sys
import requests
import asyncio  # CORREÇÃO


BOT_TOKEN = os.getenv(BOT_TOKEN)
DISCORD_CHANNEL_ID = 823376268614959105  # CORREÇÃO (int)

links_enviados = set()

def driver_config():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--disable-dev-shm-usage")  # CORREÇÃO
    chrome_options.add_argument("--no-sandbox")
    driver_path = Path(__file__).with_name("chromedriver.exe")
    service = Service(str(driver_path))
    return webdriver.Chrome(service=service, options=chrome_options)

def coletar_promotion():
    driver = driver_config()
    promocoes_novas = []

    url = "https://www.terabyteshop.com.br/promocoes"
    driver.get(url)
    sleep(5)

    try:
        produtos = driver.find_elements(By.CLASS_NAME, "product-item")
        print(f"Encontrados {len(produtos)} produtos")

        for produto in produtos:
            try:
                percent_text = produto.find_element(By.CLASS_NAME, "number").text
                percent_value = float(percent_text.replace("%", ""))

                if percent_value > 50:
                    name_product = produto.find_element(By.CLASS_NAME, "product-item__name").text
                    old_value = produto.find_element(By.CLASS_NAME, "product-item__old-price").find_element(By.TAG_NAME, "span").text
                    new_value = produto.find_element(By.CLASS_NAME, "product-item__new-price").find_element(By.TAG_NAME, "span").text
                    link = produto.find_element(By.CLASS_NAME, "product-item__name").get_attribute("href")
                    imagem_link = produto.find_element(By.CLASS_NAME, "image-thumbnail").get_attribute("src")

                    promocoes_novas.append({
                        "name_product": name_product,
                        "old_value": old_value,
                        "new_value": new_value,
                        "link": link,
                        "imagem_link": imagem_link,
                        "percent_value": percent_value
                    })
            except:
                continue

    finally:
        driver.quit()

    return promocoes_novas

def collor_embed_by_promotion(percent_value):
    if percent_value > 80:
        return discord.Color.red()
    if percent_value > 60:
        return discord.Color.orange()
    if percent_value > 20:
        return discord.Color.green()

async def enviar_promocao_embed(canal, name_product, old_value, new_value, percent_value, link, imagem_link):
    embed = discord.Embed(
        title=f"Promotion {percent_value}% OFF",
        description=name_product,
        color=collor_embed_by_promotion(percent_value),
        url=link


    )
    embed.add_field(name="De:", value=old_value, inline=True)
    embed.add_field(name="Para:", value=new_value, inline=True)
    embed.add_field(name="Desconto:", value=f"{percent_value}%", inline=True)
    embed.set_footer(text="PriceRush Promotions")

    if imagem_link:
        embed.set_image(url=imagem_link)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Ver Promoção", url=link))
    await canal.send(embed=embed, view=view)
    print(f"Notification send a discord {name_product}")


class PromotionBot(discord.Client):

    async def setup_hook(self):
        self.monitoramento_loop.start()

    @tasks.loop(minutes=10)
    async def monitoramento_loop(self):
        canal = await self.fetch_channel(DISCORD_CHANNEL_ID)
        try:
            promotions = await asyncio.to_thread(coletar_promotion)  # CORREÇÃO

            for promotion in promotions:
                await enviar_promocao_embed(canal=canal, **promotion) # CORREÇÃO
                links_enviados.add(promotion["link"])

        except Exception as e:
            print(f"Erro no monitoramento: {e}")


if __name__ == "__main__":
    intents = discord.Intents.default()
    bot = PromotionBot(intents=intents)
    bot.run(BOT_TOKEN)