import pytest
from users import forms


class TestSignUpForm():
    @pytest.mark.django_db
    def test_valid_form(self):
        form = forms.SignUpForm({
            'username': 'jake',
            'password1': 'fromstatefarm',
            'password2': 'fromstatefarm'
        })

        assert form.is_valid()

        user = form.save(commit=False)
        assert user.username == 'jake'


    def test_blank_form(self):
        form = forms.SignUpForm({})
        assert not form.is_valid()

        expected_form_errors = {
            'username': ['This field is required.'],
            'password1': ['This field is required.'],
            'password2': ['This field is required.']
        }

        assert form.errors == expected_form_errors
