# Rebase cơ bản và sự khác biệt so với merge

Document ID: 15-git-rebase
Source: https://git-scm.com/docs/git-rebase
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Khái niệm
`git rebase` phát lại các commit của nhánh lên một base commit mới, thường tạo các commit ID mới. `git merge` kết hợp lịch sử và có thể tạo merge commit, không bắt buộc viết lại commit hiện có.

## Ví dụ local
```bash
git switch feature/login
git rebase main
```
Đưa các commit của `feature/login` lên trạng thái mới nhất của local `main`.

## Nếu xảy ra conflict
```bash
git status
# resolve conflicted files
git add path/to/file
git rebase --continue
```
Dùng `git rebase --abort` để hủy rebase đang diễn ra.

## Cảnh báo
Không rebase tùy tiện lịch sử đã chia sẻ khi các thành viên khác dựa trên những commit đó. Lệnh `git pull --rebase` yêu cầu tích hợp bằng rebase thay vì merge.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-rebase
- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-pull
