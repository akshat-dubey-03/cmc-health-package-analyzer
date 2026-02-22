from scraper import scrape_health_packages

result = scrape_health_packages("https://www.docopd.com/en-in/lab/cmc-vellore")
print(f"Result length: {len(result)}")
print(result[:1000])
