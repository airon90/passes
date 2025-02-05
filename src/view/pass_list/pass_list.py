# pass_list.py
#
# Copyright 2022 Pablo Sánchez Rodríguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk

from .pass_row import PassRow


@Gtk.Template(resource_path='/me/sanchezrodriguez/passes/pass_list.ui')
class PassList(Gtk.ListBox):

    __gtype_name__ = 'PassList'

    def __init__(self):
        super().__init__()

        self.__selected_row = None
        self.set_header_func(self.on_update_header)
        self.connect('row-activated', self.on_row_activated)

    def bind_model(self, model):
        super().bind_model(model, PassRow)

    def on_row_activated(self, pass_list, pass_row):
        self.__selected_row = pass_row

    def on_update_header(self, row, row_above):
        row_header = row\
            .data()\
            .expiration_date()\
            .as_relative_pretty_string()

        row_above_header = row_above\
            .data()\
            .expiration_date()\
            .as_relative_pretty_string()\
            if row_above else None

        if not row_above or row_header != row_above_header:
            row.show_header()
        else:
            row.hide_header()

    def select_pass_at_index(self, index):
        selected_row = self.get_row_at_index(index)

        if not selected_row:
            selected_row = self.get_row_at_index(0)

        if selected_row:
            self.select_row(selected_row)
            self.emit('row-activated', selected_row)

    def selected_pass(self):
        selected_pass = None

        if self.__selected_row:
            selected_pass = self.__selected_row.data()

        return selected_pass

    def selected_pass_index(self):
        index = None

        if self.__selected_row:
            index = self.__selected_row.get_index()

        return index



    
