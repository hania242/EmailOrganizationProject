import requests
import time
import pandas as pd
from datetime import datetime

class SimpleRedditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.data = []
    
    def scrape_reddit_subreddit(self, subreddit, query, limit=50):
        """Scrape Reddit posts - minimal filtering"""
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {
            'q': query,
            'sort': 'relevance',
            'limit': limit,
            'restrict_sr': 'on'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = data['data']['children']
                
                for post in posts:
                    post_data = post['data']
                    self.data.append({
                        'source': f"r/{subreddit}",
                        'title': post_data.get('title', ''),
                        'text': post_data.get('selftext', ''),
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'created_date': datetime.fromtimestamp(post_data.get('created_utc', 0)),
                        'search_term': query,
                        'url': f"https://reddit.com{post_data.get('permalink', '')}"
                    })
                
                print(f"  Collected {len(posts)} posts from r/{subreddit} for '{query}'")
                    
            time.sleep(2)
            
        except Exception as e:
            print(f"Error scraping r/{subreddit}: {e}")
    
    def scrape_email_related_posts(self):
        """Scrape posts that might be about email organization"""
        
        # Cast a wide net - get anything email-related
        searches = [
            # Gmail specific
            ('gmail', 'organization'),
            ('gmail', 'organize'),
            ('gmail', 'cluttered'),
            ('gmail', 'too many emails'),
            ('gmail', 'inbox management'),
            ('gmail', 'email management'),
            ('gmail', 'overwhelmed'),
            ('gmail', 'productivity'),
            ('gmail', 'hard to find'),
            ('gmail', 'search emails'),
            
            # General email in productivity communities  
            ('productivity', 'email cluttered'),
            ('productivity', 'email organization'),
            ('productivity', 'gmail organization'),
            ('productivity', 'inbox cluttered'),
            ('productivity', 'too many emails'),
            ('productivity', 'email overwhelmed'),
            ('productivity', 'inbox overwhelmed'),
            ('productivity', 'email productivity'),
            
            # Email help requests
            ('NoStupidQuestions', 'email organization'),
            ('NoStupidQuestions', 'gmail organization'),
            ('NoStupidQuestions', 'too many emails'),
            ('NoStupidQuestions', 'inbox management'),
            
            # Email tips (might contain problems)
            ('LifeProTips', 'email organization'),
            ('LifeProTips', 'gmail tips'),
            ('LifeProTips', 'inbox management'),
            
            # Tech help
            ('techsupport', 'gmail organization'),
            ('techsupport', 'email management'),
        ]
        
        print("Scraping Reddit for email organization posts...")
        print("Will collect everything email-related, then we'll clean manually")
        print("-" * 60)
        
        for subreddit, query in searches:
            print(f"\nSearching r/{subreddit} for '{query}'...")
            self.scrape_reddit_subreddit(subreddit, query, limit=25)
            time.sleep(3)
    
    def save_raw_data(self):
        """Save all collected data without filtering"""
        if not self.data:
            print("No data collected!")
            return None
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_data = []
        for post in self.data:
            if post['url'] not in seen_urls:
                unique_data.append(post)
                seen_urls.add(post['url'])
        
        df = pd.DataFrame(unique_data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f'reddit_email_raw_data_{timestamp}.csv'
        df.to_csv(filename, index=False)
        
        print(f"\n" + "=" * 60)
        print("RAW REDDIT DATA COLLECTION COMPLETE")
        print("=" * 60)
        print(f"Collected {len(unique_data)} unique posts")
        print(f"Saved to: {filename}")
        print(f"Sources: {df['source'].value_counts().to_dict()}")
        
        print(f"\nSAMPLE POSTS (for you to review):")
        sample_posts = df.head(10)
        for i, post in sample_posts.iterrows():
            relevance = "📧" if any(word in post['title'].lower() for word in ['email', 'gmail', 'inbox', 'organize']) else "❓"
            print(f"{relevance} \"{post['title'][:70]}...\" ({post['score']} upvotes, {post['source']})")
        
        print(f"\nNEXT STEPS:")
        print(f"1. Open {filename} in Excel/Google Sheets")
        print(f"2. Review posts and delete irrelevant rows")
        print(f"3. Save the cleaned CSV")
        print(f"4. Send me the cleaned CSV for analysis")
        
        return filename

def main():
    scraper = SimpleRedditScraper()
    
    try:
        # Scrape everything email-related
        scraper.scrape_email_related_posts()
        
        # Save raw data for manual review
        filename = scraper.save_raw_data()
        
        if filename:
            print(f"\n✅ Raw data ready for manual cleaning: {filename}")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted")
        if scraper.data:
            scraper.save_raw_data()
    except Exception as e:
        print(f"Error: {e}")
        if scraper.data:
            scraper.save_raw_data()

if __name__ == "__main__":
    main()