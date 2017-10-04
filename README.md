# Dropbox-Paper-Utilities
examples of using Dropbox's API 


## Pull that Data 
1. Get your Dropbox API token [here](https://dropbox.github.io/dropbox-api-v2-explorer/#paper_docs/list) -> click "Get Token"
2. Replace ``ACCESS_TOKEN`` (line 7 of paperpull.py) with your token
3. Run the script
`` python paperpull.py ``
#### What's going on?
This script grabs all of your Paper Documents, their Folder info, and lumps the text into a blob for later manipulation.

This data is stored in a Pickle file called 'paper_docs.p'

For more detailed scraping of the HTML, you can modify the HTMLParser class defined in paperpull.py

## Working with the Pickle Files
a few line snippets to get you started

```python
data = pickle.load(open('paper_docs.p','rb'))
folders = [data[d]['folder'] for d in data]
text = [data[d]['text'] for d in data]
```