from gensim.models import KeyedVectors
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
import matplotlib.pyplot as plt
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ruwikiruscorpora_upos_skipgram_300_2_2018.vec')  # Путь к скачанной модели word2vec

# Наборы слов
word_sets = {
    'set1': [
        # музыкальные инструменты
        'гитара', 'скрипка', 'фортепиано', 'барабан', 'труба', 'арфа', 'виолончель', 'тромбон', 'кларнет', 'саксофон',
        # напитки
        'кофе', 'чай', 'сок', 'квас', 'лимонад', 'компот', 'морс', 'эспрессо', 'вода', 'кисель',
        # города
        'москва', 'париж', 'лондон', 'берлин', 'рим', 'мадрид', 'вена', 'прага', 'стокгольм', 'афины'
    ],
    'set2': [
        # профессии
        'врач', 'инженер', 'учитель', 'художник', 'программист', 'архитектор', 'водитель', 'библиотекарь', 'повар', 'фермер',
        # эмоции
        'радость', 'грусть', 'страх', 'удивление', 'злость', 'счастье', 'зависть', 'тоска', 'восторг', 'уныние',
        # явления природы
        'дождь', 'снег', 'ветер', 'гроза', 'туман', 'иней', 'град', 'засуха', 'ураган', 'радуга'
    ],
    'set3': [
        # растения
        'дуб', 'берёза', 'клён', 'сосна', 'ель', 'липа', 'тополь', 'осина', 'рябина', 'каштан',
        # спорт
        'футбол', 'хоккей', 'теннис', 'баскетбол', 'волейбол', 'гандбол', 'бокс', 'регби', 'плавание', 'шахматы',
        # наука
        'физика', 'химия', 'биология', 'математика', 'астрономия', 'геология', 'лингвистика', 'информатика', 'философия', 'психология'
    ]
}
# Для каждого набора кластеров должно быть 3
N_CLUSTERS = 3


def load_model(path):
    model = KeyedVectors.load_word2vec_format(path, binary=False)
    return model

def get_vectors(model, words):
    vectors = []
    valid_words = []
    for w in words:
        w_model = w.lower() + '_NOUN'
        vectors.append(model[w_model])
        valid_words.append(w)

    return np.array(vectors), valid_words

def cluster_and_plot(vectors, words, method='kmeans', n_clusters=3, set_name='set', file=None):
    if method == 'kmeans':
        clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    else:
        clusterer = AgglomerativeClustering(n_clusters=n_clusters, metric='cosine', linkage='average')
    labels = clusterer.fit_predict(vectors)
    msg = f"Результаты кластеризации методом {method}:"
    print(msg)
    if file:
        print(msg, file=file)
    for i in range(n_clusters):
        cluster_words = [words[j] for j in range(len(words)) if labels[j] == i]
        msg = f"Кластер {i+1}: {cluster_words}"
        print(msg)
        if file:
            print(msg, file=file)
    # Визуализация через PCA
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(vectors)
    plt.figure(figsize=(8,6))
    for i in range(n_clusters):
        idx = labels == i
        plt.scatter(reduced[idx,0], reduced[idx,1], label=f'Cluster {i+1}')
    for i, word in enumerate(words):
        plt.text(reduced[i,0], reduced[i,1], word, fontsize=9)
    plt.title(f'Кластеризация набора "{set_name}" методом {method}')
    plt.legend()
    plt.tight_layout()
    plt.show()


model = load_model(MODEL_PATH)
with open('results.txt', 'w', encoding='utf-8') as file:
    for set_name, words in word_sets.items():
        msg = f"\n--- Кластеризация набора: {set_name} ---"
        print(msg)
        print(msg, file=file)
        vectors, valid_words = get_vectors(model, words)

        for method in ['kmeans', 'agglomerative']:
            cluster_and_plot(vectors, valid_words, method=method, n_clusters=N_CLUSTERS, set_name=set_name, file=file)
