/* Dữ liệu và quy tắc UX cho bản giao diện. Giá đã gồm VAT. */
const A360 = (() => {
  const KEY = {
    cart: "a360_cart",
    orders: "a360_orders",
    bookings: "a360_bookings",
    vehicle: "a360_vehicle",
    session: "a360_session",
    threads: "a360_threads",
    seq: "a360_seq"
  };

  const showrooms = [
    { id: "q7", name: "Quận 7", address: "215 Nguyễn Hữu Thọ, Tân Hưng, Quận 7, TP. Hồ Chí Minh", phone: "0901 360 360", hours: "08:00–20:00", primary: true },
    { id: "td", name: "Thủ Đức", address: "12 Võ Văn Ngân, Linh Chiểu, TP. Thủ Đức", phone: "0901 360 361", hours: "08:00–20:00", primary: false },
    { id: "bt", name: "Bình Thạnh", address: "88 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP. Hồ Chí Minh", phone: "0901 360 362", hours: "08:00–19:00", primary: false }
  ];

  const vehicles = [
    { id: "camry", label: "Toyota Camry 2022" },
    { id: "civic", label: "Honda Civic 2021" },
    { id: "vf8", label: "VinFast VF8 2024" }
  ];

  const services = [
    { id: "ceramic", name: "Phủ ceramic 9H", image: "assets/img/polish.jpg", minutes: 240, priceFrom: 4500000, priceTo: 12000000, summary: "Lớp phủ bóng sâu, hạn chế bám nước và trầy xước nhẹ.", steps: ["Rửa và khử nhiễm sơn", "Đánh bóng nếu sơn còn tốt", "Phủ ceramic và nghỉ đóng rắn", "Bàn giao phiếu bảo hành"], shops: ["q7", "td"] },
    { id: "film", name: "Dán phim cách nhiệt", image: "assets/img/svc-film.jpg", minutes: 150, priceFrom: 2800000, priceTo: 7500000, summary: "Cản nhiệt, chống UV, giảm chói cho kính lái, sườn và hậu.", steps: ["Đo kính theo xe", "Dán phim và ép mép", "Kiểm tra bọt và tầm nhìn"], shops: ["q7", "td", "bt"] },
    { id: "leather", name: "Bọc ghế da", image: "assets/img/steer.jpg", minutes: 480, priceFrom: 6500000, priceTo: 18000000, summary: "May form ghế zin, giữ túi khí, chọn màu tại showroom.", steps: ["Chọn da và chỉ may", "Lấy form", "Bọc và lắp lại nội thất"], shops: ["q7", "td"] },
    { id: "detail", name: "Detailing nội thất", image: "assets/img/svc-ceramic.jpg", minutes: 180, priceFrom: 1200000, priceTo: 3500000, summary: "Vệ sinh sâu ghế, trần, sàn và khử mùi khoang máy lạnh.", steps: ["Hút bụi toàn khoang", "Xử lý theo chất liệu", "Khử mùi và dưỡng bề mặt"], shops: ["q7", "td", "bt"] },
    { id: "sound", name: "Cách âm chống ồn", image: "assets/img/dash2.jpg", minutes: 360, priceFrom: 5000000, priceTo: 15000000, summary: "Dán cách âm sàn, cửa và hốc bánh.", steps: ["Tháo nội thất cần thiết", "Dán vật liệu", "Lắp lại và chạy thử"], shops: ["q7"] },
    { id: "wash", name: "Rửa xe chuyên sâu", image: "assets/img/svc-wash.jpg", minutes: 60, priceFrom: 250000, priceTo: 650000, summary: "Quy trình 2 xô, dưỡng lốp và kính.", steps: ["Xả và rửa 2 xô", "Làm khô", "Dưỡng lốp, kính"], shops: ["q7", "td", "bt"] }
  ];

  const products = [
    {
      slug: "thung-cop-360", name: "Thùng lưu trữ cốp xe 360", brand: "360 Gear", category: "phu-kien-cop", categoryName: "Phụ kiện cốp",
      image: "assets/img/svc-film.jpg", fitment: "all", fits: [], ship: true, install: false, warranty: 12,
      blurb: "Chống nước, cố định trong cốp, ngăn đồ gọn.",
      specs: [["Chất liệu", "Nhựa cứng có gioăng"], ["Xuất xứ", "Lắp ráp trong nước"]],
      variants: [{ id: "thung-den", name: "Màu đen", sku: "COP-DEN", price: 890000, compare: 1690000, shipStock: 12, shops: { q7: 2, td: 1, bt: 0 }, weight: 1800 }]
    },
    {
      slug: "nuoc-hoa-khe-gio", name: "Nước hoa khe gió", brand: "360 Scent", category: "noi-that", categoryName: "Nội thất",
      image: "assets/img/steer.jpg", fitment: "all", fits: [], ship: true, install: false, warranty: 0,
      blurb: "Kẹp cửa gió, hương gỗ nhẹ.",
      specs: [["Dung tích", "8 ml"], ["Lắp", "Khe gió điều hòa"]],
      variants: [{ id: "nh-go", name: "Hương gỗ", sku: "SCENT-GO", price: 219000, compare: 390000, shipStock: 40, shops: { q7: 6, td: 4, bt: 4 }, weight: 80 }]
    },
    {
      slug: "oc-mam-titan", name: "Bộ ốc mâm titan", brand: "360 Wheel", category: "mam-xe", categoryName: "Mâm xe",
      image: "assets/img/rim.jpg", fitment: "list", fits: ["camry", "civic"], ship: true, install: true, warranty: 12,
      blurb: "Bộ 20 ốc, kiểu đóng. Cần đúng lazang xe.",
      specs: [["Số lượng", "20"], ["Kiểu", "Đóng"]],
      variants: [{ id: "oc-20", name: "Bộ 20 chiếc", sku: "LUG-20", price: 259000, compare: 450000, shipStock: 18, shops: { q7: 4, td: 2, bt: 0 }, weight: 600 }]
    },
    {
      slug: "camera-hanh-trinh-4k", name: "Camera hành trình 4K", brand: "360 Cam", category: "camera-hanh-trinh", categoryName: "Camera hành trình",
      image: "assets/img/hero5.jpg", fitment: "consult", fits: ["camry", "civic", "vf8"], ship: true, install: true, warranty: 12,
      blurb: "Ghi hình phía trước. Bản Pro thêm camera lùi. Cần xác nhận độ vừa trước khi lắp.",
      specs: [["Độ phân giải", "4K phía trước"], ["Kết nối", "Wi-Fi"]],
      variants: [
        { id: "cam-std", name: "Tiêu chuẩn", sku: "CAM-4K", price: 1890000, compare: 3290000, shipStock: 6, shops: { q7: 2, td: 1, bt: 0 }, weight: 350 },
        { id: "cam-pro", name: "Pro + camera lùi", sku: "CAM-4K-PRO", price: 2490000, compare: 3990000, shipStock: 2, shops: { q7: 1, td: 0, bt: 0 }, weight: 480 }
      ]
    },
    {
      slug: "man-hinh-android", name: "Màn hình Android", brand: "360 Play", category: "man-hinh-android", categoryName: "Màn hình Android",
      image: "assets/img/steer.jpg", fitment: "list", fits: ["camry", "vf8"], ship: true, install: true, warranty: 24,
      blurb: "Màn hình theo xe, có CarPlay. Chọn kích thước đúng đời xe.",
      specs: [["Hệ điều hành", "Android"], ["Bảo hành", "24 tháng"]],
      variants: [
        { id: "mh-9", name: "9 inch", sku: "AND-9", price: 5490000, compare: 6990000, shipStock: 4, shops: { q7: 1, td: 1, bt: 0 }, weight: 1600 },
        { id: "mh-10", name: "10 inch", sku: "AND-10", price: 6290000, compare: 7990000, shipStock: 0, shops: { q7: 0, td: 1, bt: 0 }, weight: 1700 }
      ]
    },
    {
      slug: "tham-lot-san", name: "Thảm lót sàn", brand: "360 Mat", category: "tham-lot-san", categoryName: "Thảm lót sàn",
      image: "assets/img/svc-ceramic.jpg", fitment: "list", fits: ["camry", "civic", "vf8"], ship: true, install: false, warranty: 12,
      blurb: "Thảm khay, ôm sàn theo xe.",
      specs: [["Chất liệu", "TPE"], ["Bộ", "Hàng trước và sau"]],
      variants: [{ id: "tham-den", name: "Đen", sku: "MAT-DEN", price: 1250000, compare: 1790000, shipStock: 9, shops: { q7: 3, td: 2, bt: 1 }, weight: 4200 }]
    },
    {
      slug: "den-bi-laser", name: "Đèn bi laser", brand: "360 Light", category: "den-bi-laser", categoryName: "Đèn bi laser",
      image: "assets/img/hero5.jpg", fitment: "consult", fits: [], ship: false, install: true, warranty: 12,
      blurb: "Nâng cấp ánh sáng. Chỉ lắp tại showroom. Cần xác nhận độ vừa trước khi lắp.",
      specs: [["Nhiệt màu", "5500K"], ["Lắp", "Tại showroom"]],
      variants: [{ id: "den-bo", name: "Bộ 2 bi", sku: "LASER-2", price: 8900000, compare: 12500000, shipStock: 0, shops: { q7: 2, td: 1, bt: 0 }, weight: 2200 }]
    },
    {
      slug: "cam-bien-lop", name: "Cảm biến áp suất lốp", brand: "360 Safe", category: "cam-bien-lop", categoryName: "Cảm biến áp suất lốp",
      image: "assets/img/blackcar.jpg", fitment: "all", fits: [], ship: true, install: true, warranty: 12,
      blurb: "Hiển thị áp suất từng lốp, gắn van trong.",
      specs: [["Cảm biến", "Van trong"], ["Màn hình", "Pin rời"]],
      variants: [{ id: "tpms", name: "Bộ 4 van", sku: "TPMS-4", price: 1590000, compare: 1990000, shipStock: 1, shops: { q7: 0, td: 2, bt: 1 }, weight: 500 }]
    }
  ];

  const categories = [...new Map(products.map((p) => [p.category, p.categoryName])).entries()].map(([id, name]) => ({ id, name }));

  function read(key, fallback) {
    const missing = () => (typeof fallback === "function" ? fallback() : fallback);
    try {
      const raw = localStorage.getItem(key);
      if (raw == null) return missing();
      return JSON.parse(raw) ?? missing();
    } catch {
      return missing();
    }
  }
  function write(key, value) { localStorage.setItem(key, JSON.stringify(value)); }

  function vnd(n) { return Number(n || 0).toLocaleString("vi-VN") + "đ"; }
  function pct(price, compare) {
    if (!compare || compare <= price) return 0;
    return Math.round((1 - price / compare) * 100);
  }
  function product(slug) { return products.find((p) => p.slug === slug) || null; }
  function variantOf(p, id) { return p.variants.find((v) => v.id === id) || p.variants[0]; }
  function stock(variant, mode, showroomId) {
    if (mode === "ship") return variant.shipStock;
    return variant.shops[showroomId] || 0;
  }
  function defaultMode(p, variant) {
    if (p.ship && stock(variant, "ship") > 0) return { mode: "ship", showroomId: "" };
    const shop = showrooms.find((s) => stock(variant, "install", s.id) > 0);
    if (p.install && shop) return { mode: "install", showroomId: shop.id };
    return null;
  }

  const cart = {
    get() { return read(KEY.cart, []); },
    save(lines) { write(KEY.cart, lines); },
    count() { return cart.get().reduce((sum, line) => sum + line.qty, 0); },
    add(input) {
      const p = product(input.slug);
      if (!p) return { ok: false, message: "Không thấy sản phẩm." };
      const variant = variantOf(p, input.variantId);
      const mode = input.mode;
      const showroomId = mode === "install" ? input.showroomId : "";
      if (mode === "ship" && !p.ship) return { ok: false, message: "Sản phẩm không giao hàng." };
      if (mode === "install" && !p.install) return { ok: false, message: "Sản phẩm không lắp tại showroom." };
      const avail = stock(variant, mode, showroomId);
      if (avail < 1) return { ok: false, message: "Biến thể này tạm hết hàng." };
      const key = variant.id + "|" + mode + "|" + showroomId;
      const lines = cart.get();
      const found = lines.find((line) => line.key === key);
      const nextQty = (found ? found.qty : 0) + (input.qty || 1);
      if (nextQty > avail || nextQty > 20) {
        return { ok: false, message: "Chỉ còn " + avail + " sản phẩm cho hình thức này." };
      }
      if (found) found.qty = nextQty;
      else lines.push({ key, slug: p.slug, variantId: variant.id, qty: input.qty || 1, mode, showroomId });
      cart.save(lines);
      return { ok: true, message: "Đã thêm " + p.name };
    },
    setQty(key, qty) {
      const lines = cart.get();
      const line = lines.find((item) => item.key === key);
      if (!line) return;
      const p = product(line.slug);
      const variant = variantOf(p, line.variantId);
      const avail = stock(variant, line.mode, line.showroomId);
      line.qty = Math.max(1, Math.min(qty, avail, 20));
      cart.save(lines);
    },
    remove(key) { cart.save(cart.get().filter((line) => line.key !== key)); },
    removeMany(keys) { cart.save(cart.get().filter((line) => !keys.includes(line.key))); }
  };

  function enrich(line) {
    const p = product(line.slug);
    const variant = p ? variantOf(p, line.variantId) : null;
    if (!p || !variant) return { ...line, invalid: "Sản phẩm không còn bán." };
    const avail = stock(variant, line.mode, line.showroomId);
    const unit = variant.price;
    return {
      ...line,
      name: p.name,
      variantName: variant.name,
      image: p.image,
      sku: variant.sku,
      unit,
      compare: variant.compare,
      avail,
      invalid: avail < 1 ? "Hết hàng." : line.qty > avail ? "Vượt tồn." : "",
      lineTotal: unit * line.qty,
      fitment: p.fitment
    };
  }

  function couponResult(code, subtotal, mode) {
    const raw = (code || "").trim().toUpperCase();
    if (!raw) return { ok: true, code: "", amount: 0, freeShip: false };
    const table = {
      HETHAN: { ok: false, message: "Mã đã hết hạn." },
      THIEU: { ok: false, min: 5000000 },
      GIAM10: { ok: true, min: 500000, rate: 0.1 },
      FREESHIP: { ok: true, freeShip: true }
    };
    const rule = table[raw];
    if (!rule) return { ok: false, message: "Không thấy mã này." };
    if (rule.message) return rule;
    if (rule.min && subtotal < rule.min) {
      return { ok: false, message: "Đơn chưa đạt giá trị tối thiểu " + vnd(rule.min) + "." };
    }
    if (rule.freeShip && mode === "install") {
      return { ok: false, message: "Mã chỉ áp dụng cho đơn giao hàng." };
    }
    return { ok: true, code: raw, amount: Math.round(subtotal * (rule.rate || 0)), freeShip: !!rule.freeShip };
  }

  function shipFee(subtotal, district, freeShip) {
    if (freeShip) return 0;
    if (!district) return null;
    const base = district === "Khác" ? 50000 : 35000;
    return subtotal >= 1000000 ? 0 : base;
  }

  const orders = {
    list() { return read(KEY.orders, seedOrders); },
    save(list) { write(KEY.orders, list); },
    create(payload) {
      const seq = read(KEY.seq, 12) + 1;
      write(KEY.seq, seq);
      const code = "DH2026" + String(seq).padStart(6, "0");
      const order = { code, createdAt: new Date().toISOString(), status: payload.status, ...payload, code };
      const list = orders.list();
      list.unshift(order);
      orders.save(list);
      return order;
    },
    update(code, patch) {
      const list = orders.list();
      const order = list.find((item) => item.code === code);
      if (!order) return null;
      Object.assign(order, patch);
      orders.save(list);
      return order;
    },
    find(code, phone) {
      const digits = (phone || "").replace(/\D/g, "");
      return orders.list().find((order) => order.code === code.trim().toUpperCase() && order.phone.replace(/\D/g, "") === digits) || null;
    }
  };

  function seedOrders() {
    const seeded = [{
      code: "DH2026000012",
      createdAt: "2026-09-28T02:00:00.000Z",
      status: "Hoàn thành",
      phone: "0901234567",
      name: "Nguyễn An",
      email: "an@example.com",
      mode: "ship",
      payment: "transfer",
      paid: true,
      showroomId: "",
      address: "12 Nguyễn Huệ, Quận 1, TP. Hồ Chí Minh",
      subtotal: 219000,
      discount: 0,
      fee: 0,
      total: 219000,
      lines: [{ slug: "nuoc-hoa-khe-gio", name: "Nước hoa khe gió", variantName: "Hương gỗ", qty: 1, unit: 219000 }]
    }];
    write(KEY.orders, seeded);
    return seeded;
  }

  const bookings = {
    list() { return read(KEY.bookings, []); },
    create(entry) {
      const item = { code: "LH" + Date.now().toString().slice(-6), status: "Chờ xác nhận", createdAt: new Date().toISOString(), ...entry };
      const list = bookings.list();
      list.unshift(item);
      write(KEY.bookings, list);
      return item;
    },
    taken(showroomId, serviceId, time) {
      if (showroomId === "q7" && serviceId === "ceramic" && time === "10:00") return true;
      return bookings.list().some((item) => item.showroomId === showroomId && item.serviceId === serviceId && item.time === time && item.status !== "Đã hủy");
    }
  };

  const slots = ["08:00", "10:00", "13:00", "15:00", "17:00"];

  const session = {
    get() { return read(KEY.session, null); },
    login(phone, name) { const value = { phone, name: name || "Khách 360" }; write(KEY.session, value); return value; },
    logout() { localStorage.removeItem(KEY.session); }
  };

  const chat = {
    thread() {
      return read(KEY.threads, { messages: [], phone: "", name: "", status: "Mới" });
    },
    save(thread) { write(KEY.threads, thread); },
    push(author, text) {
      const thread = chat.thread();
      thread.messages.push({ author, text, at: new Date().toISOString() });
      if (author === "khách" && thread.status === "Đã xong") thread.status = "Mới";
      chat.save(thread);
      return thread;
    }
  };

  const vehicle = {
    get() { return localStorage.getItem(KEY.vehicle) || ""; },
    set(id) { if (id) localStorage.setItem(KEY.vehicle, id); else localStorage.removeItem(KEY.vehicle); }
  };

  function fitsLabel(p) {
    const selected = vehicle.get();
    if (!selected) return "";
    if (p.fitment === "consult") return "Cần xác nhận độ vừa trước khi lắp.";
    if (p.fitment === "all" || p.fits.includes(selected)) return "Vừa xe của bạn";
    return "Không nằm trong danh sách vừa xe đã chọn";
  }

  return {
    showrooms, vehicles, services, products, categories,
    vnd, pct, product, variantOf, stock, defaultMode, enrich,
    couponResult, shipFee, cart, orders, bookings, slots,
    session, chat, vehicle, fitsLabel
  };
})();
