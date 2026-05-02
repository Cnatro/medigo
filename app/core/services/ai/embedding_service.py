from google import genai
from huggingface_hub import InferenceClient

from app.config import Config
import json

client_gemini = genai.Client(api_key=Config.GEMINI_API_KEY)

client_hugging_face = InferenceClient(
    api_key=Config.HUGGING_FACE_API_KEY
)


class EmbeddingService:

    def embed(self, text: str):
        res = client_gemini.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return res.embeddings[0].values

    def sumnary_answer(self, user_input, specialties, doctors, urgency=None):
        SYSTEM_PROMPT = """
                Bạn là trợ lý biên tập nội dung y tế tại Việt Nam.

                QUY TẮC TUYỆT ĐỐI:
                - CHỈ dùng tiếng Việt 100%
                - KHÔNG được dùng tiếng Anh
                - KHÔNG chẩn đoán bệnh
                - KHÔNG thay đổi thông tin bác sĩ hoặc chuyên khoa
                - KHÔNG thêm dữ liệu mới
                
                NHIỆM VỤ:
                - Viết lại nội dung cho tự nhiên, dễ hiểu, mượt mà
                
                OUTPUT:
                - Một đoạn văn tư vấn y tế rõ ràng
                - Có xuống dòng hợp lý
                - Không danh sách dài máy móc
                - CHỈ OUTPUT JSON:

                {
                  "summary": "...",
                  "advice": "..."
                }
                """

        USER_PROMPT = f"""
                Thông tin người dùng:
                {user_input}
        
                Chuyên khoa đã được hệ thống chọn:
                {specialties}
        
                Bác sĩ đề xuất:
                {doctors}
        
                Hãy viết lại thành một đoạn tư vấn y tế mượt mà, dễ hiểu cho người dùng.
                Không thay đổi bất kỳ thông tin nào.
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
