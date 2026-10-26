# Workflow: tạo nhánh tính năng, hợp nhất và xử lý conflict

Document ID: 11-merge-workflow
Source: https://git-scm.com/docs/git-switch
Language: vi
Type: curated-summary

## Phạm vi và nguồn
Tài liệu biên soạn cho demo RAG, không thay thế Git manual. Đối chiếu trực tiếp các trang chính thức khi có nghi ngờ.

## Quy trình làm tính năng
```bash
git switch main
git switch -c feature/login
# edit files
git add .
git commit -m "Implement login"
git switch main
git merge feature/login
```
`# edit files` là ghi chú, không phải lệnh Git. Nên bảo đảm `main` đã ở trạng thái cập nhật theo quy trình của nhóm trước merge.

## Nếu merge conflict
```bash
git status
# edit conflicted files
git add path/to/resolved-file
git merge --continue
```
Nếu muốn hủy merge khi đang giải quyết, cân nhắc `git merge --abort`. Dùng `git status` để biết Git đang yêu cầu bước nào.

## Kiểm tra kết quả
```bash
git log --oneline --graph -10
git status
```

## Tài liệu tham khảo
- https://git-scm.com/docs/git-switch
- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-status
- https://git-scm.com/docs/git-add
