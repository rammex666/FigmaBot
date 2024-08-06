import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType, Permissions
from nextcord.ui import View, Select, Button
from config.category import get_ticket
from main import bot


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="ticket", description="Create a ticket panel",
                            default_member_permissions=Permissions(administrator=True))
    async def ticket(self, interaction: Interaction):
        embed = nextcord.Embed(
            title="Ouvrir un ticket",
            description="Pour contacter notre équipe, merci de choisir la raison de la création de votre ticket grâce au sélécteur ci dessous !",
            color=nextcord.Color.yellow()
        )
        view = TicketSelectView()
        await interaction.response.send_message(embed=embed, view=view)


class TicketButtonView(View):
    def __init__(self, channel):
        super().__init__(timeout=None)
        self.channel = channel
        self.add_item(ClaimButton())
        self.add_item(DeleteButton())


class ClaimButton(Button):
    def __init__(self):
        super().__init__(label="Claim", style=nextcord.ButtonStyle.green)

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} a claim le ticket.")


class DeleteButton(Button):
    def __init__(self):
        super().__init__(label="Delete", style=nextcord.ButtonStyle.red)

    async def callback(self, interaction: Interaction):
        await self.channel.delete()


class TicketSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


class TicketSelect(Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Rejoindre l'équipe", value="support", emoji=""),
            nextcord.SelectOption(label="Signaler membre / problème", emoji="", value="report"),
            nextcord.SelectOption(label="Mise en avant", emoji="", value="front"),
            nextcord.SelectOption(label="Autre", emoji="", value="other")
        ]
        super().__init__(placeholder="Choisir la raison", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        guild = interaction.guild
        category = nextcord.utils.get(guild.categories, id=get_ticket())
        if not category:
            category = await guild.create_category("Tickets")
            print("aucune catégorie trouvé création d'une catégorie ticket")

        channel = await category.create_text_channel(f"ticket-{interaction.user.name}", type=ChannelType.text)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        embed = nextcord.Embed(
            title="Bievenue dans votre ticket",
            description=f"décrivez vôtre demande {interaction.user.mention}\n{self.values[0]}",
            color=nextcord.Color.green()
        )
        view = TicketButtonView(channel)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Ticket crée: {channel.mention}", ephemeral=True)

    @commands.command(name="add")
    @commands.has_permissions(administrator=True)
    async def add_member(self, ctx, member: nextcord.Member):
        if ctx.channel.category and ctx.channel.category.id == get_ticket():
            await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
            await ctx.send(f"{member.mention} a été ajouté au ticket.")

    @commands.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def remove_member(self, ctx, member: nextcord.Member):
        if ctx.channel.category and ctx.channel.category.id == get_ticket():
            await ctx.channel.set_permissions(member, read_messages=False, send_messages=False)
            await ctx.send(f"{member.mention} a été enlevé du ticket.")


def setup(bot):
    bot.add_cog(TicketSystem(bot))
