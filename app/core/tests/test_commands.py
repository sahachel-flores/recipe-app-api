"""
Test custom Django management commands.
"""
# path mocks the behavior of the database
from unittest.mock import patch
# display database errors
from psycopg2 import OperationalError as Psycopg2Error
# helper function which allows to simulate/call
# the command we are testing by the name
from django.core.management import call_command
# another error that might be thrown by the database
from django.db.utils import OperationalError
# base test class for testing our unit test
from django.test import SimpleTestCase


# mocks behavior of database (mock object)
@patch('core.management.commands.wait_for_db.Command.check')
# class we are creating is based from SimpleTestCase
class CommandTest(SimpleTestCase):
    """Test Command."""
    # one possible test case where we wait for database.
    # patched_check object replaces check by patch,
    # we use it now to cumstimize our behavior
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # when we call check inside out test_scase,
        # we want to just return a value
        patched_check.return_value = True

        call_command('wait_for_db')  # execute the command

        # Ensures that mock object is called w/ parameter database=['default']
        patched_check.assert_called_once_with(databases=['default'])

    # patch to mock the sleep method.
    # Note: postion of the parameter below correspond
    # to each @patch from the inside out
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting Operational Error"""
        # To raise an exception we use side_effect.
        # First 2 times we call the mock object,
        # we raise Psy..Error, next 3 times we raise the operational error.
        # Two and three are arbitrery values.
        # The six time we call it, we get True
        patched_check.side_effect = [Psycopg2Error] * 2 \
            + [OperationalError] * 3 + [True]

        # Call command
        call_command('wait_for_db')

        # test to check if we get 6 calls to the mock call object
        self.assertEqual(patched_check.call_count, 6)

        # making sure that pactched_check is called with the default database
        patched_check.assert_called_with(databases=['default'])
