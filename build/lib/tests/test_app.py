from flask import url_for


class TestPage(object):
    def test_home_page(self, client):
        """ Home page should respond with a success 200. """
        response = client.get(url_for('index'))
        assert response.status_code == 200

    def test_search_page(self, client):
        response = client.get(url_for('search'))
        assert response.status_code == 200

    def test_show_add_profile_page(self, client):
        response = client.get(url_for('add_profile'))
        assert response.status_code == 200

    def test_add_profile_page(self, client):
        response = client.post(url_for('add_profile'),
                               data=dict(firstName='Anna', lastName='Bankirer', email='bla@gmail.com', bio='bla bla bla'))
        assert response.status_code == 200

    def test_show_profile_page(self, client):
        response = client.get(url_for('show_profile', id=1))
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get(url_for('login'))
        assert response.status_code == 200
