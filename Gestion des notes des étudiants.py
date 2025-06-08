import tkinter as tk
from tkinter import messagebox, scrolledtext

class StudentData:
    def __init__(self):
        """Initialisation avec des données vides"""
        self.data = []  # Liste de [heures, présence]
        self.labels = []  # Liste des étiquettes (0 ou 1)

    def insert(self, hours, attendance, label):
        """Ajouter un nouvel étudiant"""
        if not (0 <= hours <= 168 and 0 <= attendance <= 100 and label in [0, 1]):
            raise ValueError("Valeurs invalides : heures (0-168), présence (0-100), étiquette (0 ou 1)")
        self.data.append([hours, attendance])
        self.labels.append(label)
        return f"Étudiant ajouté : {hours}h, {attendance}%, {'Réussite' if label == 1 else 'Échec'}"

    def update(self, index, hours=None, attendance=None, label=None):
        """Modifier les données d'un étudiant"""
        if index < 0 or index >= len(self.data):
            raise ValueError("Index invalide")
        if hours is not None:
            if not 0 <= hours <= 168:
                raise ValueError("Heures d'étude doivent être entre 0 et 168")
            self.data[index][0] = hours
        if attendance is not None:
            if not 0 <= attendance <= 100:
                raise ValueError("Présence doit être entre 0 et 100")
            self.data[index][1] = attendance
        if label is not None:
            if label not in [0, 1]:
                raise ValueError("Étiquette doit être 0 ou 1")
            self.labels[index] = label
        return f"Étudiant {index} modifié : {self.data[index]}, {'Réussite' if self.labels[index] == 1 else 'Échec'}"

    def delete(self, index):
        """Supprimer un étudiant"""
        if index < 0 or index >= len(self.data):
            raise ValueError("Index invalide")
        deleted_data = self.data.pop(index)
        deleted_label = self.labels.pop(index)
        return f"Étudiant supprimé : {deleted_data}, {'Réussite' if deleted_label == 1 else 'Échec'}"

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
        self.root.title("Gestion des Étudiants - Perceptron")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")

        self.data_manager = StudentData()
        self.perceptron = None

        # Style
        self.label_font = ("Arial", 12, "bold")
        self.entry_font = ("Arial", 10)
        self.button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 10, "bold"), "relief": "raised"}

        # Titre
        tk.Label(root, text="Gestion des Performances des Étudiants", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)

        # Cadre pour la saisie des données
        frame_input = tk.Frame(root, bg="#f0f4f8")
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Heures d'étude (0-168):", font=self.label_font, bg="#f0f4f8").grid(row=0, column=0, padx=5)
        self.hours_entry = tk.Entry(frame_input, font=self.entry_font)
        self.hours_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Présence (%):", font=self.label_font, bg="#f0f4f8").grid(row=1, column=0, padx=5)
        self.attendance_entry = tk.Entry(frame_input, font=self.entry_font)
        self.attendance_entry.grid(row=1, column=1, padx=5)

        tk.Label(frame_input, text="Étiquette (1=R, 0=E):", font=self.label_font, bg="#f0f4f8").grid(row=2, column=0, padx=5)
        self.label_entry = tk.Entry(frame_input, font=self.entry_font)
        self.label_entry.grid(row=2, column=1, padx=5)

        tk.Label(frame_input, text="Index (pour modif/suppr):", font=self.label_font, bg="#f0f4f8").grid(row=3, column=0, padx=5)
        self.index_entry = tk.Entry(frame_input, font=self.entry_font)
        self.index_entry.grid(row=3, column=1, padx=5)

        # Boutons pour la gestion des données
        frame_buttons = tk.Frame(root, bg="#f0f4f8")
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Ajouter", command=self.add_student, **self.button_style).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Modifier", command=self.update_student, **self.button_style).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Supprimer", command=self.delete_student, **self.button_style).grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="Entraîner", command=self.train_perceptron, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)

        # Zone d'affichage des données
        tk.Label(root, text="Données actuelles:", font=self.label_font, bg="#f0f4f8").pack()
        self.data_display = scrolledtext.ScrolledText(root, width=50, height=8, font=("Arial", 10))
        self.data_display.pack(pady=5)

        # Cadre pour la prédiction
        frame_predict = tk.Frame(root, bg="#f0f4f8")
        frame_predict.pack(pady=10)

        tk.Label(frame_predict, text="Prédiction - Heures:", font=self.label_font, bg="#f0f4f8").grid(row=0, column=0, padx=5)
        self.predict_hours = tk.Entry(frame_predict, font=self.entry_font)
        self.predict_hours.grid(row=0, column=1, padx=5)

        tk.Label(frame_predict, text="Présence (%):", font=self.label_font, bg="#f0f4f8").grid(row=1, column=0, padx=5)
        self.predict_attendance = tk.Entry(frame_predict, font=self.entry_font)
        self.predict_attendance.grid(row=1, column=1, padx=5)

        tk.Button(frame_predict, text="Prédire", command=self.predict, bg="#FF9800", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=5)

        # Zone de résultat de prédiction
        self.result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f4f8", fg="#333")
        self.result_label.pack(pady=5)

    def add_student(self):
        try:
            hours = float(self.hours_entry.get())
            attendance = float(self.attendance_entry.get())
            label = int(self.label_entry.get())
            message = self.data_manager.insert(hours, attendance, label)
            self.update_display(message)
            self.clear_entries()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def update_student(self):
        try:
            index = int(self.index_entry.get())
            hours = float(self.hours_entry.get()) if self.hours_entry.get() else None
            attendance = float(self.attendance_entry.get()) if self.attendance_entry.get() else None
            label = int(self.label_entry.get()) if self.label_entry.get() else None
            message = self.data_manager.update(index, hours, attendance, label)
            self.update_display(message)
            self.clear_entries()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def delete_student(self):
        try:
            index = int(self.index_entry.get())
            message = self.data_manager.delete(index)
            self.update_display(message)
            self.clear_entries()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def train_perceptron(self):
        try:
            data, labels = self.data_manager.get_data()
            if not data:
                messagebox.showerror("Erreur", "Aucune donnée pour l'entraînement")
                return
            self.perceptron = Perceptron(learning_rate=0.01, n_iterations=100)
            self.perceptron.fit(data, labels)
            messagebox.showinfo("Succès", "Perceptron entraîné avec succès !")
            self.update_display("Perceptron entraîné")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def predict(self):
        try:
            if not self.perceptron:
                messagebox.showerror("Erreur", "Entraînez le perceptron d'abord")
                return
            hours = float(self.predict_hours.get())
            attendance = float(self.predict_attendance.get())
            if not (0 <= hours <= 168 and 0 <= attendance <= 100):
                messagebox.showerror("Erreur", "Heures (0-168), présence (0-100)")
                return
            prediction = self.perceptron.predict([[hours, attendance]])[0]
            label = "Réussite" if prediction == 1 else "Échec"
            self.result_label.config(text=f"Prédiction : {hours}h, {attendance}% -> {label}")
            self.predict_hours.delete(0, tk.END)
            self.predict_attendance.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def update_display(self, message):
        self.data_display.delete(1.0, tk.END)
        data, labels = self.data_manager.get_data()
        for i, (d, l) in enumerate(zip(data, labels)):
            self.data_display.insert(tk.END, f"Étudiant {i}: {d[0]}h, {d[1]}%, {'Réussite' if l == 1 else 'Échec'}\n")
        self.data_display.insert(tk.END, f"\n{message}\n")

    def clear_entries(self):
        self.hours_entry.delete(0, tk.END)
        self.attendance_entry.delete(0, tk.END)
        self.label_entry.delete(0, tk.END)
        self.index_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PerceptronApp(root)
    root.mainloop()