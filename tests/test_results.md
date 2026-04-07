(venv) PS D:\AI In Action\lab4_agent> python -m src.agent.agent
============================================================
TravelBuddy - Trợ lý Du lịch Thông minh
Gõ 'quit' để thoát
============================================================

Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn! Cùng khám phá một số điểm đến thú vị ở Việt Nam nhé. Bạn có ý thích về biển, núi hay văn hóa lịch sử không? Hoặc bạn có ngân sách hay khoảng thời gian cụ thể nào chưa? Mình sẽ giúp bạn chọn điểm đến phù hợp!

Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights ({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Dưới đây là những chuyến bay từ Hà Nội đi Đà Nẵng mà bạn có thể tham khảo:

1. **VietJet Air**
   - Giờ khởi hành: 08:30
   - Giờ đến: 09:50
   - Giá: 890.000 VNĐ (hạng phổ thông)

2. **Bamboo Airways**
   - Giờ khởi hành: 11:00
   - Giờ đến: 12:20
   - Giá: 1.200.000 VNĐ (hạng phổ thông)

3. **Vietnam Airlines**
   - Giờ khởi hành: 06:00
   - Giờ đến: 07:20
   - Giá: 1.450.000 VNĐ (hạng phổ thông)

4. **Vietnam Airlines (Business Class)**
   - Giờ khởi hành: 14:00
   - Giờ đến: 15:20
   - Giá: 2.800.000 VNĐ (hạng thương gia)

Nếu bạn cần thêm thông tin về vé nào hay muốn đặt vé, cứ để mình biết nhé!

Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights ({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels ({'city': 'Phú Quốc'})
Gọi tool: calculate_budget ({'total_budget': 5000000, 'expenses': 'vé máy bay:1100000,khách sạn:1600000'})
Trả lời trực tiếp

TravelBuddy: Dưới đây là gợi ý cho chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm:

**Chuyến bay:**
- **VietJet Air:**
  - Giờ bay: 16:00 (ra) - 18:15 (đến)
  - Giá: 1.100.000₫

**Khách sạn:**
- **Lahana Resort (3 sao):**
  - Giá: 800.000₫/đêm
  - Nằm ở Dương Đông, rất gần biển và nhiều địa điểm tham quan.

**Tổng chi phí ước tính:**
- Vé Máy Bay: 1.100.000₫
- Khách Sạn (2 đêm): 1.600.000₫
- **Tổng: 2.700.000₫**

**Ngân sách còn lại:** 2.300.000₫

**Gợi ý thêm:**
- Với số tiền còn lại, bạn có thể tận hưởng các bữa ăn ngon, tham gia tour khám phá hoặc mua sắm quà lưu niệm. Chúc bạn có chuyến đi thật tuyệt vời!      

Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn có thể cho mình biết bạn muốn đặt khách sạn ở đâu và ngân sách cho mỗi đêm là bao nhiêu không?

Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Xin lỗi, nhưng mình chỉ giúp đỡ về các vấn đề liên quan đến du lịch, đặt vé, và đặt phòng. Nếu bạn có câu hỏi nào về việc lên kế hoạch cho chuyến đi, mình rất sẵn lòng hỗ trợ!

Bạn:


#Test tự động bằng pytest

(venv) PS D:\AI In Action\lab4_agent> pytest -v                   
================================================================== test session starts ==================================================================
platform win32 -- Python 3.11.9, pytest-9.0.2, pluggy-1.6.0 -- D:\AI In Action\lab4_agent\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\AI In Action\lab4_agent
plugins: anyio-4.13.0, langsmith-0.7.26
collected 5 items                                                                                                                                        

tests/test_agent.py::test_direct_answer_no_tool PASSED                                                                                             [ 20%]
tests/test_agent.py::test_single_tool_call_search_flights PASSED                                                                                   [ 40%]
tests/test_agent.py::test_multi_step_tool_chaining PASSED                                                                                          [ 60%]
tests/test_agent.py::test_missing_info_clarification PASSED                                                                                        [ 80%]
tests/test_agent.py::test_guardrail_refusal PASSED                                                                                                 [100%]

=================================================================== 5 passed in 2.31s ===================================================================