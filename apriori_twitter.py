import pandas as pd
import re
from dateutil.rrule import rrule, MONTHLY, DAILY
from datetime import datetime
# from cleantext import clean
# import emoji

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def give_emoji_free_text(text):
    #Lower case text, remove urls, remove punctuation
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub("[^a-z0-9@#]"," ", text)
    text = re.sub('\s+(a|an|and|the|s|t)(\s+)', '\2', text)
    return text

def apriori_algorithm(input_file, threshold, output_filename, date):
    data = pd.read_csv(input_file)
    data = data[data["date"] == date]
    data["body"] = data['body'].apply(lambda x: give_emoji_free_text(x))
    # print(data['body'])
    data["keywords"] = data["body"].str.split(" ", -1, False)
    # print(data["keywords"])
    # print(keywords)
    frequency = {}
    superset = []

    # Get initial k=1 frequency set (need to iterate over every word in every row)
    for index, row in data['keywords'].iteritems():
        # print(tweet)
        superset.append(frozenset(row))
        for item in row:
            if item == " " or item =="":
                continue
            item = frozenset([item])
            if item in frequency:
                frequency[item] = frequency[item] + 1
            else:
                frequency[item] = 1

    # Create dictionaries of frequent and not frequent items
    not_frequent = {key: val for key, val in frequency.items() if val < threshold}
    frequency = {key: val for key, val in frequency.items() if val >= threshold}
    out_put = {key: val for key, val in frequency.items()}

    frequency_k = frequency.copy()

    k = 2
    while len(frequency_k.keys()) > 0:
        # print(k)
        candidate = []
        # Generate candidates, ignoring duplicates
        for index, key in enumerate(frequency):
            for i, l in enumerate(frequency_k):
                if key.union(l) not in candidate:
                    candidate.append(key.union(l))

        # Prune candidates for subsets and make sure they are the correct length
        candidate = [x for x in candidate if x not in not_frequent and len(x) == k]
        frequency_k = {}
        for item in candidate:
            frequency_k[item] = 0
            for i in superset:
                if item.issubset(i):
                    frequency_k[item] = frequency_k[item] + 1
        # Not frequent and frequent k candidates
        not_frequent = {key: val for key, val in frequency_k.items() if val < threshold}
        frequency_k = {key: val for key, val in frequency_k.items() if val >= threshold}
        for index, key in enumerate(frequency_k):
            out_put[key] = frequency_k[key]
        k = k + 1

    with open(output_filename, 'w') as f:
        ordered_freq = sorted(out_put, key=out_put.get, reverse=True)
        st = ""
        for k in ordered_freq:
            st += " ".join(k) + " (" + str(out_put[k]) + ")\n"
        f.write(st)

# apriori_algorithm("tweets.csv", 200, "output.txt", date)
if __name__ == '__main__':
    #DEC 2, 25, 29, 30
    ignore = [datetime(2021,12,2), datetime(2021,12,7), datetime(2021,12,20), datetime(2021,12,29), datetime(2021,12,30), datetime(2022,1,13), datetime(2022,1,15), datetime(2022,1,22)]
    #date format in 2021-12-10 in csv
    start_date = datetime(2021, 12, 1)
    end_date = datetime(2022, 1, 31)
    # apriori_algorithm("tweets.csv", 10000, "all_data_apriori.csv", 0)
    for dt in rrule(freq=DAILY,dtstart=start_date, until=end_date):
        if dt in ignore:
            continue
        date = dt.strftime("%Y-%m-%d")
        print(date)
        apriori_algorithm("tweets.csv", 65, "apriori/apr_"+date+".csv", date)

