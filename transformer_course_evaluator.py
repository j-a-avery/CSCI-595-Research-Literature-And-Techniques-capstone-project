from course import Course
from course_evaluator import CourseEvaluator

from semantic_text_similarity.models import ClinicalBertSimilarity


class TransformerCourseEvaluator(CourseEvaluator):
    def __init__(self):
        self._model = ClinicalBertSimilarity(device='cpu')

    def find_matches(self, query_course: Course, catalog_courses: [Course]):
        return self._model.predict([
            (query_course.description, course.description)
            for course in catalog_courses
        ]) / 5
