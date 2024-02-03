import pandas as pd
import lyricsgenius
from lyricsgenius import Genius
#import requests
#from bs4 import BeautifulSoup

def get_billboard_year_end_list(year):
    # Sample URL to use to get hot 100 based on a year
    #https://www.billboard.com/charts/year-end/2020/hot-100-songs/
    #url = "https://www.billboard.com/charts/year-end/{year}/hot-100-songs"
    
    url = "https://www.billboard.com/charts/year-end/" + year + "/hot-100-songs"
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


    results_songs = soup.find_all('h3', attrs={'class': 'c-title'})
    # print(results)
    songs = []
    for result in results_songs:
        songs.append(result.getText().strip())
    print(songs[0:100])

    results_artists = soup.find_all('span', attrs={'class': 'c-label'})
    artists = []
    for result in results_artists:
        if result.getText().strip().isdigit():
            pass
        else:
            artists.append(result.getText().strip())
    empty_array_artists = []
    for weird_format in artists:
        if " X " in weird_format:
            fix_format = weird_format.replace(" X ", " & ")
            empty_array_artists.append(fix_format)
        
    print(artists)
    songs = songs[0:100]
    print(len(songs))
    print(len(artists))

    #print(j)
    #response = requests.get(url).text
    
    #print(response)
    #print(response.content)

    #soup = BeautifulSoup(response, 'html.parser')
    #songs = soup.find_all(song = soup.findAll("h3", {"class": "c-title  a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max",
                           #"id": "title-of-a-story"}))
    #artists = soup.find_all(class_='ye-chart-item__artist')
    
    #print(songs)
    #print(artists)
    print("-----------------------------------------------")
    year_end_list = []
    for song, artist in zip(songs, artists):
        #song_name = song.get_text(strip=True)
        #artist_name = artist.get_text(strip=True)
        year_end_list.append(f'{artist} - {song}')
     
    hot100_data_frame = pd.DataFrame(
    {'artist': artists,
     'song': songs})
    print(hot100_data_frame)
    hot100_data_frame.loc[hot100_data_frame["song"] == "Close To Me", "artist"] = "Ellie Goulding & Diplo"
    hot100_data_frame.loc[hot100_data_frame["song"] == "One Too Many", "artist"] = "Keith Urban"
    
    return hot100_data_frame

def get_xxx(year):
    x = requests.get("https://www.billboard.com/charts/hot-100/").index  #used text; then using index
    soup = BeautifulSoup(x, "html.parser")
    chart = soup.find("div",class_="lxml")
    #div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row"

    songNames = [x.text for x in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) h3")]
    authorNames = [x.text for x in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) span")]
    print(songNames)
    #print(authorNames)
    print(len(songNames))
    
    return songNames # Temp return

from bs4 import BeautifulSoup
import requests    
#x = requests.get("https://www.billboard.com/charts/hot-100/").text
#soup = BeautifulSoup(x, "html.parser")
#chart = soup.find("div",class_="lxml")
##div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row"

#songNames = [x.text for x in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) h3")]
#authorNames = [x.text for x in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) span")]
#print(songNames)
#print(authorNames)
#print(len(songNames))

if __name__ == "__main__":
    year = input('Enter the year: ')
    year_end_list = get_billboard_year_end_list(year)
    #year_end_list = get_xxx(year)
    genius = Genius("8qFbiilVB_TggP_d-IjcfNGBNi-8E2_PychaHqi5FDMq4YyowoA9-VzBiiaOZj4d5jd4S7sqW989jggbxfYliw")
    genius.timeout = 15

    if not year_end_list.empty:
        lyrics_file = open(year +".lyrics.txt", "a", encoding='utf-8')
        for index, row in year_end_list.iterrows():
            lyrics_from_genius = genius.search_song(row["song"], row["artist"])
            lyrics_file.write(lyrics_from_genius.lyrics)

        
        print('Billboard Hot 100 Year-End List for {year}:')
        for entry in year_end_list:
            print(entry)
    else:
        print('No data available for the specified year.')
        
import re
import os
import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud

#years = ["2019", "2020", "2021", "2022"]
#for year in years:
 #   f = open(year + '.lyrics.txt', 'rb')
  #  all_words = ''
   # for sentence in f.readlines():
    #    this_sentence = sentence.decode('utf-8')
     #   all_words += this_sentence
   # f.close()

    #remove identifiers like chorus, verse, etc
    #all_words = re.sub(r'[\(\[].*?[\)\]]', '', all_words)
    #remove empty lines
    #all_words = os.linesep.join([s for s in all_words.splitlines() if s])
    
    #f = open(year + '.lyrics.cleaned.txt', 'wb')
    #f.write(all_words.encode('utf-8'))
   # f.close()

import re
import os

years = ["2019", "2020", "2021", "2022"]

for year in years:
    f = open(year + '.lyrics.txt', 'rb')
    all_words = ''
    for sentence in f.readlines():
        this_sentence = sentence.decode('utf-8')
        
        # Exclude lines with artist and song information
        if not re.match(r'\d+\.\s+[A-Za-z0-9\s&\(\)\[\]\-.,]+', this_sentence):
            all_words += this_sentence

    f.close()

    # Remove identifiers like chorus, verse, etc
    all_words = re.sub(r'[\(\[].*?[\)\]]', '', all_words)
    # Remove empty lines
    all_words = os.linesep.join([s for s in all_words.splitlines() if s])
    
    f = open(year + '.lyrics.cleaned.txt', 'wb')
    f.write(all_words.encode('utf-8'))
    f.close()
    words = all_words.split(" ")
    filtered_words = [word for word in words if word not in stopwords.words('english') and len(word) > 1 and word not in ['na','la']] # remove the stopwords
    joined_words = " ".join(filtered_words)
        # Generate a word cloud image
    wordcloud = WordCloud().generate(joined_words)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(joined_words)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()
    plt.savefig(year + '_wordcloud_lyrics.png')

## Sentiment Analysis code below:
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd
df = pd.DataFrame(columns=('year', 'pos', 'neu', 'neg'))
sid = SentimentIntensityAnalyzer()
i=0
years = ["2019", "2020", "2021", "2022"]
for year in years:
    num_positive = 0
    num_negative = 0
    num_neutral = 0

    f = open(year + ".lyrics.cleaned.txt", "rb")
    for sentence in f.readlines():
        this_sentence = sentence.decode('utf-8')
        comp = sid.polarity_scores(this_sentence)
        comp = comp['compound']
        if comp >= 0.5:
            num_positive += 1
        elif comp > -0.5 and comp < 0.5:
            num_neutral += 1
        else:
            num_negative += 1

    num_total = num_negative + num_neutral + num_positive
    percent_negative = (num_negative/float(num_total))*100
    percent_neutral = (num_neutral/float(num_total))*100
    percent_positive = (num_positive/float(num_total))*100
    df.loc[i] = (year, percent_positive, percent_neutral, percent_negative)
    i+=1
    #print(year, ": ", "positive: ", num_positive, "neutral: ", num_neutral, "negative: ", num_negative)
    print(year, ": ", "positive: ", percent_positive, "% ",  num_positive, "neutral: ", percent_neutral, "% ", num_neutral,  "negative: ", percent_negative, "% ", num_negative)
                 
df.plot.bar(x='year', stacked=True)
plt.show()     