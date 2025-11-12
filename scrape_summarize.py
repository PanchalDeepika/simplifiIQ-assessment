import pandas as pd
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
import csv

# ---------- SETUP ----------
# Replace with your own Gemini API Key (free from https://makersuite.google.com/app/apikey)
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ---------- FUNCTIONS ----------

def read_urls(file_path):
    """Read URLs from a CSV, Excel, or TXT file."""
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".txt"):
        df = pd.read_csv(file_path, names=["url"])
    else:
        raise ValueError("Unsupported file format.")
    return df["url"].tolist()

def fetch_web_data(url):
    """Fetch and parse title and meta description from a webpage."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title found"
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc["content"].strip() if meta_desc and "content" in meta_desc.attrs else "No meta description found"
        return title, meta_desc
    except Exception as e:
        return "Error fetching data", str(e)

def summarize_content(title, meta_desc):
    """Generate a short AI-based summary using Gemini API."""
    prompt = f"Summarize this web page briefly:\nTitle: {title}\nDescription: {meta_desc}\nGive a concise 3-line summary."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

def save_results(results, output_file="output_summary.csv"):
    """Save all data to CSV."""
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["URL", "Title", "Meta Description", "AI Summary"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\n✅ Results saved to: {output_file}")

# ---------- MAIN WORKFLOW ----------
def main():
    input_file = "urls.csv"  # You can change this path
    urls = read_urls(input_file)

    results = []
    for url in urls:
        print(f"Processing: {url}")
        title, meta_desc = fetch_web_data(url)
        summary = summarize_content(title, meta_desc)
        results.append({
            "URL": url,
            "Title": title,
            "Meta Description": meta_desc,
            "AI Summary": summary
        })

    save_results(results)

if __name__ == "__main__":
    main()
