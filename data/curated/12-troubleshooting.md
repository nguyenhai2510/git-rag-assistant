# Các lỗi Git thường gặp và hướng chẩn đoán

Document ID: 12-troubleshooting
Source: https://git-scm.com/docs/git-status
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Push rejected: non-fast-forward
Remote có commit mà nhánh local chưa tích hợp. Chạy `git fetch origin`, xem khác biệt (`git log --oneline --graph --all`), rồi chọn merge/rebase theo workflow trước khi push lại. Tránh force-push mặc định.

## Merge conflict
Dùng `git status` xác định file bị conflict; sửa nội dung, `git add` file đã giải quyết, rồi `git merge --continue`.

## Nothing to commit
Có thể không có thay đổi nào được stage, file chưa đổi, hoặc file bị ignore. Kiểm tra `git status`, `git diff`, và `.gitignore`.

## Detached HEAD
HEAD đang trỏ trực tiếp vào commit thay vì một nhánh. Nếu tạo commit muốn giữ lại, có thể tạo nhánh tại trạng thái hiện tại với `git switch -c new-branch` trước khi chuyển đi.

## Remote not found
Kiểm tra `git remote -v`, tên remote, URL và quyền truy cập. Tên mặc định thường là `origin` nhưng không bắt buộc.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-pull
- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-push
- https://git-scm.com/docs/git-remote
