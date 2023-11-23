from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Pet
from users.models import Preference

def recommend_pets(user):
    user_pref = Preference.objects.get(adopter=user)
    user_pref_str = ' '.join([str(val) for val in user_pref.__dict__.values()])
    pets = Pet.objects.all()
    pet_strs = [' '.join([str(val) for val in pet.__dict__.values()]) for pet in pets]
    docs = [user_pref_str] + pet_strs
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    sorted_indices = cosine_similarities.argsort()[::-1]
    top_pets = [pets[int(i)] for i in sorted_indices[:5]]
    return top_pets