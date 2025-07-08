from src.utils import load_object

if __name__ == "__main__":
    preprocessor = load_object("artifacts/preprocessor.pkl")
    print("🧾 الأعمدة المطلوبة من preprocessor:")
    print(preprocessor.feature_names_in_)
