import os  # For file path and directory management
import uuid  # For generating unique file names

from flask import Blueprint, current_app, jsonify, request, url_for  
from .extns import db  
from .models import Content  

api = Blueprint("api", __name__)  # Create a Flask Blueprint for the API

@api.post("/set-content")  # Route to set content in the database
def set_content():
    data = request.json  # Retrieve JSON data from the request
    
    try:
        content = Content.query.get(data['id'])  # Check if content exists by ID
        if not content:
            # Create new content if not found
            new_content = Content(id=data['id'], content=data['content'])
            db.session.add(new_content)
        else:
            # Update content if it exists
            content.content = data['content']
        
        db.session.commit()  # Commit the changes to the database
    except:
        db.session.rollback()  # Rollback in case of errors
        return {"success": False}  # Return failure if an exception occurs

    return {"success": True}  # Return success on completion

@api.get('/get-content')  # Route to get all content
def get_content():
    data = Content.query.all()  # Fetch all content from the database
    response = {}

    for d in data:
        response[d.id] = d.content  # Populate response with ID-content pairs

    return response  # Return the response as JSON

@api.post("/verify_password")  # Route to verify a password
def verify_password():
    data = request.json  # Retrieve JSON data from the request

    current_password = "123"  # Hardcoded password for verification
    if data['password'] == current_password:
        return {"success": True}  # Return success if password matches
    
    return {"success": False}  # Return failure if password doesn't match

@api.post("/upload-image")  # Route to handle image uploads
def upload_image():
    file = request.files.get("image")  # Retrieve the uploaded image file
    id = request.form.get('id')  # Fetch 'id' from form data

    # Generate a unique filename for the image
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(current_app.static_folder, filename)  # Create file path

    # Ensure the 'uploads' directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the uploaded file to the static folder
    file.save(file_path)

    # Create a URL for the image to return to the client
    image_url = url_for('static', filename=filename, _external=True)

    # Update the content with the image URL
    content = Content.query.get(id)
    content.content = image_url

    db.session.commit()  # Commit changes to the database

    print(f"Received upload for ID: {id}, File saved as: {file_path}")  # Log the event

    return jsonify({"success": True, "imageUrl": image_url})  # Return success with the image URL