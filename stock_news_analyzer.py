import json
import requests
import time
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ollama  # Import ollama

# Configuration
watchlist = ['GESHIP', 'COCHISHIP', 'GRSE', 'Hindustan Aeronautics Limited', 'IRCON', 'IREDA']  # Add your stock symbols here
news_api_keys = ['enter your key']  # Array of API keys
email_user = 'example@gmail.com'
email_password = 'XXXXXXXXXXX'
email_to = 'example@gmail.com'
email_cc = 'example@gmail.com'  # CC email address
check_interval = 60  # Check every hour

# File to store analyzed titles
analyzed_titles_file = 'analyzed_titles.txt'

# Set to keep track of notified titles
notified_titles = set()
today = date.today()

# Current API key index
current_api_key_index = 0

# Function to fetch news
def fetch_news(stock, api_key):
    print(f"Fetching news for {stock} with API key {api_key}...")  # Debug: Print when fetching news
    url = (
        f'https://newsapi.org/v2/everything?q={stock}&'
        f'from=2024-07-09&'
        f'sortBy=publishedAt&'
        f'language=en&'
        f'apiKey={api_key}'
    )
    response = requests.get(url)
    response_json = response.json()
    if response.status_code != 200 or response_json.get('status') == 'error':
        if response_json.get('status') == 'error' and response_json.get('code') == 'rateLimited':
            raise RateLimitError(f"Rate limit error for API key {api_key}: {response_json.get('message')}")
        else:
            raise Exception(f"Failed to fetch news. Status Code: {response.status_code}")
    return response_json['articles']

# Custom exception for rate limit errors
class RateLimitError(Exception):
    pass

# Function to analyze news using Llama API for sentiment analysis
def analyze_news(articles, stock):
    results = []
    # Load analyzed titles from file
    analyzed_titles = load_analyzed_titles()
    
    for article in articles:
        title = article['title']
        if title in analyzed_titles:
            print(f"Skipping analysis for '{title}'. Already analyzed.")
            continue
        
        content = article.get('content', '')  # Use article content instead of description
        published_at = article['publishedAt']
        url = article['url']  # Fetch URL from the article
        
        # Check if the stock is mentioned prominently in the title or content
        if stock.lower() not in title.lower() and stock.lower() not in content.lower():
            continue  # Skip articles that don't prominently mention the stock
        
        print(f"Analyzing sentiment for: {title}")  # Debug: Print when analyzing sentiment
        
        # Build the content for Llama API request
        message_content = f"Provide a buy/sell/hold recommendation and a short reason behind it by analyzing the following news article about **{stock}**:\n\n" \
                          f"**Title:** {title}\n\n" \
                          f"**Content:**\n{content}\n" \
                          f"**URL:** {url}\n"
        
        # Execute the Llama API request with error handling
        try:
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": message_content}])
            llama_response = response["message"]["content"]

            # Extract sentiment and recommendation from llama_response
            # sentiment = analyze_sentiment(llama_response)
            
            results.append({
                'title': title,
                'content': content,
                'llama_response': llama_response,
                # 'sentiment': sentiment,
                'published_at': published_at,
                'url': url  # Include URL in the result
            })
            notified_titles.add(title)
            
            # Append analyzed title to file
            append_analyzed_title(title)
            
            # Send email for this analysis
            send_email(f"News Analysis and Recommendation for {stock}", results[-1])
        
        except RateLimitError as e:
            print(f"Rate limit error encountered: {str(e)}")
            raise  # Re-raise the rate limit error to handle it in the main loop
        
        except Exception as e:
            print(f"Error analyzing sentiment for: {title}. Exception: {str(e)}")
            continue
    
    return results

# # Function to analyze sentiment based on llama_response
# def analyze_sentiment(llama_response):
#     # Simplified logic for sentiment analysis based on keywords in the response
#     if 'positive' in llama_response.lower():
#         return 'Positive'
#     elif 'negative' in llama_response.lower():
#         return 'Negative'
#     else:
#         return 'Neutral'

# Function to send email
def send_email(subject, result):
    print(f"Sending email with subject: {subject}")  # Debug: Print when sending email
    
    # Construct the email body
    email_body = f"Title: {result['title']}\n\n" \
                 f"Llama Analysis: {result['llama_response']}\n" \
                 f"Published At: {result['published_at']}\n" \
                 f"URL: {result['url']}\n"
    
    try:
        # Create MIMEMultipart message and set email headers
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_to
        msg['Subject'] = subject
        msg['CC'] = email_cc  # Add CC email address

        # Attach formatted body as plain text
        msg.attach(MIMEText(email_body, 'plain'))

        # Connect to SMTP server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, [email_to, email_cc], msg.as_string())  # Include CC email address
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Function to load analyzed titles from file
def load_analyzed_titles():
    try:
        with open(analyzed_titles_file, 'r') as file:
            titles = file.readlines()
            titles = [title.strip() for title in titles]
            return set(titles)
    except FileNotFoundError:
        return set()

# Function to append analyzed title to file
def append_analyzed_title(title):
    with open(analyzed_titles_file, 'a') as file:
        file.write(title + '\n')

# Main loop
while True:
    up_to_date = True  # Flag to check if all stocks are up to date
    for stock in watchlist:
        print(f"Processing stock: {stock}")  # Debug: Print which stock is being processed
        while current_api_key_index < len(news_api_keys):
            current_api_key = news_api_keys[current_api_key_index]
            try:
                articles = fetch_news(stock, current_api_key)
                if articles:
                    analysis_results = analyze_news(articles, stock)
                    if analysis_results:
                        up_to_date = False  # There are new articles to analyze for this stock
                    else:
                        print(f"No new articles found for {stock}.")
                    break  # Exit the loop if fetching and analyzing was successful
                else:
                    print(f"No articles found for {stock} with API key: {current_api_key}")
                break  # Exit the loop if fetching was successful
            except RateLimitError as e:
                print(f"Rate limit error encountered for {stock} with API key: {current_api_key}. Exception: {str(e)}")
                current_api_key_index += 1  # Move to the next API key
            except Exception as e:
                print(f"Failed to fetch news for {stock} with API key: {current_api_key}. Exception: {str(e)}")
                break  # Exit the loop on non-rate limit error
    
    if up_to_date:
        print("You are up to date. No new articles to analyze.")
    
    print(f"Sleeping for {check_interval} seconds...")
    time.sleep(check_interval)  # Wait for the specified interval before fetching again
