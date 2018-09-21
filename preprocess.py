from bs4 import BeautifulSoup
from topics import topic_num_map
import os


def get_article_text(article):
    """
    Get a string containing the title and body of a Reuters article object
    :param article: A Reuters article object
    :return: String containing the article title and body
    """
    title = body = ""
    if article.title is not None:
        title = ' '.join(article.title.text.split()) + ". "
    if article.body is not None:
        body = ' '.join(article.body.text.split())
    return title + body


def get_article_label(topics):
    """
    Get a 90-digit binary one-hot encoded label corresponding to the given topic list
    :param topics: Set of topics to which an article belongs
    :return: 90-digit binary one-hot encoded label
    """
    category_label = [0 for x in range(90)]
    for topic in topics:
        if topic.text in topic_num_map:
            category_label[topic_num_map[topic.text]] = 1
    if sum(category_label) > 0:
        return ''.join(map(str, category_label))
    else:
        return None


def parse_documents():
    """
    Extract the Reuters-90 dataset from the SGM files in data folder according to the ApteMod splits. This method
    returns the documents that belong to at least one of the categories that have at least one document in both the
    training and the test sets. The dataset has 90 categories with a training set of 7769 documents and a test set of
    3019 documents.
    :return: Two lists containing the train and test splits along with the labels
    """
    train_documents = list()
    test_documents = list()
    for file in os.listdir('data'):
        data = open(os.path.join(os.getcwd(), "data", file), 'r')
        text = data.read()
        data.close()
        tree = BeautifulSoup(text, "html.parser")
        for article in tree.find_all("reuters"):
            if article.attrs['topics'] == "YES":
                label = get_article_label(article.topics.children)
                if label is not None:
                    if article.attrs['lewissplit'] == "TRAIN":
                        train_documents.append((label, get_article_text(article)))
                    elif article.attrs['lewissplit'] == "TEST":
                        test_documents.append((label, get_article_text(article)))
    return train_documents, test_documents


if __name__ == "__main__":
    train_documents, test_documents = parse_documents()
    print("Train, test dataset sizes:", len(train_documents), len(test_documents))
    with open("reuters_train.tsv", 'w') as tsv_file:
        for label, document in train_documents:
            tsv_file.write(label + "\t" + document + "\n")
    with open("reuters_test.tsv", 'w') as tsv_file:
        for label, document in test_documents:
            tsv_file.write(label + "\t" + document + "\n")