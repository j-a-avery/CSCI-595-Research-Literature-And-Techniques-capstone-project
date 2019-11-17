import numpy as np

from course import Course
from embedding_course_evaluator import EmbeddingCourseEvaluator


class WordwiseEmbeddingCourseEvaluator(EmbeddingCourseEvaluator):
    def _calculate_similarity(self, course1: Course, course2: Course):
        """
        Calculates similarity between two sentences by using cosine similarity
        to perform pairwise matching of words.
        The score is the average best match between vectors

        :param course1: A string representing an unprocessed sentence
        :param course2: A string representing an unprocessed sentence
        :return: score: float: the average pairwise cosine similarity between
                               the words in sentence1 and sentence2
        """

        tokens1 = self.preprocess(course1.description)
        tokens2 = self.preprocess(course2.description)

        grid = np.array([[self._wv.similarity(w, v)
                          for w in tokens1]
                         for v in tokens2])

        # The similarity is
        score = grid.max(axis=0).mean()

        return score
