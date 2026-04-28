import cloudinary.uploader

class CloudinaryService:

    @staticmethod
    def upload_image(file, folder="medigo-avatar"):
        result = cloudinary.uploader.upload(
            file,
            folder=folder
        )
        return result.get("secure_url")