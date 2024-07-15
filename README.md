Sure! Here is a detailed README for your project:

---

# Stock News Sentiment Analyzer

Automated system to fetch and analyze stock-related news articles using sentiment analysis, providing buy/sell/hold recommendations based on the sentiment. Integrates with Llama API for sentiment analysis and sends results via email to multiple recipients. The system handles rate limit errors by switching API keys to ensure continuous operation.

## Features
- Fetches news articles from multiple sources using NewsAPI.
- Switches to a different API key if the current key exceeds rate limits.
- Analyzes sentiment and generates stock recommendations using the Llama API.
- Sends detailed analysis results via email to multiple recipients.
- Maintains a log of analyzed articles to prevent duplicate processing.
- Configurable check interval for fetching and analyzing news.

## Prerequisites
- Python 3.x
- `requests` library
- `smtplib` library
- `ollama` library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stock-news-sentiment-analyzer.git
   cd stock-news-sentiment-analyzer
   ```

2. Install the required Python packages:
   ```bash
   pip install requests
   pip install ollama
   ```

## Configuration
1. Update the configuration variables in the script:
   - `watchlist`: List of stock symbols to monitor.
   - `news_api_keys`: List of NewsAPI keys to use.
   - `email_user`: Your email address for sending emails.
   - `email_password`: Your email password or app-specific password.
   - `email_to`: Primary recipient's email address.
   - `email_cc`: List of CC email addresses.
   - `check_interval`: Interval in seconds for checking news articles.

2. Ensure your email account allows less secure app access or use an app-specific password if using Gmail.

## Usage
Run the script to start monitoring and analyzing stock-related news articles:
```bash
python stock_news_analyzer.py
```

## Detailed Description
This script monitors news articles for a specified list of stocks. It fetches news articles using the NewsAPI and handles API key rate limits. It analyzes the sentiment of the news articles using the Llama API, providing buy/sell/hold recommendations. The analysis results are sent to specified email addresses, and a record of analyzed articles is maintained to avoid duplicate analysis.

## Example
The script fetches news articles for stocks like 'GESHIP', 'COCHISHIP', 'GRSE', 'Hindustan Aeronautics Limited', 'IRCON', and 'IREDA'. It uses the Llama API to analyze the sentiment of each article and provides a buy/sell/hold recommendation. The results are emailed to the specified recipients.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Contributions
Feel free to submit pull requests or raise issues if you find any bugs or have suggestions for improvements.

---

### Contact
For any queries or support, contact [your-email@example.com](mailto:your-email@example.com).

---

Replace `your-username` in the git clone URL with your GitHub username and update the email address in the Contact section with your actual email address. Let me know if you need any more customization or additional information!
