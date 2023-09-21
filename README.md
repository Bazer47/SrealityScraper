# SrealityScraper
Simple web app for scraping 500 property ads from Sreality.

## Requirements
- Python 3.8
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.
```bash
python -m pip install -r requirements.txt
```

OR
- Docker with Docker compose

## Usage
### Python
Assure you have a connection to a database. Then run
```bash
python app.py
```
The web page should be on http://127.0.0.1:5000/.

### Docker
Run
```bash
docker compose up
```
The web page should be on http://127.0.0.1:8080/.

## Contributing

Pull requests are welcome.
