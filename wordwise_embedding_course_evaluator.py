import numpy as np

from embedding_course_evaluator import EmbeddingCourseEvaluator


class WordwiseEmbeddingCourseEvaluator(EmbeddingCourseEvaluator):
    def _calculate_similarity(self, sentence1, sentence2):
        """
        Calculates similarity between two sentences by using cosine similarity
        to perform pairwise matching of words.
        The score is the average best match between vectors

        :param sentence1: A string representing an unprocessed sentence
        :param sentence2: A string representing an unprocessed sentence
        :return: score: float: the average pairwise cosine similarity between
                               the words in sentence1 and sentence2
        """

        tokens1 = self.preprocess(sentence1)
        tokens2 = self.preprocess(sentence2)

        grid = np.array([[self._wv.similarity(w, v)
                          for w in tokens1]
                         for v in tokens2])

        # The similarity is
        score = grid.max(axis=1).mean()

        return score
