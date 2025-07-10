import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import json

def ExtractParameters(url):
    try:
        UrlParsed = urlparse(url)
        return parse_qs(UrlParsed.query)
    except Exception as exp:
        return None

def CrawlExtract(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        params_list = []
        for link in soup.find_all('a', href=True):
            full_url = link['href']
            if full_url.startswith('http'):
                params = ExtractParameters(full_url)
                if params:
                    params_list.append({"url": full_url, "params": params})
        
        return params_list
    except Exception as exp:
        return None

def JsonResults(results):
    OutputFiles = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if OutputFiles:
        with open(OutputFiles, 'w') as f:
            json.dump(results, f, indent=4)
        Status.config(text=f"Results saved to {OutputFiles}")
    else:
        Status.config(text="Save canceled.")

def TXTResults(results):
    OutputFile = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if OutputFile:
        try:
            with open(OutputFile, 'w') as f:
                for result in results:
                    f.write(f"URL: {result['url']}\n")
                    f.write("Parameters:\n ")
                    for param, value in result['params'].items():
                        f.write(f"  {param}: {value}\n")
                    f.write("\n")
            Status.config(text=f"Results saved to {OutputFile}")
        except Exception as exp:
            Status.config(text="Error saving the file.")
    else:
        Status.config(text="Save canceled.")

def HTMLResults(results):
    OutputFile = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if OutputFile:
        try:
            with open(OutputFile, 'w') as f:
                f.write("<html><body>\n")
                f.write("<h1>Crawled URL Parameters</h1>\n")
                f.write("<table border='1'>\n")
                f.write("<tr><th>URL</th><th>Parameters</th></tr>\n")
                for result in results:
                    f.write(f"<tr><td>{result['url']}</td><td>\n")
                    f.write("<ul>\n")
                    for param, value in result['params'].items():
                        f.write(f"<li>{param}: {value}</li>\n")
                    f.write("</ul>\n")
                    f.write("</td></tr>\n")
                f.write("</table>\n")
                f.write("</body></html>\n")
            Status.config(text=f"Results saved to {OutputFile}")
        except Exception as exp:
            Status.config(text="Error saving the file.")
    else:
        Status.config(text="Save canceled.")

def FileFormatChoose(results):
    format_choice = messagebox.askquestion("File Format", "Would you like to save the results as a JSON file?")
    
    if format_choice == "yes":
        JsonResults(results)
    else:
        format_choice = messagebox.askquestion("File Format", "Would you like to save the results as a text file?")
        if format_choice == "yes":
            TXTResults(results)
        else:
            HTMLResults(results)

def CrawlingStart():
    url = URLEntry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a valid URL.")
        return
    
    Status.config(text="Crawling in progress, please wait...")
    results = CrawlExtract(url)
    
    if results:
        FileFormatChoose(results)
    else:
        messagebox.showerror("Error", "No parameters found or error crawling the website. Please check the URL.")
        Status.config(text="Crawl finished with errors or no parameters found.")
    
    Status.config(text="Crawl completed!")

root = tk.Tk()
root.title("LinkInspect : The Web Scraper")

WelcomeLabel = tk.Label(root, text="Welcome to the LinkInspect!", font=("Helvetica-Bold", 18), fg="Navy")
WelcomeLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

InstructionLabel = tk.Label(root, text="Please enter the URL of a website:", font=("Helvetica-Bold", 12))
InstructionLabel.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

URLEntry = tk.Entry(root, width=50, font=("Helvetica", 12))
URLEntry.grid(row=1, column=1, padx=10, pady=10)

CrawlButton = tk.Button(root, text="Start Crawl", font=("Helvetica-Bold", 12), command=CrawlingStart)
CrawlButton.grid(row=2, column=1, pady=10)

Status = tk.Label(root, text="", font=("Helvetica", 12), fg="green")
Status.grid(row=3, column=1, padx=10, pady=10)

root.minsize(100, 50)
root.mainloop()