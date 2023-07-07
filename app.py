from flask import Flask, request, jsonify, render_template
import spacy

app = Flask(__name__)

# Load the spaCy language model for text processing
nlp = spacy.load('en_core_web_sm')

# Emotion analysis rules based on keywords
emotion_rules = {
    'happy': ['happy', 'joy', 'excited', 'delighted'],
    'sad': ['sad', 'depressed', 'unhappy', 'gloomy'],
    'angry': ['angry', 'frustrated', 'irritated', 'mad'],
    'neutral': ['neutral', 'calm', 'indifferent']
}

# Stress relief techniques based on emotions
stress_relief_techniques = {
    'happy': [
        'Engage in activities you enjoy',
        'Spend time with loved ones',
        'Practice gratitude',
        'Listen to uplifting music',
        'Watch a funny movie',
        'Dance or exercise',
        'Take a walk in nature',
        'Do something creative'
    ],
    'sad': [
        'Engage in self-care activities',
        'Seek support from friends or family',
        'Express your feelings through art or writing',
        'Practice mindfulness or meditation',
        'Read a comforting book',
        'Watch a heartwarming movie',
        'Listen to calming music',
        'Engage in gentle exercises like yoga or stretching'
    ],
    'angry': [
        'Practice deep breathing or meditation',
        'Engage in physical exercise',
        'Take a break to calm down',
        'Write in a journal',
        'Engage in a hobby',
        'Practice assertive communication',
        'Find a healthy outlet for your anger',
        'Seek professional help if needed'
    ],
    'neutral': [
        'Practice mindfulness',
        'Engage in a hobby',
        'Spend time in nature',
        'Take deep breaths',
        'Listen to soothing music',
        'Read a book',
        'Try relaxation techniques',
        'Engage in positive self-talk'
    ]
}

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error rendering template: {str(e)}", 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get user input from the request
        input_data = request.json
        text = input_data['text']
        
        # Perform emotion analysis
        emotion = determine_emotion(text)
        
        # Retrieve the stress relief techniques based on the identified emotion
        stress_relief = retrieve_stress_relief(emotion)
        
        # Prepare the response
        response = {
            'emotion': emotion,
            'stress_relief': stress_relief
        }
        
        return jsonify(response)
    except Exception as e:
        return f"Error processing chat: {str(e)}", 500

def determine_emotion(text):
    # Process the text using spaCy
    doc = nlp(text)
    
    # Initialize emotion scores
    emotion_scores = {emotion: 0 for emotion in emotion_rules}
    
    # Calculate emotion scores based on keyword matching
    for emotion, keywords in emotion_rules.items():
        for keyword in keywords:
            if keyword in text:
                emotion_scores[emotion] += 1
    
    # Determine the dominant emotion based on the scores
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # If no emotion is matched, default to neutral
    if emotion_scores[dominant_emotion] == 0:
        dominant_emotion = 'neutral'
    
    return dominant_emotion

def retrieve_stress_relief(emotion):
    # Retrieve the stress relief techniques based on the identified emotion
    return stress_relief_techniques.get(emotion, [])

if __name__ == '__main__':
    app.debug = True  # Enable debug mode for detailed error messages
    app.run()
