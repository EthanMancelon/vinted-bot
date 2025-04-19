import discord
import asyncio
from playwright.async_api import async_playwright
import os

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')
    while True:
        await check_vinted()
        await asyncio.sleep(60)

async def check_vinted():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = "https://www.vinted.fr/catalog?search_text=jean%20levis&price_to=5.0&currency=EUR&size_ids[]=1636&status_ids[]=2&status_ids[]=1&status_ids[]=6&brand_ids[]=10&order=newest_first&page=1"
        await page.goto(url)

        items = await page.query_selector_all("div.feed-grid__item")
        if items:
            first_item = items[0]
            link = await first_item.query_selector("a")
            href = await link.get_attribute("href")
            full_url = "https://www.vinted.fr" + href

            channel = client.get_channel(CHANNEL_ID)
            await channel.send(f"Nouvel article trouvé : {full_url}")
        await browser.close()

client.run(TOKEN)
