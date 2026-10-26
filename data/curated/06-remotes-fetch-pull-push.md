# Remote repositories: remote, fetch, pull, push

Document ID: 06-remotes-fetch-pull-push
Source: https://git-scm.com/docs/git-remote
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Kiểm tra và thêm remote
```bash
git remote -v
git remote add origin https://github.com/example/project.git
```

## Fetch
```bash
git fetch origin
```
`git fetch` tải đối tượng và cập nhật remote-tracking references tương ứng; không tự gộp nội dung vào nhánh đang làm việc.

## Pull
```bash
git pull --ff-only
```
`git pull` thực hiện fetch rồi tích hợp lịch sử vào nhánh hiện tại. Tùy tham số/cấu hình, việc tích hợp có thể fast-forward, merge, hoặc rebase. Không nên khẳng định pull luôn bằng `fetch + merge`.

## Push
```bash
git push -u origin feature/login
```
Đẩy nhánh local lên remote; `-u` thiết lập upstream tracking cho lần sau. Cần quyền push và có thể bị từ chối nếu remote đã tiến lên.

## Khi dùng gì?
- Muốn xem thay đổi remote trước khi tích hợp: `fetch`.
- Muốn cập nhật nhánh local với upstream: `pull` (chọn cách tích hợp phù hợp).
- Muốn xuất bản commit local: `push`.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-remote
- https://git-scm.com/docs/git-fetch
- https://git-scm.com/docs/git-pull
- https://git-scm.com/docs/git-push
