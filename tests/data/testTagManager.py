import unittest
from mushroom.data.TagManager import TagManager



class testTagManager(unittest.TestCase):
    def test_tag_creation(self):
        manager = TagManager.from_nb_tags(2)
        tag = manager.get_tag("cat1")
        self.assertEquals(tag, [1,0])
        tag = manager.get_tag("cat2")
        self.assertEquals(tag, [0,1])

    def test_tag_reget(self):
        manager = TagManager.from_nb_tags(2)
        tag = manager.get_tag("cat1")
        tag2 = manager.get_tag("cat1")
        self.assertEquals(tag2, [1,0])
        tag = manager.get_tag("cat2")
        tag2 = manager.get_tag("cat2")
        self.assertEquals(tag2, [0,1])

    def test_too_many_tags(self):
        manager = TagManager.from_nb_tags(2)
        manager.get_tag("cat1")
        manager.get_tag("cat2")
        self.assertRaises(Exception,manager.get_tag, "cat3")

