"""The app's entry module."""

import random
import os
from typing import Optional, Union
import ui
from data_export.plain import export as export_plain
from data_export.xml   import export as export_xml
from data_export.json  import export as export_json

class State:
    """A container for an app's state."""

    def __init__(self, **kwargs):
        """Create a new app state container."""

        self.items = kwargs

    def get(self, key: str) -> any:
        """Return the value of an app's state item or `None` if no such item exists in the state
        container.

        :param key: The key of a state item.
        :type key: str
        :return: The value of an app's state item, identified by `key`.
        :rtype: any
        """

        return self.items.get(key)

    def set(self, key: str, value: any) -> None:
        """Set a state item to a certain value.

        :param key: The key of a state item.
        :type key: str
        :param value: The value to set the state item to.
        :type value: any
        """

        if callable(value):
            value(self.items[key])
        else:
            self.items[key] = value

class Application(ui.Frame):
    """The GUI app."""

    def __init__(self):
        """Initialize a new shuffler.

        :param items_file: A path to a file containing the items for this shuffler.
        :type items_file: str
        :param interval: The interval, in milliseconds, between two items showing up on screen,
        defaults to 100. The smaller this number is the faster the shuffle will be.
        :type interval: int, optional
        """

        ui.Frame.__init__(self, None)
        self.export_formats = (
            ('TXT', self._export_txt),
            ('XML', self._export_xml),
            ('JSON', self._export_json)
        )
        self.state = State(**{
            'shuffle_list': [],
            'shuffle_list_filepath': None,
            'picked': [],
            'interval': 50,
            'value': ui.StrBinding('Choose an items file'),
            'shuffle_btn': None,
            'shuffling_in_progress': False,
            'picked_items_container': None,  # ui.List
        })
        self._setup_layout(minwidth=520, minheight=110)
        self.grid(sticky=ui.FULL_STRETCH)
        self._create_widgets()

    def _setup_layout(self, minwidth: int, minheight: int) -> None:
        """Setup some general app layout parameters.

        :param minwidth: The app window's minimum width.
        :type minwidth: int
        :param minheight: The app window's minimum height.
        :type minheight: int
        """

        self._config_window(minwidth, minheight)
        self._make_resizable()

    def _config_window(self, minwidth: int, minheight: int) -> None:
        """Configure the app's main (top-level) window.

        :param minwidth: The app window's minimum width.
        :type minwidth: int
        :param minheight: The app window's minimum height.
        :type minheight: int
        """

        window = self.winfo_toplevel()
        window.title('Shuffler')
        window.minsize(minwidth, minheight)
        window['padx'] = 10
        window['pady'] = 10

    def _make_resizable(self) -> None:
        """Make this app's window resizable."""

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)      # App's top-level windows's row (the only one)
        top.columnconfigure(0, weight=1)   # App's top-level windows's column (the only one)

        self.columnconfigure(5, weight=1)  # App's content's 6th column

    def start(self) -> None:
        """Start the app."""

        self.mainloop()

    def _create_widgets(self) -> None:
        """Create the app's GUI."""

        # The currently visible item
        ui.widget(ui.Label, self, textvariable=self.state.get('value'), font=('Futura', 20),
                  grid={'columnspan': 4, 'sticky': ui.LEFT + ui.TOP})
        # The 'Import' button
        ui.widget(ui.Button, self, text='Import', command=self._load_shuffle_list,
                  grid={'row': 1, 'sticky': ui.H_STRETCH})
        # The 'Export' button
        ui.widget(ui.Button, self, text='Export', command=self._export_picked,
                  grid={'row': 1, 'column': 1, 'sticky': ui.H_STRETCH})
        # The 'Start/Stop' button
        self.state.set('shuffle_btn', ui.widget(ui.Button, self, text='Start',
                                                command=self._toggle_shuffler,
                                                grid={'row': 1, 'column': 2,
                                                      'sticky': ui.H_STRETCH}))
        # The 'Pick (item)' button
        ui.widget(ui.Button, self, text='Pick', command=self._pick_item,
                  grid={'row': 1, 'column': 3, 'sticky': ui.H_STRETCH})
        # The 'Reset' button
        ui.widget(ui.Button, self, text='Reset', command=self._reset,
                  grid={'row': 2, 'sticky': ui.H_STRETCH})
        # The 'Quit' button
        ui.widget(ui.Button, self, text='Quit', command=self.quit,
                  grid={'row': 2, 'column': 1, 'sticky': ui.LEFT})
        # The list of picked items
        ui.widget(ui.Frame, self, width=10, grid={'column': 4})  # Left spacer (10px)
        self.state.set('picked_items_container', ui.List(
            parent=self, items=self.state.get('picked'), bg='lightgrey', height=5, relief=ui.SUNKEN,
            grid={'row': 0, 'column': 5, 'rowspan': 3, 'sticky': ui.FULL_STRETCH},
            scroll_grid={'rowspan': 3}))

    def _toggle_shuffler(self) -> None:
        """Start/stop shuffling."""

        def start_shuffling():
            """Start the shuffling process."""

            random.shuffle(self.state.get('shuffle_list'))
            self._toggle_shuffle_state('on')
            i = 0
            self._start_item_flash_loop(i)

        if not self.state.get('shuffle_list') and not self.state.get('shuffle_list_filepath'):
            self._load_shuffle_list(fresh=False)
        if not self.state.get('shuffling_in_progress'):
            if not self.state.get('shuffle_list'):
                self._reset()
            start_shuffling()
            return

        self._toggle_shuffle_state('off')

    def _toggle_shuffle_state(self, state: str, update_btn_label: Union[bool, str] = True,
                              btn_state: Optional[int] = None) -> None:
        """Toggle the state of the shuffler on or off. An internal flag is set to indicate the
        shuffling process ('on' state) is in progress or stopped ('off' state). There's also the
        option to set the 'Shuffle' button's labbel and/or disable it.

        :param state: The desired state of the shuffler. Can be either 'on' or 'off'.
        :type state: str
        :param update_btn_label: If set to a boolean value, will cause the 'Shuffle' button's label
        to be either updated (True) to reflect the new state of the shuffler or not (False). If set
        to a string value, it will be used as the 'Shuffle' button's label.
        :type update_btn_label: Union[bool, str]
        :param btn_state: The desired state of the 'Shuffle' button, either `ui.NORMAL` or
        `ui.DISABLED`.
        :type btn_state: int
        """

        if state == 'on':
            self.state.set('shuffling_in_progress', True)
            if isinstance(update_btn_label, bool) and update_btn_label:
                self.state.get('shuffle_btn')['text'] = 'Stop'
            elif isinstance(update_btn_label, str):
                self.state.get('shuffle_btn')['text'] = update_btn_label
        elif state == 'off':
            self.state.set('shuffling_in_progress', False)
            if isinstance(update_btn_label, bool) and update_btn_label:
                self.state.get('shuffle_btn')['text'] = 'Start'
            elif isinstance(update_btn_label, str):
                self.state.get('shuffle_btn')['text'] = update_btn_label
        if btn_state:
            self.state.get('shuffle_btn')['state'] = btn_state

    def _pick_item(self) -> None:
        """'Pick' the currently visible item, put it on a list and remove it from the shuffle list.
        """

        if self.state.get('shuffle_list') and self.state.get('shuffling_in_progress'):
            self._toggle_shuffle_state('off', update_btn_label=False)
            self._transfer_item_to_picked_list(self.state.get('value').get())
            if not self.state.get('shuffle_list'):  # Shuffle list is empty
                self.state.get('value').set('No more items. Reset/Restart.')
                ui.config(widget_=self.state.get('shuffle_btn'), opts={'text': 'Restart'})
                return
            self._toggle_shuffle_state('on', update_btn_label=False)

    def _transfer_item_to_picked_list(self, item_: str) -> None:
        """Remove an item from the shuffle list and put it on the list of picked items.

        :param item_: The item to transfer.
        :type item_: str
        """

        self.state.set('shuffle_list',
                       [item for item in self.state.get('shuffle_list') if item != item_])
        self.state.get('picked').append(item_)
        self.state.get('picked_items_container').add(item_)

    def _start_item_flash_loop(self, i: int) -> None:
        """Start a loop in which items from the shuffle list are shown briefly (flashed) on-screen
        in sequence, one after the other.

        :param i: The index number (zero based) of the item to show (flash).
        :type i: int
        """

        if self.state.get('shuffling_in_progress'):
            try:
                self.state.set('value', lambda it: it.set(self.state.get('shuffle_list')[i]))
            except IndexError:
                i = 0
            else:
                i += 1 if i < len(self.state.get('shuffle_list')) - 1 else \
                    -len(self.state.get('shuffle_list'))
            if self.state.get('shuffling_in_progress'):
                self.after(self.state.get('interval'), lambda: self._start_item_flash_loop(i))

    def _load_shuffle_list(self, fresh: bool = True) -> None:
        """Get the items for the shuffler from the content of the file at path. Each "item" from
        that file is expected to be placed on a separate line. Consider a file with the following
        content:

        ::

            0882918273
            0888123456
            0887192534

        Each of those numbers will turn into an item for the shuffler to work with.

        :param fresh: Wheather a selection of a new items file is intended, defaults to `True`.
        If left at `True`, a file selection window will appear for the user to choose the shuffle
        list source, else the previously chosen items file will be used, if its pat has been stored.
        :type fresh: bool
        """

        if fresh:
            self.state.set('shuffle_list_filepath', ui.file_chooser())
        else:
            if not self.state.get('shuffle_list_filepath'):
                self.state.set('shuffle_list_filepath', ui.file_chooser())
        with open(self.state.get('shuffle_list_filepath'), encoding='utf-8') as file:
            lines = [line.strip(' \n') for line in file.readlines()]
            self.state.set('shuffle_list', list(set(filter(lambda line: line.strip(), lines))))
            self.state.set('value', lambda it: it.set(f'{len(self.state.get("shuffle_list"))} '
                                                       'items loaded. Ready to start.'))

    def _export_picked(self) -> None:
        """Export the list of picked items to a file."""

        if self.state.get('picked'):
            path = ui.file_saver()
            proc = self._get_export_proc(path)
            if proc:
                proc(path)

    def _get_export_proc(self, path: str) -> Optional[callable]:
        """Get the procedure for exporting the picked items. That's done by retreiving the extension
        of the file at `path` and using it to search in the the app's list of supported export
        fromats. For example, if `path` was */path/to/picked-items.xml*, it's assumed that an XML
        export is needed, so the appropriate procedure will returned.

        If the export file's extension does not correspond to a supported file format, ``None`` is
        returned.

        The list of supported formats along with their procedures is stored in this class's
        ``export_formats``.

        :param path: The path to the export file.
        :type path: str
        :return: The export procedure, if a supported export format is detected, `None` otherwise.
        :rtype: Optional[callable]
        """

        _, file = os.path.split(path)
        ext = os.path.splitext(file)[1].lower().strip('.')
        procs = list(filter(lambda it: it[0].lower() == ext, self.export_formats))
        return procs[0][1]

    def _export_txt(self, path: str) -> None:
        """Export the picked items into a .txt file.

        :param path: The full path to the export file.
        :type path: str
        """

        export_plain(items=self.state.get('picked'), path=path)

    def _export_xml(self, path: str) -> None:
        """Export the picked items into a XML file.

        :param path: The full path to the export file.
        :type path: str
        """

        export_xml(root_el_name='Items', child_el_name='Item',
                   items=self.state.get('picked'), path=path)

    def _export_json(self, path: str) -> None:
        """Export the picked items into a .json file.

        :param path: The full path to the export file.
        :type path: str
        """

        export_json(items=self.state.get('picked'), path=path)

    def _reset(self) -> None:
        """"""

        if self.state.get('picked'):
            restart_shuffle = False
            if self.state.get('shuffling_in_progress'):
                self._toggle_shuffle_state('off')
                restart_shuffle = True
            self.state.set('shuffle_list', self.state.get('shuffle_list') +
                                           self.state.get('picked'))
            self.state.set('picked', [])
            self.state.get('picked_items_container').remove_all()
            if restart_shuffle:
                self._toggle_shuffle_state('on')
            else:
                ui.config(self.state.get('shuffle_btn'), opts={'text': 'Start'})
            self.state.get('value').set('Shuffler reset.')

def main() -> None:
    """Start the application."""

    if __name__ == '__main__':
        Application().start()

main()
