import cv2
import numpy as np
from PIL import Image

def analyze_image(image_path, pixel_to_cm=0.026, density=1.0):
    """
    Analyse une image pour extraire la taille, l'épaisseur et estimer le poids de l'objet.
    :param image_path: Chemin de l'image
    :param pixel_to_cm: Facteur de conversion pixel vers cm (par défaut 0.026 cm/pixel pour 96 DPI)
    :param density: Densité de l'objet en g/cm³ (par défaut 1.0)
    :return: Dictionnaire avec les résultats
    """
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Impossible de charger l'image.")

    # Convertir en niveaux de gris et seuillage
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("Aucun objet détecté dans l'image.")

    # Prendre le plus grand contour (objet principal)
    contour = max(contours, key=cv2.contourArea)

    # Calculer la boîte englobante pour la taille
    x, y, w, h = cv2.boundingRect(contour)
    width_cm = w * pixel_to_cm
    height_cm = h * pixel_to_cm

    # Calculer l'épaisseur (approximation via la largeur minimale du contour)
    rect = cv2.minAreaRect(contour)
    thickness_cm = min(rect[1]) * pixel_to_cm

    # Estimer le volume (approximation comme un prisme)
    area_cm2 = cv2.contourArea(contour) * (pixel_to_cm ** 2)
    volume_cm3 = area_cm2 * thickness_cm

    # Estimer le poids (volume * densité)
    weight_g = volume_cm3 * density

    # Retourner les résultats
    return {
        "largeur_cm": round(width_cm, 2),
        "hauteur_cm": round(height_cm, 2),
        "epaisseur_cm": round(thickness_cm, 2),
        "poids_estime_g": round(weight_g, 2)
    }

def main():
    # Exemple d'utilisation
    image_path = "objet.jpg"  # Remplacer par le chemin de votre image
    try:
        results = analyze_image(image_path, pixel_to_cm=0.026, density=1.0)
        print("Résultats de l'analyse :")
        print(f"Largeur : {results['largeur_cm']} cm")
        print(f"Hauteur : {results['hauteur_cm']} cm")
        print(f"Épaisseur : {results['epaisseur_cm']} cm")
        print(f"Poids estimé : {results['poids_estime_g']} g")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()