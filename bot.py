
import os, discord
from discord.ext import commands
from discord import app_commands
from fetcher import get_cetus_bounties
import dashboard

TOKEN=os.getenv("DISCORD_TOKEN")

intents=discord.Intents.default()
bot=commands.Bot(command_prefix="!", intents=intents)

class Cetus(commands.Cog):
    def __init__(self,bot): self.bot=bot

    @app_commands.command(name="cetus", description="Show Cetus bounties (live)")
    async def cetus(self, interaction: discord.Interaction):
        bounties=get_cetus_bounties()
        if not bounties:
            await interaction.response.send_message("Failed to fetch Cetus bounties.")
            return
        embed=discord.Embed(title="Cetus Bounties", color=discord.Color.orange())
        for job in bounties:
            embed.add_field(
                name=f"{job['type']} (Lv {job['levels']})",
                value="**Stages:** "+", ".join(job['stages'])+
                      "\n**Rewards:**\n" + "\n".join(f"- {r}" for r in job['rewards']),
                inline=False
            )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Cetus(bot))

@bot.event
async def on_ready():
    await bot.load_extension("bot")
    await bot.tree.sync()
    print("Bot online.")

dashboard.start()  # start web dashboard
bot.run(TOKEN)
