from newspaper import Article

def scrape_article_text(url):
    """
    Mengunjungi URL, men-download, dan mengambil teks utama artikel.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        # Mengembalikan (teks isi, judul)
        return article.text, article.title
    except Exception as e:
        print(f"Gagal scrape URL: {url} | Error: {e}")
        return None, None