from app import app
from unittest import TestCase


"""Tests need work, it currently doesnt work"""

class pokemon_search(TestCase):
    def test_pokemon_search(self):
        with app.test_client() as client:
            res = client.get('/pokemon/1')
            html = res.get_data(as_text=True)
            self.assertIn('bulbasaur', html)

