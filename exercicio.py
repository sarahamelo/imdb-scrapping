import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

# Headers globais para serem usados nas requisições
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept-Language': 'pt-BR'}

MAX_THREADS = 10

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = requests.get(movie_link, headers=headers)
    
    if response.status_code == 200:
        movie_soup = BeautifulSoup(response.content, 'html.parser')
        title = None
        date = None
        rating = None
        plot = None

        # Extrair título
        title_tag = movie_soup.find("span", {"class": "hero__primary-text", "data-testid": "hero__primary-text"})
        if title_tag:
            title = title_tag.text.strip()

        # Extrair data de lançamento
        date_tag = movie_soup.find_all('a', {'class:', 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})
        if date_tag:
            second_link = date_tag[-2]
            date = second_link.text.strip()

        #date_tag = movie_soup.find_all('a', {'href:', '/title/tt0111161/releaseinfo?ref_=tt_ov_rdat'})
        #if date_tag:
        #   date = date_tag.text.strip()

        # Extrair avaliação
        rating_tag = movie_soup.find("span", {"class": "sc-d541859f-1 imUuxf"})
        if rating_tag:
            rating = rating_tag.text.strip()

        # Extrair resumo
        plot_tag = movie_soup.find("span", {"role": "presentation", "data-testid": "plot-l", "class": "sc-3ac15c8d-1 gkeSEi"})
        if plot_tag:
            plot = plot_tag.text.strip()

        if all([title, date, rating, plot]):
            print(f'Título: {title}, Data: {date}, Avaliação: {rating}, Resumo: {plot}')
            with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                movie_writer.writerow([title, date, rating, plot])
        else:
            print(f'Falha ao extrair dados de {movie_link}: {title}, {date}, {rating}, {plot}')
    else:
        print(f'Falha ao acessar {movie_link}: Código de status {response.status_code}')



def extract_movies(soup):
    # Verificar se a tabela existe antes de tentar acessar seu conteúdo
    movies_list = soup.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base', "role":'presentation'})
    
    if movies_list:
        movie_items = movies_list.find_all('li')

        if movie_items:
            movie_links = ['https://imdb.com' + item.find('a')['href'] for item in movie_items if item.find('a')]
            movie_links = movie_links[:10]
            if movie_links:
                threads = min(MAX_THREADS, len(movie_links))
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    executor.map(extract_movie_details, movie_links)
        else:
            print("Lista encontrada, mas não possui 'li'.")
    else:
        print("Lista de filmes não encontrada no HTML.")

def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/top/'
    response = requests.get(popular_movies_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        extract_movies(soup)
    else:
        print(f'Falha ao recuperar a lista de filmes: Código de status {response.status_code}')

    end_time = time.time()
    print('Tempo total: ', end_time - start_time)

if __name__ == '__main__':
    main()
