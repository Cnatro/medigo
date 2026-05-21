from firebase_admin import auth


class FirebaseService:

    @staticmethod
    def verify_token(id_token):

        try:
            decoded_token = auth.verify_id_token(id_token)

            return {
                "uid": decoded_token.get("uid"),
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture")
            }

        except Exception as e:
            raise Exception(f"Invalid firebase token: {str(e)}")
