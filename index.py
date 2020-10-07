# Import dependencies
from riotwatcher import LolWatcher, ApiError
from PIL import Image, ImageDraw, ImageFont
import requests
from math import floor
import time
#from flask import Flask
from threading import Thread, Timer

# Flask initialization
# app = Flask(__name__, static_url_path='/')

# @app.route('/')
# def hello():
#     return 'App is running!'

# Riot global Variables
lol_api_key = 'RGAPI-411683ad-be21-4aa6-bea7-51105194705c'
lol = LolWatcher(lol_api_key)
lol_region = 'br1'
lol_summonernick = 'SirMonteiro007'

def updatestats():

    # Picking the information from riot

    summoner = lol.summoner.by_name(lol_region, lol_summonernick)
    summoner_ranked_stats = lol.league.by_summoner(lol_region, summoner['id'])
    lol_version_for_region = lol.data_dragon.versions_for_region(lol_region)
    lol_profileicon_url = 'http://ddragon.leagueoflegends.com/cdn/' + lol_version_for_region['n']['profileicon'] + '/img/profileicon/' + str(summoner['profileIconId']) + '.png'

    lol_winrate = str(floor(summoner_ranked_stats[0]['wins']/(summoner_ranked_stats[0]['losses'] + summoner_ranked_stats[0]['wins'])*100))

    # Final image texts
    img_strgs = {
        '1': summoner['name'],
        '2': summoner_ranked_stats[0]['tier'].title() + ' ' + summoner_ranked_stats[0]['rank'] + ' ' + str(summoner_ranked_stats[0]['leaguePoints']) + ' LP',
        '3': summoner_ranked_stats[0]['queueType'].split('_')[1].title() + ' 5v5',
        '4': str(summoner_ranked_stats[0]['wins']) + 'W ' + str(summoner_ranked_stats[0]['losses']) + 'L ' + ' ' + lol_winrate + '%'
    }

    # Largest line on final image to determine final image width
    maiorstr = sorted(img_strgs.items(), key=lambda x: len(x[1]), reverse=True)

    # Texts font
    font = ImageFont.truetype('./assets/Montserrat-SemiBold.ttf', 14)

    # Final image width
    largest_text_width = font.getsize(maiorstr[0][1])[0]
    img_width = 100 + largest_text_width + 100

    # Creating the final image...
    img = Image.new('RGBA', (img_width, 100), color = (0, 0, 0, 100))

    # Paste all images on final image
    img_profileicon_ddragon = requests.get(lol_profileicon_url, stream=True)
    img_profileimage = Image.open(img_profileicon_ddragon.raw).resize((80,80))
    img_rank = Image.open('./assets/img/' + summoner_ranked_stats[0]['tier'] + '.png').resize((100,100))
    img.paste(img_profileimage, (10,10))
    img.alpha_composite(img_rank, (img_width-100,0))

    # Write texts on final image
    d = ImageDraw.Draw(img)
    d.text((100,10), img_strgs.get('1'), font=font, fill=(255,255,255))
    d.text((100,30), img_strgs.get('2'), font=font, fill=(255,255,255))
    d.text((100,50), img_strgs.get('3'), font=font, fill=(255,255,255))
    d.text((100,70), img_strgs.get('4'), font=font, fill=(255,255,255))

    # Save image
    img.save('./summoner_stats.png')

    # Update every 30 seconds
    time.sleep(30)
    updatestats()


# Initialize all functions
# if __name__ == '__main__':
#     Thread(target = updatestats).start()
#     Thread(target = app.run(port=80, threaded=True)).start()
updatestats()