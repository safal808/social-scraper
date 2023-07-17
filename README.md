# Instagram and Facebook Link Extractor

This program is a Python application that helps you extract unique Instagram and Facebook links from a list of URLs provided in either a CSV or a text file. It utilizes the `tkinter` library for a simple graphical user interface (GUI) and the `requests`, `re`, `csv`, and `concurrent.futures` modules for processing the URLs and extracting links in parallel.

## How to Use

1. Make sure you have Python installed on your system.

2. Download the `main.py` file and save it to your preferred location.

3. Install the required dependencies by running the following command in your terminal or command prompt:

   ```
   pip install requests
   ```

4. Run the program by executing the `main.py` file.

5. The GUI window will open, allowing you to click the "Process URLs" button.

6. A file dialog will pop up, prompting you to select the file containing the list of URLs you want to process. Choose a CSV or a text file that contains the URLs, one per line.

7. The program will start processing the URLs in batches. It will connect to each URL, read its HTML content, and extract Instagram and Facebook links from it.

8. After processing is complete, two text files will be created in the same directory as the `main.py` file:

   - `ig_links.txt`: This file contains unique Instagram links extracted from the provided URLs.

   - `non_ig_fb_links.txt`: This file contains unique links that are not Instagram but are associated with Facebook.

9. A message box will appear, informing you that the process is complete and showing the names of the generated output files.

## Note

- The program uses a batch processing approach with a batch size of 1 URL by default. You can adjust the `BATCH_SIZE` variable in the code to process URLs in larger batches, depending on your system's capabilities and the size of the URL list.

- If any connection errors or timeouts occur while processing the URLs, the program will skip those URLs and continue processing the rest. The skipped URLs will be displayed in the console.

- For successful execution, ensure that the `tkinter` library and the required dependencies are installed on your system.

- Please use this program responsibly and respect the terms of service and privacy policies of the websites you're scraping data from.

## Disclaimer

This program is provided as-is with no warranties or guarantees. The developers are not responsible for any misuse or consequences resulting from the use of this program. Use it responsibly and ensure compliance with applicable laws and regulations.
