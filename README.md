# scrapeX

### Twitter Trending Topics Scraper

A web scraping tool that uses Selenium and ProxyMesh to fetch the top 5 trending topics from Twitter's homepage, stores the data in MongoDB, and displays the results on a webpage.

## Installation

### Steps

1. Clone the repository

```sh
git clone https://github.com/yuvrajrathva/scrapeX.git
```

```sh
cd scrapeX
```

2. Set up a virtual environment and install dependencies with pipenv

```sh
pipenv install
```

3. Activate the virtual environment

```sh
pipenv shell
```

4. Set up MongoDB

Ensure MongoDB is installed and running on your local machine. If not, follow the instructions [here](https://docs.mongodb.com/manual/installation/).


## Running the scraper

1. Run the Flask app

```sh
python app.py
```

2. Open your browser and go to http://127.0.0.1:5000/
3. Enter your Twitter username and password on the form.
Click "Run Script" ans wait to fetch and display the result.
