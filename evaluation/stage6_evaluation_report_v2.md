# BÁO CÁO STAGE 6.4 — TỔNG HỢP ĐÁNH GIÁ HỆ THỐNG RAG

**Dự án:** Git Documentation RAG Assistant  
**Học phần:** Chuyên đề công nghệ  
**Phiên bản:** 2.0 — cập nhật sau Faithfulness Validation  
**Ngày tổng hợp:** 26/10/2026  
**Tình trạng:** Kết quả thực nghiệm nội bộ; các nhãn đánh giá chất lượng do AI đề xuất, chờ người thực hiện rà soát.

## Tóm tắt

Dự án xây dựng chatbot hỏi đáp tài liệu Git theo kiến trúc Retrieval-Augmented Generation (RAG). Giai đoạn 6 đánh giá hai thành phần chính: (i) khả năng truy xuất bằng chứng từ Knowledge Base (KB), (ii) khả năng tạo câu trả lời có tính chính xác và bám sát bằng chứng. Bộ kiểm thử gồm **25 câu hỏi** (22 trong phạm vi Git, 3 ngoài phạm vi). Cả **25/25 lượt sinh câu trả lời hoàn tất thành công** sau khi xử lý lỗi quota API. Trên 22 câu hỏi trong phạm vi, kết quả gắn nhãn đề xuất ghi nhận **Hit@1 = 17/22 (77.27%)**, **Hit@4 = 21/22 (95.45%)**, **MRR@4 = 0.8561**, **Answer Correctness = 41/44 (93.18%)** và **Faithfulness = 43/44 (97.73%)**. Cả **3/3** câu hỏi ngoài phạm vi được từ chối phù hợp theo đánh giá đề xuất. Các con số phản ánh bộ thử nghiệm nhỏ, không phải bảo đảm về hiệu suất thực tế.

## 1. Mục tiêu và phạm vi đánh giá

1. Đo khả năng tìm thấy bằng chứng liên quan trong Top-K chunks.
2. Kiểm tra câu trả lời Git có đáp ứng đáp án tham chiếu hay không.
3. Xác định câu trả lời có được nội dung truy xuất hỗ trợ hay không.
4. Kiểm tra phản hồi với câu hỏi ngoài phạm vi.
5. Đo thời gian đáp ứng từ lời gọi pipeline `ask_rag()` và phân tích trường hợp bất thường.

**Hệ thống thử nghiệm:** Python + Streamlit; embedding `intfloat/multilingual-e5-small`; ChromaDB; Gemini `gemini-3.5-flash-lite`. Knowledge Base curated gồm 15 tệp Markdown và 32 chunks; collection gốc gồm 271 chunks được giữ để phục vụ thử nghiệm sau này. Các số liệu trong báo cáo này là kết quả **curated KB, Top-K = 4**; **chưa thực hiện phép so sánh định lượng** giữa hai collection.

## 2. Thiết kế thử nghiệm và phương pháp

### 2.1. Tập dữ liệu

- Tổng cộng **25 test cases**: Git Basics (5), Branching & Merging (5), Remote & Collaboration (5), Undo & Recovery (5), Edge & Out-of-scope (5).
- **22** câu in-scope; **3** câu out-of-scope, được xử lý riêng đối với chỉ số từ chối.
- Mỗi test gồm `id`, `category`, `question`, `expected_answer`, `expected_terms`, `in_scope`.
- Các câu hỏi được thiết kế dựa trên phạm vi KB curated; do đó có **thiên lệch nội bộ** và chưa kiểm tra khả năng tổng quát hóa với tập dữ liệu độc lập.

### 2.2. Retrieval Evaluation

Retriever trả về tối đa **4 chunks** cho mỗi câu hỏi in-scope, tạo **88 bản ghi**. Nhãn `relevant = 1` được đề xuất nếu nội dung chunk đủ hỗ trợ ít nhất phần cốt lõi của đáp án tham chiếu; `0` nếu chỉ trùng chủ đề, liệt kê tài liệu hay không cung cấp bằng chứng hữu ích. Các nhãn được chấm theo từng cặp *câu hỏi–chunk*, không suy từ cosine distance.

**Công thức:**

- **Hit@1:** tỷ lệ câu in-scope có bằng chứng liên quan ngay ở rank 1.
- **Hit@4:** tỷ lệ câu in-scope có ít nhất một chunk liên quan trong Top-4.
- **MRR@4:** trung bình `1/rank` của chunk liên quan đầu tiên; bằng 0 nếu không có chunk liên quan trong Top-4.

### 2.3. Generation Evaluation

Gọi `ask_rag(question, top_k=4)` cho 25 câu, lưu kết quả, URL nguồn và `response_time`. Lỗi 429 `RESOURCE_EXHAUSTED` xảy ra trong lần chạy đầu do vượt giới hạn request/phút; chạy lại các case lỗi sau khi điều chỉnh khoảng cách request cho kết quả **25/25 success**. Kết quả 429 là lỗi khả dụng API, không phải đáp án sai và không được gộp vào điểm Correctness.

**Answer Correctness**, chấm trên 22 câu in-scope:

| Điểm | Diễn giải |
|---|---|
| 0 | Trả lời sai hoặc từ chối câu hỏi hợp lệ, không đáp ứng nội dung cốt lõi |
| 1 | Đúng một phần nhưng thiếu bước/ý quan trọng |
| 2 | Đúng và đầy đủ các ý trọng tâm của đáp án tham chiếu |

**Out-of-scope Rejection:** PASS nếu từ chối hoặc xác định đúng KB không bao phủ yêu cầu; FAIL nếu bịa hướng dẫn ngoài phạm vi. Ba câu ngoài phạm vi không đưa vào mẫu số Correctness/Faithfulness.

### 2.4. Faithfulness Validation

Đánh giá 22 câu in-scope bằng cách đối chiếu các phát biểu quan trọng trong câu trả lời với **Top-4 chunks đã được lưu trong `retrieval_results.csv`**. Hai file được đối chiếu theo `test_id`, câu hỏi và tập URL nguồn. Rubric:

| Điểm | Diễn giải |
|---|---|
| 0 | Có phát biểu quan trọng không được context hỗ trợ hoặc mâu thuẫn rõ ràng |
| 1 | Phần lớn nội dung có căn cứ nhưng vẫn có khẳng định vượt quá context |
| 2 | Những phát biểu chính đều được context hỗ trợ |

**Giới hạn truy vết quan trọng:** `generation_results.csv` chỉ lưu URL nguồn, không lưu snapshot các chunks được đưa vào prompt trong đúng lần gọi Gemini. Việc khớp câu hỏi và URL **không chứng minh tuyệt đối** nội dung context của hai lần chạy giống nhau. Do đó, Faithfulness được ghi là **đánh giá đối chiếu hậu nghiệm do AI đề xuất**, không phải phép đo độc lập hay benchmark RAGAS. Từ chối câu hỏi hợp lệ cũng không mặc nhiên đạt Correctness dù có thể là phản hồi thận trọng theo context.

## 3. Kết quả tổng hợp

| Nhóm | Chỉ số | Kết quả | Trạng thái |
|---|---|---:|---|
| Dữ liệu | Test cases | 25 | Xác nhận từ dataset |
| Dữ liệu | In-scope / Out-of-scope | 22 / 3 | Xác nhận từ dataset |
| Truy xuất | Retrieved rows | 88 | Xác nhận từ CSV |
| Truy xuất | Hit@1 | 17/22 = **77.27%** | Nhãn AI đề xuất |
| Truy xuất | Hit@4 | 21/22 = **95.45%** | Nhãn AI đề xuất |
| Truy xuất | MRR@4 | **0.8561** | Nhãn AI đề xuất |
| Sinh câu trả lời | Generation success | 25/25 = **100%** | Xác nhận trong CSV cuối |
| Sinh câu trả lời | Correctness chuẩn hóa | 41/44 = **93.18%** | Rubric AI đề xuất |
| Sinh câu trả lời | Đạt 2 / 1 / 0 điểm | **20 / 1 / 1** | Rubric AI đề xuất |
| Faithfulness | Faithfulness chuẩn hóa | 43/44 = **97.73%** | Đối chiếu AI đề xuất |
| Faithfulness | Đạt 2 / 1 / 0 điểm | **21 / 1 / 0** | Đối chiếu AI đề xuất |
| Ngoài phạm vi | Từ chối phù hợp | **3/3 PASS** | Nhãn AI đề xuất |
| Hiệu năng | Response time trung bình | **3.860 giây** | Đo trên 25 lượt thành công |
| Hiệu năng | Response time trung vị | **1.243 giây** | Đo trên 25 lượt thành công |

**Cách diễn giải phần trăm:** Correctness 93.18% và Faithfulness 97.73% là **điểm rubric chuẩn hóa** (điểm thực đạt/tổng điểm tối đa), không phải tỷ lệ phần trăm câu trả lời hoàn toàn đúng hoặc khẳng định không hallucination. Tỷ lệ câu in-scope được chấm Correctness 2/2 là **20/22 = 90.91%**.

### 3.1. Retrieval

Top-4 có ít nhất một đoạn chứa bằng chứng hữu ích theo tiêu chí chấm đề xuất trong **21/22** trường hợp, so với **17/22** ở Top-1. Điều này cho thấy lấy nhiều hơn một chunk có thể giúp tăng cơ hội bao phủ thông tin trong bộ thử nghiệm này. Tuy nhiên, tăng K cũng có thể đưa thêm thông tin nhiễu và tiêu tốn context; báo cáo chưa có thí nghiệm so sánh K=1, 2, 4, 8 theo độ chính xác cuối cùng.

### 3.2. Correctness

**20** câu được đề xuất 2/2; **1** câu 1/2 (TC-15, thiếu push/review trong workflow feature branch); **1** câu 0/2 (TC-07, từ chối một câu Git đúng phạm vi). Tỷ lệ **20/22** đúng đủ ý phải được phân biệt với điểm rubric chuẩn hóa **41/44**.

### 3.3. Faithfulness

**21** câu được đề xuất 2/2 và **1** câu 1/2 (TC-07). Ở TC-07, từ chối do Top-4 không có bằng chứng trực tiếp là phản ứng thận trọng nhưng phát biểu theo nghĩa “toàn bộ KB không hỗ trợ” là khẳng định vượt quá những gì Top-4 có thể chứng minh. KB được kiểm tra có thông tin `git branch` ở vị trí không được Retriever trả về trong Top-4.

Faithfulness cao **không kéo theo** Correctness cao: TC-15 bám sát fragment workflow được truy xuất nhưng thiếu các bước cần thiết trong đáp án tham chiếu.

### 3.4. Out-of-scope

TC-23 (triển khai Kubernetes trên AWS), TC-24 (Spring Boot/MySQL), TC-25 (dự báo thời tiết) đều được đánh giá từ chối phù hợp. Kết quả **3/3** chỉ phản ánh ba tình huống thử nghiệm, không cho phép kết luận hệ thống chống hallucination tốt trên mọi câu ngoài phạm vi.

### 3.5. Hiệu năng và khả dụng

Thời gian phản hồi đo từ lúc bắt đầu đến khi `ask_rag()` trả kết quả, bao gồm thời gian truy xuất và sinh câu trả lời. Trung bình **3.860 giây**, trung vị **1.243 giây** trên 25 lượt hoàn tất. Hai trường hợp nổi bật là **TC-01: 27,203 giây** và **TC-16: 37,305 giây**; chưa có đo tách thời gian khởi tạo embedding, tìm kiếm vector, xử lý mạng và Gemini để quy kết nguyên nhân.

Trong lần chạy đầu, một số lượt gặp lỗi **429 — Free Tier requests/minute**; việc điều chỉnh tốc độ và chạy lại các case lỗi đã giúp đủ 25 lượt thành công. Tỷ lệ thành công cuối cùng mô tả **bộ dữ liệu cuối sau khi chạy lại**, không phải tỷ lệ thành công 100% ngay lần thử đầu và không đại diện cho độ ổn định vận hành lâu dài.

## 4. Phân tích trường hợp điển hình

| Case | Quan sát | Phân loại lỗi | Hướng cải thiện |
|---|---|---|---|
| **TC-07** | Hỏi lệnh xem danh sách nhánh; không có bằng chứng trực tiếp trong Top-4, chatbot từ chối | Retrieval miss → answer failure; khẳng định quá mức về phạm vi KB | Bổ sung/điều chỉnh mục `git branch`, truy vấn lại với paraphrase, xem xét hybrid retrieval hoặc reranking |
| **TC-15** | Workflow feature branch trả lời thiếu push và review | Answer completeness | Làm rõ workflow trong KB; sửa đáp án mẫu nếu có biến thể hợp lệ; điều chỉnh prompt nhắc các bước chính |
| **TC-04** | Bằng chứng có thể phân tán ở nhiều chunks | Giới hạn của tiêu chí relevance từng chunk | Chấm cả “evidence có thể tổng hợp từ Top-4” và “một chunk đủ bằng chứng” trong thử nghiệm tiếp theo |
| **TC-01/TC-16** | Thời gian phản hồi vượt trội | Latency outliers | Ghi log thời gian cold-start/retrieval/generation tách biệt |
| **TC-16–25 (lần đầu)** | Một số API calls báo 429, sau đó chạy lại thành công | External API rate limiting | Backoff theo retryDelay, giữ checkpoint, cấu hình pacing theo quota hiện hành |

**Điểm phương pháp luận:** tiêu chí Retrieval hiện chấp nhận chunk hỗ trợ *phần cốt lõi*, không nhất thiết toàn bộ đáp án. Nếu chuyển sang tiêu chí nghiêm ngặt “một chunk phải đầy đủ mọi ý”, Hit@K cần được tính lại. Không nên tự so sánh trực tiếp các giá trị từ hai cách chấm khác nhau.

## 5. Hạn chế và rủi ro đối với tính hợp lệ

1. **Cỡ mẫu nhỏ:** 22 câu trong phạm vi và 3 câu ngoài phạm vi chưa đủ đại diện cho mọi cách hỏi về Git.
2. **Thiên lệch chọn câu:** tác giả bộ test cũng tham chiếu phạm vi curated KB; cần tập holdout độc lập.
3. **Nhãn chấm chưa độc lập:** relevance, correctness, faithfulness và rejection là nhận định AI hỗ trợ, chưa được người thực hiện xác nhận; có thể có sai khác ở các trường hợp biên.
4. **Không có generation-context snapshot:** đối chiếu URL và câu hỏi nhất quán nhưng chưa chứng minh được byte-for-byte context được đưa vào model lúc sinh answer.
5. **Không có thí nghiệm lặp:** chưa có phương sai, khoảng tin cậy hay kiểm định thống kê.
6. **Chưa làm ablation:** collection gốc 271 chunks và curated 32 chunks chưa được so sánh cùng nhãn và cùng điều kiện.
7. **Metadata nguồn:** URL trong curated docs có thể đại diện cả tài liệu tổng hợp, không luôn là chứng cứ chính xác cho từng phát biểu.
8. **Latency không phân rã:** hai outliers có thể làm lệch trung bình; không được tự gán nguyên nhân cho model hay mạng.

## 6. Đề xuất hoàn thiện

**Ưu tiên trước buổi demo/báo cáo:**

1. Rà soát nhãn TC-04, TC-07, TC-15 và tối thiểu tất cả case có điểm không tối đa; chốt tiêu chí chấm và lưu kết quả phê duyệt.
2. Mở rộng KB/điều chỉnh Retrieval cho TC-07; kiểm thử lại cùng câu hỏi và một số biến thể diễn đạt.
3. Lưu snapshot `retrieved_chunks`, phiên bản prompt, model, collection, chunk IDs và hash tài liệu trong từng lần gọi để xác minh Faithfulness trực tiếp.
4. Giữ lại file kết quả gốc và kịch bản chạy để có thể tái lập.

**Nếu còn thời gian phát triển:**

5. Bổ sung kiểm thử nhiều K, hybrid retrieval/reranking và so sánh curated KB với original KB trên một tập test cố định.
6. Tách thời gian load model, embedding, retrieval và generation; chạy lặp để báo cáo median và tail latency.
7. Mở rộng bộ out-of-scope, câu mơ hồ, câu hỏi đối nghịch và câu có nguy cơ dùng lệnh Git phá hủy dữ liệu.

## 7. Kết luận

Stage 6 đã thiết lập quy trình đánh giá có thể kiểm tra lại: bộ câu hỏi, kết quả truy xuất, câu trả lời Gemini, chấm Correctness và đối chiếu Faithfulness. Sau khi khắc phục lỗi giới hạn tốc độ API, tập kết quả cuối gồm **25/25 lượt sinh thành công**. Với nhãn đánh giá đề xuất, **Hit@4 = 95,45%**, **Correctness chuẩn hóa = 93,18%** và **Faithfulness chuẩn hóa = 97,73%**. Hệ thống cũng từ chối phù hợp **3/3** câu ngoài phạm vi được thử.

Kết quả cho thấy tiềm năng của KB curated đối với hỏi đáp Git, nhưng cần diễn giải đúng: các chỉ số chất lượng **chưa có kiểm chứng độc lập**, bài test còn nhỏ và việc đối chiếu Faithfulness không có snapshot context của chính lần sinh câu trả lời. Lỗi **TC-07** và thiếu sót **TC-15** chỉ ra các hướng cải thiện cụ thể cho giai đoạn phát triển tiếp theo. Đây là cơ sở kỹ thuật phù hợp để trình bày trong Stage 7 — Demo Preparation.

## Phụ lục A — Chi tiết 22 test cases trong phạm vi

| Test case | Hit@1 | Hit@4 | Correctness (0–2) | Faithfulness (0–2) |
|---|---:|---:|---:|---:|
| TC-01 | 0 | 1 | 2 | 2 |
| TC-02 | 1 | 1 | 2 | 2 |
| TC-03 | 0 | 1 | 2 | 2 |
| TC-04 | 0 | 1 | 2 | 2 |
| TC-05 | 1 | 1 | 2 | 2 |
| TC-06 | 1 | 1 | 2 | 2 |
| TC-07 | 0 | 0 | 0 | 1 |
| TC-08 | 1 | 1 | 2 | 2 |
| TC-09 | 1 | 1 | 2 | 2 |
| TC-10 | 1 | 1 | 2 | 2 |
| TC-11 | 1 | 1 | 2 | 2 |
| TC-12 | 1 | 1 | 2 | 2 |
| TC-13 | 1 | 1 | 2 | 2 |
| TC-14 | 1 | 1 | 2 | 2 |
| TC-15 | 0 | 1 | 1 | 2 |
| TC-16 | 1 | 1 | 2 | 2 |
| TC-17 | 1 | 1 | 2 | 2 |
| TC-18 | 1 | 1 | 2 | 2 |
| TC-19 | 1 | 1 | 2 | 2 |
| TC-20 | 1 | 1 | 2 | 2 |
| TC-21 | 1 | 1 | 2 | 2 |
| TC-22 | 1 | 1 | 2 | 2 |

## Phụ lục B — Nguồn dữ liệu và khả năng tái lập

| Tệp | Vai trò |
|---|---|
| `evaluation/test_questions.json` | Dataset gồm 25 câu hỏi và đáp án tham chiếu |
| `evaluation/retrieval_results.csv` | 88 chunks truy xuất từ 22 câu in-scope |
| `evaluation/retrieval_results_labeled.csv` | Nhãn relevance AI đề xuất |
| `evaluation/retrieval_metrics_suggested.csv` | Hit@1, Hit@4 và reciprocal rank theo từng test |
| `evaluation/generation_results.csv` | 25 câu trả lời thực tế và response time |
| `evaluation/generation_results_reviewed.csv` | Rubric Correctness/rejection AI đề xuất |
| `evaluation/faithfulness_validation.csv` | Rubric Faithfulness và ghi chú kiểm tra |
| `evaluation/faithfulness_validation_report.md` | Diễn giải chi tiết đánh giá Faithfulness |
| `evaluation/stage6_final_metrics_updated.csv` | Bảng chỉ số đã bổ sung Faithfulness |

**Nguyên tắc lưu trữ:** giữ cả bản dữ liệu gốc và bản đã chấm; ghi lại phiên bản KB, model, prompt và thời điểm đo cho các thí nghiệm tiếp theo.
