import discord
from discord.ext import commands
import requests

def get_litecoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=krw'
    response = requests.get(url)
    data = response.json()
    return data['litecoin']['krw']

def calculate_krw_amount(litecoin_amount):
    litecoin_price = get_litecoin_price()
    return litecoin_amount * litecoin_price

def calculate_litecoin_amount(krw_amount):
    litecoin_price = get_litecoin_price()
    return krw_amount / litecoin_price

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

class KRWToLTCModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="KRW to LTC")
        self.krw_amount = discord.ui.TextInput(label="KRW Amount", style=discord.TextStyle.short)
        self.add_item(self.krw_amount)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            krw_amount = float(self.krw_amount.value)
        except ValueError:
            await interaction.response.send_message("Please input only numbers.", ephemeral=True)
            return

        litecoin_amount = calculate_litecoin_amount(krw_amount)
        await interaction.response.send_message(f"{krw_amount} KRW is {litecoin_amount:.6f} LTC", ephemeral=True)

class LTCToKRWModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="LTC to KRW")
        self.litecoin_amount = discord.ui.TextInput(label="LTC Amount", style=discord.TextStyle.short)
        self.add_item(self.litecoin_amount)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            litecoin_amount = float(self.litecoin_amount.value)
        except ValueError:
            await interaction.response.send_message("Please input only numbers.", ephemeral=True)
            return

        krw_amount = calculate_krw_amount(litecoin_amount)
        await interaction.response.send_message(f"{litecoin_amount} LTC is {krw_amount:.2f} KRW", ephemeral=True)

class CalcView(discord.ui.View):
    @discord.ui.button(label="KRW to LTC", style=discord.ButtonStyle.primary)
    async def krw_to_ltc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(KRWToLTCModal())

    @discord.ui.button(label="LTC to KRW", style=discord.ButtonStyle.primary)
    async def ltc_to_krw_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LTCToKRWModal())

@bot.command(name='calc')
async def calc(ctx):
    view = CalcView()
    await ctx.send("Choose an option:", view=view)

bot.run()
