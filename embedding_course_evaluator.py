from gensim.models import KeyedVectors
from gensim.parsing.preprocessing import preprocess_string
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_numeric
from gensim.parsing.preprocessing import strip_short

from nltk.corpus import stopwords

from evaluators import CourseEvaluator


class EmbeddingCourseEvaluator(CourseEvaluator):
    _stopwords = stopwords.words('english')

    def __init__(self, vector_file):
        self._wv = KeyedVectors.load(vector_file)

    def preprocess(self, sentence):
        """
        Tokenize the sentence, and filter it using some of
        Gensim's preprocessing filters along with
        NLTK's smaller stopwords list,
        and also filter out words that are out-of-vocabulary.
        :param sentence: a string representing a sentence to clean and tokenize
        :return: a list of tokens
        """

        filters = [lambda t: t.lower(),
                   strip_punctuation,
                   strip_multiple_whitespaces,
                   strip_numeric,
                   strip_short]

        tokens = [token for token in preprocess_string(sentence, filters)
                  if token not in self._stopwords
                  and token in self._wv.vocab.keys()]

        return tokens
