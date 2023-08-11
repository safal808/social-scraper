import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import re
import csv
import concurrent.futures

def process_urls():
    # Read URLs from a file
    filename = filedialog.askopenfilename(title="Select File", filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")))
    if not filename:
        return

    urls = []
    if filename.endswith(".txt"):
        with open(filename, "r") as file:
            urls = file.readlines()
    elif filename.endswith(".csv"):
        with open(filename, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                urls.extend(row)

    # Create sets to store unique Instagram links and Facebook links
    ig_links = set()
    non_ig_fb_links = set()

    BATCH_SIZE = 1  # Adjust batch size as needed

    # Batch processing URLs
    batches = [urls[i:i + BATCH_SIZE] for i in range(0, len(urls), BATCH_SIZE)]

    def process_batch(batch):
        batch_ig_links = set()
        batch_non_ig_fb_links = set()
        for url in batch:
            url = url.strip()

            # Skip empty URLs
            if not url:
                continue

            try:
                # Connect to the URL
                website = requests.get(url, timeout=5)

                # Read HTML
                html = website.text

                # Use re.findall to grab all the links
                pattern_ig = r'"((http|ftp)s?://(www\.)?instagram.com/[^"]+)"'
                pattern_fb = r'"((http|ftp)s?://(www\.)?facebook.com/[^"]+)"'
                links_ig = re.findall(pattern_ig, html)
                links_fb = re.findall(pattern_fb, html)

                # Process Instagram links
                for link in links_ig:
                    clean_link = link[0]

                    # Check if the link is already in the set
                    # Skip if it exists in the set to eliminate duplicates
                    if clean_link in ig_links:
                        continue

                    batch_ig_links.add(clean_link)

                # Process Facebook links
                for link in links_fb:
                    clean_link = link[0]

                    # Check if the link is already in the set
                    # Skip if it exists in the set to eliminate duplicates
                    if clean_link in non_ig_fb_links:
                        continue

                    batch_non_ig_fb_links.add(clean_link)
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                # Handle connection errors or timeouts
                print("Error connecting to:", url)
                continue

        return batch_ig_links, batch_non_ig_fb_links

    # Use concurrent.futures for parallel execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit batch processing tasks
        batch_tasks = [executor.submit(process_batch, batch) for batch in batches]

        # Retrieve results as they become available
        for future in concurrent.futures.as_completed(batch_tasks):
            batch_ig_links, batch_non_ig_fb_links = future.result()
            ig_links.update(batch_ig_links)
            non_ig_fb_links.update(batch_non_ig_fb_links)

    # Append unique Instagram links to a text file
    ig_output_filename = "ig_links.txt"
    with open(ig_output_filename, "w") as file:
        for link in ig_links:
            file.write(link + "\n")

    # Append unique non-Instagram but with Facebook links to a text file
    non_ig_fb_output_filename = "non_ig_fb_links.txt"
    with open(non_ig_fb_output_filename, "w") as file:
        for link in non_ig_fb_links:
            file.write(link + "\n")

    messagebox.showinfo("Process Complete", "Instagram links stored in {}\nNon-Instagram but with Facebook links stored in {}".format(ig_output_filename, non_ig_fb_output_filename))


window = tk.Tk()
window.title("Instagram and Facebook Link Extractor")
window.geometry("300x300")

process_button = tk.Button(window, text="Process URLs", command=process_urls)
process_button.pack(pady=120)

window.ainloop()

