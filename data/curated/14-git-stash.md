# Lưu tạm thay đổi với git stash

Document ID: 14-git-stash
Source: https://git-scm.com/docs/git-stash
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Khi nào dùng?
Khi cần chuyển công việc tạm thời mà chưa sẵn sàng commit, `git stash` có thể lưu thay đổi tracked trong working tree/index.

## Các lệnh
```bash
git stash push -m "WIP login"
git stash list
git stash apply
git stash pop
```
- `apply`: áp dụng stash nhưng giữ entry trong stash list.
- `pop`: áp dụng và xóa entry nếu áp dụng thành công; có thể có conflict.
- Theo mặc định, file untracked không được stash. Dùng `git stash push -u` nếu cần đưa cả untracked files (trừ ignored files).

## Lưu ý
Stash không thay thế backup dài hạn. Trước khi stash hãy kiểm tra `git status`.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-stash
- https://git-scm.com/docs/git-status
