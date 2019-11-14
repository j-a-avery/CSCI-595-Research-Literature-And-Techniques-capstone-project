import numpy as np
from scipy.spatial.distance import cosine

from embedding_course_evaluator import EmbeddingCourseEvaluator
from course import Course


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

        means1 = vector1.mean(axis=0)
        means2 = vector2.mean(axis=0)

        cossim = cosine(means1, means2)

        return cossim
