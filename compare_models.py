# TODO: Move this to a Jupyter notebook

from course import Course
from averaged_sentence_vector_course_evaluator import AveragedSentenceVectorCourseEvaluator
from transformer_course_evaluator import TransformerCourseEvaluator
from wordnet_course_evaluator import WordNetCourseEvaluator
from wordwise_embedding_course_evaluator import WordwiseEmbeddingCourseEvaluator

import pickle
import logging
# logging.basicConfig(level=logging.DEBUG)
import datetime

import pandas as pd


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

# TODO: Add all trained models for vectorized evaluators.
#   I did this already for wordwise comparison,
#   but it might help accuracy for the averaged vector evaluator
# TODO: Fix transformer class
# TODO: Make title and short title static members of the Evaluator classes
MODELS = [
    ("Averaged Sentence Vectors using Word2Vec Embeddings", "asv_w2v",
     AveragedSentenceVectorCourseEvaluator, "data/wikipedia.w2v.kv"),
    ("Averaged Sentence Vectors using FastText Embeddings", "asv_ft",
     AveragedSentenceVectorCourseEvaluator, "data/wikipedia.ft.kv"),
    ("Word-wise Vector Comparisons using Word2Vec Embeddings", "wwc_w2v",
     WordwiseEmbeddingCourseEvaluator, "data/wikipedia.w2v.kv"),
    ("Word-wise Vector Comparisons using FastText Embeddings", "wwc_ft",
     WordwiseEmbeddingCourseEvaluator, "data/wikipedia.ft.kv"),
    # ("Transformer Sentence Vectors using BERT (CUDA)", "bert_cuda", TransformerCourseEvaluator, 'cuda'),
    # ("Transformer Sentence Vectors using BERT (CPU)", "bert_cpu", TransformerCourseEvaluator, 'cpu'),
    ("Wu-Palmer WordNet Similarity", "wn_wup", WordNetCourseEvaluator, None),
]

samples = [
    Course("CSCI", "152", "TAMUC Programming Fundamentals II", "Review of control structures and data types with emphasis on structured data types. Applies the object-oriented programming paradigm, focusing on the definition and use of classes along with the fundamentals of object-oriented design. Includes basic analysis of algorithms, searching and sorting techniques, and an introduction to software engineering."),
    Course("CS", "1337", "UTD Computer Science I", "Review of control structures and data types with emphasis on structured data types. Applies the object-oriented programming paradigm, focusing on the definition and use of classes along with the fundamentals of object-oriented design. Includes basic analysis of algorithms, searching and sorting techniques, and an introduction to software engineering. Programming language of choice is C/C++. Students will also be registered for an exam section."),
    Course("CS", "2336", "UTD Computer Science II", "Further applications of programming techniques, introducing the fundamental concepts of data structures and algorithms. Topics include recursion, fundamental data structures (including stacks, queues, linked lists, hash tables, trees, and graphs), and algorithmic analysis. Includes comprehensive programming projects. Programming language of choice is Java. Credit cannot be received for both CS 2337 and (CS 2336 or CE 2336 or TE 2336)."),
    Course("MATH", "192", "TAMUC Calculus II", "This course examines integral calculus of functions of one variable, and some integral calculus of functions of two variables, as follows. Topics include techniques of integration; applications of the integral; improper integrals; limits involving indeterminate forms; sequences and series; some exposure to multiple integrals; and use of computer technology. Prerequisite: MATH 2413."),
    Course("MUS", "127", "TAMUC Ear Training II", 'A course designed to enable students to sight-sing and take dictation in complex rhythms and melodies. Prerequisite: Music 117 with a grade of "C" or better.'),
    Course("ACCT", "222", "TAMUC Principles of Accounting II", "A study of the role of management accounting and control in business firms with an emphasis on organizational activities that create value for customers. Topics include activity based costing, cost behavior, cost allocation, pricing and product mix decisions, capital budgeting, compensation, benchmarking and continuous improvement, and behavioral and organizational issues. Prerequisite: ACCT 221 or Acct 2301."),
    Course("BSC", "254", "TAMUC General Microbiology", "Four semester hours (3 lecture, 3 lab). (1) Study of microbiology emphasizing fundamental principles and applications (not interchangeable with BSC 306)."),
    Course("CSCI", "126", "TAMUC Intro to Computing", "An introduction to computers, network communications, and information systems. This course provides the student with knowledge about hardware, software and data management systems. The student is provided experience with an operating system environment, application software including productivity tools, and the use of the internet to communicate and search for information. This course will not count toward a major or minor in computer science or computer information systems."),
    Course("CSCI", "131", "TAMUC Visual Basic Programming", "This course is designed to provide the student with introductory computer programming skills using an object-oriented computer language. Topics to be covered are algorithms and problem-solving, fundamental programming constructs such as sequence, selection, iteration, and functions, object-oriented interface and program design, and event-driven computer programming with an emphasis on business applications. Prerequisite: MIS 128, MATH 1314 or 1324. This course will not count toward a major or minor in computer science or computer information systems."),
    Course("CSCI", "241", "TAMUC Machine Language and Organization", "Basic computer organization; machine cycle, digital representation of data and instructions; assembly language programming, assembler, loader, macros, subroutines, and program linkages. Prerequisite: CSCI 151."),
]

expected = [
    "COSC-1437", "COSC-1437", "COSC-2436", "MATH-2414", "MUSI-1117",
    "ACCT-2302", "BIOL-2420", "COSC-1301", None, "COSC-2425"
]

catalog = [Course.from_dict(course)
           for course
           in pickle.load(open("data/dcccd.catalog", "rb"))]

results = {}

# TODO: For ease of analysis, DataFrame should be:
#   index (auto-generated)
#   method short title
#   comparision Course id, title, description
#   best match Course id, title, description
for title, fn, mdl_type, param in MODELS:
    print(f"Evaluating using {title}")
    model = mdl_type(param)

    results[title] = pd.DataFrame(columns=["Course", "Time", "Results"])

    for course in samples:
        start = datetime.datetime.now()
        matches = model.find_matches(course, catalog, min_match=0.9, max_results=10)
        end = datetime.datetime.now()

        duration = (end - start).total_seconds()
        print(f"{course}, {duration}s")

        results[title] = results[title].append({
            "Course": course,
            "Time": duration,
            "Results": matches
        }, ignore_index=True)

    # fn = title.split(' ').join()
    results[title].to_csv(f"data/{fn}.csv")
    print(f"Saved results as data/{fn}.csv\n\n")

    del model  # hurry up and free some memory
