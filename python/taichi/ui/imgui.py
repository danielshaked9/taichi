from contextlib import contextmanager


class Gui:
    """For declaring IMGUI components in a :class:`taichi.ui.Window`
    created by the GGUI system.

    Args:
        gui: reference to a `PyGui`.
    """

    def __init__(self, gui) -> None:
        self.gui = gui

    @contextmanager
    def sub_window(self, name, x, y, width, height):
        """Creating a context manager for subwindow.

        Note:
            All args of this method should align with `begin`.

        Args:
            x (float): The x-coordinate (between 0 and 1) of the top-left \
                corner of the subwindow, relative to the full window.
            y (float): The y-coordinate (between 0 and 1) of the top-left \
                corner of the subwindow, relative to the full window.
            width (float): The width of the subwindow relative to the full window.
            height (float): The height of the subwindow relative to the full window.

        Example::

            >>> with gui.sub_window(name, x, y, width, height) as g:
            >>>     g.text("Hello, World!")
        """
        self.begin(name, x, y, width, height)
        try:
            yield self
        finally:
            self.end()

    def begin(self, name, x, y, width, height):
        """Creates a subwindow that holds imgui widgets.

        All widget function calls (e.g. `text`, `button`) after the `begin`
        and before the next `end` will describe the widgets within this subwindow.

        Args:
            x (float): The x-coordinate (between 0 and 1) of the top-left \
                corner of the subwindow, relative to the full window.
            y (float): The y-coordinate (between 0 and 1) of the top-left \
                corner of the subwindow, relative to the full window.
            width (float): The width of the subwindow relative to the full window.
            height (float): The height of the subwindow relative to the full window.
        """
        self.gui.begin(name, x, y, width, height)

    def end(self):
        """End the description of the current subwindow."""
        self.gui.end()

    def text(self, text, color=None):
        """Declares a line of text."""
        if color is None:
            self.gui.text(text)
        else:
            self.gui.text_colored(text, color)

    def checkbox(self, text, old_value):
        """Declares a checkbox, and returns whether or not it has been checked.

        Args:
            text (str): a line of text to be shown next to the checkbox.
            old_value (bool): whether the checkbox is currently checked.
        """
        return self.gui.checkbox(text, old_value)

    def slider_int(self, text, old_value, minimum, maximum):
        """Declares a slider, and returns its newest value.

        Args:
            text (str): a line of text to be shown next to the slider
            old_value (int) : the current value of the slider.
            minimum (int): the minimum value of the slider.
            maximum (int): the maximum value of the slider.

        Returns:
            int: the updated value of the slider.
        """
        return self.gui.slider_int(text, old_value, minimum, maximum)

    def slider_float(self, text, old_value, minimum, maximum):
        """Declares a slider, and returns its newest value.

        Args:
            text (str): a line of text to be shown next to the slider
            old_value (float): the current value of the slider.
            minimum (float): the minimum value of the slider.
            maximum (float): the maximum value of the slider.
        """
        return self.gui.slider_float(text, old_value, minimum, maximum)

    def color_edit_3(self, text, old_value):
        """Declares a color edit palate.

        Args:
            text (str): a line of text to be shown next to the palate.
            old_value (Tuple[float]): the current value of the color, this \
                should be a tuple of floats in [0,1] that indicates RGB values.
        """
        return self.gui.color_edit_3(text, old_value)

    def button(self, text):
        """Declares a button, and returns whether or not it had just been clicked.

        Args:
            text (str): a line of text to be shown next to the button.
        """
        return self.gui.button(text)

    def input_text(self, text, old_value):
        """Declares a text input box, and returns its newest value.

        Args:
            text (str): a line of text to be shown next to the input box.
            old_value (str): the current value of the text input.

        Returns:
            str: the updated value of the text input.
        """
        return self.gui.input_text(text, old_value)

    def graph(self, title, values, scale_min=None, scale_max=None,
              graph_size_x=0.0, graph_size_y=0.0, overlay_text=""):
        """Declares a line graph widget.

        Args:
            title (str): the title of the graph.
            values (list[float]): the data points to plot.
            scale_min (float or None): minimum scale value, None for auto-scale.
            scale_max (float or None): maximum scale value, None for auto-scale.
            graph_size_x (float): width of the graph, 0 for auto-fit.
            graph_size_y (float): height of the graph, 0 for default.
            overlay_text (str): text shown over the plot area.
        """
        self.gui.graph(title, values, scale_min, scale_max,
                       graph_size_x, graph_size_y, overlay_text)

    def graph_histogram(self, title, values, scale_min=None, scale_max=None,
                        graph_size_x=0.0, graph_size_y=0.0, overlay_text=""):
        """Declares a histogram (bar chart) widget.

        Args:
            title (str): the title of the histogram.
            values (list[float]): the data points to plot.
            scale_min (float or None): minimum scale value, None for auto-scale.
            scale_max (float or None): maximum scale value, None for auto-scale.
            graph_size_x (float): width of the graph, 0 for auto-fit.
            graph_size_y (float): height of the graph, 0 for default.
            overlay_text (str): text shown over the plot area.
        """
        self.gui.graph_histogram(title, values, scale_min, scale_max,
                                 graph_size_x, graph_size_y, overlay_text)

    def combo(self, name, old_value, items):
        """Declares a dropdown combo box.

        Args:
            name (str): label for the combo box.
            old_value (int): current selected index.
            items (list[str]): list of items to display.

        Returns:
            int: the updated selected index.
        """
        return self.gui.combo(name, old_value, items)

    def radio_button(self, name, active):
        """Declares a radio button.

        Args:
            name (str): label for the radio button.
            active (bool): whether the radio button is currently active.

        Returns:
            bool: True if the radio button was clicked.
        """
        return self.gui.radio_button(name, active)

    def listbox(self, name, old_value, items, height_in_items=-1):
        """Declares a scrollable listbox.

        Args:
            name (str): label for the listbox.
            old_value (int): current selected index.
            items (list[str]): list of items to display.
            height_in_items (int): number of visible items (-1 for default).

        Returns:
            int: the updated selected index.
        """
        return self.gui.listbox(name, old_value, items, height_in_items)

    def input_int(self, name, old_value, step=1, step_fast=100):
        """Declares an integer input with +/- step buttons.

        Args:
            name (str): label for the input.
            old_value (int): current value.
            step (int): small step increment.
            step_fast (int): fast step increment.

        Returns:
            int: the updated value.
        """
        return self.gui.input_int(name, old_value, step, step_fast)

    def input_float(self, name, old_value, step=0.0, step_fast=0.0):
        """Declares a float input with +/- step buttons.

        Args:
            name (str): label for the input.
            old_value (float): current value.
            step (float): small step increment.
            step_fast (float): fast step increment.

        Returns:
            float: the updated value.
        """
        return self.gui.input_float(name, old_value, step, step_fast)

    def drag_float(self, name, old_value, speed=1.0, v_min=0.0, v_max=0.0):
        """Declares a click-and-drag float adjustment widget.

        Args:
            name (str): label for the widget.
            old_value (float): current value.
            speed (float): drag speed multiplier.
            v_min (float): minimum value (0.0 for no limit).
            v_max (float): maximum value (0.0 for no limit).

        Returns:
            float: the updated value.
        """
        return self.gui.drag_float(name, old_value, speed, v_min, v_max)

    def drag_int(self, name, old_value, speed=1.0, v_min=0, v_max=0):
        """Declares a click-and-drag integer adjustment widget.

        Args:
            name (str): label for the widget.
            old_value (int): current value.
            speed (float): drag speed multiplier.
            v_min (int): minimum value (0 for no limit).
            v_max (int): maximum value (0 for no limit).

        Returns:
            int: the updated value.
        """
        return self.gui.drag_int(name, old_value, speed, v_min, v_max)

    def progress_bar(self, fraction, size_x=-1.0, size_y=0.0, overlay=""):
        """Declares a horizontal progress bar.

        Args:
            fraction (float): progress value in [0.0, 1.0].
            size_x (float): width of the bar (-1 for auto).
            size_y (float): height of the bar (0 for default).
            overlay (str): text to overlay on the bar.
        """
        self.gui.progress_bar(fraction, size_x, size_y, overlay)

    def separator(self):
        """Declares a horizontal divider line."""
        self.gui.separator()

    def same_line(self, offset=0.0, spacing=-1.0):
        """Places the next widget on the same row.

        Args:
            offset (float): x offset from the start of the line.
            spacing (float): spacing between the previous and next widget.
        """
        self.gui.same_line(offset, spacing)

    def text_wrapped(self, text):
        """Declares word-wrapped text.

        Args:
            text (str): the text to display.
        """
        self.gui.text_wrapped(text)

    def collapsing_header(self, name):
        """Declares an expandable section header.

        Args:
            name (str): label for the header.

        Returns:
            bool: True if the section is open.
        """
        return self.gui.collapsing_header(name)

    def tree_node(self, name):
        """Declares a tree node. Must call tree_pop() if this returns True.

        Args:
            name (str): label for the tree node.

        Returns:
            bool: True if the node is open.
        """
        return self.gui.tree_node(name)

    def tree_pop(self):
        """Closes a tree node opened by tree_node()."""
        self.gui.tree_pop()

    @contextmanager
    def tree(self, name):
        """Context manager for tree nodes. Automatically calls tree_pop().

        Args:
            name (str): label for the tree node.

        Yields:
            bool: True if the node is open.
        """
        opened = self.gui.tree_node(name)
        try:
            yield opened
        finally:
            if opened:
                self.gui.tree_pop()

    def tooltip(self, text):
        """Shows hover text on the previous widget.

        Args:
            text (str): the tooltip text.
        """
        self.gui.tooltip(text)

    def color_edit_4(self, name, old_value):
        """Declares an RGBA color picker.

        Args:
            name (str): label for the color picker.
            old_value (tuple[float]): current RGBA value as a 4-tuple of floats in [0, 1].

        Returns:
            tuple[float]: the updated RGBA value.
        """
        return self.gui.color_edit_4(name, old_value)

    def input_text_multiline(self, name, old_value, width=0.0, height=0.0):
        """Declares a multi-line text editor.

        Args:
            name (str): label for the text editor.
            old_value (str): current text content.
            width (float): width of the editor (0 for auto).
            height (float): height of the editor (0 for auto).

        Returns:
            str: the updated text content.
        """
        return self.gui.input_text_multiline(name, old_value, width, height)

    @contextmanager
    def tab_bar(self, name):
        """Context manager for a tab bar.

        Args:
            name (str): identifier for the tab bar.

        Yields:
            bool: True if the tab bar is visible.
        """
        visible = self.gui.begin_tab_bar(name)
        try:
            yield visible
        finally:
            if visible:
                self.gui.end_tab_bar()

    @contextmanager
    def tab(self, name):
        """Context manager for a tab item inside a tab_bar.

        Args:
            name (str): label for the tab.

        Yields:
            bool: True if this tab is currently selected.
        """
        selected = self.gui.begin_tab_item(name)
        try:
            yield selected
        finally:
            if selected:
                self.gui.end_tab_item()

    @contextmanager
    def table(self, name, column, outer_size_x=0.0, outer_size_y=0.0):
        """Context manager for a table.

        Args:
            name (str): identifier for the table.
            column (int): number of columns.
            outer_size_x (float): outer width (0 for auto).
            outer_size_y (float): outer height (0 for auto).

        Yields:
            bool: True if the table is visible.
        """
        visible = self.gui.begin_table(name, column, outer_size_x, outer_size_y)
        try:
            yield visible
        finally:
            if visible:
                self.gui.end_table()

    def table_next_row(self):
        """Advances to the next row in a table."""
        self.gui.table_next_row()

    def table_next_column(self):
        """Advances to the next column in a table.

        Returns:
            bool: True if the column is visible.
        """
        return self.gui.table_next_column()

    def table_setup_column(self, label):
        """Sets up a column header label in a table.

        Args:
            label (str): the column header text.
        """
        self.gui.table_setup_column(label)

    def table_headers_row(self):
        """Submits a header row for the current table."""
        self.gui.table_headers_row()
