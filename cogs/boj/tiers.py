from discord.ext.commands.bot import Bot


color = [0xa75618, 0x4e608d, 0xffae00, 0x00ffa1, 0x00afff, 0xff0042]
prefix = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']
number = ['V', 'IV', 'III', 'II', 'I']

def level_to_tier(level):
    return prefix[(level - 1) // 5], number[(level - 1) % 5], color[(level - 1) // 5]

def find_emoji(bot:Bot, level):
    tier, number, color = level_to_tier(level)
    emojiname = 'unranked' if level == 0 else f'{tier.lower()}{5 - ((level - 1) % 5)}'
    for emoji in bot.emojis:
        if emoji.name == emojiname:
            return emoji
    return None