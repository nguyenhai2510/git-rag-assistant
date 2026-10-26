# Khởi tạo và sao chép repository: git init, git clone

Document ID: 02-init-clone
Source: https://git-scm.com/docs/git-init
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Khởi tạo repository mới
```bash
mkdir demo-repo
cd demo-repo
git init
```
`git init` tạo repository Git trong thư mục hiện tại; không tự tạo commit. Có thể đặt tên nhánh đầu bằng `git init -b main` nếu phiên bản Git hỗ trợ.

## Sao chép repository có sẵn
```bash
git clone https://github.com/example/project.git
```
`git clone` tạo thư mục làm việc mới, tải dữ liệu repository và thiết lập remote mặc định thường có tên `origin`.

## Phân biệt
- `git init`: bắt đầu quản lý một thư mục bằng Git, không tự kết nối remote.
- `git clone`: tạo bản sao từ repository có sẵn và cấu hình kết nối đến nguồn.
- Khi dùng URL ví dụ, thay `example/project` bằng repository thật.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-init
- https://git-scm.com/docs/git-clone
