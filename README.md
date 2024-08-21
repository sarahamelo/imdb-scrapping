# imdb-scrapping
Using python (beautifulSoup) to web scraping the top 10 movies from IMDB website.

### What is Web Scraping?
Is the process of using computer programming to extract website's data and converting it in information.

### About the little project
What we are doing here is getting the top 10 movies from IMDB website and returning the title, release date, rating and the plot. After that, the program will create a .csv file that will contain the top 10 and their information.
To get there, we need to set a little things first like getting the libraries we are going to need.

``` python
import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup
```

The most important library we are getting is the BeautifulSoup, which is perfect for what we need.
According to the library's document:
> Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves programmers hours or days of work.
<br>
<br>

---

``` python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept-Language': 'pt-BR'}
```

This code defines a dictionary called headers that contains custom HTTP headers. These headers are used when making an HTTP request, usually to a web server, and inform the server about the environment of the client making the request.
sse código define uma função chamada extract_movie_details, que faz uma requisição HTTP para um link de um filme e obtém os detalhes desse filme a partir da resposta do servidor. Vamos analisar cada parte:
<br>
<br>

---

``` python
def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = requests.get(movie_link, headers=headers)
```

This defines the extract_movie_details function, which accepts an argument called movie_link. This argument must be a URL that points to a movie details page.

`time.sleep(random.uniform(0, 0.2))` 
Before making the request, the function pauses (sleep) for a random period between 0 and 0.2 seconds. This is done to avoid sending multiple requests in quick succession, which could be interpreted as automated (possibly malicious) behavior by a web server. It is a common technique in web scraping to avoid being blocked.

`response = requests.get(movie_link, headers=headers)`
The function then makes a GET request to the URL provided in movie_link using the requests library.
It uses the previously defined headers dictionary as the request header. This includes the User-Agent header to simulate a specific browser and Accept-Language to set the language preference.
The request response is stored in the response variable.
<br>
<br>

---

``` python
if response.status_code == 200:
        movie_soup = BeautifulSoup(response.content, 'html.parser')
        title = None
        date = None
        rating = None
        plot = None
```

This code snippet adds logic to process the HTTP response obtained from the request to the movie page. Let's detail what each line does:

`if response.status_code == 200:`
This verifies that the request was successful. HTTP status code 200 indicates that the request was received successfully and the server returned the desired response. If response.status_code equals 200, the code inside this if block will be executed.
movie_soup = BeautifulSoup(response.content, 'html.parser')
If the request is successful, the response content (response.content) is passed to the BeautifulSoup function, which is part of the beautifulsoup4 library.
BeautifulSoup is used to parse (parse) the page's HTML, converting it into a Python object that facilitates navigation and data extraction from the HTML structure.
response.content contains the raw HTML of the web page, and 'html.parser' is the parser that will be used to interpret the HTML.

`title = None`
`date = None`
`rating = None`
`plot = None`
These lines are initializing four variables (title, date, rating, plot) with the value None. They will probably be used to store information extracted from the movie page.
Initializing these variables with None ensures that they have a default value in case data extraction fails or the specific information is not present on the page.
<br>
<br>

---

``` python
        title_tag = movie_soup.find("span", {"class": "hero__primary-text", "data-testid": "hero__primary-text"})
        if title_tag:
            title = title_tag.text.strip()

        date_tag = movie_soup.find_all('a', {'class:', 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})
        if date_tag:
            second_link = date_tag[-2]
            date = second_link.text.strip()

        rating_tag = movie_soup.find("span", {"class": "sc-eb51e184-1 ljxVSS"})
        if rating_tag:
            rating = rating_tag.text.strip()

        plot_tag = movie_soup.find("span", {"role": "presentation", "data-testid": "plot-l", "class": "sc-2d37a7c7-1 dCcJCA"})
        if plot_tag:
            plot = plot_tag.text.strip()
```

This code snippet details how specific data (title, release date, rating, and summary) is extracted from the movie page's HTML using the BeautifulSoup library. Let's understand each part:

![image](https://github.com/user-attachments/assets/0bb2f6db-7374-44f2-82e2-9c61d266c11b)


- ```movie_soup.find("span", {"class": "hero__primary-text", "data-testid": "hero__primary-text"}):```
This code searches the element `span` in the HTML that has the class "hero__primary_text" and the attribute "data-testid" with value "hero__primary-text".
If this element was found, it is stored in the variable _title_tag_
- ```if title_tag:```:
If _title_tag_ is not None (which it means, if the element was found), the code inside the block if will be executed.
- ```title = title_tag.text.strip()```:
The text contained in element _title_tag_ is extracted and any aditional blan space is removed with `strip(). The result is stored in the variable _title_.

The same logic is applied to _date_tag_, _rating_tag_ and _plot_tag_.
<br>
<br>

---

``` python
if all([title, date, rating, plot]):
            print(f'Título: {title}, Data: {date}, Avaliação: {rating}, Resumo: {plot}')
            with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
                movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                movie_writer.writerow([title, date, rating, plot])
        else:
            print(f'Falha ao extrair dados de {movie_link}: {title}, {date}, {rating}, {plot}')
    else:
        print(f'Falha ao acessar {movie_link}: Código de status {response.status_code}')
```
This code snippet adds the final logic to process the data extracted from a movie page and save it to a CSV file. Let's understand each part:

### **Completeness Check**
``` python
if all([title, date, rating, plot]):
all([title, date, rating, plot]):
```
The all() function checks whether all elements in the given list are true (that is, whether all values ​​are other than None or False).
If all the title, date, rating, and plot variables contain valid values ​​(not None), the code block inside this if will be executed.

### **Details Printing**
``` python
print(f'Title: {title}, Date: {date}, Rating: {rating}, Summary: {plot}')
```
This prints to the console the movie details that were extracted and stored in the title, date, rating and plot variables.

### **Save to a CSV File**
``` python
with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
    movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    movie_writer.writerow([title, date, rating, plot])
```
`with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:`:
Opens the movies.csv file in add mode ('a'). This means that the data will be added to the end of the file, without overwriting the existing content.
newline='' and encoding='utf-8' are used to ensure that the file is written correctly with UTF-8 encoding and without adding extra lines between data lines.

`movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL):`
Creates a csv.writer object that will be used to write data to the CSV file. The field delimiter is the comma (,), and strings containing commas or quotation marks will be enclosed in quotation marks (").

`movie_writer.writerow([title, date, rating, plot]):`
Writes a new line to the CSV file with the title, date, rating and plot values ​​as columns.
<br>
<br>

---

``` python
def extract_movies(soup):
    # Verificar se a tabela existe antes de tentar acessar seu conteúdo
    movies_list = soup.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list--base'})
    
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
```
This code defines a function called extract_movies, which extracts movie links from a web page and then uses multiple threads to process those links simultaneously. Let's detail how it works:

### **Check Table Existence**

``` python
movies_list = soup.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list- -base'})
```

`soup.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list--base '})`:
Searches for a `<ul>` element (unordered list) with the specified classes. This element must contain the movie list items.

`if movies_list:`:
Checks whether the `<ul>` element was found. If it is not found, the code inside the if will not be executed.

### **Extract List Items**
 
``` python
movie_items = movies_list.find_all('li')
```
`movies_list.find_all('li')`:
If the list was found, this line searches for all `<li>` items (list items) within the `<ul>` element. Each `<li>` item must represent a movie.

### **Get Movie Links**
``` python
if movie_items:
    movie_links = ['https://imdb.com' + item.find('a')['href'] for item in movie_items if item.find('a')]
    movie_links = movie_links[:10]
```
`if movie_items:`:
Checks that the list of movie items is not empty.

`movie_links = ['https://imdb.com' + item.find('a')['href'] for item in movie_items if item.find('a')]`:
Creates a list of movie links. For each list item (item), find the first <a> link and concatenate it with 'https://imdb.com' to get the full movie URL.

`movie_links = movie_links[:10]`:
Limits the list to a maximum of 10 links, to avoid processing an excessive number of movies at once.

### **Process Links with Multiple Threads**
``` python
if movie_links:
    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)
```
`if movie_links:`:
Checks for movie links to process.

`threads = min(MAX_THREADS, len(movie_links)):`
Determines the number of threads to use, which is the lesser of MAX_THREADS (a predefined value for the maximum number of threads) and the number of available movie links.

`with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:`:
Creates a ThreadPoolExecutor with the number of threads defined in threads.

`executor.map(extract_movie_details, movie_links)`:
Uses the executor's map method to apply the extract_movie_details function to each movie link in movie_links. This allows details from movies to be extracted in parallel.
<br>
<br>

-- 

``` python
def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    response = requests.get(popular_movies_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        extract_movies(soup)
    else:
        print(f'Falha ao recuperar a lista de filmes: Código de status {response.status_code}')

    end_time = time.time()
    print('Tempo total: ', end_time - start_time)
```
The code defines the main function, which is responsible for coordinating the process of extracting movie data from the IMDB page. Let's understand each part:

![image](https://github.com/user-attachments/assets/99c708d7-99bf-4103-8c64-85e3a8fc506a)


### **Record the Start Time**
`start_time = time.time()`
time.time(): Captures the current timestamp in seconds since the epoch (usually January 1, 1970). This value is used to calculate the total execution time of the main function.

### **Define the URL and Make the Request**
``` python
popular_movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
response = requests.get(popular_movies_url, headers=headers)
```
`popular_movies_url`: Defines the URL that contains the list of the most popular films on IMDB.

`requests.get(popular_movies_url, headers=headers)`: Makes a GET request for the defined URL, using the specified headers to simulate a browser and avoid problems with blocking.

### **Check Request Status**
``` python
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_movies(soup)
else:
    print(f'Failed to retrieve movie list: Status code {response.status_code}')
``` 
`if response.status_code == 200:`: Checks whether the request was successful. If the status code is 200, the response content is parsed.

`soup = BeautifulSoup(response.content, 'html.parser')`: Creates a BeautifulSoup object to parse the HTML of the received page.

`extract_movies(soup)`: Calls the extract_movies function, passing the BeautifulSoup object to extract the movie links and process them.

`else:`: If the request fails (status code other than 200), an error message is printed with the returned status code.

### **Record and Print Execution Time**
``` python
end_time = time.time()
print('Total time: ', end_time - start_time)
``` 
`end_time = time.time()`: Captures the current timestamp after code execution.

`print('Total time: ', end_time - start_time)`: Calculates the total execution time of the main function by subtracting the start time (start_time) from the end time (end_time). Prints the total execution time in seconds.
<br>
<br>
<br>


## Conclusion
We can reformulate the program to get more information or more movies. What about the top 100 movies next time? We can do that.
The code is in this repository if you want to enjoy it, change something or even use it for anything.
This little project was made for my course: BackEnd Developer with Python (By: EBAC)
<br>
<br>
Last modified on: 21.08.2024

By: @sarahamelo
