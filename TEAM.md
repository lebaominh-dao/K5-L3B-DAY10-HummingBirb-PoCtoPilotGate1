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
|   2 | Nguyễn Đức Hải | 2A202603943 | Kỹ sư cổng (vòng 2) |  |
|   3 | Trần Phú Thái | 2A202604001 |  |  |
|   4 | Vũ Quang Hải | 2A202603935 | Vận hành và pháp lý |  |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenDucHai-2A202603943

### Phần việc phụ trách

Vai **Kỹ sư cổng (vòng 2)**. CP4 (khối 3) với thẻ **S7**: nhận thẻ, câu 3.0–3.7, Phiếu C mục C0–C11, sửa `lab10/guards.py`,
thêm chỉ số trong `lab10/monitors.py`, chạy lệnh 6.

### Đóng góp cụ thể

- Nhận thẻ S7 vào `incidents/S7/`, chạy lệnh 6 **trước khi sửa**: cổng vòng 1 đã đưa lộ dữ liệu trên thẻ từ 30 → 0, chỉ còn ô
  `6 monitor` đỏ.
- Dò trace hai kiểu lỗi khác nguồn: chữ khách gõ bị chép sang hãng (`S7-01@11`) và đơn quà tự gắn liên hệ người nhận dù khách không
  gõ gì (`S7-20@11`); đối chứng `S7-05` (mã vận đơn không phải SĐT).
- Sửa cổng `notify_carrier` từ "lọc khoá" thành **dựng lại thông báo hãng từ nguồn sự thật** theo `carrier_notice_fields` (bảo đảm,
  không dò-và-che), ghi sự kiện `carrier_notice_stripped`.
- Thêm chỉ số `carrier_notice_contact_rate` (không cần nhãn) và điều kiện dừng tương ứng trong `operations.stop_conditions`.
- Phát hiện và sửa một regression của chính bản sửa (lệnh `notify_carrier` không mang `order_id` → bộ nền rơi về 0,5), ghi trung thực
  vào C0.
- Phiếu C: bảng soát lỗi, hiệu chỉnh lòng tin C3.3, HAZOP của thẻ, spec và giả định môi trường, fault tree trước/sau, bảng sửa,
  risk register, checklist và runbook 4–5.

### Bằng chứng

- Commit `5e4e2a7` *Nhận thẻ S7* và `1834350` *LAB 10: S7 · cổng notify_carrier …*.
- Lần chạy: grade trước khi sửa `R-S7-grade-20261119-161609-26eaa3`; lần sửa lỗi `R-S7-after-20261119-161706-dba546` /
  `R-base-after-20261119-161706-dba546` (regression); bản cuối `R-S7-after-20261119-161801-cc3998`, bộ nền
  `R-base-after-20261119-161801-cc3998`; grade `R-S7-grade-20261119-161802-cc3998`: `1 integrity ✅ · 3 visible ✅ ·
  5 regression ✅ · 6 monitor ✅` (chỉ số mới 0 trên bộ nền, 0,75 trên thẻ).
- Phiếu C mục C0, C2, C7, C8.

### Exit ticket

- Học được: "chỉ cho đi những trường đã liệt kê" là **ngăn**, còn "dò mẫu SĐT rồi che" chỉ là **giảm** (viết "0987 654 321" là lọt,
  mã vận đơn thì bị che nhầm); và phải chạy lại bộ nền sau mỗi lần sửa vì chính bản sửa cũng có thể gây hỏng.
- Còn chưa chắc: cổng và chỉ số chưa thấy trường hợp thông tin liên hệ nằm sẵn trong một trường được phép (ví dụ `district` nhập sai).

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
