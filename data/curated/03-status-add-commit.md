# Kiểm tra, staging và commit: status, add, commit

Document ID: 03-status-add-commit
Source: https://git-scm.com/docs/git-status
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Kiểm tra trạng thái
```bash
git status
git status --short
```
Giúp phân biệt thay đổi chưa stage, đã stage và file chưa được Git theo dõi.

## Staging
```bash
git add README.md
git add .
```
`git add .` stage thay đổi nằm dưới đường dẫn hiện tại, kể cả xóa file đã theo dõi trong phạm vi đó. Kiểm tra lại bằng `git status` trước khi commit.

## Commit
```bash
git commit -m "Document setup steps"
git log --oneline -5
```
Commit tạo snapshot dựa trên index. `git commit -am "message"` stage và commit các thay đổi đối với **file đã được theo dõi**, không tự thêm file mới chưa theo dõi.

## Các câu hỏi thường gặp
- Thêm file mới nhưng commit không chứa file? Cần `git add <file>` trước.
- Sửa file sau khi stage thì sao? Index vẫn giữ phiên bản lúc stage; stage lại để đưa bản mới vào commit.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-add
- https://git-scm.com/docs/git-commit
