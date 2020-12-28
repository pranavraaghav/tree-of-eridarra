# Tree of Eridarra
Tree of Eridarra is a discord bot that I custom built for my private discord server - Eridarra.

## Read this before you proceed:
1. The code was written on **repl.it** which also handles the version control for this project. 
2. The discord bot token has been hidden from the public by storing it in a .env file that can only be accessed during repl.it runtime
3. The bot uses replit's database module to store some information
4. The bot works on the surface but the code still needs some refinement under the hood to truly call it a working bot. welp. 
5. I've outline how I manage to keep the bot running 24x7 on repl.it later on in this document

## How to use:
You're gonna need to generate your own discord bot token in order to use this code as your own bot (instructions for which can be easily found online)

Clone the code to your computer, then add bot token value to the main.py file under a variable named TOKEN. Run main.py and boom, you have a working bot. 

## How I keep the bot running 24x7 
I used repl.it to make this work. By default, repl.it will stop your code from running if you close the tab, however, while running servers it continues to run for up to 1 hour without any requests to the server. 
keep_alive.py contains the code to start and run a flask server. The flask server is instantiated along with the discord bot in main.py. I use uptimerobot.com to ping the flask server every 5 
minutes - this refreshes the 1 hour timeout on the entire session, thus keeping my discord bot alive until I manually stop it. 
