# git revert và git restore: hoàn tác an toàn theo tình huống

Document ID: 09-revert-restore
Source: https://git-scm.com/docs/git-revert
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Revert commit đã ghi vào lịch sử
```bash
git revert HEAD
```
`git revert` tạo commit mới đảo tác động của commit trước đó (nếu thao tác hoàn tất thành công); thường phù hợp cho commit đã push vì không viết lại lịch sử cũ. Revert có thể phát sinh conflict.

## Bỏ stage một file nhưng giữ nội dung đang sửa
```bash
git restore --staged README.md
```
Mặc định đưa index của file trở về phiên bản ở HEAD, trong khi working tree vẫn giữ thay đổi.

## Bỏ thay đổi chưa commit của file tracked
```bash
git restore README.md
```
Mặc định phục hồi working tree theo index; thay đổi chưa được lưu của file có thể bị mất. Hãy xem `git diff` trước.

## Khác nhau
- `reset`: có thể di chuyển HEAD và cập nhật index/working tree.
- `revert`: tạo commit mới đảo thay đổi của commit cũ.
- `restore`: phục hồi nội dung file trong index hoặc working tree; không tự tạo commit.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-revert
- https://git-scm.com/docs/git-restore
- https://git-scm.com/docs/git-reset
