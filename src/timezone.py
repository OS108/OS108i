#!/usr/bin/env python3

from gi.repository import Gtk
import os.path
import os
from sys_handler import timezone_dictionary
# Folder use for the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"
time = '%stimezone' % tmp
tzdictionary = timezone_dictionary()


class TimeZone:

    def continent_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>Continent</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def city_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>City</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def Continent_Selection(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
        self.city_store.clear()
        if treeiter is not None:
            value = model[treeiter][0]
            self.continent = value
            for line in tzdictionary[self.continent]:
                self.city_store.append(None, [line])
            self.citytreeView.set_cursor(0)

    def City_Selection(self, tree_selection, button3):
        model, treeiter = tree_selection.get_selected()
        if treeiter is not None:
            value = model[treeiter][0]
            self.city = value
            button3.set_sensitive(True)
        # else:
        #     button3.set_sensitive(False)

    def save_selection(self):
        timezone = '%s/%s' % (self.continent, self.city)
        time_file = open(time, 'w')
        time_file.writelines(timezone)
        time_file.close()
        return

    def __init__(self, button3):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        table = Gtk.Table(1, 2, True)
        tzTitle = '<b><span size="xx-large">Time Zone Selection</span></b>'
        label = Gtk.Label(tzTitle)
        label.set_use_markup(True)
        table.attach(label, 0, 2, 0, 1)
        box2.pack_start(table, False, False, 0)
        hbox = Gtk.HBox(False, 10)
        hbox.set_border_width(5)
        box2.pack_start(hbox, True, True, 5)
        hbox.show()

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str)
        for line in tzdictionary:
            store.append(None, [line])
        self.continenttreeView = Gtk.TreeView(store)
        self.continenttreeView.set_model(store)
        self.continenttreeView.set_rules_hint(True)
        self.continent_columns(self.continenttreeView)
        self.continenttree_selection = self.continenttreeView.get_selection()
        self.continenttree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.continenttree_selection.connect("changed",
                                             self.Continent_Selection)
        sw.add(self.continenttreeView)
        sw.show()
        hbox.pack_start(sw, True, True, 5)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.city_store = Gtk.TreeStore(str)
        self.citytreeView = Gtk.TreeView(self.city_store)
        self.citytreeView.set_model(self.city_store)
        self.citytreeView.set_rules_hint(True)
        self.city_columns(self.citytreeView)
        tree_selection = self.citytreeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.City_Selection, button3)
        sw.add(self.citytreeView)
        sw.show()
        hbox.pack_start(sw, True, True, 5)
        return

    def get_model(self):
        self.continenttreeView.set_cursor(1)
        return self.box1
