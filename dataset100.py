from newspaper import Article

url = "https://www.benzinga.com/analyst-ratings/price-target/20/05/16093262/10-biggest-price-target-changes-for-friday"
article = Article(url)
article.download()
article.parse()

print(article.text)
