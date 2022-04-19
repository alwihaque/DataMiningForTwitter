#  THIS  CODE  IS  MY  OWN  WORK,  IT  WAS  WRITTEN
# WITHOUT CONSULTING CODE WRITTEN BY OTHER STUDENTS. Alwi Haque
import pandas as pd
import re
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
    return text


def prune_sub_sets(candidate_list, keys_to_remove):
    subsets = []
    for item in candidate_list:
        for key in keys_to_remove:
            is_sub_set = set(key).issubset(item)
            if is_sub_set:
                subsets.append(item)
    for subset in subsets:
        if subset in candidate_list:
            del candidate_list[subset]
    return candidate_list


def create_candidate_items(k, item_sets):
    first_item_set = list(item_sets[0].keys())
    candidate_item_set = {}
    if k == 1:
        for i in range(len(first_item_set)):
            for j in range(len(first_item_set)):
                if first_item_set[i][0] is not first_item_set[j][0]:
                    candidate_as_array = [first_item_set[i][0], first_item_set[j][0]]
                    candidate = tuple(candidate_as_array)
                    candidate_item_set[candidate] = 0
        # Remove same combination
        # res = {tuple(sorted(x)): y for x, y in candidate_item_set.items()}
        candidate_item_set = {tuple(sorted(x)): y for x, y in candidate_item_set.items()}
        return candidate_item_set
    else:
        freq_item_set = list(item_sets[len(item_sets) - 1].keys())
        for i in range(len(freq_item_set)):
            for j in range(len(first_item_set)):
                candidate_as_array = list(freq_item_set[i])
                if first_item_set[j][0] not in candidate_as_array:
                    candidate_as_array.append(first_item_set[j][0])
                    candidate = tuple(candidate_as_array)
                    candidate_item_set[candidate] = 0
        candidate_item_set = {tuple(sorted(x)): y for x, y in candidate_item_set.items()}
        return candidate_item_set


def apriori_algorithm(input_file, min_sup_count, output_filename, date):
    data = pd.read_csv(input_file)
    data = data[data["date"] == date]
    keywords = data.body.tolist()
    item_set = {}
    k = 1
    frequency_list = []
    for keyword in keywords:
        # remove emojis from keyword
        give_emoji_free_text(keyword)
        each_keyword = keyword.split(' ')
        for word in each_keyword:
            word_array = [word]
            if tuple(word_array) in item_set:
                item_set[tuple(word_array)] = item_set.get(tuple(word_array)) + 1
            else:
                item_set[tuple(word_array)] = 1
    keys_to_remove = []
    for item in item_set:
        if item_set[item] < min_sup_count:
            keys_to_remove.append(item)
    for key in keys_to_remove:
        del item_set[key]
    frequency_list.append(item_set)
    while True:
        candidate_list = create_candidate_items(k, frequency_list)
        candidate_list = prune_sub_sets(candidate_list, keys_to_remove)
        for item in candidate_list:
            for word in keywords:
                item_as_array = list(item)
                word_array = word.split(';')
                if all(it in word_array for it in item_as_array):
                    candidate_list[item] = candidate_list.get(item) + 1
        for item in candidate_list:
            if candidate_list[item] < min_sup_count:
                keys_to_remove.append(item)
        for key in keys_to_remove:
            if key in candidate_list:
                del candidate_list[key]
        if len(candidate_list) == 0:
            break
        frequency_list.append(candidate_list)
        k = k + 1
    final_list = []
    for candidate in frequency_list:
        for value in candidate:
            value = [value, candidate[value]]
            final_list.append(value)
    final_list = sorted(final_list, key=lambda x: x[1], reverse=True)

    with open(output_filename, 'w') as f:
        for value in final_list:
            for word in value[0]:
                f.write(word)
                f.write(" ")
            f.write("(")
            f.write(str(value[1]))
            f.write(")")
            f.write("\n")



# apriori_algorithm("tweets.csv", 200, "output.txt")
