from course import Course
from averaged_sentence_vector_course_evaluator import AveragedSentenceVectorCourseEvaluator
from transformer_course_evaluator import TransformerCourseEvaluator
from wordnet_course_evaluator import WordNetCourseEvaluator
from wordwise_embedding_course_evaluator import WordwiseEmbeddingCourseEvaluator

import pickle
import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("Loading TAMUC catalog")
tamuc_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/tamuc.catalog", "rb"))
    if course["description"] != ""  # there's some bad data in the scrape; ignore it.
]
logging.debug(f"Found {len(tamuc_catalog)} courses.")


logging.debug("Loading DCCCD catalog")
dcccd_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/dcccd.catalog", "rb"))
]
logging.debug(f"Found {len(dcccd_catalog)} courses")

logging.debug("Loading UTD catalog")
utd_catalog = [
    Course.from_dict(course)
    for course
    in pickle.load(open("./data/utd.catalog", "rb"))
]
logging.debug(f"Found {len(utd_catalog)} courses")

MODELS = [
    ("Averaged Sentence Vectors using Word2Vec Embeddings",
     AveragedSentenceVectorCourseEvaluator, "data/wikipedia.w2v.kv"),
    # ("Averaged Sentence Vectors using FastText Embeddings",
    #  AveragedSentenceVectorCourseEvaluator, "data/wikipedia.ft.kv"),
    # ("Word-wise Vector Comparisons using Word2Vec Embeddings",
    #  WordwiseEmbeddingCourseEvaluator, "data/wikipedia.w2v.kv"),
    # ("Word-wise Vector Comparisons using FastText Embeddings",
    #  WordwiseEmbeddingCourseEvaluator, "data/wikipedia.ft.kv"),
    ("Transformer Sentence Vectors using BERT (CUDA)", TransformerCourseEvaluator, 'cuda'),
    # ("Transformer Sentence Vectors using BERT (CPU)", TransformerCourseEvaluator, 'cpu'),
    # ("Wu-Palmer WordNet Similarity", WordNetCourseEvaluator, None),
]

course_to_eval_for_now = dcccd_catalog[1374]
print(f"Evaluating {course_to_eval_for_now}")
print(course_to_eval_for_now.description)

for title, mdl_type, param in MODELS:
    print(f"Evaluating using {title}")
    logging.info(f"Evaluating using {title}")
    model = mdl_type(param)
    matches = model.find_matches(course_to_eval_for_now, utd_catalog)
    logging.info(f"Best UTD match: {matches[0]}")
    matches = model.find_matches(course_to_eval_for_now, tamuc_catalog)
    logging.info(f"Best TAMUC match: {matches[0]}")
    del model
