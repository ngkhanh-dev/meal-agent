# import json
# # from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from services.menus import get_menus
# import json
# import re
# import os
# from dotenv import load_dotenv
# from tracing import trace_node
# load_dotenv()

# # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0, 
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# def extract_json(raw: str) -> dict:
#     raw = raw.strip()
#     raw = re.sub(r"^```json", "", raw)
#     raw = re.sub(r"```$", "", raw)
    
#     try:
#         return json.loads(raw)
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Invalid JSON from LLM:\n{raw}") from e

# @trace_node("menu_agent")
# def menu_agent(state):

#     time_prompt = f"""
#     Dựa trên yêu cầu của người dùng: "{state['user_message']}", hãy thực hiện:
    
#     1. KIỂM TRA LOGIC:
#        - Nếu không có thông tin ngày: Chỉ trả về "không có thông tin ngày".
#        - Nếu ngày kết thúc sớm hơn ngày bắt đầu: Chỉ trả về "nhập sai logic ngày".
    
#     2. ĐỊNH DẠNG THỜI GIAN:
#        - Chuyển đổi về định dạng: YYYY-MM-DDT01:50:11.098Z.
#        - Nếu chỉ có 1 ngày (A): fromDate = AT01:50:11.098Z, toDate = (A+1)T01:50:11.098Z.
    
#     3. ĐẦU RA JSON (BẮT BUỘC):
#        {{
#          "fromDate": "YYYY-MM-DDT01:50:11.098Z",
#          "toDate": "YYYY-MM-DDT01:50:11.098Z",
#          "isSpecial": 0
#        }}
#     """

#     time_info = llm.invoke(time_prompt).content
#     menus_params = extract_json(time_info)
#     print("*"*1000000000000000000000000000000000000)
#     print(menus_params)
#     menus = get_menus(menus_params["fromDate"], menus_params["toDate"], 0)
    
#     prompt = f"""
#     I. Thông tin menu:
#     {menus}
#     II. Yêu cầu người dùng ({state["user_message"]}):

#         1. Khoảng thời gian: [Điền ngày bắt đầu] đến [Điền ngày kết thúc]
        
#         2. Dữ liệu thực đơn: [Dán văn bản hoặc tải ảnh thực đơn tại đây]
        
#     III. Quy tắc xử lý logic (Ưu tiên theo thứ tự):
        
#         1. Kiểm tra sự tồn tại của ngày: Nếu người dùng không cung cấp thông tin ngày hoặc khoảng ngày: Chỉ trả về duy nhất dòng chữ "không có thông tin ngày" và không nói gì thêm.
        
#         2. Kiểm tra logic ngày: Nếu ngày kết thúc sớm hơn ngày bắt đầu (Ví dụ: từ 30/12 đến 25/12): Chỉ trả về duy nhất dòng chữ "nhập sai logic ngày" và không nói gì thêm.

#         3. Chuyển đổi định dạng thời gian: - Mọi mốc thời gian phải được chuyển về định dạng: YYYY-MM-DDT00:00:00.098Z.

# Nếu user chỉ nhập 1 ngày (a), mốc thời gian sẽ tính từ aT00:00:00.098Z đến (a+1)T00:00:00.098Z.
        
#         4. Trích xuất và Lọc dữ liệu: Đối chiếu lịch phục vụ trong thực đơn với khoảng ngày yêu cầu. Chỉ lấy các món có lịch bán nằm trong khoảng thời gian này.
#     """
    
#     raw = llm.invoke(prompt).content
#     print("ĐÃ ĐẾN ĐÂY")
#     print("RAW LLM OUTPUT:", repr(raw))
#     data = extract_json(raw)
#     print("-"*20)
#     print("DATA: ", data)

#     state["selected_items"] = data["items"]
#     return state

import json
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from services.menus import get_menus
from tracing import trace_node

load_dotenv()

# Sử dụng model ID chính xác để tránh lỗi 404
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0, 
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_json(raw: str) -> dict:
    """Trích xuất khối JSON từ văn bản của LLM một cách an toàn."""
    raw = raw.strip()
    match = re.search(r'(\{.*\}|\[.*\])', raw, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            clean_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)
            try:
                return json.loads(clean_str)
            except:
                return {}
    return {}

@trace_node("menu_agent")
def menu_agent(state: dict):
    """
    Node tra cứu thực đơn. 
    Chỉ thực hiện tìm kiếm và trả về thông tin bổ sung, không thay đổi state gốc.
    """
    user_msg = state.get("user_message", "")
    # Cung cấp ngữ cảnh thời gian thực tế (Năm 2026 theo hệ thống của bạn)
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # --- BƯỚC 1: TRÍCH XUẤT THAM SỐ TÌM KIẾM ---
    time_prompt = f"""
    Hệ thống đang ở thời điểm: {current_time}.
    Dựa trên câu hỏi: "{user_msg}", trích xuất tham số tra cứu menu.
    
    YÊU CẦU:
    1. Trả về JSON với: fromDate, toDate (ISO 8601) và isSpecial (1 nếu là bún/phở/món nước, 0 nếu là cơm).
    2. Nếu người dùng chỉ nói "thứ 2" hoặc "ngày 5", hãy tự tính toán dựa trên ngày hiện tại.

    CHỈ TRẢ VỀ JSON:
    {{
      "fromDate": "YYYY-MM-DDT00:00:00.000Z",
      "toDate": "YYYY-MM-DDT23:59:59.000Z",
      "isSpecial": 0
    }}
    """
    
    try:
        # Gọi LLM lấy tham số
        res = llm.invoke(time_prompt)
        params = extract_json(res.content)
        
        if not params:
            return {"error": "Không thể xác định thời gian tra cứu", "menu_results": []}

        # --- BƯỚC 2: TRA CỨU DỮ LIỆU (LOOKUP ONLY) ---
        # Gọi hàm xử lý logic đã viết ở các bước trước
        found_menus = get_menus(
            from_date_str=params.get("fromDate"), 
            to_date_str=params.get("toDate"), 
            is_special=params.get("isSpecial", 0)
        )
    
        # --- BƯỚC 3: GEN CÂU TRẢ LỜI ---
        # Chuyển list kết quả thành text để LLM đọc
        if found_menus:
            menu_context = ""
            for menu in found_menus:
                menu_context += f"- Ngày {menu['date']}: {', '.join(menu['items'])}\n"
        else:
            menu_context = "Không tìm thấy dữ liệu."

        final_prompt = f"""
        Bạn là trợ lý nhà ăn. Hãy trả lời câu hỏi: "{user_msg}" 
        Dựa trên dữ liệu:
        {menu_context}
        
        Lưu ý: Trình bày đẹp mắt, dễ đọc.
        """
        
        final_res = llm.invoke(final_prompt)
        
        # Trả về state bổ sung
        return {
            # "search_params": params,
            # "menu_results": found_menus,
            "menu_message": final_res.content # Biến bạn cần
        }
        
    except Exception as e:
        print(f"LỖI TẠI MENU_AGENT: {str(e)}")
        return {
            "error": f"Lỗi truy xuất: {str(e)}",
            "menu_results": []
        }