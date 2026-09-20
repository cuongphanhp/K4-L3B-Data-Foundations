# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Phan Đại Cương
**Nhóm:** [Tên nhóm]
**Ngày:** 20-9-2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> *Viết 1-2 câu:*

**Ví dụ có độ tương tự CAO:**
- Câu A:
- Câu B:
- Tại sao tương đồng:

**Ví dụ có độ tương tự THẤP:**
- Câu A:
- Câu B:
- Tại sao khác:

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> *Viết 1-2 câu:*

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> *Đáp án:*

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> *Viết 1-2 câu:*

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> *Viết 2-3 câu: dùng biểu thức chính quy (regex) gì để phát hiện câu? Xử lý trường hợp ngoại lệ (edge case) nào?*

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Tôi dùng các dấu phân cách theo thứ tự ưu tiên `\n\n`, `\n`, `. `, khoảng trắng và cuối cùng là cắt theo ký tự. `_split` đệ quy thử dấu phân cách hiện tại; các phần ngắn được gom lại cho đến khi gần `chunk_size=500`, còn phần quá dài được tách tiếp bằng dấu phân cách kế tiếp. Base case là chuỗi rỗng, chuỗi không vượt quá kích thước chunk hoặc không còn dấu phân cách.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?*

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?*

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?*

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
# Dán kết quả (output) của: pytest tests/ -v
```

Kết quả chạy ngày 20/09/2026 trên Python 3.13.9:

```text
42 passed in 0.04s
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | cao / thấp | | |
| 2 | | | cao / thấp | | |
| 3 | | | cao / thấp | | |
| 4 | | | cao / thấp | | |
| 5 | | | cao / thấp | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:*

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Thời gian hỗ trợ đổi trả hàng tại Tiki là bao lâu? | `buyer-chinh-sach-doi-tra-hoan-tien#1`: phần mở đầu chính sách đổi trả | 0.8981 | Có trong top-3; đoạn nêu 30 ngày ở top-2 (0.8533) | Tiki hỗ trợ đổi trả trong vòng 30 ngày từ khi nhận hàng; một số sản phẩm có ngoại lệ. |
| 2 | Sản phẩm nào không được đổi trả theo nhu cầu của khách hàng? | `buyer-chinh-sach-doi-tra-hoan-tien#8`: danh mục hạn chế đổi trả | 0.8780 | Có, top-1 | Các nhóm như đồ lót, đồ bơi, nước hoa, voucher/dịch vụ, thực phẩm tươi sống và một số sản phẩm mùa vụ không được đổi trả do đổi ý. |
| 3 | Khách hàng cần làm gì để được bảo hành sản phẩm tại Tiki? | `buyer-chinh-sach-bao-hanh#0`: nơi và cách gửi bảo hành | 0.8943 | Có, top-1 | Khách hàng có thể mang sản phẩm đến hãng hoặc liên hệ Tiki để Tiki thu hồi tận nơi/tiếp nhận tại HUB; cần cung cấp thông tin và hình ảnh/clip lỗi khi được yêu cầu. |
| 4 | Nhà bán cần xử lý kiện hàng trả như thế nào? | `seller-faq-doi-tra-bao-hanh#1`: đồng kiểm, quay clip và khiếu nại | 0.8376 | Có, top-1 | Nhà bán cần đồng kiểm với đơn vị vận chuyển, quay clip mở kiện; nếu hàng sai hoặc hư hỏng thì giữ hàng và khiếu nại trên Seller Center. |
| 5 | Quy trình xử lý đổi trả bảo hành của nhà bán trong mô hình FBT là gì? | `seller-fbt-quy-trinh-doi-tra-bao-hanh#0`: nguyên tắc và các bước quy trình FBT | 0.8623 | Có, top-1 | Tiki tiếp nhận và thu hồi; nhà bán nhận/kiểm tra hàng, xử lý đổi trả hoặc bảo hành, sau đó phối hợp để gửi hàng lại cho khách. |

**Cấu hình benchmark:** `RecursiveChunker(chunk_size=500)`, top-3, 5 tài liệu thương mại điện tử; backend chạy thực tế là `gemini-embedding-001`. Tổng cộng có 85 chunks. Bảng trên tóm tắt ngữ cảnh mà agent sẽ sử dụng; lệnh `bench.py` chỉ đo retrieval, chưa gọi LLM để sinh câu trả lời.

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điểm retrieval tự đánh giá:** 9 / 10. Câu 1 được 1 điểm vì thông tin trực tiếp về “30 ngày” đứng ở top-2; bốn câu còn lại có chunk phù hợp ở top-1 và đạt 2 điểm/câu.

**Đánh giá:** Recursive chunking giữ được cấu trúc tiêu đề và đoạn văn tốt hơn cắt cố định, nên các câu hỏi theo quy trình như câu 4 và 5 truy xuất đúng tài liệu ngay top-1. Điểm hạn chế là một chunk mở đầu mang tính tổng quan có thể đứng trước chunk chứa con số chính xác, như ở câu 1; có thể cải thiện bằng overlap hoặc reranking theo tiêu đề/metadata.

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Cùng một bộ tài liệu nhưng cách chia chunk ảnh hưởng rõ đến việc thông tin chi tiết có nằm ở top-1 hay không. Recursive chunking phù hợp với tài liệu chính sách có nhiều tiêu đề và danh sách, nhưng cần kết hợp metadata hoặc overlap để tăng khả năng giữ ngữ cảnh giữa các đoạn.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | / 5 |
| Hướng tiếp cận của tôi (My Approach) | / 10 |
| Hoàn thiện code (Core Implementation — tests) | / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | / 5 |
| Kết quả truy xuất của tôi (Competition Results) | / 10 |
| **Tổng phần cá nhân** | **/ 60** |
