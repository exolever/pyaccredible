#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyaccredible` package."""


import unittest
from datetime import datetime

from pyaccredible.client import AccredibleWrapper


class TestPyaccredible(unittest.TestCase):
    """Tests for `pyaccredible` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.client = AccredibleWrapper('')
        self.client.API_URL = 'https://private-anon-3d8bf32214-accrediblecredentialapi.apiary-mock.com/v1/'

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_create_group(self):
        """Test something."""
        data = {
            "name": "new group",
            "course_name": "Intro to Prgramming",
            "course_description": "Description of course",
            "course_link": "http://www.example.com",
            "language": "en",
            "attach_pdf": True,
            "design_id": None
        }

        response = self.client.group_create(**data)
        self.assertEqual(response.status_code, 200)

    def test_create_credencial(self):
        """Test something."""
        data = {
            'name': 'First Name',
            'email': 'name@example.org',
            'group_id': 999,
            'issued_on': datetime(2018, 10, 10)
        }

        response = self.client.credential_create(**data)
        self.assertEqual(response.status_code, 200)

    def test_update_credential(self):
        data = {'approved': True}
        response = self.client.credential_update(credential_id=999, **data)
        self.assertEqual(response.status_code, 200)

    def test_bulk_create_credencial(self):
        """Test something."""
        data = {
            'participants': [],
            'group_id': 999,
            'issued_on': datetime(2018, 10, 10)
        }
        data['participants'].append(['name1', 'name1@example.org'])
        data['participants'].append(['name2', 'name2@example.org'])
        response = self.client.credential_create_bulk(**data)
        self.assertEqual(response.status_code, 200)
