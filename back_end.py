from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing so frontend can talk to backend without issues
CORS(app)

# Temporary in-memory store for stories (will reset if app restarts)
stories = []

# Root endpoint for basic health check / testing server status
@app.route('/')
def home():
    return jsonify({"message": "BeThSm Backend is alive!"})

# GET all stories - returns stories in reverse chronological order (newest first)
@app.route('/stories', methods=['GET'])
def get_stories():
    return jsonify(stories[::-1])

# POST a new story
@app.route('/stories', methods=['POST'])
def post_story():
    data = request.get_json()  # Get JSON payload from frontend
    # Get user inputs with defaults & sanitization
    nickname = data.get('nickname', 'Anonymous').strip() or 'Anonymous'
    content = data.get('content', '').strip()
    mood = data.get('mood', '🫥 Untagged')
    sensitive = data.get('sensitive', False)

    # Validate content: reject empty stories
    if not content:
        return jsonify({'error': 'Empty story content'}), 400

    # Build new story object with unique ID & timestamp
    new_story = {
        'id': str(uuid.uuid4()),  # Unique identifier for this story
        'nickname': nickname,
        'content': content,
        'mood': mood,
        'sensitive': sensitive,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'comments': [],  # Start with no comments
        'upvotes': 0     # Start with zero upvotes
    }
    stories.append(new_story)  # Save to in-memory list
    return jsonify(new_story), 201  # Return the created story with HTTP 201 Created

# POST a comment to a specific story by story ID
@app.route('/stories/<story_id>/comments', methods=['POST'])
def post_comment(story_id):
    data = request.get_json()
    comment = data.get('comment', '').strip()

    # Reject empty comments
    if not comment:
        return jsonify({'error': 'Empty comment'}), 400

    # Find story by ID
    for story in stories:
        if story['id'] == story_id:
            # Append comment with timestamp and reaction counters
            story['comments'].append({
                'comment': comment,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reactions': {"❤️": 0, "🔥": 0, "😮": 0}  # Reaction emoji counters
            })
            return jsonify(story)  # Return updated story

    # Story not found
    return jsonify({'error': 'Story not found'}), 404

# POST to upvote a story
@app.route('/stories/<story_id>/upvote', methods=['POST'])
def upvote_story(story_id):
    # Find story by ID
    for story in stories:
        if story['id'] == story_id:
            story['upvotes'] += 1  # Increase upvotes count
            return jsonify({'upvotes': story['upvotes']})

    return jsonify({'error': 'Story not found'}), 404

# POST to react to a specific comment on a story
@app.route('/stories/<story_id>/comments/<int:comment_index>/react', methods=['POST'])
def react_to_comment(story_id, comment_index):
    data = request.get_json()
    emoji = data.get('emoji')

    # Validate emoji reaction
    if emoji not in ["❤️", "🔥", "😮"]:
        return jsonify({'error': 'Invalid reaction emoji'}), 400

    # Find story and comment by index
    for story in stories:
        if story['id'] == story_id:
            if 0 <= comment_index < len(story['comments']):
                # Increment reaction count
                story['comments'][comment_index]['reactions'][emoji] += 1
                return jsonify(story['comments'][comment_index])
            else:
                return jsonify({'error': 'Comment index out of range'}), 404

    return jsonify({'error': 'Story not found'}), 404

# GET the featured story based on engagement (comments + upvotes)
@app.route('/featured', methods=['GET'])
def get_featured_story():
    if not stories:
        return jsonify({'message': 'No stories yet'})
    
    # Sort stories by total engagement, descending
    scored = sorted(stories, key=lambda x: len(x['comments']) + x['upvotes'], reverse=True)
    return jsonify(scored[0])

# Run the app in debug mode (auto reloads on code changes)
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing so frontend can talk to backend without issues
CORS(app)

# Temporary in-memory store for stories (will reset if app restarts)
stories = []

# Root endpoint for basic health check / testing server status
@app.route('/')
def home():
    return jsonify({"message": "BeThSm Backend is alive!"})

# GET all stories - returns stories in reverse chronological order (newest first)
@app.route('/stories', methods=['GET'])
def get_stories():
    return jsonify(stories[::-1])

# POST a new story
@app.route('/stories', methods=['POST'])
def post_story():
    data = request.get_json()  # Get JSON payload from frontend
    # Get user inputs with defaults & sanitization
    nickname = data.get('nickname', 'Anonymous').strip() or 'Anonymous'
    content = data.get('content', '').strip()
    mood = data.get('mood', '🫥 Untagged')
    sensitive = data.get('sensitive', False)

    # Validate content: reject empty stories
    if not content:
        return jsonify({'error': 'Empty story content'}), 400

    # Build new story object with unique ID & timestamp
    new_story = {
        'id': str(uuid.uuid4()),  # Unique identifier for this story
        'nickname': nickname,
        'content': content,
        'mood': mood,
        'sensitive': sensitive,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'comments': [],  # Start with no comments
        'upvotes': 0     # Start with zero upvotes
    }
    stories.append(new_story)  # Save to in-memory list
    return jsonify(new_story), 201  # Return the created story with HTTP 201 Created

# POST a comment to a specific story by story ID
@app.route('/stories/<story_id>/comments', methods=['POST'])
def post_comment(story_id):
    data = request.get_json()
    comment = data.get('comment', '').strip()

    # Reject empty comments
    if not comment:
        return jsonify({'error': 'Empty comment'}), 400

    # Find story by ID
    for story in stories:
        if story['id'] == story_id:
            # Append comment with timestamp and reaction counters
            story['comments'].append({
                'comment': comment,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reactions': {"❤️": 0, "🔥": 0, "😮": 0}  # Reaction emoji counters
            })
            return jsonify(story)  # Return updated story

    # Story not found
    return jsonify({'error': 'Story not found'}), 404

# POST to upvote a story
@app.route('/stories/<story_id>/upvote', methods=['POST'])
def upvote_story(story_id):
    # Find story by ID
    for story in stories:
        if story['id'] == story_id:
            story['upvotes'] += 1  # Increase upvotes count
            return jsonify({'upvotes': story['upvotes']})

    return jsonify({'error': 'Story not found'}), 404

# POST to react to a specific comment on a story
@app.route('/stories/<story_id>/comments/<int:comment_index>/react', methods=['POST'])
def react_to_comment(story_id, comment_index):
    data = request.get_json()
    emoji = data.get('emoji')

    # Validate emoji reaction
    if emoji not in ["❤️", "🔥", "😮"]:
        return jsonify({'error': 'Invalid reaction emoji'}), 400

    # Find story and comment by index
    for story in stories:
        if story['id'] == story_id:
            if 0 <= comment_index < len(story['comments']):
                # Increment reaction count
                story['comments'][comment_index]['reactions'][emoji] += 1
                return jsonify(story['comments'][comment_index])
            else:
                return jsonify({'error': 'Comment index out of range'}), 404

    return jsonify({'error': 'Story not found'}), 404

# GET the featured story based on engagement (comments + upvotes)
@app.route('/featured', methods=['GET'])
def get_featured_story():
    if not stories:
        return jsonify({'message': 'No stories yet'})
    
    # Sort stories by total engagement, descending
    scored = sorted(stories, key=lambda x: len(x['comments']) + x['upvotes'], reverse=True)
    return jsonify(scored[0])

# Run the app in debug mode (auto reloads on code changes)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


