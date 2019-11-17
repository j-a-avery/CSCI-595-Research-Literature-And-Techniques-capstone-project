from course import Course


class CourseSimilarity:
    """
    Class for holding course similarity measures.
    This allows for easier sorting and reporting of similarities
    compared to previous solution of (sim: float, from_course: Course) tuples

    When a course is evaluated, its evaluation is stored as a new
    CourseSimilarity object. Evaluations are then stored as lists of
    CourseSimilarity objects, which can then be sorted easily based on
    similarity scores.

    CourseSimilarity objects essentially behave as annotated floats.
    All boolean and arithmetic operations are defined to operate on
    just the score member variable, allowing for e.g. sorting lists of
    CourseSimilarity scores, or finding average similarities.
    """
    def __init__(self, similarity_score: float, to_course: Course, from_course: Course):
        self.score = similarity_score
        self.to_course = to_course
        self.from_course = from_course

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __hash__(self):
        return hash((self.score, self.to_course, self.from_course))

    def __bool__(self):
        """
        :return: True if self.score is really close to 1.0 (ε=1e-10)
                 In other words, if the scores are essentially identical.
                 If necessary, this could be extended to allow for
                 larger epsilons as a class member, so that e.g.
                 scores greater than 0.9 could be considered True
        """
        return abs(1 - self.score) < 1e-10

    # Numeric operators
    # Note that these all convert to bare floats
    def __add__(self, other):
        return self.score + other.score

    def __sub__(self, other):
        return self.score - other.score

    def __mul__(self, other):
        return self.score * other.score

    def __truediv__(self, other):
        return self.score / other.score

    def __floordiv__(self, other):
        return self.score // other.score

    def __mod__(self, other):
        return self.score % other.score

    def __divmod__(self, other):
        return divmod(self.score, other.score)

    def __pow__(self, other, modulo=None):
        """
        In what situation would you actually raise a score to another score?!
        (included for completeness, since it's one whole line to write.)
        :param other: another score
        :param modulo: modulo value
        :return: self raised to the other power. Why? Who knows.
                 Maybe it could come up in some weird geometric mean?
        """
        return pow(self.score, other.score, modulo)

    def __str__(self):
        """
        :return: e.g.
            "1.00000 CSCI-595 Research Literature and Techniques ->
                CSCI-595 Research Literature and Techniques"
            (sans newline and indentation)
        """
        return f"{self.score:.5f} {str(self.from_course)} -> {str(self.to_course)}"
