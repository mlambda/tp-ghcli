"""Graphical User Interface (GUI) to interact with GitHub issues."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from requests import HTTPError

from .api import create_issue, list_issues
from .io import save_issues_to_file


def _open_list_window() -> None:
    # Crée une nouvelle fenêtre pour lister les issues
    list_window = tk.Toplevel()
    list_window.title("List Issues")  # Définit le titre de la fenêtre

    # Ajoute un cadre (frame) pour organiser les widgets
    frame = ttk.Frame(list_window, padding="10")
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Fonction pour ouvrir une boîte de dialogue et choisir un fichier où sauvegarder
    # les issues
    def browse_file() -> None:
        # Ouvre une boîte de dialogue pour choisir un fichier, avec l'extension .json
        # par défaut
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        # Si l'utilisateur choisit un fichier, le chemin est inséré dans l'entrée
        if file_path:
            entry_outputfile.delete(0, tk.END)  # Efface l'entrée
            entry_outputfile.insert(0, file_path)  # Insère le chemin du fichier

    # Fonction pour récupérer les issues depuis un dépôt GitHub et les sauvegarder dans
    # un fichier
    def retrieve_and_save_issues() -> None:
        # Récupère les valeurs des champs d'entrée
        owner = entry_owner.get()
        repo = entry_repo.get()
        outputfile = entry_outputfile.get()

        # Vérifie que tous les champs sont remplis
        if not owner or not repo or not outputfile:
            messagebox.showerror(
                "Error",
                "Please provide all required inputs: Owner, Repository, and Output "
                "File.",
            )
            return

        # Appelle la fonction pour lister les issues du dépôt
        try:
            issues = list_issues(owner, repo)

            # Si des issues sont récupérées elles sont sauvegardées dans le fichier
            # spécifié
            if issues:
                save_issues_to_file(issues, Path(outputfile))
                messagebox.showinfo(
                    "Success", f"Issues successfully saved to {outputfile}"
                )
        except HTTPError:
            messagebox.showerror(
                "Error", "Failed to retrieve issues. Check the repository details."
            )

    # Création des widgets pour l'interface de la fenêtre
    ttk.Label(frame, text="Owner:").grid(row=0, column=0, padx=10, pady=5)
    entry_owner = ttk.Entry(frame)
    entry_owner.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(frame, text="Repository:").grid(row=1, column=0, padx=10, pady=5)
    entry_repo = ttk.Entry(frame)
    entry_repo.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(frame, text="Output File:").grid(row=2, column=0, padx=10, pady=5)
    entry_outputfile = ttk.Entry(frame)
    entry_outputfile.grid(row=2, column=1, padx=10, pady=5)

    # Bouton pour parcourir les fichiers
    browse_button = ttk.Button(frame, text="Browse", command=browse_file)
    browse_button.grid(row=2, column=2, padx=10, pady=5)

    # Bouton pour récupérer et sauvegarder les issues
    retrieve_button = ttk.Button(
        frame, text="Retrieve and Save Issues", command=retrieve_and_save_issues
    )
    retrieve_button.grid(row=3, column=1, padx=10, pady=10)


def _open_create_window() -> None:
    # Crée une nouvelle fenêtre pour créer une issue
    create_window = tk.Toplevel()
    create_window.title("Create Issue")  # Définit le titre de la fenêtre

    # Ajoute un cadre (frame) pour organiser les widgets
    frame = ttk.Frame(create_window, padding="10")
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Fonction pour soumettre une nouvelle issue
    def submit_issue() -> None:
        # Récupère les valeurs des champs d'entrée
        owner = entry_owner.get()
        repo = entry_repo.get()
        title = entry_title.get()
        body = text_body.get("1.0", tk.END).strip()  # Récupère le contenu de l'issue

        # Vérifie que tous les champs sont remplis
        if owner and repo and title and body:
            # Appelle la fonction pour créer une issue
            try:
                result = create_issue(owner, repo, title, body)
                messagebox.showinfo(
                    "Success", f"Issue created: {result.url}"
                )  # Message de succès
            except HTTPError:
                messagebox.showerror(
                    "Error", "Failed to create the issue. Check your input."
                )
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    # Création des widgets pour l'interface de la fenêtre
    ttk.Label(frame, text="Owner:").grid(row=0, column=0, padx=10, pady=5)
    entry_owner = ttk.Entry(frame)
    entry_owner.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(frame, text="Repository:").grid(row=1, column=0, padx=10, pady=5)
    entry_repo = ttk.Entry(frame)
    entry_repo.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(frame, text="Title:").grid(row=2, column=0, padx=10, pady=5)
    entry_title = ttk.Entry(frame)
    entry_title.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(frame, text="Body:").grid(row=3, column=0, padx=10, pady=5)
    # Zone de texte multiligne pour le corps de l'issue
    text_body = tk.Text(frame, width=40, height=10)
    text_body.grid(row=3, column=1, padx=10, pady=5)

    # Bouton pour soumettre l'issue
    submit_button = ttk.Button(frame, text="Create Issue", command=submit_issue)
    submit_button.grid(row=4, column=1, padx=10, pady=10)


def create_gui() -> None:
    """Create the GHCLI GUI."""
    # Crée la fenêtre principale de l'application
    root = tk.Tk()
    root.title("GHCLI")  # Définit le titre de la fenêtre principale

    # Ajoute un cadre (frame) pour organiser les widgets
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Bouton pour ouvrir la fenêtre de liste des issues
    list_button = ttk.Button(frame, text="List Issues", command=_open_list_window)
    list_button.pack(padx=20, pady=10)

    # Bouton pour ouvrir la fenêtre de création d'une issue
    create_button = ttk.Button(frame, text="Create Issue", command=_open_create_window)
    create_button.pack(padx=20, pady=10)

    # Démarre la boucle principale de Tkinter
    root.mainloop()
