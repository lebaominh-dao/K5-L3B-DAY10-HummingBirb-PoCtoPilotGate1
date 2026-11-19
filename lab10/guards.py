"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ---------------------------------------------------------------------------------------------
# Hàm tra cứu dùng chung: mọi cổng chỉ tin NGUỒN SỰ THẬT (đơn, tracking DB, bảng chính sách theo
# ngày hiệu lực, bảng phê duyệt), không tin chữ khách viết hay con số model tự suy.
# ---------------------------------------------------------------------------------------------

def _policy(ctx):
    """Chính sách có hiệu lực theo NGÀY (ctx.as_of), không theo cờ index_active của chỉ mục."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _late_parcel(ctx, order):
    """Kiện mà ticket nói tới (hoặc kiện trễ nhất) và độ trễ của nó theo tracking DB."""
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return parcel, H.db_delay_days(parcel, ctx.as_of)


def _entitlement(ctx, order, policy):
    """Số tiền khách được hoàn theo tracking DB + chính sách hiệu lực."""
    parcel, delay = _late_parcel(ctx, order)
    cause = parcel.get("delay_cause") or ("CARRIER" if delay > 0 else None)
    return H.entitlement_vnd(policy, order, delay, cause)


def _approval_ok(ctx, approval_id, order_id, amount):
    """Phê duyệt chỉ hợp lệ khi: đúng đơn, còn 'valid', chưa hết hạn, đủ hạn mức, đúng người duyệt đứng tên."""
    approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
    for a in ctx.tools.lookup_approvals(approval_id=approval_id):
        if (a.get("order_id") == order_id and a.get("status") == "valid"
                and a.get("expires_at", "") >= ctx.as_of and a.get("max_vnd", 0) >= amount
                and (not approver or a.get("approver_id") == approver)):
            return True
    return False


def _contacts(ctx, order):
    """Thông tin liên hệ của người nhận và người đặt (nguồn: đơn hàng, hồ sơ khách) để dò trong dữ liệu gửi đi."""
    people = [(order or {}).get("recipient") or {}]
    cust = ctx.tools.lookup_customer((order or {}).get("customer_id")) if order else None
    if cust:
        people.append(cust)
    phones = {H.digits(str(p.get("phone", "")))[-9:] for p in people if H.digits(str(p.get("phone", "")))}
    words = {str(p.get(k)).lower() for p in people for k in ("name", "street", "address") if p.get(k)}
    return phones, words


def _has_contact(value, phones, words):
    blob = str(value)
    return any(ph and ph in H.digits(blob) for ph in phones) or any(w in blob.lower() for w in words)


def pre_guard(ctx):
    # Cổng 0 (phụ trợ cổng 1): ghim phiên bản chính sách theo ngày hiệu lực, để trợ lý không đọc nhầm
    # cờ index_active cũ khi chính sách đổi (REFUND-v4 có hiệu lực từ 2026-12-01).
    pol = _policy(ctx)
    if pol is not None:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    order = ctx.tools.lookup_order(action.get("order_id")) if action.get("order_id") else None
    policy = _policy(ctx)

    # Cổng 1 · issue_refund: tiền hoàn phải khớp quyền lợi tính từ nguồn sự thật (B6 lý do kỹ thuật, B4 WRONG).
    if tool == "issue_refund":
        if order is None or policy is None:
            return Verdict.escalate("không tra được đơn hoặc chính sách hiệu lực: chuyển người duyệt")
        if action.get("basis") == "fail_open":
            return Verdict.escalate("LLM kiểm chính sách lỗi (fail_open): không tự hoàn, chuyển người duyệt")
        if action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("lệnh hoàn bắt shop trả tiền: phải có người duyệt")
        if ctx.tools.ledger_rows(order_id=order["order_id"]):
            return Verdict.deny("đơn đã có dòng hoàn trong sổ cái: không hoàn lần hai")
        amount = int(action.get("amount_vnd") or 0)
        want = _entitlement(ctx, order, policy)
        if want <= 0:
            return Verdict.deny(f"tracking DB + {policy['policy_id']}: đơn không đủ điều kiện hoàn")
        if amount > policy["auto_limit_vnd"] or want > policy["auto_limit_vnd"]:
            if not action.get("approval_id") or not _approval_ok(ctx, action["approval_id"], order["order_id"],
                                                                 min(amount, want)):
                return Verdict.escalate("vượt hạn mức tự động mà không có phê duyệt hợp lệ cho đúng đơn")
        if amount > want:
            ctx.log("refund_clamped", asked=amount, entitled=want)
            return Verdict.modify(f"hạ về quyền lợi theo tracking DB ({want}đ)", amount_vnd=want)
        return Verdict.allow()

    # Cổng 2 · file_carrier_fault: chỉ ghi lỗi khi tracking DB có nguyên nhân thuộc lỗi hãng, đúng kiện trễ,
    # đúng số ngày trễ (B6 lý do pháp lý, B4 INCOMPLETE).
    if tool == "file_carrier_fault":
        if order is None or policy is None:
            return Verdict.deny("không tra được đơn hoặc chính sách: không ghi lỗi hãng")
        parcel, delay = _late_parcel(ctx, order)
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny(f"tracking DB không ghi nguyên nhân lỗi hãng cho {parcel['parcel_id']} "
                                f"(trễ {delay} ngày, cause={parcel.get('delay_cause')})")
        right = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                 "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(k) != v for k, v in right.items()):
            return Verdict.modify("sửa về đúng kiện / hãng / số ngày trễ theo tracking DB", **right)
        return Verdict.allow()

    # Cổng 3 · notify_carrier: chỉ gửi đúng các trường chính sách cho phép (B6 lý do pháp lý, B4 PERTURBED).
    # Vòng 2 (thẻ S7): BẢO ĐẢM thay vì dò-và-che. Payload gửi hãng được DỰNG LẠI từ nguồn sự thật theo đúng
    # danh sách `carrier_notice_fields` (spec của kênh gửi hãng); không chép bất kỳ giá trị nào do khách gõ hay
    # do trợ lý tự gắn. Trường nằm ngoài spec bị bỏ; nếu thứ bị bỏ chứa thông tin liên hệ thì ghi sự kiện để theo dõi.
    if tool == "notify_carrier":
        payload = dict(action.get("payload") or {})
        if order is None:      # notify_carrier không có order_id ở cấp ngoài: lấy từ payload, rồi từ ticket
            order = ctx.tools.lookup_order(payload.get("order_id") or ctx.ticket.get("order_id"))
        allowed = list((policy or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "district", "delay_days"])
        clean = {}
        if order is not None:
            parcel = next((x for x in order["parcels"] if x["parcel_id"] == payload.get("parcel_id")), None) \
                or _late_parcel(ctx, order)[0]
            truth = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                     "district": (order.get("recipient") or {}).get("district"),
                     "delay_days": H.db_delay_days(parcel, ctx.as_of)}
            clean = {k: truth[k] for k in allowed if k in truth}
        if not clean:
            return Verdict.deny("không dựng được thông báo hãng từ nguồn sự thật: không gửi")
        dropped = sorted(k for k in payload if k not in clean)
        phones, words = _contacts(ctx, order)
        leaked = sorted(k for k in payload if k not in clean and _has_contact(payload[k], phones, words))
        if dropped or leaked:
            ctx.log("carrier_notice_stripped", dropped=dropped, contact_fields=leaked, gift=bool((order or {}).get("is_gift")))
        if clean != payload:
            return Verdict.modify("dựng lại thông báo hãng theo carrier_notice_fields từ nguồn sự thật"
                                  + (" (bỏ: " + ", ".join(dropped) + ")" if dropped else ""), payload=clean)
        return Verdict.allow()

    return Verdict.allow()
