# Git căn bản: repository, working tree, index, HEAD

Document ID: 01-git-concepts
Source: https://git-scm.com/docs/git
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Khái niệm
Git là hệ thống quản lý phiên bản phân tán. **Working tree** chứa file đang chỉnh sửa; **index** (staging area) ghi nhận phiên bản sẽ được đưa vào commit tiếp theo; **repository** lưu các commit và đối tượng Git. `HEAD` thường trỏ tới nhánh đang được checkout và qua đó xác định commit hiện tại.

## Chu trình phổ biến
```bash
git status
git add README.md
git commit -m "Update README"
```
`git add` đưa nội dung hiện tại của file vào staging area; nếu sửa tiếp sau `git add`, cần `git add` lại để stage thay đổi mới. `git commit` tạo một commit từ nội dung đang được stage.

## Tình huống hỏi đáp
- **`git add` có commit không?** Không, chỉ stage thay đổi.
- **Làm sao xem file nào được sửa hoặc stage?** Dùng `git status`.
- **HEAD có phải tên branch không?** HEAD thường là symbolic reference đến branch, nhưng có thể ở trạng thái detached HEAD.

## Tài liệu tham khảo
- https://git-scm.com/docs/git
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-add
