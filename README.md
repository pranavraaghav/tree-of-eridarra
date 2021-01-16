# Tree of Eridarra
Tree of Eridarra is a discord bot that I custom built for my private discord server - Eridarra.

## Features:
1. Inspiring and motivating quotes upon command
2. System where a user can start "working" for X minutes and bot will ask them to get back to work if they text within the next X minutes.

## Read this before you proceed:
You need to provide your own bot's token in order for this program to work. 
Create a folder named ".env" and add this line: 
TOKEN=<your-bot-token>

**note:** Do not enclose bot token under within quotes. 

**It should look something like this**:
TOKEN= JfnDFKShFEHASFHDhSD.fdafLUhdshfds
(I mashed my keys to get that value, don't bother trying to use that^)

Run main.py and you should have a working bot. 

## How I keep the bot running 24x7 
I run this bot locally at home on my raspberry pi 4 B. 

## Packages used
1. discord.py - accessing discord's API for bots
2. dotenv - working with .env files
