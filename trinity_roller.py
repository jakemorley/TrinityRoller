from collections.abc import Iterable
import discord
import pytest
import re
from roller import Roller

TOKEN = open(r"..\private\token.txt", "r").read()
TEST = True

client = discord.Client()

def check_dice_input(dice_str):
    dice_check = re.match('([1-9][0-9]*)(n|(r[1-9])|m)?', dice_str)
    if dice_check is not None:
        chunks = dice_check.groups()
        dice_pool = int(chunks[0])
        reroll = 10
        if any(c is not None for c in chunks[1:]):
            if chunks[1] == 'n':
                reroll = None
            else:
                reroll = int(chunks[1][-1]) # just need the last character with the reroll value
        return dice_pool, reroll

    return None, None



@client.event
async def on_message(msg):
    # handle the case of the bot replying to itself
    if msg.author == client.user:
        return None

    if msg.content.startswith('/nroll') or msg.content.startswith('/mroll'):
        #check if Nova or Mundane
        target_number = 7
        if msg.content.startswith('/mroll'):
            target_number = 8
        #roll some dice
        ret_msg = "Rolled no dice: "
        msg_chunks = msg.content.split()
        #we don't care about the first one - it's /nroll
        dice_pool, reroll = check_dice_input(msg_chunks[1].lower())
        if dice_pool is None:
            ret_msg = ret_msg + "{} is not a valid dice format".format(msg_chunks[1])
        else:
            die_roller = Roller(10, dice_pool, reroll=reroll)
            result = die_roller.roll()
            reduced_result = []
            for r in result:
                if isinstance(r, Iterable):
                    [reduced_result.append(i) for i in r]
                else:
                    reduced_result.append(r)
            print(reduced_result)
            successes = len([r for r in reduced_result if r >= target_number])
            ret_msg = "{} : {} successes".format(result, successes) if successes != 1 \
                else "{} : {} success".format(result, successes)

        await client.send_message(msg.channel, ret_msg)
    elif msg.content.startswith('/nhelp'):
        #send help
        ret_msg = "Welcome to trinity_roller.py - the Trinity - Continuum Dice Roller\r" \
                  "Usage:\r" \
                  "\tuse /nroll for Novas and /mroll for Mundanes - examples below assume nroll" \
                  "\t/nroll <dicepool> - rolls <dicepool> dice, keeping and re-rolling 10s\r, with default target number of 7" \
                  "\t/nroll <dicepool>n - rolls <dicepool> dice with no re-rolls\r" \
                  "\t/nroll <dicepool>r<#> - rolls <dicepool> dice, keeping and re-rolling any result of <#> or greater"
        await client.send_message(msg.channel, ret_msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

if not TEST:
    client.run(TOKEN)


def test_1d10():
    result1, result2 = check_dice_input('1')
    assert result1 == 1
    assert result2 == 10


def test_10d10():
    result1, result2 = check_dice_input('10')
    assert result1 == 10
    assert result2 == 10


def test_10d10_no_reroll():
    result1, result2 = check_dice_input('10n')
    assert result1 == 10
    assert result2 is None


def test_10d10_reroll_8():
    result1, result2 = check_dice_input('10r8')
    assert result1 == 10
    assert result2 == 8


def test_garbage():
    result1, result2 = check_dice_input('garbage')
    assert result1 is None
    assert result2 is None
