import requests
from bs4 import BeautifulSoup
import json
import time
import re
from playwright.sync_api import sync_playwright
from collections import defaultdict

def clean_text(text):
    """Remove newlines, tabs, and extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def scrape_quotes_and_links(num_pages=1):
    """Scrape quotes and collect author links using BeautifulSoup"""
    print("\n" + "="*50)
    print("STEP 1: Scraping quotes with BeautifulSoup")
    print("="*50)
    
    # Dictionary to store quotes by author
    quotes_by_author = defaultdict(list)
    author_links = {}  
    
    for page_num in range(1, num_pages + 1):
        try:
            url = f'https://www.goodreads.com/quotes?page={page_num}'
            print(f"\nFetching page {page_num}/{num_pages}...")
            
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            r.raise_for_status()
            
            bs = BeautifulSoup(r.content, 'html.parser')
            quote_containers = bs.select('div.quote')
            
            for container in quote_containers:
                # Extract quote text
                quote_text_elem = container.select_one('div.quoteText')
                if not quote_text_elem:
                    continue
                quote_text = quote_text_elem.get_text(strip=True, separator=' ')
                
                # Extract author name
                author_tag = quote_text_elem.find('span', class_='authorOrTitle')
                author_name = clean_text(author_tag.get_text()) if author_tag else "Unknown"
                
                # Extract author link
                link_tag = container.select_one('a.leftAlignedImage')
                if link_tag and link_tag.get('href'):
                    href = link_tag.get('href')
                    if 'images' not in href and '/author/show/' in href:
                        full_url = f"https://www.goodreads.com{href}"
                        author_links[author_name] = full_url
                
                quote_clean = clean_text(quote_text.split('―')[0])
                
                # Extract tags
                tags = []
                tag_elements = container.select('div.greyText.smallText.left a')
                for tag in tag_elements:
                    tag_text = tag.get_text(strip=True)
                    if tag_text:
                        tags.append(tag_text)
                
                quotes_by_author[author_name].append({
                    'text': quote_clean,
                    'tags': tags
                })
            
            print(f"  ✓ Scraped {len(quote_containers)} quotes")
            time.sleep(1)
            
        except requests.RequestException as e:
            print(f"  ✗ Error fetching page {page_num}: {e}")
            continue
    
    print(f"\n✓ Total authors found: {len(quotes_by_author)}")
    print(f"✓ Total quotes scraped: {sum(len(q) for q in quotes_by_author.values())}")
    
    return quotes_by_author, author_links

def scrape_author_details(author_links):
    """Scrape author bio details using Playwright"""
    print("\n" + "="*50)
    print("STEP 2: Scraping author details with Playwright")
    print("="*50)
    
    author_details = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        for idx, (author_name, author_url) in enumerate(author_links.items(), 1):
            try:
                print(f"\n[{idx}/{len(author_links)}] Visiting: {author_name}")
                
                page.goto(author_url, timeout=10000)
                page.wait_for_selector('h1.authorName', timeout=5000)
                
                # Extract author bio
                bio = "No bio available"
                if page.locator('div.aboutAuthorInfo').is_visible():
                    try:
                        more_link = page.locator('div.aboutAuthorInfo a:has-text("...more")')
                        if more_link.is_visible(timeout=1000):
                            more_link.click()
                            time.sleep(0.5)
                    except:
                        pass
                    
                    bio_raw = page.locator('div.aboutAuthorInfo').text_content()
                    bio = clean_text(bio_raw.replace('edit data', '').replace('...more', ''))
                
                # Extract birth date
                birth_date = "Unknown"
                try:
                    birth_elem = page.locator('div.dataItem:has-text("Born")').locator('div.dataValue')
                    if birth_elem.is_visible(timeout=1000):
                        birth_date = clean_text(birth_elem.text_content())
                except:
                    pass
                
                # Extract website
                website = None
                try:
                    website_elem = page.locator('div.dataItem:has-text("Website")').locator('a')
                    if website_elem.is_visible(timeout=1000):
                        website = website_elem.get_attribute('href')
                except:
                    pass
                
                author_details[author_name] = {
                    'bio': bio,
                    'birth_date': birth_date,
                    'website': website,
                    'profile_url': author_url
                }
                
                print(f"  ✓ Scraped details for {author_name}")
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error scraping {author_name}: {str(e)}")
                author_details[author_name] = {
                    'bio': 'Error fetching bio',
                    'birth_date': 'Unknown',
                    'website': None,
                    'profile_url': author_url
                }
                continue
        
        browser.close()
    
    return author_details

def combine_data(quotes_by_author, author_details):
    """Combine quotes and author details into final structure"""
    print("\n" + "="*50)
    print("STEP 3: Combining data")
    print("="*50)
    
    final_data = []
    
    for author_name, quotes in quotes_by_author.items():
        author_info = author_details.get(author_name, {})
        
        author_obj = {
            'author': author_name,
            'bio': author_info.get('bio', 'No bio available'),
            'birth_date': author_info.get('birth_date', 'Unknown'),
            'website': author_info.get('website'),
            'profile_url': author_info.get('profile_url', 'Unknown'),
            'quote_count': len(quotes),
            'quotes': quotes
        }
        
        final_data.append(author_obj)
    
    final_data.sort(key=lambda x: x['quote_count'], reverse=True)
    
    return final_data

def main():
    num_pages = int(input("How many pages do you want to scrape? "))
    include_bios = input("Do you want to scrape author bios? (yes/no): ").lower()
    
    # Step 1: Scrape quotes and collect author links
    quotes_by_author, author_links = scrape_quotes_and_links(num_pages)
    
    # Step 2: Optionally scrape author details
    author_details = {}
    if include_bios == 'yes' and author_links:
        author_details = scrape_author_details(author_links)
    
    # Step 3: Combine everything
    final_data = combine_data(quotes_by_author, author_details)
    
    # Save to JSON
    output_file = 'authors_with_quotes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*50}")
    print(f"✓ Successfully scraped {len(final_data)} authors")
    print(f"✓ Total quotes: {sum(a['quote_count'] for a in final_data)}")
    print(f"✓ Data saved to '{output_file}'")
    print("="*50)

if __name__ == '__main__':
    main()