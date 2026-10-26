# Xem lịch sử và khác biệt: log, show, diff

Document ID: 07-history-diff
Source: https://git-scm.com/docs/git-log
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Xem lịch sử
```bash
git log --oneline --graph --decorate -10
git show HEAD
```
`git log` liệt kê commit; `git show HEAD` hiển thị thông tin và diff của commit HEAD theo cấu hình mặc định.

## Xem thay đổi
```bash
git diff
git diff --staged
git diff HEAD
```
- `git diff`: so sánh working tree với index đối với các file được theo dõi.
- `git diff --staged`: so sánh index với HEAD.
- `git diff HEAD`: so sánh working tree với HEAD cho các file được theo dõi.

## Tình huống
Trước commit, chạy `git diff --staged` để đọc chính xác nội dung đã stage.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-log
- https://git-scm.com/docs/git-show
- https://git-scm.com/docs/git-diff
