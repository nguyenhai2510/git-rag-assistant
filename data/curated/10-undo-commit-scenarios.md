# Tình huống: sửa commit, hoàn tác commit, tránh ghi đè lịch sử

Document ID: 10-undo-commit-scenarios
Source: https://git-scm.com/docs/git-reset
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Tình huống A — Commit gần nhất sai message, chưa push
```bash
git commit --amend -m "Correct message"
```
`--amend` tạo commit thay thế; commit ID thường đổi. Tránh tùy tiện amend commit đã chia sẻ.

## Tình huống B — Đã commit nhưng muốn giữ code và stage lại
```bash
git reset --soft HEAD~1
```
Dịch chuyển HEAD về commit cha, giữ nguyên index và working tree.

## Tình huống C — Muốn hủy commit mới nhất, giữ code nhưng bỏ stage
```bash
git reset --mixed HEAD~1
```
Working tree giữ thay đổi, index được đặt lại.

## Tình huống D — Commit lỗi đã push lên nhánh chung
```bash
git revert <commit-hash>
```
Tạo một commit đảo tác động thay vì rewrite nhánh chung. Trường hợp revert một merge commit cần lựa chọn mainline parent riêng; không dùng ví dụ trên một cách máy móc.

## Quy tắc an toàn
Trước thao tác: `git status`, `git log --oneline -5`; nếu dữ liệu quan trọng, tạo nhánh dự phòng. Không tự đề xuất force-push hoặc reset hard khi chưa hiểu bối cảnh.

## Tài liệu tham khảo
- https://git-scm.com/docs/git-reset
- https://git-scm.com/docs/git-revert
- https://git-scm.com/docs/git-commit
