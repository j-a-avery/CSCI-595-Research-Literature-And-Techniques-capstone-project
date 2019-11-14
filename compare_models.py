from course import Course
from averaged_sentence_vector_course_evaluator import AveragedSentenceVectorCourseEvaluator
from transformer_course_evaluator import TransformerCourseEvaluator
from wordnet_course_evaluator import WordNetCourseEvaluator
from wordwise_embedding_course_evaluator import WordwiseEmbeddingCourseEvaluator

import pickle

tamuc_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/tamuc.catalog", "rb"))
]

dcccd_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/dcccd.catalog", "rb"))
]

utd_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/utd.catalog", "rb"))
]

MODELS = [
    ("Averaged Sentence Vectors using Word2Vec Embeddings",
     AveragedSentenceVectorCourseEvaluator, "data/wikipedia.w2v.kv"),
    ("Averaged Sentence Vectors using FastText Embeddings",
     AveragedSentenceVectorCourseEvaluator, "data/wikipedia.ft.kv"),
    ("Word-wise Vector Comparisons using Word2Vec Embeddings",
     WordwiseEmbeddingCourseEvaluator, "data/wikipedia.w2v.kv"),
    ("Word-wise Vector Comparisons using FastText Embeddings",
     WordwiseEmbeddingCourseEvaluator, "data/wikipedia.ft.kv"),
    ("Transformer Sentence Vectors using BERT", TransformerCourseEvaluator, None),
    ("Wu-Palmer WordNet Similarity", WordNetCourseEvaluator, None),
]

for title, mdl_type, param in MODELS:
    print("Evaluating using", title)
    model = mdl_type(param)
    matches = model.find_matches(dcccd_catalog[1374], utd_catalog)
    print(matches[0])
    matches = model.find_matches(dcccd_catalog[1374], tamuc_catalog)
    print(matches[0])
    del model
