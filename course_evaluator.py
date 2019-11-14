from course import Course


class CourseEvaluator:
    """
    CourseEvaluator: Parent class which provides an interface to be implemented
    by specific CourseEvaluator subclasses.
    """

    def __init__(self):
        _implementation_error_message = f"{self.__name__} is a stub. Use one of its derived classes."
        raise RuntimeError(self._implementation_error_message)

    def find_matches(self, query_course: Course, candidate_courses: [Course],
                     *, max_results=None, min_match=None):
        """
        Evaluates a course against a list of other courses, using a
        _calculate_similarity method that is specific to the subclass.
        :param query_course:
        :param candidate_courses:
        :param max_results:
        :param min_match:
        :return:
        """

        candidates = [(self._calculate_similarity(query_course, candidate_course), candidate_course)
                      for candidate_course in candidate_courses]

        if min_match is not None:
            candidates = [(score, course)
                          for (score, course) in candidates
                          if score >= min_match]

        if max_results is not None:
            candidates = candidates[:max_results]

        return candidates
