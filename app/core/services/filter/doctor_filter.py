from sqlalchemy import or_

from app.infrastructure.models import DoctorModel, UserModel, SpecialtyModel, ClinicModel, DoctorSpecialtyModel


class DoctorFilter:
    def __init__(self, query, params):
        self.query = query
        self.params = params

    def get_single(self, key, default=""):
        value = self.params.get(key, default)

        if isinstance(value, list):
            return value[0]

        return value

    def get_list(self, key):
        value = self.params.get(key)

        if value is None:
            value = self.params.get(f"{key}[]")

        if isinstance(value, list):
            return value

        if value is None:
            return []

        return [value]

    def apply(self):

        search = self.get_single("search").strip()
        if search:
            keyword = f"%{search}%"
            self.query = self.query.filter(
                or_(
                    UserModel.full_name.ilike(keyword),
                    SpecialtyModel.name.ilike(keyword),
                    ClinicModel.name.ilike(keyword),
                )
            )

        specialties = self.get_list("specialties")
        if specialties:
            self.query = self.query.filter(
                DoctorSpecialtyModel.specialty_id.in_(specialties)
            )

        clinics = self.get_list("clinics")
        if clinics:
            self.query = self.query.filter(
                DoctorModel.clinic_id.in_(clinics)
            )

        min_price = float(self.get_single("minPrice", 0))
        if min_price is not None:
            self.query = self.query.filter(
                DoctorSpecialtyModel.consultation_fee >= float(min_price)
            )

        max_price = float(self.get_single("maxPrice", 999999999))
        if max_price is not None:
            self.query = self.query.filter(
                DoctorSpecialtyModel.consultation_fee <= float(max_price)
            )

        min_rating = float(self.get_single("minRating", 0))
        if min_rating:
            self.query = self.query.filter(
                DoctorModel.rating_avg >= float(min_rating)
            )

        sort_by = self.get_single("sortBy")
        if sort_by == 'createdAt':
            self.query = self.query.order_by(DoctorModel.created_at.desc())
        elif sort_by == "rating":
            self.query = self.query.order_by(DoctorModel.rating_avg.desc())

        elif sort_by == "price_asc":
            self.query = self.query.order_by(DoctorSpecialtyModel.consultation_fee)

        elif sort_by == "price_desc":
            self.query = self.query.order_by(DoctorSpecialtyModel.consultation_fee)

        return self.query
