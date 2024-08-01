from django.core.exceptions import ValidationError
import os
import re

def validate_image(file):
	valid_mime_types = ['image/jpeg', 'image/jpg', 'image/png']
	valid_file_extensions = ['.jpg', '.jpeg', '.png']
	max_file_size = 1048576

	ext = os.path.splitext(file.name)[1].lower()
	if ext not in valid_file_extensions:
		raise ValidationError('Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png')

	if file.size > max_file_size:
		raise ValidationError('File size exceeds the maximum limit of 1MB.')

	if file.content_type not in valid_mime_types:
		raise ValidationError('Unsupported file type. Allowed types are: jpeg, jpg, png.')

def validate_password(password):
	if len(password) < 8:
		raise ValidationError("Password must be at least 8 characters long.")

	if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
		raise ValidationError("Password must contain at least one special character.")

	if not re.search(r'\d', password):
		raise ValidationError("Password must contain at least one digit.")
	pass

def validate_username(username):
	if len(username) < 3:
		raise ValidationError("Username must be at least 3 characters long.")
	pass
