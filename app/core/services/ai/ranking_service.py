from collections import defaultdict


class RankingService:

    def specialty_ranking(self, specialties, matched_symptoms):
        scores = defaultdict(float)

        symptom_map = {
            s["id"]: s for s in matched_symptoms
        }

        for s in specialties:
            symptom = symptom_map.get(s.symptom_id)
            if symptom:
                scores[s.specialty_id] += (s.weight * symptom["similarity"])

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],  # [('specialty_id' , 1.90)]
            reverse=True
        )

        return ranked

    def doctor_ranking(self, doctors):
        ranked_doctors = []

        for d in doctors:
            score = (
                    d.rating_avg * 0.6 +
                    d.experience_years * 0.4
                # doctor.available_slots * 0.3
            )

            ranked_doctors.append({
                "id": d.id,
                "full_name": d.full_name,
                "clinic_name": d.clinic_name,
                "rating_avg": d.rating_avg,
                "experience_years": d.experience_years,
                "score": score,
            })

        ranked_doctors.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_doctors[:5]

    def detect_urgency(self, matched_symptoms):
        pass
