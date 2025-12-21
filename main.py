import pandas as pd
from bs4 import BeautifulSoup
import requests


"""
Goodreads Quote Scraper
Scrapes quotes from goodreads.com/quotes and saves to CSV """


def main():
    try:
        r = requests.get('https://www.goodreads.com/quotes',headers={'User-Agent': 'Mozilla/5.0'},timeout=10)
        r.raise_for_status()  
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return
    
    bs=BeautifulSoup(r.content,'html.parser')
    
    select=bs.select_one('div.mainContentContainer').find_all('div',class_='quoteText')
    
    quotes_data = []
    for item in select:
        text = item.get_text(strip=True, separator='\n')
        quotes_data.append({'quote': text})

    df = pd.DataFrame(quotes_data)
    df.to_csv('quotes.csv', index=False)
    print(f"Successfully scraped {len(quotes_data)} quotes and saved to quotes.csv")
    


if __name__ == "__main__":
    main()
