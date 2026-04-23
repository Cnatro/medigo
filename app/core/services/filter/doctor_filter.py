from app.infrastructure.models import DoctorModel, UserModel, SpecialtyModel


class DoctorFilter:
    def __init__(self, query, params):
        self.query = query
        self.params = params

    def apply(self):

        if self.params.get("specialties"):
            self.query = self.query.filter(
                SpecialtyModel.id.in_(self.params["specialties"])
            )

        if self.params.get("name"):
            self.query = self.query.filter(
                UserModel.full_name.ilike(f"%{self.params['name']}%")
            )


        if self.params.get("min_experience"):
            self.query = self.query.filter(
                DoctorModel.experience_years >= self.params["min_experience"]
            )


        if self.params.get("min_rating"):
            self.query = self.query.filter(
                DoctorModel.rating_avg >= self.params["min_rating"]
            )

        return self.query