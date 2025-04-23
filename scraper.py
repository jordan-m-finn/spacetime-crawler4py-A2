import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup # PLEASE INSTALL THIS PACKAGE FOR HTML PARSING
#by running 'pip install beautifulsoup4' in terminal
# must also install the lxml parser by running 'pip install lxml' in terminal
# documentation can be found here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from tokenizer import tokenize, computeWordFrequencies, get_longest_page, get_50_most_common

unique_links = set() #to track URL's that we have already seen
word_count = {} # to store the URL and the word count
all_word_freq = {} # to store word frequency


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    # checking if there was a problem with the page, if there is we do not return anything
    if resp.status != 200: 
        print(f"Error {resp.status} for {url}: {resp.error}")
        return []
    
    print(f"In extract_next_links: {url}")

    hyperlinks = []

    soup = BeautifulSoup(resp.raw_response.content, 'lxml') # parse the content of the page 

    potential_links = soup.find_all('a', href=True) # with the soup, find all the 'a' tags that have a href
    just_links = [a['href'] for a in potential_links] # get the hyperlinks themselves without the tags

    for link in just_links:
        complete_link = urljoin(resp.url, link) # make sure all the links are complete links 

        parsed = urlparse(complete_link) # parse the complete link and remove the fragment if it has one
        if parsed.fragment:
            complete_link = complete_link.split('#')[0]

        if is_valid(complete_link): # making sure it is within the domains and paths specified
            hyperlinks.append(complete_link) # add the complete link to the list we will return
            unique_links.add(complete_link) # add it to the set of unique links (for the deliverable)

    # ALL CODE BELOW THIS LINE IS FOR DELIVERABLE

    text = soup.get_text(separator=' ') # getting all the text from the soup and seperating it so we can use tokenizer
   
    tokens = tokenize(text) 
    word_freq = computeWordFrequencies(tokens)

    word_count[resp.url] = len(tokens) # to get the word count for the page
    
    for word in word_freq: # sum up word frequencies
        if word in word_freq:
            all_word_freq[word] += word_freq[word]
        else:
            all_word_freq[word] = word_freq[word]

    return hyperlinks

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #the domains we are supposed to keep
        domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]
        
        # check if the domain is valid from the list and then in the today.uci.edu case, 
        # make sure it has the path that we want to keep too
        if not (any(parsed.netloc.endswith(domain) for domain in domains) or
            ("today.uci.edu" in parsed.netloc and 
             "/department/information_computer_sciences" in parsed.path)):
            return False

        # check if url is too long
        if len(url) > 2000:
            return False

        # check for crawler traps
        if re.search(r"calendar|/>(year|month|day)=\d+", parsed.path.lower()):
            return False
        
        # check patterns that may indicate a crawler trap
        path_segments = parsed.path.split('/')
        # might need to adjust threshold during testing
        if len(path_segments) > 8:
            return False
        
        # check for any repetitions that may indicate a crawler trap
        if len(set(path_segments)) < len(path_segments) / 2:
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def print_summary(): # what we need for report
    print("SUMMARY: -----------------------------------")
    print(f"Total unique links: {len(unique_links)}")
    print(f"Page with longest word count: {get_longest_page(word_count)}")

    most_common_words = get_50_most_common(all_word_freq)
    for word, freq in most_common_words:
        print(f"{word}: {freq}")