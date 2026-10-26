# Tra cứu nhanh Git CLI theo mục tiêu

Document ID: 13-command-cheatsheet
Source: https://git-scm.com/docs/git
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Tác vụ thường gặp
| Muốn làm gì? | Lệnh ví dụ |
| --- | --- |
| Xem trạng thái | `git status` |
| Stage một file | `git add README.md` |
| Commit thay đổi đã stage | `git commit -m "Update"` |
| Tạo và chuyển nhánh | `git switch -c feature/login` |
| Xem lịch sử gọn | `git log --oneline` |
| Lấy remote updates chưa tích hợp | `git fetch origin` |
| Pull chỉ khi có thể fast-forward | `git pull --ff-only` |
| Xem thay đổi đã stage | `git diff --staged` |
| Bỏ stage file | `git restore --staged README.md` |
| Hoàn tác commit mới nhất nhưng giữ stage | `git reset --soft HEAD~1` |
| Đảo commit đã chia sẻ | `git revert <commit-hash>` |

Đây là các ví dụ; tùy workflow và trạng thái repository, trước khi chạy cần kiểm tra `git status`.

## Tài liệu tham khảo
- https://git-scm.com/docs/git
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-add
- https://git-scm.com/docs/git-commit
- https://git-scm.com/docs/git-switch
- https://git-scm.com/docs/git-fetch
- https://git-scm.com/docs/git-pull
- https://git-scm.com/docs/git-reset
- https://git-scm.com/docs/git-revert
