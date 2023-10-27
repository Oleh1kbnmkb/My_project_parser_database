import requests
from bs4 import BeautifulSoup


def get_vacancies(dish_title: str):
    correct_title = dish_title.replace(' ', '+')
    urls = f'https://smachno.ua/ua?s={correct_title}'

    response = requests.get(urls)
    soup = BeautifulSoup(response.content, 'html.parser')

    all_links = soup.select('.shortcut_row_item')

    result = []

    for link in all_links:
        url = link.select_one('a')['href']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.select_one('h1').text.strip()
        description_element = soup.select_one('.content_post_excerpt')
        if description_element:
            description = description_element.text.strip()
        else:
            description = "Опис відсутній"

        img_divs = soup.find_all('div', class_='thumbnail-wrapper')
        img = [img.find('img')['src'] for img in img_divs]

        dish_obj = {
            'name': name,
            'url': url,
            'description': description,
            'img': img
        }
        result.append(dish_obj)


    return result



# urls = 'https://smachno.ua/ua?s=%D0%BF%D0%B8%D1%80%D1%96%D0%B3'
#
# response = requests.get(urls, headers= {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
# soup = BeautifulSoup(response.content, 'html.parser')
#
# all_links = soup.select('.shortcut_row_item')
#
# for link in all_links:
#   url = link.select_one('a')['href']
#   print(url)

  # result = []

  # for link in all_links:
  #   url = link.select_one('a')['href']
  #   response = requests.get(url)
  #   soup = BeautifulSoup(response.content, 'html.parser')
  #
  #   name = soup.select_one('h1').text.strip()
  #   description_element = soup.select_one('.content_post_excerpt')
  #   if description_element:
  #     description = description_element.text.strip()
  #   else:
  #     description = "Опис відсутній"
  #
  #   img_divs = soup.find_all('div', class_='thumbnail-wrapper')
  #   img = [img.find('img')['src'] for img in img_divs]

  #   dish_obj = {
  #     'name': name,
  #     'url': url,
  #     'description': description,
  #     'img': img
  #   }
  #   result.append(dish_obj)
  #
  # return result

