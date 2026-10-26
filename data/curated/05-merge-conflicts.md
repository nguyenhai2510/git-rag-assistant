# Merge nhánh và xử lý conflict

Document ID: 05-merge-conflicts
Source: https://git-scm.com/docs/git-merge
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Gộp nhánh
```bash
git switch main
git merge feature/login
```
Lệnh gộp các thay đổi từ nhánh chỉ định vào nhánh hiện tại. Nếu có thể fast-forward, Git chỉ dịch chuyển con trỏ nhánh; nếu lịch sử rẽ nhánh, một merge commit có thể được tạo.

## Khi xảy ra merge conflict
1. `git status` để xác định các file conflict.
2. Mở file, giải quyết các vùng đánh dấu `<<<<<<<`, `=======`, `>>>>>>>` (không để nguyên dấu đánh dấu trong nội dung đã giải quyết).
3. `git add <file>` để đánh dấu đã giải quyết.
4. `git merge --continue` (hoặc commit theo hướng dẫn Git) để hoàn tất.

## Hủy merge đang thực hiện
```bash
git merge --abort
```
Lệnh cố khôi phục trạng thái trước merge, nhưng không được bảo đảm giữ được mọi thay đổi chưa commit trong trường hợp phức tạp. Tốt nhất commit hoặc stash thay đổi trước khi merge.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-status
