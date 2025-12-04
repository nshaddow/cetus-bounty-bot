import discord
from discord.ext import commands, tasks
import json
import requests
import os
from rotation import generate_rotation
from lua_seed_adapter import seed_from_worldstate
from datetime import datetime, timezone

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

INTENTS = discord.Intents.default()

class Cetus(commands.Cog):
    def init(self, bot):
        self.bot = bot
        self.check_cycle.start()

        with open("data/cetus_bounties.json") as f:
            self.bounties = json.load(f)

        self.last_announced = None

    # --------------------------
    # Worldstate fetch
    # --------------------------

    def fetch_worldstate(self):
        try:
            data = requests.get(
                "https://api.warframestat.us/pc",
                timeout=5
            ).json()
            return data
        except:
            return {}

    # --------------------------
    # Embed Builder
    # --------------------------

    def build_rotation_embed(self, rotation, phase, seed):
        color = 0xffc542 if phase == "DAY" else 0x3e8ed0
        embed = discord.Embed(
            title=f"Cetus {phase} Cycle",
            color=color,
            description=f"Seed: {seed}"
        )
        for tier, stages in rotation.items():
            embed.add_field(
                name=f"Tier {tier}",
                value="\n".join(f"• {s}" for s in stages),
                inline=False
            )
        embed.set_footer(text="Warframe Cetus Bounty Rotation")
        return embed
    #--------------------------,
    #Slash Commands,
    #--------------------------,
    @discord.app_commands.command(
        name="cetus",
        description="Show current bounty rotation"
    )
    async def cetus(self, interaction: discord.Interaction):
        ws = self.fetch_worldstate()
        is_day = ws.get("cetusCycle", {}).get("isDay", True)
        seed = seed_from_worldstate(ws)

        rotation = generate_rotation(self.bounties, seed)
        embed = self.build_rotation_embed(
            rotation,
            "DAY" if is_day else "NIGHT",
            seed
        )

        await interaction.response.send_message(embed=embed)

    # --------------------------
    # Forced announce
    # --------------------------

    @discord.app_commands.command(
        name="cetus_force_announce",
        description="Force a bounty announcement"
    )
    async def force_announce(self, interaction):
        ws = self.fetch_worldstate()
        is_day = ws.get("cetusCycle", {}).get("isDay", True)
        seed = seed_from_worldstate(ws)
        rotation = generate_rotation(self.bounties, seed)
        embed = self.build_rotation_embed(
            rotation,
            "DAY" if is_day else "NIGHT",
            seed
        )
        await interaction.response.send_message("Announcement sent!", ephemeral=True)
        channel = interaction.channel
        await channel.send(embed=embed)

    #--------------------------
    #Auto announcer every minute,
    #--------------------------
    @tasks.loop(minutes=1)
    async def check_cycle(self):
        ws = self.fetch_worldstate()
        is_day = ws.get("cetusCycle", {}).get("isDay", True)

        key = f"{is_day}-{datetime.now().hour}"

        if key == self.last_announced:
            return

        self.last_announced = key

        # Announce in first guild channel found
        if self.bot.guilds:
            guild = self.bot.guilds[0]
            channel = guild.text_channels[0]

            seed = seed_from_worldstate(ws)
            rotation = generate_rotation(self.bounties, seed)
            embed = self.build_rotation_embed(
                rotation,
                "DAY" if is_day else "NIGHT",
                seed
            )
            await channel.send(embed=embed)

    @check_cycle.before_loop
    async def before(self):
        await self.bot.wait_until_ready()

#--------------------------
#Bot init,
#--------------------------
bot = commands.Bot(command_prefix="!", intents=INTENTS)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        guild = discord.Object(id=int(GUILD_ID)) if GUILD_ID else None
        if guild:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
        else:
            await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print("SYNC ERROR:", e)

bot.add_cog(Cetus(bot))
bot.run(TOKEN)