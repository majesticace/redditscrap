import time
import httpx
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration for email
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
RECIPIENT_EMAIL = 'recipient@example.com'

# Function to send email
def send_email(new_posts):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'New Deals on Buildapcsales Subreddit'
    
    body = "New deals found:\n\n" + "\n\n".join(
        [f"Title: {post['title']}\nURL: {post['url']}" for post in new_posts])
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)

# Main scraping and filtering function
def scrape_and_filter():
    base_url = 'https://www.reddit.com'
    endpoint = '/r/buildapcsales'
    category = '/hot'

    url = base_url + endpoint + category + ".json"
    after_post_id = None

    dataset = []

    for _ in range(5):
        params = {
            'limit': 100,
            't': 'hour',  # time unit (hour, day, week, month, year, all)
            'after': after_post_id
        }
        response = httpx.get(url, params=params)
        print(f'fetching "{response.url}"...')
        if response.status_code != 200:
            raise Exception('Failed to fetch data')

        json_data = response.json()
        dataset.extend([rec['data'] for rec in json_data['data']['children']])
        after_post_id = json_data['data']['after']
        time.sleep(0.5)

    # Filter the dataset for relevant information
    filtered_data = []
    for post in dataset:
        title = post.get('title', '').lower()
        if ('4080 super' in title and 'white' in title) or ('4k' in title and 'oled' in title and 'monitor' in title):
            filtered_data.append({
                'title': post.get('title', ''),
                'url': post.get('url', ''),
                'created_utc': post.get('created_utc', ''),
                'selftext': post.get('selftext', ''),
                'upvote_ratio': post.get('upvote_ratio', ''),
                'num_comments': post.get('num_comments', '')
            })

    return filtered_data

# Initial dataset
previous_dataset = []

while True:
    current_dataset = scrape_and_filter()
    new_posts = [post for post in current_dataset if post not in previous_dataset]

    if new_posts:
        print(f'Found {len(new_posts)} new posts. Sending email...')
        send_email(new_posts)
        previous_dataset.extend(new_posts)
    
    # Save the current dataset to CSV
    df = pd.DataFrame(current_dataset)
    df.to_csv('filtered_reddit_posts.csv', index=False)
    
    # Sleep for an hour before the next iteration
    time.sleep(3600)
