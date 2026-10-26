import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("LLM_MODEL")

if not api_key:
    raise ValueError("GOOGLE_API_KEY chưa được cấu hình")

if not model_name:
    raise ValueError("LLM_MODEL chưa được cấu hình")

client = genai.Client(api_key=api_key)

try:
    print(f"Đang kiểm tra model: {model_name}")

    response = client.models.generate_content(
        model=model_name,
        contents=(
            "Trả lời bằng tiếng Việt, ngắn gọn: "
            "Lệnh git fetch khác git pull như thế nào?"
        ),
    )

    print("\n===== GEMINI RESPONSE =====")
    print(response.text or "Model không trả về văn bản.")

finally:
    client.close()