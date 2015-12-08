class TagManager:
    def __init__(self):
        self.nb_categories = 0
        self._tag_numbers= {}
        self._tag_dict = {}

    @classmethod
    def from_nb_tags(cls, nb_categories):
        manager = cls()
        manager.nb_categories = nb_categories
        return manager

    def get_current_nb_categories(self):
        return len(self._tag_numbers)

    def get_tag(self, cat_identifier):
        if cat_identifier in self._tag_dict:
            return self._tag_dict[cat_identifier]

        number = self.get_current_nb_categories()
        if(number > self.nb_categories):
            raise Exception("Too many categories created")

        self._tag_numbers[cat_identifier] = number
        tag = self._create_tag(number)
        self._tag_dict[cat_identifier] = tag

        return tag



    def _create_tag(self, current_categorie):
        tag = []
        for i in range(self.nb_categories):
            tag.append(0)
        tag[current_categorie] = 1
        return tag