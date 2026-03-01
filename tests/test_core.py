"""Tests for Pramana OGM base classes."""

import uuid
from unittest import TestCase
from pramana import (
    PramanaException, PramanaObject, PramanaRole, PramanaParticular,
)


class TestPramanaObject(TestCase):

    def test_default_guid_is_empty(self):
        obj = PramanaObject()
        self.assertEqual(obj.pramana_guid, uuid.UUID(int=0))

    def test_explicit_guid(self):
        gid = uuid.uuid4()
        obj = PramanaObject(id=gid)
        self.assertEqual(obj.pramana_guid, gid)

    def test_generate_id(self):
        obj = PramanaObject()
        gid = obj.generate_id()
        self.assertNotEqual(gid, uuid.UUID(int=0))
        self.assertEqual(obj.pramana_guid, gid)

    def test_generate_id_immutable(self):
        obj = PramanaObject()
        obj.generate_id()
        with self.assertRaises(PramanaException):
            obj.generate_id()

    def test_generate_id_fails_if_already_set(self):
        obj = PramanaObject(id=uuid.uuid4())
        with self.assertRaises(PramanaException):
            obj.generate_id()

    def test_pramana_id_is_none(self):
        obj = PramanaObject()
        self.assertIsNone(obj.pramana_id)

    def test_pramana_hash_url(self):
        gid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        obj = PramanaObject(id=gid)
        self.assertEqual(obj.pramana_hash_url, f"https://pramana.dev/entity/{gid}")

    def test_pramana_url_falls_back_to_hash(self):
        gid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        obj = PramanaObject(id=gid)
        self.assertEqual(obj.pramana_url, obj.pramana_hash_url)

    def test_class_id(self):
        self.assertEqual(PramanaObject.CLASS_ID, PramanaObject.ROOT_ID)
        self.assertEqual(
            PramanaObject.CLASS_URL,
            f"https://pramana.dev/entity/{PramanaObject.ROOT_ID}",
        )

    def test_get_roles_empty(self):
        obj = PramanaObject()
        self.assertEqual(obj.get_roles(), [])


class TestPramanaRole(TestCase):

    def test_label(self):
        role = PramanaRole("TestRole")
        self.assertEqual(role.label, "TestRole")

    def test_instance_of(self):
        parent = PramanaRole("Parent")
        child = PramanaRole("Child")
        child.instance_of = parent
        self.assertIs(child.instance_of, parent)

    def test_subclass_of(self):
        parent = PramanaRole("Parent")
        child = PramanaRole("Child")
        child.subclass_of = parent
        self.assertIs(child.subclass_of, parent)

    def test_parent_child_roles(self):
        parent = PramanaRole("Parent")
        child = PramanaRole("Child")
        parent.child_roles.append(child)
        child.parent_roles.append(parent)
        self.assertIn(child, parent.child_roles)
        self.assertIn(parent, child.parent_roles)

    def test_get_roles_returns_self(self):
        role = PramanaRole("MyRole")
        roles = role.get_roles()
        self.assertEqual(len(roles), 1)
        self.assertIs(roles[0], role)

    def test_role_hierarchy(self):
        root = PramanaRole("Root")
        mid = PramanaRole("Mid")
        leaf = PramanaRole("Leaf")
        mid.subclass_of = root
        root.child_roles.append(mid)
        mid.parent_roles.append(root)
        leaf.subclass_of = mid
        mid.child_roles.append(leaf)
        leaf.parent_roles.append(mid)
        self.assertEqual(len(root.child_roles), 1)
        self.assertEqual(len(mid.child_roles), 1)
        self.assertEqual(len(leaf.child_roles), 0)


class TestPramanaParticular(TestCase):

    def test_class_id(self):
        self.assertEqual(
            PramanaParticular.CLASS_ID,
            uuid.UUID("13000000-0000-4000-8000-000000000004"),
        )

    def test_inherits_pramana_object(self):
        p = PramanaParticular()
        self.assertIsInstance(p, PramanaObject)

    def test_generate_id(self):
        p = PramanaParticular()
        gid = p.generate_id()
        self.assertNotEqual(gid, uuid.UUID(int=0))
