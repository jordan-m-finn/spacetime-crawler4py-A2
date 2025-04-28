
# imported my functions from assignment 1 - Rachael Le
def tokenize(text_string):
    token_list = []
    token = []

    alphanum = set("abcdefghijklmnopqrstuvwxyz0123456789")

    for char in text_string:
        if char.lower() in alphanum: # specify we only want english alphabet and numbers in tokens
            token.append(char.lower())
        else:
            if token: # if not alphanumeric, see if the token is empty, if not empty add the token to the collection
                token_string = ''.join(token)
                token_list.append(token_string)
                token = []

    if token: # if the last character is alphanumeric, catch the token
        token_string = ''.join(token)
        token_list.append(token_string)

    return token_list

def computeWordFrequencies(token_list): 
    word_freq={}

    for token in token_list: 
        if token not in word_freq: # if not in the dict add it with a count of one
            word_freq[token]=1
        else:
            word_freq[token]+=1 #if in dict, increment everytime you see the same token
    
    return word_freq

def get_longest_page(word_count): 
    if not word_count:
        return "N/A (no pages with words)"
    longest_page = max(word_count, key=word_count.get)
    return longest_page, word_count[longest_page]

    #longest_page = max(word_count, key=word_count.get) # get the page with the most words
    #return longest_page, word_count[longest_page] # return the page and the number of words in it

def get_50_most_common(all_word_freq): 

    # english stop words we want to exclude
    stop_words = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "t", "s"
    }

    clean_word_freq = {}

    for word in all_word_freq: # removing the stop words
        if word not in stop_words:
            clean_word_freq[word] = all_word_freq[word]

    sorted_word_freq = sorted(clean_word_freq.items(), key=lambda item: item[1], reverse=True) 
    most_common = sorted_word_freq[:50]

    return most_common

