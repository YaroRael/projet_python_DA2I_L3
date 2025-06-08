import tkinter as tk
from tkinter import messagebox, scrolledtext

class PersonnelData:
    def __init__(self):
        """Initialisation avec des données vides"""
        self.data = []  # Liste de [heures_travail, productivité]
        self.labels = []  # Liste des étiquettes (0 ou 1)

    def insert(self, hours, productivity, label):
        """Ajouter un nouvel employé"""
        if not (0 <= hours <= 168 and 0 <= productivity <= 100 and label in [0, 1]):
            raise ValueError("Valeurs invalides : heures (0-168), productivité (0-100), étiquette (0 ou 1)")
        self.data.append([hours, productivity])
        self.labels.append(label)
        return f"Employé ajouté : {hours}h, {productivity}%, {'Performant' if label == 1 else 'Non performant'}"

    def update(self, index, hours=None, productivity=None, label=None):
        """Modifier les données d'un employé"""
        if index < 0 or index >= len(self.data):
            raise ValueError("Index invalide")
        if hours is not None:
            if not 0 <= hours <= 168:
                raise ValueError("Heures de travail doivent être entre 0 et 168")
            self.data[index][0] = hours
        if productivity is not None:
            if not 0 <= productivity <= 100:
                raise ValueError("Productivité doit être entre 0 et 100")
            self.data[index][1] = productivity
        if label is not None:
            if label not in [0, 1]:
                raise ValueError("Étiquette doit être 0 ou 1")
            self.labels[index] = label
        return f"Employé {index} modifié : {self.data[index]}, {'Performant' if self.labels[index] == 1 else 'Non performant'}"

    def delete(self, index):
        """Supprimer un employé"""
        if index < 0 or index >= len(self.data):
            raise ValueError("Index invalide")
        deleted_data = self.data.pop(index)
        deleted_label = self.labels.pop(index)
        return f"Employé supprimé : {deleted_data}, {'Performant' if deleted_label == 1 else 'Non performant'}"

    def get_data(self):
        """Retourner les données actuelles"""
        return self.data, self.labels

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=100):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = 0

    def activation_function(self, x):
        """Fonction d'activation : seuil binaire"""
        return 1 if x >= 0 else 0

    def fit(self, X, y):
        """Entraînement du perceptron"""
        if not X:
            raise ValueError("Aucune donnée pour l'entraînement")
        n_features = len(X[0])
        self.weights = [0] * n_features
        self.bias = 0
        for _ in range(self.n_iterations):
            for i, x_i in enumerate(X):
                linear_output = sum(w * x for w, x in zip(self.weights, x_i)) + self.bias
                y_predicted = self.activation_function(linear_output)
                update = self.lr * (y[i] - y_predicted)
                for j in range(n_features):
                    self.weights[j] += update * x_i[j]
                self.bias += update

    def predict(self, X):
        """Prédiction pour de nouvelles données"""
        predictions = []
        for x_i in X:
            linear_output = sum(w * x for w, x in zip(self.weights, x_i)) + self.bias
            predictions.append(self.activation_function(linear_output))
        return predictions

class PerceptronApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion du Personnel - Perceptron")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f4f8")

        self.data_manager = PersonnelData()
        self.perceptron = None

        # Style
        self.label_font = ("Arial", 12, "bold")
        self.button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 10, "bold"), "relief": "raised"}

        # Titre
        tk.Label(root, text="Gestion du Personnel", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)

        # Boutons pour ouvrir les fenêtres
        tk.Button(root, text="Ajouter un employé", command=self.open_add_window, **self.button_style).pack(pady=5)
        tk.Button(root, text="Modifier un employé", command=self.open_update_window, **self.button_style).pack(pady=5)
        tk.Button(root, text="Supprimer un employé", command=self.open_delete_window, **self.button_style).pack(pady=5)
        tk.Button(root, text="Entraîner le perceptron", command=self.open_train_window, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(root, text="Prédire performance", command=self.open_predict_window, bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(root, text="Voir données et graphique", command=self.open_data_graph_window, bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    def open_add_window(self):
        window = tk.Toplevel(self.root)
        window.title("Ajouter un employé")
        window.geometry("300x200")
        window.configure(bg="#f0f4f8")

        tk.Label(window, text="Heures de travail (0-168):", font=self.label_font, bg="#f0f4f8").pack()
        hours_entry = tk.Entry(window, font=("Arial", 10))
        hours_entry.pack()

        tk.Label(window, text="Productivité (%):", font=self.label_font, bg="#f0f4f8").pack()
        productivity_entry = tk.Entry(window, font=("Arial", 10))
        productivity_entry.pack()

        tk.Label(window, text="Étiquette (1=P, 0=N):", font=self.label_font, bg="#f0f4f8").pack()
        label_entry = tk.Entry(window, font=("Arial", 10))
        label_entry.pack()

        def add():
            try:
                hours = float(hours_entry.get())
                productivity = float(productivity_entry.get())
                label = int(label_entry.get())
                message = self.data_manager.insert(hours, productivity, label)
                messagebox.showinfo("Succès", message)
                window.destroy()
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(window, text="Ajouter", command=add, **self.button_style).pack(pady=10)

    def open_update_window(self):
        window = tk.Toplevel(self.root)
        window.title("Modifier un employé")
        window.geometry("300x250")
        window.configure(bg="#f0f4f8")

        tk.Label(window, text="Index de l'employé:", font=self.label_font, bg="#f0f4f8").pack()
        index_entry = tk.Entry(window, font=("Arial", 10))
        index_entry.pack()

        tk.Label(window, text="Heures de travail (0-168, vide=inchangé):", font=self.label_font, bg="#f0f4f8").pack()
        hours_entry = tk.Entry(window, font=("Arial", 10))
        hours_entry.pack()

        tk.Label(window, text="Productivité (%, vide=inchangé):", font=self.label_font, bg="#f0f4f8").pack()
        productivity_entry = tk.Entry(window, font=("Arial", 10))
        productivity_entry.pack()

        tk.Label(window, text="Étiquette (1=P, 0=N, vide=inchangé):", font=self.label_font, bg="#f0f4f8").pack()
        label_entry = tk.Entry(window, font=("Arial", 10))
        label_entry.pack()

        def update():
            try:
                index = int(index_entry.get())
                hours = float(hours_entry.get()) if hours_entry.get() else None
                productivity = float(productivity_entry.get()) if productivity_entry.get() else None
                label = int(label_entry.get()) if label_entry.get() else None
                message = self.data_manager.update(index, hours, productivity, label)
                messagebox.showinfo("Succès", message)
                window.destroy()
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(window, text="Modifier", command=update, **self.button_style).pack(pady=10)

    def open_delete_window(self):
        window = tk.Toplevel(self.root)
        window.title("Supprimer un employé")
        window.geometry("300x150")
        window.configure(bg="#f0f4f8")

        tk.Label(window, text="Index de l'employé:", font=self.label_font, bg="#f0f4f8").pack()