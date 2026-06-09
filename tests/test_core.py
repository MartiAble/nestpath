import unittest

from nestpath import delete_path, get_path, has_path, parse_path, set_path
from nestpath.core import PathSyntaxError


class ParsePathTests(unittest.TestCase):
    def test_parse_simple_path(self):
        self.assertEqual(parse_path("user.profile.name"), ["user", "profile", "name"])

    def test_parse_mixed_path(self):
        self.assertEqual(parse_path("users[0].email"), ["users", 0, "email"])

    def test_parse_escaped_characters(self):
        self.assertEqual(parse_path(r"settings.theme\.dark.enabled"), ["settings", "theme.dark", "enabled"])

    def test_reject_invalid_path(self):
        with self.assertRaises(PathSyntaxError):
            parse_path("user..name")


class GetSetDeleteTests(unittest.TestCase):
    def test_set_path_creates_missing_containers(self):
        data = {}
        set_path(data, "users[0].profile.email", "alice@example.com")
        self.assertEqual(data, {"users": [{"profile": {"email": "alice@example.com"}}]})

    def test_get_path_returns_default(self):
        data = {"users": []}
        self.assertEqual(get_path(data, "users[1].name", default="unknown"), "unknown")

    def test_get_path_raises_without_default(self):
        with self.assertRaises(KeyError):
            get_path({}, "missing.value")

    def test_has_path(self):
        data = {"meta": {"ready": True}}
        self.assertTrue(has_path(data, "meta.ready"))
        self.assertFalse(has_path(data, "meta.missing"))

    def test_delete_dict_key(self):
        data = {"meta": {"ready": True, "version": 1}}
        self.assertTrue(delete_path(data, "meta.version"))
        self.assertEqual(data, {"meta": {"ready": True}})

    def test_delete_list_item(self):
        data = {"users": ["alice", "bob", "carol"]}
        self.assertTrue(delete_path(data, "users[1]"))
        self.assertEqual(data, {"users": ["alice", "carol"]})

    def test_type_mismatch_raises_on_set(self):
        with self.assertRaises(TypeError):
            set_path([], "user.name", "alice")


if __name__ == "__main__":
    unittest.main()
