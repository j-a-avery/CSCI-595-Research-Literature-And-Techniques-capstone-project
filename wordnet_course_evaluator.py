from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk import pos_tag


from evaluators import CourseEvaluator
from course import Course


class WordNetCourseEvaluator(CourseEvaluator):
    def __init__(self, *args):
        pass

    @classmethod
    def _penn_to_wn(cls, tag):
        """Convert between a Penn Treebank tag and a simplified WordNet tag"""
        new_tag = None

        if tag.startswith("N"):
            new_tag = 'n'

        if tag.startswith("V"):
            new_tag = 'v'

        if tag.startswith("J"):
            new_tag = 'a'

        if tag.startswith("R"):
            new_tag = 'r'

        return new_tag

    @classmethod
    def _tagged_to_synset(cls, word, tag):
        """Convert a tagged word to a WordNet synset"""
        wn_tag = cls._penn_to_wn(tag)
        if wn_tag is None:
            return None

        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    @classmethod
    def _sentence_to_synset(cls, sentence):
        """Tokenize a sentence and convert it to a list of synsets"""
        # Tokenize and tag
        tokens = pos_tag(word_tokenize(sentence))

        # Get synsets for tagged words
        synsets = [cls._tagged_to_synset(*tagged_word) for tagged_word in tokens]

        # Remove empty synsets
        synsets = [ss for ss in synsets if ss]

        return synsets

    @classmethod
    def _calculate_similarity(cls, course1: Course, course2: Course):
        """Compute the similarity between two sentences using WordNet"""
        synsets1 = cls._sentence_to_synset(course1.description)
        synsets2 = cls._sentence_to_synset(course2.description)

        score, count = 0.0, 0

        # For each word in sentence1, find the most similar word (if any) in sentence2
        for synset in synsets1:
            scores = [synset.wup_similarity(ss) for ss in synsets2]

            # Remove empty scores
            scores = [s for s in scores if s is not None]

            if scores == []:
                best_score = 0
            else:
                best_score = max(scores)

            # Make sure similarity is computable
            if best_score is not None:
                score += best_score
                count += 1

        # Average the values
        if count == 0:
            score = 0
        else:
            score /= count

        return score

    @classmethod
    def find_matches(cls, query_course: Course, catalog_courses: [Course]):
        candidates = [
            (cls._calculate_similarity(query_course,
                                       candidate_course),
             candidate_course)
            for candidate_course in catalog_courses
        ]

        candidates = sorted(candidates, reverse=True)

        return candidates
