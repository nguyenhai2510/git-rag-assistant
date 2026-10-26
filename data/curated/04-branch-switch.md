# Quản lý và chuyển nhánh: branch, switch

Document ID: 04-branch-switch
Source: https://git-scm.com/docs/git-branch
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Quản lý nhánh
```bash
git branch
git branch -a
git branch feature/login
```
`git branch feature/login` chỉ tạo nhánh, không chuyển sang nhánh đó.

## Chuyển nhánh hoặc tạo và chuyển
```bash
git switch feature/login
git switch -c feature/payment
```
`git switch -c` tạo nhánh mới rồi checkout nhánh. Cần kiểm tra `git status` khi có thay đổi chưa commit; Git có thể từ chối chuyển nếu thao tác ghi đè thay đổi.

## Xóa nhánh
```bash
git branch -d feature/login
```
`-d` kiểm tra trạng thái merge trước khi xóa. `-D` ép xóa nhánh local và có nguy cơ mất tham chiếu đến commit chưa tích hợp; tránh dùng nếu chưa kiểm tra.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-branch
- https://git-scm.com/docs/git-switch
- https://git-scm.com/docs/git-checkout
