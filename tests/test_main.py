"""Test the app's entry module."""

import unittest
from unittest.mock import Mock, patch
from main import Application, State, main as main_fn

class TestMain(unittest.TestCase):
    """Test the functioning of the app's entry (`main.py`) module."""

    @patch('main.__name__', '__main__')
    @patch('main.Application')
    def test_app_main_func_starts_the_gui_app_when_main_module_is_invoked(self, app: Mock) -> None:
        """Confirm that the app's `main()` function starts up the GUI app when the `main.py` module
        is invoked (when `__name__ == '__main__'`)."""

        main_fn()
        # Confirm that two calls of the Application mock have been made
        # (the first one initializes an Application object and second to starts the GUI app)
        self.assertEqual(2, len(app.mock_calls))
        # Confirm that the call to start the GUI app has been made
        self.assertEqual('().start', app.mock_calls[1][0])

    @patch('main.__name__', '__non-main__')
    @patch('main.Application')
    def test_app_main_func_does_not_starts_the_gui_app_when_main_module_is_just_referenced(
        self, app: Mock) -> None:
        """Confirm that the app's `main()` function does not start up the GUI app when the `main.py`
        module is just referenced (imported) (when `__name__ != '__main__'`)."""

        main_fn()
        self.assertEqual(0, len(app.mock_calls))

class TestAppState(unittest.TestCase):
    """Test the functioning of an (app) `State`."""

    def test_a_value_is_retrieved_from_an_app_state(self) -> None:
        """Confirm that a value is retrieved from an (app) `State`."""

        state = State(key1='value1')
        self.assertEqual('value1', state.get('key1'))

    def test_nothing_is_returned_for_a_non_existing_key_in_an_app_state(self) -> None:
        """Confirm that `None` is returned when trying to get a value by a non-existent key from an
        (app) `State`."""

        state = State(key1='value1')
        self.assertIsNone(state.get('key2'))

    def test_an_app_state_invokes_a_callable_when_trying_to_set_an_item_to_a_value(self) -> None:
        """Confirm that an (app) `State` invokes a passed in callable in the process of setting one
        of its items to a certain value."""

        state = State(key1='value1')
        setter = Mock()
        state.set('key1', setter)
        setter.assert_called_once_with('value1')

    def test_an_app_state_item_is_set_to_a_certain_value(self) -> None:
        """Confirm that an (app) `State`'s item is set to a certain value"""

        state = State(key1='value1')
        state.set('key1', 'value2')
        self.assertEqual('value2', state.get('key1'))

class TestApplication(unittest.TestCase):
    """Test the functioning of an `Application` instance."""

    def test_app_gets_initialized_with_certain_properties(self) -> None:
        """Confirm that an `Application` instance gets initialized with certain properties."""

        app = Application()
        main_window = app.winfo_toplevel()
        self.assertEqual('Shuffler', main_window.title())
        self.assertEqual((520, 110), main_window.minsize())
        self.assertEqual(10, main_window['padx'])
        self.assertEqual(10, main_window['pady'])

    @patch('main.Application.mainloop')
    def test_app_starts_up(self, main_loop: Mock) -> None:
        """Confirm that an `Application` starts up."""

        app = Application()
        app.start()
        main_loop.assert_called()
