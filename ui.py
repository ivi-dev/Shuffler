"""UI building utilities. Pretty much all of this module's utilities are wrappers for the tkinter_
GUI widget set. Their purpose is to provide a simplified interface for creating and managing tkinter
widgets.

.. _tkinter: https://tkdocs.com/shipman/
"""

import tkinter as tk
from tkinter import filedialog

# Widget types
Frame = tk.Frame
Label = tk.Label
Button = tk.Button

# Widget positioning options (see https://tkdocs.com/shipman/grid.html)
FULL_STRETCH = tk.W + tk.E + tk.N + tk.S  # Stretch a widget in both horizontal and vertical
H_STRETCH = tk.W + tk.E                   # Stretch a widget horizontally
V_STRETCH = tk.N + tk.S                   # Stretch a widget vertically
LEFT = tk.W                               # Place a widget to the left of its container
RIGHT = tk.E                              # Place a widget to the right of its container
TOP = tk.N                                # Place a widget to the top of its container
BOTTOM = tk.S                             # Place a widget to the bottom of its container

# Widget states
DISABLED = tk.DISABLED
NORMAL = tk.NORMAL

# Relief styles
SUNKEN = tk.SUNKEN

def widget(class_: tk.Widget, *args: any, **kwargs: any) -> tk.Widget:
    """Create a GUI widget. The returned widget is actually a tkinter_ widget. All list and keyword
    arguments will be passed to the specific tkinter widget's constructor.

    .. _tkinter: https://tkdocs.com/shipman/

    :param class_: The widget's class.
    :type class_: tk.Widget
    :return: The created widget.
    :rtype: tk.Widget
    """

    grid_opts, = _pop(['grid'], from_=kwargs)
    widget_ = class_(*args, **kwargs)
    widget_.grid(**grid_opts)
    return widget_

def config(widget_: tk.Widget, opts: dict) -> None:
    """Set a widget's options.

    :param widget_: The widget to configure.
    :type widget_: tk.Widget
    :param opts: A dictionary of the options to apply to `widget`. Here's an example of setting a
    button's label and state:

    ::
        btn = widget(Button, parent, grid={'row': 0, 'column': 1})
        config(btn, opts={'text': 'Try again later', 'state': DISABLED})

    :type opts: dict
    """

    for opt, value in opts.items():
        widget_[opt] = value

def file_chooser() -> str:
    """Present a file choosing dialog to the user.

    :return: The full path to the user-chosen file.
    :rtype: str
    """

    return filedialog.askopenfilename()

def file_saver() -> str:
    """Present a file save dialog to the user.

    :return: The user-selected file save location.
    :rtype: str
    """

    return filedialog.asksaveasfilename()

class StrBinding(tk.StringVar):
    """An object that helps bind a widget's property to a certain textual content. This class is a
    thin wrapper for the tkinter's StringVar_ and it's main purpose is to ease the initialization of
    such objects.

    .. _StringVar: https://tkdocs.com/shipman/control-variables.html
    """

    def __init__(self, val: str):
        """Create a new string binding with initial content.

        :param val: A string to initialize this binding with.
        :type val: str
        """

        super().__init__()
        self.set(val)

class NamedList(tk.LabelFrame):
    """A UI widget with a title, and the ability to display items as a list."""

    def __init__(self, parent: tk.Widget, label: str = 'List', placeholder: str = '<Empty>',
                 items: list[any] = (), **kwargs):
        """Initialize a new named list.

        :param parent: A widget to register this one to.
        :type parent: tk.Widget
        :param label: The list's label.
        :type label: str
        :param placeholder: Text to show to the user in case the list is empty.
        :type placeholder: str
        :param items: The list's items.
        :type items: list
        """

        grid_opts, item_opts = _pop(['grid', 'item_args'], from_=kwargs)
        super().__init__(parent, text=label, **kwargs)
        self._make_resizable()
        self.placeholder = self._placeholder(text=placeholder)
        self.item_widgets = self._add_all(items, **item_opts)
        self.grid(**grid_opts)

    def _make_resizable(self) -> None:
        """Make this app's window resizable."""

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def add(self, item: any, **kwargs: any) -> None:
        """Add an item to the list.

        :param item: The item to add.
        :type item: any
        :param kwargs: Keyword arguments to pass onto the `ui.widget` function for creating the UI
        widget.
        :type kwargs: any
        """

        if not self.item_widgets:
            self.placeholder.grid_forget()
            self.placeholder = None
        self.item_widgets.append(widget(Label, self, text=str(item), **kwargs))

    def remove_all(self) -> None:
        """Remove all items from the list."""

        for widget_ in self.item_widgets:
            widget_.grid_forget()
        self.item_widgets = []

    def _add_all(self, items: list[any], **kwargs) -> None:
        """Create a UI widget for each of the items on the `list`.

        :param items: The list of items.
        :type items: list
        :param kwargs: Keyword arguments to pass onto the `ui.widget` function for creating the UI
        widget.
        :type kwargs: any
        """

        return [widget(Label, self, text=str(item), **kwargs) for item in items]

    def _placeholder(self, text: str) -> tk.Widget:
        """Display a placeholder text, typically when the list is empty.

        :param text: The placeholder's text.
        :type text: str
        :return: A UI widget.
        :rtype: tk.Widget
        """

        return widget(Label, self, text=text, state=DISABLED, grid={'sticky': H_STRETCH})

def _pop(items: list[str], from_: dict) -> tuple:
    """Pop a value(s) off a dictionary and return them as a tuple. For example the following pop two
    of the values from a dictionary, key'd 'key1' and 'key2':

    >>> key1, key2 = _pop(
            items=['key1', 'key2'],
            from_={'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        )
    >>> ('value1', 'value2')

    :param items: A list of keys to pop off `from_`.
    :type items: list[str]
    :param from_: The dictionary to pop items off.
    :type from_: dict
    :return: A tuple of the values of the popped dictionary keys.
    :rtype: tuple
    """

    return tuple(from_.pop(key) for key in items)

class List(tk.Listbox):
    """A UI widget that displays items as a list."""

    def __init__(self, parent: tk.Widget, items: list[str] = (), **kwargs: any):
        """Initialize a new list.

        :param parent: A widget to register this one to.
        :type parent: tk.Widget
        :param items: The list's items.
        :type items: list[str]
        :param kwargs: Keyword arguments to pass onto the underlying tkinter Listbox_ constructor.
        :type kwargs: any

        .. _Listbox: https://tkdocs.com/shipman/listbox.html
        """

        self._items = list(items)
        self._list = StrBinding(' '.join(self._items))
        grid_opts, scroll_grid_opts = _pop(['grid', 'scroll_grid'] ,from_=kwargs)
        scrollbar_grid_opts = self._scrollbar_grid_opts(grid_opts, scroll_grid_opts)
        scrollbar = self._scrollbar(parent, **scrollbar_grid_opts)
        super().__init__(parent, listvariable=self._list,
                         yscrollcommand=scrollbar.set, **kwargs)
        self.grid(**grid_opts)

    def _update_binding(self) -> None:
        """Update the internal binding object, supplying the list with items."""

        self._list.set(' '.join(self._items))

    def _scrollbar_grid_opts(self, list_grid_opts: dict, scroll_grid_opts: dict) -> dict:
        """Return a complete dictionary of this `List`'s scrollbar's grid options.

        :param list_grid_opts: The grid options of this `List`.
        :type list_grid_opts: dict
        :param scroll_grid_opts: The grid options of this `List`'s scrollbar.
        :type scroll_grid_opts: dict
        :return: A complete dictionary of this `List`'s scrollbar's grid options.
        :rtype: dict
        """

        row = list_grid_opts.get('row') if list_grid_opts.get('row') is not None else 0
        column = list_grid_opts.get('column') + 1 if list_grid_opts.get('column') is not None else 1
        return {**{'row': row, 'column': column}, **scroll_grid_opts}

    def _scrollbar(self, parent: tk.Widget, **grid_opts) -> tk.Scrollbar:
        """Construct a scrollbar.

        :parram parent: The widget to register the scrollbar to.
        :type parent: tk.Widget
        :return: A scrollbar widget.
        :rtype: tk.WScrollbar
        """

        scrollbar = widget(tk.Scrollbar, parent, orient=tk.VERTICAL,
                           grid={**grid_opts, **{'sticky': TOP + BOTTOM + LEFT}})
        scrollbar['command'] = self.yview
        return scrollbar

    def add(self, item: str) -> None:
        """Add an item to the list.

        :param item: The item to add.
        :type item: str
        """

        self._items.append(item)
        self._update_binding()

    def get_all(self) -> list[str]:
        """Return all of this list's items.

        :return: All of this list's items.
        :rtype: list[str]
        """

        return self._items

    def remove_all(self) -> None:
        """Remove all items from the list."""

        self._items = []
        self._list.set('')

class OptionMenu(tk.OptionMenu):
    """A list of selectable options."""

    def __init__(self, parent: tk.Widget, biniding: StrBinding, options: list[str] = (),
                 **kwargs: any):
        """Initialize a new selectable options list.

        :param parent: A widget to register this one to.
        :type parent: tk.Widget
        :param biniding: A string binding that will reflect the currently selected option.
        :type biniding: StrBinding
        :param options: The list of options.
        :type options: list
        :param kwargs: Keyword arguments to pass onto the underlying tkinter OptionMenu_
        constructor.
        :type kwargs: any

        .. _OptionMenu: https://tkdocs.com/shipman/listbox.html
        """

        self._value = biniding
        self._value.set(options[0])
        grid_opts = _pop(['grid'] ,from_=kwargs)[0]
        super().__init__(parent, self._value, *options, **kwargs)
        self.grid(**grid_opts)

    def get(self) -> str:
        """Return the currently selected option.

        :return: The currently selected option.
        :rtype: str
        """

        return self._value.get()

    def set(self, value: str) -> None:
        """Set the currently selected option.

        :param value: The desired selected option.
        :type value: str
        """

        self._value.set(value)
