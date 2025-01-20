from tkinter import ttk

def sort_column(tree_name: ttk.Treeview, col, reverse=False):
    """
    Sortiert die Einträge einer Spalte in einer `ttk.Treeview`-Tabelle.

    Diese Funktion sortiert die Inhalte der angegebenen Spalte entweder numerisch oder alphanumerisch,
    abhängig vom Datentyp der Spaltenwerte. Zusätzlich wird die Reihenfolge der Einträge im Treeview
    aktualisiert, und die Tags für "oddrow" (ungerade Zeilen) und "evenrow" (gerade Zeilen) werden
    entsprechend neu gesetzt. Der Header der Spalte wird so konfiguriert, dass ein Klick auf den Header
    die Sortierrichtung umkehrt.

    Args:
        tree_name (ttk.Treeview): Die Treeview-Instanz, deren Spalte sortiert werden soll.
        col (str): Der Name der zu sortierenden Spalte.
        reverse (bool, optional): Gibt an, ob die Sortierung in umgekehrter Reihenfolge erfolgen soll.
            Standardmäßig False für aufsteigende Sortierung.

    Raises:
        ValueError: Falls beim Überprüfen von numerischen Werten ein unerwarteter Typ auftritt.

    Notes:
        - Die Funktion überprüft, ob alle Werte in der Spalte numerisch sind (sofern nicht leer)
          und wählt basierend darauf die geeignete Sortierlogik (numerisch oder alphanumerisch).
        - Nach der Sortierung werden die Tags für "oddrow" und "evenrow" neu gesetzt, um ein visuelles
          Unterscheiden der Zeilen zu ermöglichen.
        - Die Funktion modifiziert den Header der Spalte, sodass beim nächsten Klick die Sortierrichtung
          umgekehrt wird.
    """
    # Daten aus der Treeview abrufen
    data = [(tree_name.set(item, col), item) for item in tree_name.get_children('')]

    # Prüfen, ob die Spalte hauptsächlich numerische Daten enthält
    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Entscheiden, ob die Spalte als Zahl oder Text sortiert werden soll
    if all(is_numeric(row[0]) for row in data if row[0] != ''):
        key_func = lambda x: float(x[0])
    else:
        key_func = lambda x: str(x[0])

    # Daten sortieren
    data.sort(key=key_func, reverse=reverse)

    # Reihenfolge in der Treeview aktualisieren
    for index, (_, item) in enumerate(data):
        tree_name.move(item, "", index)

    # Tags für odd/even-Reihen neu setzen
    for index, item in enumerate(tree_name.get_children('')):
        tag = "oddrow" if index % 2 == 0 else "evenrow"
        tree_name.item(item, tags=(tag,))

    # Header aktualisieren, um Sortierrichtung zu wechseln
    tree_name.heading(col, command=lambda c=col: sort_column(tree_name, c, not reverse))
