from tkinter import ttk

def sort_column(tree_name: ttk.Treeview, col, reverse=False):
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
