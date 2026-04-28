from app.api.app import create_app
from app.dependencies import init_cloudinary

app = create_app()

if __name__ == "__main__":
    init_cloudinary()
    app.run(debug=True, use_reloader=False)