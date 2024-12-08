import nextcord, datetime, config
from nextcord.ext import commands


intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    bot.add_view(ticketview())
    bot.add_view(ticketcloseview())
    print(f"Logged in as {bot.user}")



class ticketcloseview(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @nextcord.ui.button(label="ปิดห้อง", style=nextcord.ButtonStyle.red, custom_id="close", emoji="🔒")
    async def close(self, button: nextcord.Button, interaction: nextcord.Interaction):
        guild = interaction.guild
        user = interaction.user
        channel = interaction.channel


        if "closed" in channel.name: 
            await interaction.response.send_message(content="ห้องนี้ปิดไปแล้ว!", ephemeral=True)
            return

        overwrites = {guild.default_role: nextcord.PermissionOverwrite(read_messages=False)}  


        for member in guild.members:
            overwrites[member] = nextcord.PermissionOverwrite(read_messages=False)
        
        await channel.edit(overwrites=overwrites)


        await channel.edit(name=f"{channel.name}-closed")

        log_channel_id = config.logch
        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            log_embed = nextcord.Embed(
                    title="🔔 แจ้งเตือนการทำกิจกรรม",
                    color=nextcord.Color.green()
                )
            log_embed.add_field(name="🎁 ผู้ใช้งาน", value=user.mention, inline=False)
            log_embed.add_field(name="🔒 รูปเเบบห้อง", value="ปิดห้อง", inline=False)
            log_embed.set_thumbnail(url=interaction.user.avatar.url)
            log_embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await log_channel.send(embed=log_embed)
        await interaction.response.send_message(content="ปิดห้องสำเร็จ", ephemeral=True)








class ticketview(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  

    @nextcord.ui.button(label="สอบถาม", style=nextcord.ButtonStyle.success, custom_id="qa", emoji="❓")
    async def qa(self, button:nextcord.Button, interaction:nextcord.Interaction):
        guild = interaction.guild  
        user = interaction.user
        channel_name = f"ticket-{user.name}".lower()
        category_id = config.categoryid 
        category = guild.get_channel(category_id)

        existing_channel = nextcord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"ห้อง `{channel_name}` มีอยู่แล้ว!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),  
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True) 
        }
        new_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category)
        embed = nextcord.Embed(
            title="𝐓𝐈𝐂𝐊𝐄𝐓 𝐒𝐘𝐒𝐓𝐄𝐌",
            description="```สามารถสอบภามข้อมูลที่ท่อนต้องการได้เลยครับ```",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1315041008047882263/1315041064771387492/DALLE_2024-12-05_23.56.52_-_A_professional_logo_for_NovaCraft_Dev_Studio_featuring_a_sleek_and_modern_design_with_a_blue_sky_theme._The_central_element_is_a_stylized_computer_in.webp?ex=6755f6ee&is=6754a56e&hm=54d4619e1551f3f287af0b4e41c03814f8c0b187525bc0136663c576fa55cef5&")  # ใช้ไอคอนเริ่มต้นหากไม่มีไอคอนเซิร์ฟเวอร์
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        await new_channel.send(embed=embed, view=(ticketcloseview()))
        log_channel_id = config.logch
        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            log_embed = nextcord.Embed(
                    title="🔔 แจ้งเตือนการทำกิจกรรม",
                    color=nextcord.Color.green()
                )
            log_embed.add_field(name="🎁 ผู้ใช้งาน", value=user.mention, inline=False)
            log_embed.add_field(name="🔒 รูปเเบบห้อง", value="สอบถาม", inline=False)
            log_embed.set_thumbnail(url=interaction.user.avatar.url)
            log_embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await log_channel.send(embed=log_embed)
        await interaction.response.send_message(content=f"สร้างห้อง {new_channel.name} เรียบร้อยแล้ว!", ephemeral=True)


    @nextcord.ui.button(label="สั่งทำบอท", style=nextcord.ButtonStyle.success, custom_id="buy", emoji="🛠️")
    async def buy(self, button:nextcord.Button, interaction:nextcord.Interaction):
        guild = interaction.guild  
        user = interaction.user
        channel_name = f"ticket-{user.name}".lower()
        category_id = config.categoryid 
        category = guild.get_channel(category_id)

        existing_channel = nextcord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"ห้อง `{channel_name}` มีอยู่แล้ว!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),  
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)  
        }
        new_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category)
        embed = nextcord.Embed(
            title="𝐓𝐈𝐂𝐊𝐄𝐓 𝐒𝐘𝐒𝐓𝐄𝐌",
            description="```กรุณาส่งรายละเอียดบอทที่ท่านต้องการทำหรือบอกชื่อรายการสินค้าที่ท่านต้องการซื้อ```",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1315041008047882263/1315041064771387492/DALLE_2024-12-05_23.56.52_-_A_professional_logo_for_NovaCraft_Dev_Studio_featuring_a_sleek_and_modern_design_with_a_blue_sky_theme._The_central_element_is_a_stylized_computer_in.webp?ex=6755f6ee&is=6754a56e&hm=54d4619e1551f3f287af0b4e41c03814f8c0b187525bc0136663c576fa55cef5&")  # ใช้ไอคอนเริ่มต้นหากไม่มีไอคอนเซิร์ฟเวอร์
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        await new_channel.send(embed=embed, view=(ticketcloseview()))
        log_channel_id = config.logch
        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            log_embed = nextcord.Embed(
                    title="🔔 แจ้งเตือนการทำกิจกรรม",
                    color=nextcord.Color.green()
                )
            log_embed.add_field(name="🎁 ผู้ใช้งาน", value=user.mention, inline=False)
            log_embed.add_field(name="🔒 รูปเเบบห้อง", value="สั่งทำบอท", inline=False)
            log_embed.set_thumbnail(url=interaction.user.avatar.url)
            log_embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await log_channel.send(embed=log_embed)
        await interaction.response.send_message(content=f"สร้างห้อง {new_channel.name} เรียบร้อยแล้ว!", ephemeral=True)

    @nextcord.ui.button(label="เเจ้งปัญหา", style=nextcord.ButtonStyle.red, custom_id="report", emoji="📩")
    async def report(self, button:nextcord.Button, interaction:nextcord.Interaction):
        guild = interaction.guild  
        user = interaction.user
        channel_name = f"ticket-{user.name}".lower()
        category_id = config.categoryid 
        category = guild.get_channel(category_id)

        existing_channel = nextcord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"ห้อง `{channel_name}` มีอยู่แล้ว!", ephemeral=True)
            return

        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),  
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True) 
        }
        new_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category)
        embed = nextcord.Embed(
            title="𝐓𝐈𝐂𝐊𝐄𝐓 𝐒𝐘𝐒𝐓𝐄𝐌",
            description="```สามารถเเจ้งปัญหาที่ท่านพบกับตัวสินค้าได้เลยครับ```",
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1315041008047882263/1315041064771387492/DALLE_2024-12-05_23.56.52_-_A_professional_logo_for_NovaCraft_Dev_Studio_featuring_a_sleek_and_modern_design_with_a_blue_sky_theme._The_central_element_is_a_stylized_computer_in.webp?ex=6755f6ee&is=6754a56e&hm=54d4619e1551f3f287af0b4e41c03814f8c0b187525bc0136663c576fa55cef5&")  # ใช้ไอคอนเริ่มต้นหากไม่มีไอคอนเซิร์ฟเวอร์
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        await new_channel.send(embed=embed, view=(ticketcloseview()))
        log_channel_id = config.logch
        log_channel = guild.get_channel(log_channel_id)
        if log_channel:
            log_embed = nextcord.Embed(
                    title="🔔 แจ้งเตือนการทำกิจกรรม",
                    color=nextcord.Color.green()
                )
            log_embed.add_field(name="🎁 ผู้ใช้งาน", value=user.mention, inline=False)
            log_embed.add_field(name="🔒 รูปเเบบห้อง", value="เเจ้งปัญหา", inline=False)
            log_embed.set_thumbnail(url=interaction.user.avatar.url)
            log_embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await log_channel.send(embed=log_embed)
        await interaction.response.send_message(content=f"สร้างห้อง {new_channel.name} เรียบร้อยแล้ว!", ephemeral=True)




@bot.slash_command(description="Setup embed with buttons")
async def setup(interaction: nextcord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้", ephemeral=True)
        return
    await interaction.response.send_message(content="สำเร็จ", ephemeral=True)
    embed = nextcord.Embed(
        title="𝐓𝐈𝐂𝐊𝐄𝐓 𝐒𝐘𝐒𝐓𝐄𝐌",
        description="```สามารถสอบถามเเละสั่งซื้อสิ้นค้าได้ผ่านห้องนี้เเละเเจ้งปัญหาได้ผ่านห้แงนี้เช่นกัน```",
        color=nextcord.Color.blue()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1315041008047882263/1315041064771387492/DALLE_2024-12-05_23.56.52_-_A_professional_logo_for_NovaCraft_Dev_Studio_featuring_a_sleek_and_modern_design_with_a_blue_sky_theme._The_central_element_is_a_stylized_computer_in.webp?ex=6755f6ee&is=6754a56e&hm=54d4619e1551f3f287af0b4e41c03814f8c0b187525bc0136663c576fa55cef5&")  # ใช้ไอคอนเริ่มต้นหากไม่มีไอคอนเซิร์ฟเวอร์
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    embed.set_image(url="https://media.discordapp.net/attachments/1314563681467764756/1315037269228261396/DALLE_2024-12-08_02.28.10_-_A_professional_shop_banner_for_NovaCraft_Dev_Studio_featuring_the_central_logo_with_a_glowing_neon_blue_effect._The_design_is_sleek_and_futuristic_w.webp?ex=6755f365&is=6754a1e5&hm=f996063ba9b3cf045afff00f37b67f9bc7193e9589feb2194db45e50f66991b5&=&format=webp&width=922&height=527")
    await interaction.channel.send(embed=embed, view=(ticketview()))

bot.run(config.token)