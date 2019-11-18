from course import Course
from course_similarity import CourseSimilarity

import logging

#TODO: Move all evaluator classes to this file.
class CourseEvaluator:
    """
    CourseEvaluator: Parent class which provides an interface to be implemented
    by specific CourseEvaluator subclasses.
    """

    def __init__(self):
        _implementation_error_message = f"{self.__name__} is a stub. Use one of its derived classes."
        raise RuntimeError(self._implementation_error_message)

    def find_matches(self, query_course: Course, candidate_courses: [Course],
                     *, max_results=None, min_match=None, no_match=None,
                     **kwargs) -> [CourseSimilarity]:
        """
        Evaluates a course against a list of other courses, using a
        _calculate_similarity method that is specific to the subclass.
        :param query_course: Course:
        :param candidate_courses: [Course]:
        :param max_results: int: Only return the max_results best matches
        :param min_match: float: Filter the results list, and only return those
                results whose match percentage is >= min_match
        :param no_match: String or None: {"best", "empty", "iterate", None}
                If filtering by min_match produces an empty list, then
                compensate based on value:
            "best": If max_results is None, then return the single best result.
                    If max_results is defined, then fall back to max_results
                    behavior, ignoring the min_match filter.
            "empty": Return the empty results list.
            "iterate": Continuously iterate the value of min_match until a non-
                    empty results list is produced. The default behavior is to
                    reduce min_match by 10% every time, unless a value is passed
                    for iteration as a kwarg.
        :param kwargs
        :return:
        """

        logging.info(f"Finding matches for {query_course}")
        candidates = [CourseSimilarity(
                self._calculate_similarity(query_course, candidate_course),
                query_course,
                candidate_course)
            for candidate_course in candidate_courses]

        candidates = sorted(candidates, reverse=True)

        if min_match is not None:
            filtered_candidates = filter(lambda c: c.score >= min_match,
                                         candidates)
            if len(filtered_candidates == 0):
                candidates = candidates[0]
            else:
                candidates = candida
            candidates = [cs for cs in candidates
                          if cs.score >= min_match]


        if max_results is not None:
            candidates = candidates[:max_results]

        return candidates
