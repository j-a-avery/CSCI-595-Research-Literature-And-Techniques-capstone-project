from course import Course


class CourseSimilarity:
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

    def __str__(self):
        return f"{self.score:.5f} {str(self.from_course)}->{str(self.to_course)}"
