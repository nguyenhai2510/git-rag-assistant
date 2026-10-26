# git reset: soft, mixed, hard và cảnh báo mất dữ liệu

Document ID: 08-reset-modes
Source: https://git-scm.com/docs/git-reset
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Mục đích
`git reset [<mode>] <commit>` dịch chuyển HEAD của nhánh hiện tại đến commit chỉ định, và có thể cập nhật index/working tree tùy chế độ. Với cách gọi theo đường dẫn, `git reset <path>` chủ yếu cập nhật index thay vì di chuyển HEAD.

## Các chế độ
- `--soft`: dịch chuyển HEAD, **giữ nguyên index và working tree**.
- `--mixed` (mặc định khi dùng chế độ reset commit): dịch chuyển HEAD và đặt lại index, **giữ working tree**.
- `--hard`: dịch chuyển HEAD và đặt lại index cùng working tree, **có thể làm mất thay đổi chưa commit**; một số file chưa được theo dõi bị ghi đè cũng có thể bị xóa.

## Hoàn tác commit gần nhất nhưng giữ code đã stage
```bash
git reset --soft HEAD~1
```
`HEAD~1` là commit cha đầu tiên của HEAD; lệnh cần có commit cha phù hợp. Thay đổi từ commit vừa được bỏ khỏi lịch sử nhánh vẫn nằm trong staging area.

## Hoàn tác commit nhưng muốn bỏ staging, giữ file đã sửa
```bash
git reset --mixed HEAD~1
```
Các thay đổi còn ở working tree và thường không được stage.

## Cảnh báo
Tránh `git reset --hard HEAD~1` nếu bạn muốn giữ thay đổi cục bộ. Trên nhánh đã chia sẻ, di chuyển lịch sử bằng reset rồi force-push có thể gây xung đột cho người khác; cân nhắc `git revert`.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-reset
