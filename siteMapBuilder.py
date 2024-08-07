from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests,time,os

def url():
    time.sleep(1)
    global url 
    url = input('Write your website domain: ').strip()  
    try:
        global response
        checking = url[-1]
        if checking == '/' :
            pass
        else:
            url = url + '/'
        response = requests.get(url)
        start_crawling()
    except requests.exceptions.RequestException as e:
        print('please write a valid url , try again : this error has occured',e)
        url()




def start_crawling():
    os.system('cls')
    print('crawling web pages')
    time.sleep(3)
    global checked_links
    checked_links=[]
    checked_links.append(url)
    crawling_web_pages()





def crawling_web_pages():
    global responses 
    control = 0
    while control < len(checked_links):
        try:
            responses = requests.get(checked_links[control])
            responses.raise_for_status()
            source_code = responses.text
            soup = BeautifulSoup(source_code, 'html.parser')
            new_links = [w['href'] for w in soup.findAll('a', href=True)]
            
            counter = 0
            while counter < len(new_links):
                link = new_links[counter]
                if link: 
                    if 'http' not in link: # an absolute link
                        if link[0] == '/':
                            link = link[1:]  # Remove leading '/' cuz we already added it 
                        link = url + link 
                new_links[counter] = link
                counter += 1

            counter2 = 0
            while counter2 < len(new_links):
                link = new_links[counter2]
                if ('.jpg' not in link and '.png' not in link and 'mailto' not in link and 
                    link not in checked_links and url in link):
                    checked_links.append(link)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f'{control}/{len(checked_links)}')
                    print(f'{control} web pages crawled and {len(checked_links)} found')
                    print(link)
                counter2 += 1

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{control}/{len(checked_links)}')
            print(f'{control} web pages crawled and {len(checked_links)} found')
            print(checked_links[control]) 

            control += 1
        except requests.exceptions.RequestException as e:
            print(f'Error fetching {checked_links[control]}: {e}')
            control += 1  

    time.sleep(1)
    creating_site_map()

    
        

                     

def creating_site_map():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Creating sitemap...')
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for link in checked_links:
        url_element = ET.SubElement(urlset, 'url')
        ET.SubElement(url_element, 'loc').text = str(link)
    
    tree = ET.ElementTree(urlset)
    tree.write('sitemap.xml')
    print('Your sitemap is ready')
    time.sleep(2)

     

                 
url()