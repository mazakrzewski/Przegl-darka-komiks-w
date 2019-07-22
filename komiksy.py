#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk , GdkPixbuf
import urllib
import urllib2
from bs4 import BeautifulSoup
import random


class Komix(Gtk.Window):
    """klasa zawierajaca komix."""

    def otwoz_komix(self):
        """otwiera komix jerzeli jest na dysku jesli nie najpierw pobiera go i zapisuje na dysku."""

        url = urllib2.urlopen('http://xkcd.com/' + str(self.aktualny_numer_komix))
        soup = BeautifulSoup(url, 'html.parser')
        self.window.set_title(soup.find(id='ctitle').get_text() + " nr " + str(self.aktualny_numer_komix))
        self.image.set_from_file(str(self.aktualny_numer_komix) + '.jpg')

        try:
            x=GdkPixbuf.Pixbuf.new_from_file(str(self.aktualny_numer_komix) + '.jpg')
            self.image.set_from_pixbuf(x)
            print "komiks byl na dysku"
        except:
            # jesli nie ma komiksu na dysku pobiesz go
            try:
                urllib.urlretrieve("http:" + soup.find(id='comic').img['src'],
                                   str(self.aktualny_numer_komix) + ".jpg")
                self.image.set_from_file(str(self.aktualny_numer_komix) + '.jpg')
            except:
                print "problem z pobraniem komisku"

    def najstarszy_komix(self, btn):
        """Przejscie do najstarszyego komiksu."""
        self.aktualny_numer_komix = 1
        self.otwoz_komix()

    def poprzedni_komix(self, btn):
        """Przejscie do poprzedniego komiksu."""
        if self.aktualny_numer_komix != 1:
            self.aktualny_numer_komix -= 1
            # komiksu 404 niema
            if self.aktualny_numer_komix == 404:
                self.aktualny_numer_komix -= 1
            self.otwoz_komix()
        else:
            print "to jest najstarszy komiks"

    def losowy_komix(self, btn):
        """Przejscie do losowego komiksu."""
        self.aktualny_numer_komix = random.randint(1, self.max_numer_komix)
        if (self.aktualny_numer_komix == 404):
            self.aktualny_numer_komix = 403
        self.otwoz_komix()

    def nastepny_komix(self, btn):
        """Przejscie do nastepnego komiksu."""
        if self.aktualny_numer_komix != self.max_numer_komix:
            self.aktualny_numer_komix += 1
            # komiksu 404 niema
            if self.aktualny_numer_komix == 404:
                self.aktualny_numer_komix += 1
            self.otwoz_komix()
        else:
            print "to jest najnowszy komiks"

    def najnowszy_komix(self, btn):
        """Przejscie do najnowszego komiksu."""
        self.aktualny_numer_komix = self.max_numer_komix
        self.otwoz_komix()

    def wybrany_komix(self, btn):
        """Przejscie_do_wybranego_komiksu."""
        try:
            k = int(self.pole_text.get_text())
            if 0 <= k and k <= self.max_numer_komix and k != 404:
                self.aktualny_numer_komix = k
                self.otwoz_komix()
            else:
                print "komiks nr. " + self.pole_text.get_text() + " nie istnieje"
        except:
            print "\"" + self.pole_text.get_text() + "\"" + " nie jest liczba"

    def __init__(self):
        """Inicjuje powstanie planszy. """
        self.window = Gtk.Window()
        self.window.set_title("komiks")
        self.window.set_default_size(150, 150)
        url = urllib2.urlopen('http://xkcd.com/')
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())
        soup = BeautifulSoup(url, 'html.parser')
        self.max_numer_komix = int(soup.find(rel="prev")['href'].replace("/", "")) + 1
        self.aktualny_numer_komix = self.max_numer_komix
        urllib.urlretrieve("http:" + soup.find(id='comic').img['src'], str(self.aktualny_numer_komix) + ".jpg")

        # ukladam przyciski na siatce
        grid = Gtk.Grid()

        b = Gtk.Button(label="Najstarszy komix")
        grid.attach(b, 0, 0, 1, 2)
        b.connect("clicked", self.najstarszy_komix)

        b = Gtk.Button(label="Poprzedni komix")
        grid.attach(b, 1, 0, 1, 2)
        b.connect("clicked", self.poprzedni_komix)

        b = Gtk.Button(label="Losowy komix")
        grid.attach(b, 2, 0, 1, 2)
        b.connect("clicked", self.losowy_komix)

        self.pole_text = Gtk.Entry()
        self.pole_text.set_text("wybierz komix")
        grid.attach(self.pole_text, 3, 0, 1, 1)

        b = Gtk.Button(label="Ok")
        grid.attach(b, 3, 1, 1, 1)
        b.connect("clicked", self.wybrany_komix)

        b = Gtk.Button(label="Nastepny komix")
        grid.attach(b, 4, 0, 1, 2)
        b.connect("clicked", self.nastepny_komix)

        b = Gtk.Button(label="Najnowszy komix")
        grid.attach(b, 5, 0, 1, 2)
        b.connect("clicked", self.najnowszy_komix)

        self.image = Gtk.Image()
        grid.attach(self.image, 0, 5, 6, 6)
        self.otwoz_komix()
        self.window.add(grid)
        # kolumny maja miec identyczna szerokosc
        grid.set_column_homogeneous(True)
        self.window.show_all()

Komix()
Gtk.main()
