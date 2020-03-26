#plsa_model.py
import sys
import math, tqdm
import numpy as np
from random import seed, random

class PLSA():
    def __init__(self, collection):
        self.collection = collection
        self.plsa_function()

    def plsa_function(self, num_of_topics=5):
        seed(1)
        self.prob_lambda = random()
        print(self.prob_lambda)
        self.build_vocabulary()
        doc_count = self.document_count()
        self.build_topics(num_of_topics, doc_count)
        self.vocab_size = len(self.vocabulary)

        plsa_result = []
        for i, document in enumerate(self.documents):
            log_result = []
            for j in range(len(document)):
                word = document[j]
                self.p_wd = self.p_w_D(word, document)

                product = []
                for topic_n in range(num_of_topics):
                    self.p_kC = self.p_k_C(word, topic_n)
                    self.p_wT = self.p_w_T(word, topic_n)

                    product.append(self.p_kC * self.p_wT)
                self.k = sum(product)

                log_result.append(self.log_likelihood(self.p_wd, self.k))
            plsa_result.append(sum(log_result))
        plsa_final = sum(plsa_result)

        print("PLSA FINAL: ", plsa_final)

    ############# EM Steps #############
    def e_step(self):
        self.n_dk = (self.p_kC * self.p_wT) / self.k
        self.n_wk = (self.prob_lambda * self.p_wd)/ (self.prob_lambda * self.p_wd * self.k)

    def m_step(self):
        for j in self.vocab_size:
            sum(self.n_dk * (1-self.n_wk))

        for i in n:
            denomenator = sum(numerators)
        total = numerator/denomenator

    ############# Likelihood #############

    def log_likelihood(self, p_wd, k):
        total = self.prob_lambda * p_wd + (1-self.prob_lambda)*k
        log_result = math.log(total)

        return log_result

    def rel_log_likelihood(self):
        pass

    ############# Probability #############
    def p_w_D(self, word, doc):
        word_count = 0
        for w in doc:
            if w == word:
                word_count+=1
        p_wd = word_count/len(doc)
        return p_wd

    def p_k_C(self, word, topic_n):
        word_count = 0
        for w in self.vocabulary:
            if w == word:
                word_count+=1
        p_kC = word_count/len(self.vocabulary)
        return p_kC

    def p_w_T(self, word, topic_n):
        word_count = 0
        topic_size = 0
        for i in range(len(self.topics[topic_n])):
            document = self.topics[topic_n][i].split()
            topic_size += len(document)
            for j in range(len(document)):
                if document[j] == word:
                    word_count+=1
        p_wT = word_count/topic_size
        return p_wT

    ############# Preprocessing #############
    def build_topics(self, num_of_topics, doc_count):
        self.topics = {}
        topic_list = []
        doc_per_topic = int(doc_count / num_of_topics)

        t_num = 0
        for d_num in range(doc_count):
            if d_num/(t_num+1) == doc_per_topic-1:
                topic_list.append(self.documents[d_num])
                self.topics[t_num] = topic_list
                t_num+=1
            else:
                topic_list.append(self.documents[d_num])

    def build_vocabulary(self):
        self.vocabulary = []
        for sent in self.collection:
            self.vocabulary.append(sent.split())

    def document_count(self):
        self.documents = []
        for doc in self.collection:
            self.documents.append(doc)
        return len(self.documents)

if __name__ == "__main__":
    filename = sys.argv[1]
    collection = open(filename, 'r').readlines()
    PLSA(collection)
