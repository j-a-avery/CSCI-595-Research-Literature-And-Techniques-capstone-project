from course import Course
from evaluators import CourseEvaluator

from semantic_text_similarity.models import ClinicalBertSimilarity
import numpy as np


class TransformerCourseEvaluator(CourseEvaluator):
    def __init__(self, device='cuda'):
        self._model = ClinicalBertSimilarity(device=device)

    def _calculate_similarity(self, course1: Course, course2: Course):
        pass

    def preprocess(self, sentence):
        pass

    # find_matches is in super. Do not overload it here.
    #TODO: move the code from find_matches to _calculate_similarity




    def find_matches(self, query_course: Course, catalog_courses: [Course]):
        sim = self._model.predict([
            (query_course.description, course.description)
            for course in catalog_courses
        ]) / 5

        np.flip(sim.sort())

        return sim
