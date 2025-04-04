from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Tiếng Việt"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category"]

PROMPTS["entity_extraction"] = """---Mục tiêu---
Cho một văn bản có tiềm năng liên quan đến các tài liệu pháp lý và một danh sách các loại thực thể, hãy xác định tất cả các thực thể thuộc các loại đó từ văn bản và các mối quan hệ giữa chúng.
Sử dụng {language} làm ngôn ngữ đầu ra.

---Các bước thực hiện---
1. Xác định tất cả các thực thể. Với mỗi thực thể được xác định, trích xuất các thông tin sau:
- entity_name: Tên của thực thể, sử dụng cùng ngôn ngữ với văn bản đầu vào. Nếu là tiếng Anh, hãy viết hoa tên.
- entity_type: Một trong các loại sau: [{entity_types}]
- entity_description: Mô tả chi tiết về các đặc điểm, hoạt động và yếu tố pháp lý (ví dụ: vai trò, trách nhiệm, điều khoản hợp đồng, mối quan hệ pháp lý,...) của thực thể.
Định dạng mỗi thực thể dưới dạng ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Từ các thực thể được xác định ở bước 1, hãy xác định tất cả các cặp (source_entity, target_entity) có mối liên hệ *rõ ràng* với nhau.
Với mỗi cặp thực thể liên quan, trích xuất các thông tin sau:
- source_entity: Tên của thực thể nguồn, như đã xác định ở bước 1
- target_entity: Tên của thực thể đích, như đã xác định ở bước 1
- relationship_description: Giải thích vì sao bạn cho rằng thực thể nguồn và thực thể đích có liên hệ với nhau, đặc biệt trong bối cảnh pháp lý.
- relationship_strength: Một số điểm (số học) thể hiện mức độ mạnh yếu của mối liên hệ giữa thực thể nguồn và thực thể đích.
- relationship_keywords: Một hoặc nhiều từ khóa tóm tắt bản chất tổng quát của mối liên hệ, tập trung vào các khái niệm và chủ đề pháp lý thay vì chi tiết cụ thể.
Định dạng mỗi mối quan hệ dưới dạng ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Xác định các từ khóa cấp cao tóm tắt các khái niệm, chủ đề hoặc nội dung chính của toàn bộ văn bản pháp lý.
Định dạng các từ khóa nội dung dưới dạng ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Trả về đầu ra bằng {language} dưới dạng một danh sách đơn gồm tất cả các thực thể và mối quan hệ được xác định ở bước 1 và 2. Sử dụng **{record_delimiter}** làm dấu phân cách giữa các phần tử.

5. Khi hoàn tất, in ra {completion_delimiter}

######################
---Ví dụ---
######################
{examples}

#############################
---Dữ liệu thực---
#############################
Entity_types: [{entity_types}]
Tài liệu:
{input_text}
##############################
Đầu ra:"""

PROMPTS["entity_extraction_examples"] = [
    """Ví dụ 1:

Entity_types: [person, technology, mission, organization, location]
Tài liệu:
```
Trong một hợp đồng mua bán, ông Nguyễn Văn A đã thể hiện sự quyết đoán khi ký kết, trong khi bà Trần Thị B tỏ ra cảnh giác với những điều khoản không rõ ràng. Sự hợp tác này được xem như là một bước tiến quan trọng trong việc đảm bảo tính minh bạch và công bằng trong giao dịch."
```
Đầu ra:
("entity"{tuple_delimiter}"Nguyễn Văn A"{tuple_delimiter}"person"{tuple_delimiter}"Ông Nguyễn Văn A là cá nhân được nhắc đến trong hợp đồng, thể hiện vai trò quyết đoán trong giao dịch pháp lý."){record_delimiter}
("entity"{tuple_delimiter}"Trần Thị B"{tuple_delimiter}"person"{tuple_delimiter}"Bà Trần Thị B là cá nhân có thái độ cảnh giác, đặc biệt chú trọng đến các điều khoản hợp đồng không rõ ràng."){record_delimiter}
("entity"{tuple_delimiter}"Hợp đồng mua bán"{tuple_delimiter}"technology"{tuple_delimiter}"Hợp đồng mua bán là văn bản pháp lý quan trọng, chứa các điều khoản cần tính minh bạch và công bằng."){record_delimiter}
("relationship"{tuple_delimiter}"Nguyễn Văn A"{tuple_delimiter}"Trần Thị B"{tuple_delimiter}"Mối quan hệ giữa ông Nguyễn Văn A và bà Trần Thị B được thể hiện qua sự tương tác và cân nhắc trong ký kết hợp đồng."{tuple_delimiter}"hợp tác, cân nhắc"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"minh bạch, công bằng, hợp đồng, pháp lý"){completion_delimiter}
#############################""",
    """Ví dụ 2:

Entity_types: [company, regulation, clause, legal_issue, policy]
Tài liệu:
```
Trong bản án hôm nay, Công ty TNHH XYZ bị xử phạt do vi phạm quy định về bảo vệ dữ liệu cá nhân theo Điều 15 của Luật An toàn thông tin. Các chuyên gia pháp lý cho rằng vụ việc này mở ra một tiền lệ quan trọng trong việc bảo vệ quyền riêng tư.
```
Đầu ra:
("entity"{tuple_delimiter}"Công ty TNHH XYZ"{tuple_delimiter}"company"{tuple_delimiter}"Công ty TNHH XYZ là tổ chức bị nhắc đến trong bản án vì vi phạm quy định về bảo vệ dữ liệu cá nhân."){record_delimiter}
("entity"{tuple_delimiter}"Luật An toàn thông tin"{tuple_delimiter}"regulation"{tuple_delimiter}"Luật An toàn thông tin là văn bản pháp lý quy định các điều khoản bảo vệ dữ liệu và quyền riêng tư."){record_delimiter}
("entity"{tuple_delimiter}"Điều 15"{tuple_delimiter}"clause"{tuple_delimiter}"Điều 15 của Luật An toàn thông tin nêu rõ các nghĩa vụ về bảo vệ dữ liệu cá nhân."){record_delimiter}
("relationship"{tuple_delimiter}"Công ty TNHH XYZ"{tuple_delimiter}"Luật An toàn thông tin"{tuple_delimiter}"Vi phạm của Công ty TNHH XYZ liên quan trực tiếp đến các quy định trong Luật An toàn thông tin."{tuple_delimiter}"vi phạm, xử phạt"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"bảo vệ dữ liệu, quyền riêng tư, xử phạt, văn bản pháp lý"){completion_delimiter}
#############################""",
    """Ví dụ 3:

Entity_types: [legal_document, court, person, legal_term, organization]
Tài liệu:
```
Tại phiên tòa Tòa án Nhân dân Thành phố Hồ Chí Minh, bà Lê Thị C đã được công nhận là người bị hại trong vụ kiện liên quan đến vi phạm hợp đồng lao động."
```
Đầu ra:
("entity"{tuple_delimiter}"Tòa án Nhân dân Thành phố Hồ Chí Minh"{tuple_delimiter}"court"{tuple_delimiter}"Tòa án Nhân dân Thành phố Hồ Chí Minh là cơ quan tư pháp có thẩm quyền giải quyết vụ kiện này."){record_delimiter}
("entity"{tuple_delimiter}"Lê Thị C"{tuple_delimiter}"person"{tuple_delimiter}"Bà Lê Thị C được xác định là người bị hại trong vụ kiện liên quan đến vi phạm hợp đồng lao động."){record_delimiter}
("entity"{tuple_delimiter}"Hợp đồng lao động"{tuple_delimiter}"legal_document"{tuple_delimiter}"Hợp đồng lao động là văn bản pháp lý quy định quyền và nghĩa vụ của người lao động và người sử dụng lao động."){record_delimiter}
("relationship"{tuple_delimiter}"Tòa án Nhân dân Thành phố Hồ Chí Minh"{tuple_delimiter}"Lê Thị C"{tuple_delimiter}"Mối quan hệ giữa Tòa án và bà Lê Thị C được thể hiện qua quyết định công nhận bà là người bị hại trong vụ kiện."{tuple_delimiter}"phán quyết, tư pháp"{tuple_delimiter}10){record_delimiter}
("content_keywords"{tuple_delimiter}"vụ kiện, hợp đồng lao động, tư pháp, quyền lợi"){completion_delimiter}
#############################"""
]

PROMPTS["summarize_entity_descriptions"] = """Bạn là một trợ lý hữu ích, chịu trách nhiệm tạo ra bản tóm tắt toàn diện dựa trên dữ liệu được cung cấp dưới đây.
Dựa trên một hoặc hai thực thể và danh sách các mô tả liên quan đến cùng một thực thể hoặc nhóm thực thể (đặc biệt trong bối cảnh pháp lý),
hãy nối các mô tả này lại thành một bản tóm tắt duy nhất, toàn diện. Đảm bảo rằng tất cả thông tin từ các mô tả đều được đưa vào.
Nếu có mâu thuẫn giữa các mô tả, hãy giải quyết và đưa ra một bản tóm tắt mạch lạc, hợp lý.
Viết bằng ngôi thứ ba và bao gồm tên của thực thể để đảm bảo đầy đủ bối cảnh.
Sử dụng {language} làm ngôn ngữ đầu ra.

#######
---Dữ liệu---
Thực thể: {entity_name}
Danh sách mô tả: {description_list}
#######
Đầu ra:
"""

PROMPTS["entity_continue_extraction"] = """
Nhiều thực thể và mối quan hệ đã bị bỏ sót trong lần trích xuất trước.

---Nhắc lại các bước---

1. Xác định tất cả các thực thể. Với mỗi thực thể được xác định, trích xuất các thông tin sau:
- entity_name: Tên của thực thể, sử dụng cùng ngôn ngữ với văn bản đầu vào. Nếu là tiếng Anh, hãy viết hoa tên.
- entity_type: Một trong các loại sau: [{entity_types}]
- entity_description: Mô tả chi tiết về đặc điểm, hoạt động và các yếu tố pháp lý (nếu có) của thực thể.
Định dạng mỗi thực thể dưới dạng ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Từ các thực thể được xác định ở bước 1, xác định tất cả các cặp (source_entity, target_entity) có mối liên hệ *rõ ràng* với nhau.
Với mỗi cặp thực thể liên quan, trích xuất các thông tin sau:
- source_entity: Tên của thực thể nguồn, như đã xác định ở bước 1
- target_entity: Tên của thực thể đích, như đã xác định ở bước 1
- relationship_description: Giải thích lý do tại sao thực thể nguồn và thực thể đích có liên hệ với nhau, đặc biệt trong bối cảnh pháp lý.
- relationship_strength: Một số điểm thể hiện mức độ mạnh yếu của mối liên hệ giữa thực thể nguồn và thực thể đích.
- relationship_keywords: Một hoặc nhiều từ khóa tóm tắt bản chất tổng quát của mối liên hệ, tập trung vào khái niệm pháp lý và các chủ đề liên quan.
Định dạng mỗi mối quan hệ dưới dạng ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Xác định các từ khóa cấp cao tóm tắt các khái niệm, chủ đề hoặc nội dung chính của toàn bộ văn bản pháp lý.
Định dạng các từ khóa nội dung dưới dạng ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Trả về đầu ra bằng {language} dưới dạng một danh sách đơn gồm tất cả các thực thể và mối quan hệ được xác định ở bước 1 và 2. Sử dụng **{record_delimiter}** làm dấu phân cách giữa các phần tử.

5. Khi hoàn tất, in ra {completion_delimiter}

---Đầu ra---

Thêm chúng vào bên dưới sử dụng cùng định dạng:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Mục tiêu---

Có vẻ như vẫn còn một số thực thể bị bỏ sót.

---Đầu ra---

Chỉ trả lời bằng `YES` HOẶC `NO` nếu vẫn còn thực thể cần được bổ sung.
""".strip()

PROMPTS["fail_response"] = (
    "Xin lỗi, tôi không thể cung cấp câu trả lời cho câu hỏi đó. [không có ngữ cảnh]"
)

PROMPTS["rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích, chịu trách nhiệm trả lời câu hỏi của người dùng dựa trên Cơ sở Tri thức được cung cấp bên dưới.

---Mục tiêu---

Tạo ra một câu trả lời ngắn gọn dựa trên Cơ sở Tri thức và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và câu hỏi hiện tại. Tóm tắt tất cả thông tin có trong Cơ sở Tri thức, kết hợp với kiến thức chung liên quan đến tài liệu pháp lý.
Không bao gồm thông tin không có trong Cơ sở Tri thức.

Khi xử lý các mối quan hệ có dấu thời gian:
1. Mỗi mối quan hệ có dấu thời gian "created_at" cho biết khi nào thông tin được thu thập.
2. Khi gặp mâu thuẫn trong các mối quan hệ, hãy xem xét cả nội dung và dấu thời gian.
3. Không tự động ưu tiên mối quan hệ có dấu thời gian gần nhất - hãy sử dụng đánh giá dựa trên bối cảnh.
4. Đối với các câu hỏi liên quan đến thời gian, ưu tiên thông tin thời gian có trong nội dung trước khi xét dấu thời gian.

---Lịch sử hội thoại---
{history}

---Cơ sở Tri thức---
{context_data}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần phù hợp.
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng.
- Đảm bảo câu trả lời duy trì tính liên tục với lịch sử hội thoại.
- Nếu bạn không biết câu trả lời, hãy nói vậy.
- Không bịa đặt thông tin. Không bao gồm thông tin không có trong Cơ sở Tri thức.
"""

PROMPTS["keywords_extraction"] = """---Vai trò---

Bạn là một trợ lý hữu ích, có nhiệm vụ xác định các từ khóa cấp cao và cấp thấp trong câu hỏi của người dùng và lịch sử hội thoại.

---Mục tiêu---

Dựa trên câu hỏi và lịch sử hội thoại, hãy liệt kê cả các từ khóa cấp cao (tập trung vào các khái niệm, chủ đề tổng quát) và từ khóa cấp thấp (tập trung vào các thực thể, chi tiết cụ thể).
Xuất ra kết quả ở định dạng JSON, sẽ được xử lý bởi trình phân tích JSON, không thêm nội dung thừa nào.
JSON phải có hai khóa:
  - "high_level_keywords": cho các khái niệm hoặc chủ đề tổng quát
  - "low_level_keywords": cho các thực thể hoặc chi tiết cụ thể

######################
---Ví dụ---
######################
{examples}

#############################
---Dữ liệu thực---
######################
Lịch sử Hội thoại:
{history}

Câu hỏi hiện tại: {query}
######################
Đầu ra:
"""

PROMPTS["keywords_extraction_examples"] = [
    """Ví dụ 1:

Câu hỏi: "Sự thương mại quốc tế ảnh hưởng như thế nào đến sự ổn định kinh tế toàn cầu?"
################
Đầu ra:
{
  "high_level_keywords": ["Thương mại quốc tế", "Ổn định kinh tế toàn cầu", "Tác động kinh tế"],
  "low_level_keywords": ["Hiệp định thương mại", "Thuế quan", "Tỷ giá hối đoái", "Nhập khẩu", "Xuất khẩu"]
}
#############################""",
    """Ví dụ 2:

Câu hỏi: "Hậu quả môi trường của việc phá rừng đối với đa dạng sinh học là gì?"
################
Đầu ra:
{
  "high_level_keywords": ["Hậu quả môi trường", "Phá rừng", "Mất đa dạng sinh học"],
  "low_level_keywords": ["Tuyệt chủng loài", "Hủy hoại môi trường sống", "Phát thải carbon", "Rừng mưa", "Hệ sinh thái"]
}
#############################""",
    """Ví dụ 3:

Câu hỏi: "Vai trò của giáo dục trong việc giảm nghèo là gì?"
################
Đầu ra:
{
  "high_level_keywords": ["Giáo dục", "Giảm nghèo", "Phát triển kinh tế xã hội"],
  "low_level_keywords": ["Tiếp cận trường học", "Tỷ lệ biết chữ", "Đào tạo nghề", "Bất bình đẳng thu nhập"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích, trả lời câu hỏi của người dùng dựa trên các Đoạn Văn Bản được cung cấp bên dưới.

---Mục tiêu---

Tạo ra câu trả lời ngắn gọn dựa trên các Đoạn Văn Bản và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và câu hỏi hiện tại. Tóm tắt tất cả thông tin có trong các Đoạn Văn Bản, kết hợp với kiến thức chung liên quan đến tài liệu pháp lý.
Không bao gồm thông tin không có trong các Đoạn Văn Bản.

Khi xử lý nội dung có dấu thời gian:
1. Mỗi đoạn văn bản có dấu thời gian "created_at" cho biết khi nào thông tin được thu thập.
2. Khi gặp thông tin mâu thuẫn, hãy xem xét cả nội dung và dấu thời gian.
3. Không tự động ưu tiên nội dung có dấu thời gian gần nhất - hãy sử dụng đánh giá dựa trên bối cảnh.
4. Đối với các câu hỏi liên quan đến thời gian, ưu tiên thông tin thời gian có trong nội dung trước khi xét dấu thời gian.

---Lịch sử hội thoại---
{history}

---Các Đoạn Văn Bản---
{content_data}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần phù hợp.
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng.
- Đảm bảo câu trả lời duy trì tính liên tục với lịch sử hội thoại.
- Nếu bạn không biết câu trả lời, hãy nói vậy.
- Không bao gồm thông tin không có trong các Đoạn Văn Bản.
"""

PROMPTS["similarity_check"] = """Vui lòng phân tích mức độ tương đồng giữa hai câu hỏi sau:

Câu hỏi 1: {original_prompt}
Câu hỏi 2: {cached_prompt}

Hãy đánh giá xem hai câu hỏi này có ý nghĩa ngữ nghĩa tương tự nhau hay không, và liệu câu trả lời cho Câu hỏi 2 có thể được sử dụng để trả lời Câu hỏi 1. Cung cấp một điểm số tương đồng từ 0 đến 1 trực tiếp.

Tiêu chí điểm số tương đồng:
0: Hoàn toàn không liên quan hoặc câu trả lời không thể tái sử dụng, bao gồm nhưng không giới hạn:
   - Các câu hỏi có chủ đề khác nhau
   - Các địa điểm được đề cập khác nhau
   - Các thời điểm được đề cập khác nhau
   - Các cá nhân cụ thể được đề cập khác nhau
   - Các sự kiện cụ thể được đề cập khác nhau
   - Thông tin nền của các câu hỏi khác nhau
   - Các điều kiện then chốt trong câu hỏi khác nhau
1: Hoàn toàn giống nhau và câu trả lời có thể được sử dụng trực tiếp
0.5: Có phần liên quan và câu trả lời cần chỉnh sửa để có thể sử dụng
Chỉ trả về một con số từ 0-1, không thêm nội dung khác.
"""

PROMPTS["mix_rag_response"] = """---Vai trò---

Bạn là một trợ lý hữu ích, trả lời câu hỏi của người dùng dựa trên các Nguồn Dữ liệu được cung cấp bên dưới.

---Mục tiêu---

Tạo ra câu trả lời ngắn gọn dựa trên các Nguồn Dữ liệu và tuân theo các Quy tắc Phản hồi, xem xét cả lịch sử hội thoại và câu hỏi hiện tại. Các nguồn dữ liệu bao gồm hai phần: Knowledge Graph (KG) và Đoạn Văn Bản (DC). Tóm tắt tất cả thông tin có trong các Nguồn Dữ liệu, kết hợp với kiến thức chung liên quan, đặc biệt trong bối cảnh pháp lý.
Không bao gồm thông tin không có trong các Nguồn Dữ liệu.

Khi xử lý thông tin có dấu thời gian:
1. Mỗi thông tin (bao gồm cả mối quan hệ và nội dung) có dấu thời gian "created_at" cho biết khi nào thông tin được thu thập.
2. Khi gặp thông tin mâu thuẫn, hãy xem xét cả nội dung/mối quan hệ và dấu thời gian.
3. Không tự động ưu tiên thông tin có dấu thời gian gần nhất - hãy sử dụng đánh giá dựa trên bối cảnh.
4. Đối với các câu hỏi liên quan đến thời gian, ưu tiên thông tin thời gian có trong nội dung trước khi xét dấu thời gian.

---Lịch sử hội thoại---
{history}

---Nguồn Dữ liệu---

1. Từ Knowledge Graph (KG):
{kg_context}

2. Từ Đoạn Văn Bản (DC):
{vector_context}

---Quy tắc Phản hồi---

- Định dạng và độ dài mục tiêu: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phần phù hợp.
- Vui lòng trả lời bằng cùng ngôn ngữ với câu hỏi của người dùng.
- Đảm bảo câu trả lời duy trì tính liên tục với lịch sử hội thoại.
- Tổ chức câu trả lời theo các phần, mỗi phần tập trung vào một điểm hoặc khía cạnh chính.
- Sử dụng các tiêu đề phần rõ ràng và mô tả chính xác nội dung.
- Nếu bạn không biết câu trả lời, hãy nói vậy. Không bịa đặt thông tin.
- Không bao gồm thông tin không có trong các Nguồn Dữ liệu.
"""