from google import genai
from huggingface_hub import InferenceClient

from app.config import Config

client_gemini = genai.Client(api_key=Config.GEMINI_API_KEY)

client_hugging_face = InferenceClient(
    api_key=Config.HUGGING_FACE_API_KEY
)


class EmbeddingService:

    def embed(self, text: str):
        res = client_gemini.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config={
                "output_dimensionality": 768
            }

        )
        return res.embeddings[0].values

    def sumnary_answer(self, user_input, specialty_names):
        SYSTEM_PROMPT = """
                Bạn là trợ lý hỗ trợ sức khỏe tại Việt Nam.
        
                QUY TẮC:
                - Chỉ dùng tiếng Việt
                - Không chẩn đoán bệnh
                - Không kê thuốc
                - Chỉ đưa lời khuyên cơ bản
        
                Trả về JSON:
        
                {
                  "summary": "...",
                  "advice": "..."
                }
                """

        USER_PROMPT = f"""
        Người dùng mô tả:

        {user_input}

        Chuyên khoa phù hợp:
        {specialty_names}

        Hãy:
        - tóm tắt vấn đề người dùng đang gặp
        - đưa lời khuyên cơ bản
        - khuyên đặt lịch khám nếu cần
        """

        # Mức độ cảnh báo:
        # {urgency}
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT
            }
        ]

        res = client_hugging_face.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
            messages=messages,
            temperature=0.1,
            top_p=0.8,
            max_tokens=600
        )

        return res.choices[0].message.content
