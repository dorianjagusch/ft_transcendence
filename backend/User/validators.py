from django.core.exceptions import ValidationError
import os

def validate_image(file):
	valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
	valid_file_extensions = ['.jpg', '.jpeg', '.png', '.gif']
	max_file_size = 2097152

	ext = os.path.splitext(file.name)[1].lower()
	if ext not in valid_file_extensions:
		raise ValidationError('Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png, .gif.')

	if file.size > max_file_size:
		raise ValidationError('File size exceeds the maximum limit of 2MB.')

	if file.content_type not in valid_mime_types:
		raise ValidationError('Unsupported file type. Allowed types are: jpeg, png, gif.')
