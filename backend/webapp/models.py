from .extns import db  # Import the database object

# Define the 'Content' model which represents a table in the database
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each content item
    content = db.Column(db.Text)  # Field to store the content (text or image URL)
    