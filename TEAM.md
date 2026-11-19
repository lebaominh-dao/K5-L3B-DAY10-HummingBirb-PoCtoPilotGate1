# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): HummingBirb
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-HummingBirb-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S7

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đào Lê Bảo Minh | 2A202604010 |  | ✅ |
|   2 | Nguyễn Đức Hải | 2A202603943 |  |  |
|   3 | Trần Phú Thái | 2A202604001 |  |  |
|   4 | Vũ Quang Hải | 2A202603935 | Vận hành và pháp lý |  |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VuQuangHai-2A202603935

### Phần việc phụ trách

Vai **Vận hành và pháp lý**. CP5: quyết định Gate 1 v2 (Phiếu C mục C12) và ba dòng bắt buộc, `submission/submission.json`,
bảng thành viên `TEAM.md`, lệnh 7 gom bài nộp.

### Đóng góp cụ thể

- Viết quyết định v2 **Tiếp tục** (đổi từ Thu hẹp ở v1), đối chiếu từng vế của dòng "Tiếp tục" đã ký: 5 chỉ số bắt buộc và 3 ngưỡng
  business_ops đạt trên bộ nền **và** gói S7, không vượt trần, không ca mới hỏng; đặt hạn xem lại 28/11 (trước REFUND-v4 ngày 01/12).
- Viết ba dòng bắt buộc có số (giả định môi trường về hợp đồng 4 trường và tracking DB; cổng ngăn hay giảm; cần đo lại gì trong pilot).
- Điền `submission/submission.json` (team, 4 thành viên dạng `HoVaTen-MSSV`, thẻ S7, v1/v2, ba dòng) và bảng thành viên `TEAM.md`.
- Chạy lệnh 7 tới khi in `ĐỦ THÀNH PHẦN` và đẩy bài nộp.

### Bằng chứng

- Commit `3b7a333` *LAB 10: bài nộp* (`submission/`, `TEAM.md`, Phiếu C mục C12).
- Lệnh 7: `ĐỦ THÀNH PHẦN`; `submission/manifest.json`; report ba mốc S7 base `R-S7-before-20261119-161802-cc3998`,
  prepared `R-S7-prepared-20261119-161802-cc3998`, after `R-S7-after-20261119-161802-cc3998`.
- Phiếu C mục C12 (bằng chứng 1–3, dòng `decision_rule` khớp, mục "Chỉ ở v2").

### Exit ticket

- Học được: cả bốn quyết định đều có thể đạt; điều làm quyết định đứng vững là nó khớp **từng vế** của tiêu chí đã ký và có mã lần chạy
  đi kèm, không phải việc chọn phương án an toàn nhất.
- Còn chưa chắc: "Tiếp tục" trên dữ liệu mock có còn đúng khi chạy với lưu lượng thật và REFUND-v4 hay không; đó là việc phải đo lại
  trước Bước đánh giá 2.
