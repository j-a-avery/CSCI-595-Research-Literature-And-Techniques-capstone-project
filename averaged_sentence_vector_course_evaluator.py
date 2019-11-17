import numpy as np
from scipy.spatial.distance import cosine

from embedding_course_evaluator import EmbeddingCourseEvaluator
from course import Course

import logging


class AveragedSentenceVectorCourseEvaluator(EmbeddingCourseEvaluator):
    def _calculate_similarity(self, course1: Course, course2: Course):
        """
        Calculates similarity between two sentences by calculating cosine
        similarity between the averages of their word embedding vectors.

        :param course1: A string representing an unprocessed sentence
        :param course2: A string representing an unprocessed sentence
        :return: score: float: the cosine similarity between the two averaged
                                embedding vectors
        """
        tokens1 = self.preprocess(course1.description)
        tokens2 = self.preprocess(course2.description)

        vector1 = np.array([self._wv[token] for token in tokens1])
        vector2 = np.array([self._wv[token] for token in tokens2])

        course1_mean = vector1.mean(axis=0)
        course2_mean = vector2.mean(axis=0)

        cossim = 1-cosine(course1_mean, course2_mean)

        if vector2.size == 0:
            logging.warning(f"Course: {course2}")
            logging.warning(f"Descr:  >{course2.description}<")
            logging.warning(f"Tokens: {tokens2}")
            logging.warning(f"Vector: {vector2}")
            logging.warning(f"Cossim: {cossim}")

        return cossim
