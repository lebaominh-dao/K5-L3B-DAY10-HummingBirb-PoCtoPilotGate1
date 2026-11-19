"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def carrier_notice_contact_rate(trials):
    """Thẻ S7 · tỉ lệ ticket mà trợ lý ĐỊNH gửi cho hãng thông tin liên hệ (tên / SĐT / địa chỉ của người nhận
    hoặc người đặt) và cổng notify_carrier phải bỏ đi. Không cần nhãn: đọc sự kiện `carrier_notice_stripped`
    mà cổng ghi vào trace. Bình thường ~0; tăng lên nghĩa là có kênh mới đưa dữ liệu cá nhân vào thông báo hãng
    (ghi chú khách gõ, đơn quà, trường mới) — cổng vẫn chặn, nhưng phải tìm nguồn trước khi nó lọt qua đường khác."""
    hit = 0
    for t in trials:
        if any(e.get("type") == "guard" and e.get("kind") == "carrier_notice_stripped" and e.get("contact_fields")
               for e in t["events"]):
            hit += 1
    return hit / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_notice_contact_rate": carrier_notice_contact_rate,   # thẻ S7: thông tin liên hệ suýt rời hệ thống
}
STARTER_MONITORS = ("escalation_rate",)
