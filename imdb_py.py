import discord
from discord.ext import commands
from imdb import IMDb

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix='"', intents=intents)

# To notify when bot is ready
@client.event  # Function decorator
async def on_ready():  # on_ready for when bot is ready
    print("Bot is ready")

@client.listen()
async def on_message(message):

    if message.content.lower().startswith(">mo"): # Runs when a mssg starts with >mo
        ia = IMDb()

        movie = message.content[4:] # Gets movie name from mssg
        movies = ia.search_movie(movie)
        m_id = movies[0].getID()

        m_data = ia.get_movie(m_id)

        title = m_data["title"]
        try: 
            directors = ", ".join(map(str, m_data["directors"]))
        except KeyError:
            directors = ''

        try:
            rating = m_data["rating"]
        except KeyError:
            rating = ''

        try:
            year = m_data["year"]
        except KeyError:
            year = ''

        try:
            image = m_data["full-size cover url"]
        except KeyError:
            image = 'No Image Found'

        try:
            season_no = m_data["number of seasons"]
        except KeyError:
            season_no = 0

        try:
            seasons = m_data["seasons"]
        except KeyError:
            seasons = ''

        try:
            actors = ''
            if len(m_data["cast"]) > 15:
                for i in range(15):
                    actors += m_data["cast"][i]["name"]
                    actors += ", "
            else:
                actors = ", ".join(map(str, m_data["cast"]))
        except KeyError:
            actors = ''

        genre = m_data["genres"]
        genres = ""
        for i in genre:
            genres += i
            genres += " " # for converting genres to a readable string

        
        await message.channel.send(image) # Sends movie image
        await message.channel.send(
            f">>> **Title:**\n{title}\n\n**Genre:**\n{genres}\n\n**Rating:**\n{rating}\n\n**Year:**\n{year}\n\n**No. of seasons:**\n{season_no}\n\n**Seasons:**\n{seasons}\n\n**Directors:**\n{directors}\n\n**Actors:**\n{actors}"
        ) # Sends movie details

key = "client key here"
client.run(key) 