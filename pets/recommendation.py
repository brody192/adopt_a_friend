from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Pet
from users.models import Preference

def recommend_pets(user):
    # Get user's preferences
    user_pref = Preference.objects.get(adopter=user)

    # Convert user's preferences to a string
    user_pref_str = ' '.join([str(val) for val in user_pref.__dict__.values()])

    # Get all pets and convert their attributes to strings
    pets = Pet.objects.all()
    pet_strs = [' '.join([str(val) for val in pet.__dict__.values()]) for pet in pets]

    # Create a list with the user's preferences and all pets
    docs = [user_pref_str] + pet_strs

    # Convert the categorical data to numerical data with TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)

    # Calculate the cosine similarity between the user's preferences and each pet
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get the indices of the pets sorted by similarity
    sorted_indices = cosine_similarities.argsort()[::-1]

    # Return the top 5 pets
    top_pets = [pets[int(i)] for i in sorted_indices[:5]]
    return top_pets