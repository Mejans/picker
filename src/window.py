# Copyright 2024 MezoAhmedII
# SPDX-License-Identifier: GPL-3.0-or-later

from random import choice
from gettext import gettext as __
from gi.repository import Gtk, Gio, Adw, Gdk

@Gtk.Template(resource_path='/io/github/mezoahmedii/Picker/window.ui')
class PickerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PickerWindow'

    elementsList = Gtk.Template.Child()
    entryRow = Adw.EntryRow(title=__("Add something..."), show_apply_button=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings(schema_id="io.github.mezoahmedii.Picker")

        self.settings.bind("width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("is-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("is-fullscreen", self, "fullscreened",
                           Gio.SettingsBindFlags.DEFAULT)

        self.createAction("chooseElement", self.onChooseElement)

        self.entryRow.connect("apply", self.onEnterElement, _)
        self.elementsList.add(self.entryRow)

    def onEnterElement(self, widget, __):
        if bool(self.entryRow.get_text().strip()):
            actionRow = Adw.ActionRow(title=self.entryRow.get_text().strip().replace("&", "&amp;"))
            removeButton = Gtk.Button(icon_name="remove-symbolic",
                                      valign="center")
            removeButton.get_style_context().add_class("destructive-action")
            removeButton.connect("clicked", self.removeElement, actionRow)
            actionRow.add_suffix(removeButton)
            self.elementsList.add(actionRow)
            self.entryRow.set_text("")
            self.entryRow.set_show_apply_button(False)
            self.entryRow.set_show_apply_button(True)

    def onChooseElement(self, widget, _):
        elements = []
        child = self.entryRow.get_parent().get_first_child()
        while child is not None:
            elements.append(child)
            child = child.get_next_sibling()
        elements.pop(0)
        chosenElement = ""

        dialog = Adw.AlertDialog()

        dialog.add_response("dismiss", __("Okay"))
        dialog.set_default_response("dismiss")

        if elements == []:
            dialog.set_heading(__("Nothing to choose from"))
            dialog.set_body(__("Please enter some things to be chosen from."))
        else:
            chosenElement = choice(elements)
            dialog.set_heading(chosenElement.get_title().replace("&amp;", "&"))
            dialog.set_body(__("has been chosen!"))
            dialog.add_response("copy", __("Copy it"))
            dialog.set_response_appearance("copy",
                                           Adw.ResponseAppearance.SUGGESTED)
            dialog.add_response("remove", __("Remove it"))
            dialog.set_response_appearance("remove",
                                           Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.choose(self, None, self.onDialogResponse, chosenElement)

    def removeElement(self, widget, element):
        self.elementsList.remove(element)

    def onDialogResponse(self, dialog, task, element):
        response = dialog.choose_finish(task)
        if response == "copy":
            Gdk.Display.get_default().get_clipboard().set(element.get_title())
        if response == "remove":
            self.removeElement(None, element)

    def createAction(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)


