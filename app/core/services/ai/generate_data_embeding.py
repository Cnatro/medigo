from google import genai
import time


client = genai.Client(api_key="AIzaSyDxsZdZeRTckvzDQbfcRPerOPWP_vQd2gY")


def generate_data():
    base_symptoms = [
        "sốt cao kèm ho",
        "khó thở khi vận động",
        "đau ngực dữ dội",
        "tim đập nhanh",
        "chóng mặt liên tục",
        "mất ngủ kéo dài",
        "đau đầu dữ dội",
        "tê tay chân",
        "co giật nhẹ",
        "run tay",
        "mờ mắt",
        "nhìn đôi",
        "ngứa da toàn thân",
        "mụn trứng cá nặng",
        "phát ban dị ứng",
        "nổi mề đay",
        "đau bụng âm ỉ",
        "tiêu chảy nhiều lần",
        "buồn nôn liên tục",
        "quấy khóc trẻ em",
    ]

    levels = ["nhẹ", "trung bình", "nặng"]

    symptoms = []
    for i in range(200):
        s = base_symptoms[i % len(base_symptoms)]
        lv = levels[i % len(levels)]
        symptoms.append(f"{s} mức {lv}")

    # ======================
    # 2. EMBEDDING FUNCTION (768 GEMINI)
    # ======================
    def embed(text):
        res = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return res.embeddings[0].values  # 768 dim

    # ======================
    # 3. GENERATE FILES
    # ======================
    sql_lines = []
    txt_lines = []

    for i, s in enumerate(symptoms, 1):
        sid = f"sym{i:03d}"

        print(f"Embedding {sid}...")

        emb = embed(s)

        # SQL format pgvector
        sql_lines.append(
            f"INSERT INTO symptom(id, name, description, embedding) VALUES "
            f"('{sid}', '{s}', '', '{emb}'::vector);"
        )

        txt_lines.append(s)

        time.sleep(0.2)  # tránh rate limit

    # ======================
    # 4. WRITE FILES
    # ======================
    with open("symptom_200.sql", "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))

    with open("symptom_200.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(txt_lines))

    print("DONE!")


if __name__ == "__main__":
    generate_data()