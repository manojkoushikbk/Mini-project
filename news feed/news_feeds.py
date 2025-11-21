import tkinter as tk
from tkinter import scrolledtext
from newspaper import Article
import feedparser

rss_url = "https://www.thehindu.com/news/national/feeder/default.rss"

# Parse the RSS feed
feed = feedparser.parse(rss_url)

def extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return {
        "title": article.title,
        "authors": article.authors,
        "publish_date": article.publish_date,
        "text": article.text
    }

def display_feeds():
    text_area.delete(1.0, tk.END)
    for entry in feed.entries[:5]:
        article_data = extract_article(entry.link)
        title = article_data['title']
        authors = ", ".join(article_data['authors']) if article_data['authors'] else "Unknown"
        publish_date = article_data['publish_date'] if article_data['publish_date'] else "Unknown"
        adata = article_data['text'][:500].split('.')
        content = adata[0] + "." + adata[1]

        text_area.insert(tk.END, f"Title: {title}\n")
        text_area.insert(tk.END, f"Authors: {authors}\n")
        text_area.insert(tk.END, f"Published Date: {publish_date}\n")
        text_area.insert(tk.END, f"Content: {content}.\n")
        text_area.insert(tk.END, "-" * 50 + "\n")

# Create main GUI window
root = tk.Tk()
root.title("News Feed Viewer")
root.geometry("600x400")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
text_area.pack(pady=10)

refresh_button = tk.Button(root, text="Refresh Feeds", command=display_feeds)
refresh_button.pack()

display_feeds()

root.mainloop()