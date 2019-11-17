class Course:
    def __init__(self, subject, number, title, description, common_course_number=None):
        self.subject = subject
        self.number = number
        self.title = title
        self.description = description
        self.common_course_number = common_course_number

    def __repr__(self):
        return f"{self.subject}-{self.number} \"{self.title}\""

    def __lt__(self, other):
        if self.subject == other.subject:
            return self.number < other.number
        else:
            return self.subject < other.subject

    def __gt__(self, other):
        if self.subject == other.subject:
            return self.number > other.number
        else:
            return self.subject > other.subject

    def __eq__(self, other):
        return (self.subject == other.subject
                and self.number == other.number
                and self.title == other.title
                and self.description == other.description
                and self.common_course_number == other.common_course_number)

    @staticmethod
    def from_dict(course_dict):
        """
        Creates and returns a new Course object from a dictionary object
        :param dict_object: a dict with the following fields:
                subject
                number
                title
                description
                common_course_number (optional)
        :return: a new Course object from the dictionary's contents
        """
        subject = course_dict.get("subject")
        number = course_dict.get("number")
        title = course_dict.get("title")
        desc = course_dict.get("description")
        ccn = course_dict.get("common_course_number")

        return Course(subject, number, title, desc, ccn)

    def to_dict(self):
        return {
            "subject": self.subject,
            "number": self.number,
            "title": self.title,
            "description": self.description,
            "common_course_number": self.common_course_number
        }

    def full(self):
        s = f"{self.subject}-{self.number}{f'({self.common_course_number})' if self.common_course_number else ''} "
        s += f"{self.title}\n{self.description}"

        return s
