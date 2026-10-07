const pageId = document.body.dataset.page;
const params = new URLSearchParams(location.search);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
}
function toast(message) {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.remove("show"), 2200);
}
function shopName(id) {
  return A360.showrooms.find((shop) => shop.id === id)?.name || "";
}
function vehicleName(id) {
  return A360.vehicles.find((car) => car.id === id)?.label || "";
}

function chrome(main, active) {
  const count = A360.cart.count();
  const links = [
    ["index.html", "Trang chủ", "home"],
    ["dich-vu.html", "Dịch vụ", "services"],
    ["phu-kien.html", "Sản phẩm", "catalog"],
    ["showroom.html", "Showroom", "shops"],
    ["index.html#lien-he", "Liên hệ", "contact"]
  ];
  return `
    <header class="header">
      <div class="wrap header-bar">
        <a class="logo" href="index.html"><span class="logo-badge">360</span><span><strong>AUTO DETAILING</strong><small>Phụ kiện & chăm sóc xe</small></span></a>
        <nav class="nav" id="nav">
          ${links.map(([href, label, id]) => `<a class="${id === active ? "active" : ""}" href="${href}">${label}</a>`).join("")}
        </nav>
        <div class="header-actions">
          <a class="icon-btn" href="tim-kiem.html" aria-label="Tìm kiếm">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
          </a>
          <a class="cart-link" href="gio-hang.html" aria-label="Giỏ hàng">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/><path d="M3 4h2l2.2 11h11.3l2-7H7"/></svg>
            ${count ? `<span class="cart-badge">${count}</span>` : ""}
          </a>
          <a class="btn btn-red" href="dich-vu.html">Đặt lịch</a>
          <button class="icon-btn menu-toggle" type="button" data-act="menu" aria-label="Mở menu">☰</button>
        </div>
      </div>
    </header>
    <main class="page"><div class="wrap">${main}</div></main>
    <footer class="footer"><div class="wrap footer-row">
      <span>© 2026 360 Auto Detailing</span>
      <span><a href="tra-cuu-don.html">Tra cứu đơn</a> · <a href="tai-khoan.html">Tài khoản</a> · <a href="quan-tri.html">Khu vận hành</a></span>
    </div></footer>
    <div class="chat-dock">
      <div class="chat-box" id="chatBox" hidden>
        <header><strong>Chat 360</strong><button type="button" data-act="close-chat" style="background:transparent;color:#fff;border:0;font-size:18px">×</button></header>
        <div class="chat-log" id="chatLog"></div>
        <form id="chatForm"><input name="text" placeholder="Nhắn cho showroom..." required><button class="btn btn-blue" type="submit">Gửi</button></form>
      </div>
      <button class="bubble chat" type="button" data-act="open-chat" aria-label="Mở chat">Chat</button>
      <a class="bubble zalo" href="https://zalo.me/0901360360" target="_blank" rel="noreferrer">Zalo</a>
      <a class="bubble phone" href="tel:0901360360" aria-label="Gọi">☎</a>
    </div>
    <div class="toast" id="toast" role="status"></div>`;
}

function paint(html) {
  document.getElementById("app").innerHTML = html;
  drawChat();
  window.scrollTo(0, 0);
}

function drawChat() {
  const log = document.getElementById("chatLog");
  if (!log) return;
  const thread = A360.chat.thread();
  log.innerHTML = thread.messages.map((msg) => `<div class="msg ${esc(msg.author)}">${esc(msg.text)}</div>`).join("") || `<div class="msg he-thong">Xin chào. Bạn cần tư vấn phụ kiện hay đặt lịch chăm sóc xe?</div>`;
  log.scrollTop = log.scrollHeight;
}

function catalogPage() {
  const cat = params.get("cat") || "";
  const selected = A360.vehicle.get();
  const sort = params.get("sort") || "new";
  let list = A360.products.filter((item) => !cat || item.category === cat);
  if (params.get("stock") === "1") list = list.filter((item) => item.variants.some((v) => v.shipStock > 0 || Object.values(v.shops).some((n) => n > 0)));
  if (sort === "price-asc") list = [...list].sort((a, b) => a.variants[0].price - b.variants[0].price);
  if (sort === "price-desc") list = [...list].sort((a, b) => b.variants[0].price - a.variants[0].price);
  if (sort === "discount") list = [...list].sort((a, b) => A360.pct(b.variants[0].price, b.variants[0].compare) - A360.pct(a.variants[0].price, a.variants[0].compare));
  const title = A360.categories.find((item) => item.id === cat)?.name || "Phụ kiện xe hơi";
  return chrome(`
    <p class="crumb"><a href="index.html">Trang chủ</a> / ${esc(title)}</p>
    <h1>${esc(title)}</h1>
    <p class="lead">Lọc theo xe đang chọn để thấy phụ kiện vừa xe. Giá đã gồm VAT.</p>
    <div class="layout">
      <aside class="panel">
        <h2>Bộ lọc</h2>
        <label class="field">Xe của bạn
          <select data-act="vehicle">
            <option value="">Tất cả xe</option>
            ${A360.vehicles.map((car) => `<option value="${car.id}" ${car.id === selected ? "selected" : ""}>${esc(car.label)}</option>`).join("")}
          </select>
        </label>
        <div class="checks">
          ${A360.categories.map((item) => `<label><input type="radio" name="cat" ${item.id === cat ? "checked" : ""} data-act="cat" value="${item.id}"> ${esc(item.name)}</label>`).join("")}
          <label><input type="radio" name="cat" ${cat === "" ? "checked" : ""} data-act="cat" value=""> Tất cả</label>
          <label><input type="checkbox" data-act="instock" ${params.get("stock") === "1" ? "checked" : ""}> Còn hàng</label>
        </div>
      </aside>
      <div>
        <label class="field" style="max-width:220px">Sắp xếp
          <select data-act="sort">
            <option value="new" ${sort === "new" ? "selected" : ""}>Mới nhất</option>
            <option value="price-asc" ${sort === "price-asc" ? "selected" : ""}>Giá tăng</option>
            <option value="price-desc" ${sort === "price-desc" ? "selected" : ""}>Giá giảm</option>
            <option value="discount" ${sort === "discount" ? "selected" : ""}>Giảm sâu nhất</option>
          </select>
        </label>
        <div class="grid-3">
          ${list.map(card).join("") || `<p>Không có sản phẩm khớp bộ lọc.</p>`}
        </div>
      </div>
    </div>`, "catalog");
}

function card(p) {
  const variant = p.variants[0];
  const off = A360.pct(variant.price, variant.compare);
  const fit = A360.fitsLabel(p);
  const klass = fit.startsWith("Vừa") ? "ok" : fit.startsWith("Không") ? "no" : "warn";
  return `<article class="card product-card">
    <a href="san-pham.html?slug=${p.slug}"><img src="${p.image}" alt="${esc(p.name)}"></a>
    <div class="pad">
      ${off ? `<span class="tag">-${off}%</span>` : ""}
      ${fit ? `<span class="tag ${klass}">${esc(fit)}</span>` : ""}
      <h3><a href="san-pham.html?slug=${p.slug}">${esc(p.name)}</a></h3>
      <div class="price"><b>${A360.vnd(variant.price)}</b>${variant.compare > variant.price ? `<s>${A360.vnd(variant.compare)}</s>` : ""}</div>
      <div class="row-actions"><a class="btn btn-blue" href="san-pham.html?slug=${p.slug}">Xem và chọn</a></div>
    </div>
  </article>`;
}

function productPage() {
  const p = A360.product(params.get("slug"));
  if (!p) return chrome(`<h1>Không thấy sản phẩm</h1><p><a href="phu-kien.html">Về danh mục</a></p>`, "catalog");
  const variantId = params.get("v") || p.variants[0].id;
  const variant = A360.variantOf(p, variantId);
  const mode = params.get("mode") || (p.ship && variant.shipStock > 0 ? "ship" : "install");
  const showroomId = params.get("shop") || A360.showrooms.find((shop) => (variant.shops[shop.id] || 0) > 0)?.id || "q7";
  const fit = A360.fitsLabel(p);
  const shops = A360.showrooms.filter((shop) => (variant.shops[shop.id] || 0) > 0);
  return chrome(`
    <p class="crumb"><a href="index.html">Trang chủ</a> / <a href="phu-kien.html?cat=${p.category}">${esc(p.categoryName)}</a> / ${esc(p.name)}</p>
    <div class="pdp">
      <div class="card gallery"><img src="${p.image}" alt="${esc(p.name)}"></div>
      <div class="card buy">
        <p class="tag">${esc(p.brand)} · ${esc(variant.sku)}</p>
        <h1>${esc(p.name)}</h1>
        <div class="price"><b>${A360.vnd(variant.price)}</b> ${variant.compare > variant.price ? `<s>${A360.vnd(variant.compare)}</s>` : ""}</div>
        <p>${esc(p.blurb)}</p>
        ${fit ? `<p class="note">${esc(fit)}</p>` : ""}
        <strong>Phiên bản</strong>
        <div class="variants">
          ${p.variants.map((item) => {
            const dead = item.shipStock < 1 && !Object.values(item.shops).some((n) => n > 0);
            return `<button type="button" class="${item.id === variant.id ? "on" : ""}" ${dead ? "disabled" : ""} data-act="variant" data-v="${item.id}">${esc(item.name)}</button>`;
          }).join("")}
        </div>
        ${p.ship ? `<label class="choice ${mode === "ship" ? "on" : ""}"><input type="radio" name="mode" data-act="mode" value="ship" ${mode === "ship" ? "checked" : ""} ${variant.shipStock < 1 ? "disabled" : ""}><span><b>Giao tận nơi</b><br>Kho giao hàng còn ${variant.shipStock}</span></label>` : ""}
        ${p.install ? `<label class="choice ${mode === "install" ? "on" : ""}"><input type="radio" name="mode" data-act="mode" value="install" ${mode === "install" ? "checked" : ""} ${shops.length ? "" : "disabled"}><span><b>Lắp hoặc nhận tại showroom</b><br>${shops.length ? "Chọn showroom còn hàng" : "Hết hàng tại showroom"}</span></label>` : ""}
        ${mode === "install" ? `<label class="field">Showroom<select data-act="shop">${shops.map((shop) => `<option value="${shop.id}" ${shop.id === showroomId ? "selected" : ""}>${esc(shop.name)} · còn ${variant.shops[shop.id]}</option>`).join("")}</select></label>` : ""}
        <div class="qty"><button type="button" data-act="qty" data-dir="-1">−</button><strong id="qty">${params.get("qty") || 1}</strong><button type="button" data-act="qty" data-dir="1">+</button></div>
        <p></p>
        <button class="btn btn-red" type="button" data-act="add" data-slug="${p.slug}">Thêm vào giỏ</button>
      </div>
    </div>
    <div class="tabs">
      <button type="button" class="on" data-act="tab" data-tab="mo-ta">Mô tả</button>
      <button type="button" data-act="tab" data-tab="thong-so">Thông số</button>
      <button type="button" data-act="tab" data-tab="danh-gia">Đánh giá</button>
    </div>
    <div class="card" id="tab-mo-ta" style="padding:16px"><p>${esc(p.blurb)} Bảo hành ${p.warranty ? p.warranty + " tháng" : "theo hóa đơn"}.</p></div>
    <div class="card" id="tab-thong-so" hidden style="padding:0"><table class="spec-table">${p.specs.map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join("")}</table></div>
    <div class="card" id="tab-danh-gia" hidden style="padding:16px">${reviews(p)}</div>`, "catalog");
}

function reviews(p) {
  const session = A360.session.get();
  const bought = session && A360.orders.list().some((order) => order.status === "Hoàn thành" && order.phone.replace(/\D/g, "") === session.phone.replace(/\D/g, "") && order.lines.some((line) => line.slug === p.slug));
  return `<p><b>4,8</b> / 5 từ đánh giá đã duyệt</p>
    <p>Khách đã mua: đúng mô tả, lắp nhanh tại Quận 7.</p>
    ${bought ? `<form id="reviewForm"><label class="field">Đánh giá của bạn<textarea name="text" minlength="20" required placeholder="Tối thiểu 20 ký tự"></textarea></label><button class="btn btn-blue" type="submit">Gửi đánh giá</button></form>` : `<p class="note">Đăng nhập bằng số điện thoại của đơn đã hoàn thành để đánh giá. Tài khoản mẫu: 0901234567, mã 123456, đã mua nước hoa khe gió.</p><a href="tai-khoan.html">Về tài khoản</a>`}`;
}

function cartPage() {
  const lines = A360.cart.get().map(A360.enrich);
  const modes = [...new Set(lines.map((line) => line.mode))];
  const mixed = modes.length > 1;
  return chrome(`
    <p class="crumb"><a href="index.html">Trang chủ</a> / Giỏ hàng</p>
    <h1>Giỏ hàng</h1>
    ${mixed ? `<div class="alert">Một đơn không gồm cả giao tận nơi và lắp tại showroom. Hãy thanh toán từng nhóm.</div>` : ""}
    ${lines.length ? lines.map(lineView).join("") : `<div class="card" style="padding:16px"><p>Giỏ đang trống.</p><a class="btn btn-blue" href="phu-kien.html">Xem phụ kiện</a></div>`}
    ${modes.map((mode) => summary(lines.filter((line) => line.mode === mode), mode, mixed)).join("")}
  `, "catalog");
}

function lineView(line) {
  return `<article class="card" style="padding:12px 14px;margin-bottom:10px">
    <div class="cart-line">
      <img src="${line.image || ""}" alt="">
      <div>
        <strong>${esc(line.name || "Sản phẩm")}</strong>
        <div>${esc(line.variantName || "")} · ${line.mode === "ship" ? "Giao tận nơi" : "Lắp tại " + esc(shopName(line.showroomId))}</div>
        <div>${A360.vnd(line.unit || 0)}</div>
        ${line.invalid ? `<div class="alert">${esc(line.invalid)}</div>` : ""}
        <div class="qty"><button type="button" data-act="line-qty" data-key="${esc(line.key)}" data-dir="-1">−</button><span>${line.qty}</span><button type="button" data-act="line-qty" data-key="${esc(line.key)}" data-dir="1">+</button>
        <button type="button" data-act="remove" data-key="${esc(line.key)}">Xóa</button></div>
      </div>
      <b>${A360.vnd(line.invalid ? 0 : line.lineTotal)}</b>
    </div>
  </article>`;
}

function summary(lines, mode, mixed) {
  const usable = lines.filter((line) => !line.invalid);
  const subtotal = usable.reduce((sum, line) => sum + line.lineTotal, 0);
  if (!lines.length) return "";
  const blocked = lines.some((line) => line.invalid);
  return `<aside class="card money" style="padding:16px;margin:12px 0">
    <h2>${mode === "ship" ? "Nhóm giao hàng" : "Nhóm lắp tại showroom"}</h2>
    <div><span>Tạm tính</span><b>${A360.vnd(subtotal)}</b></div>
    ${blocked ? `<p class="alert">Có dòng hết hàng. Xóa hoặc giảm số lượng trước khi thanh toán.</p>` : ""}
    <a class="btn btn-red ${blocked ? "is-off" : ""}" href="thanh-toan.html?mode=${mode}">Thanh toán nhóm này</a>
  </aside>`;
}

function checkoutPage() {
  const mode = params.get("mode") === "install" ? "install" : "ship";
  const lines = A360.cart.get().map(A360.enrich).filter((line) => line.mode === mode && !line.invalid);
  if (!lines.length) return chrome(`<h1>Không có món để thanh toán</h1><a href="gio-hang.html">Về giỏ</a>`, "catalog");
  const code = params.get("coupon") || "";
  const district = params.get("district") || "";
  const subtotal = lines.reduce((sum, line) => sum + line.lineTotal, 0);
  const coupon = A360.couponResult(code, subtotal, mode);
  const fee = mode === "install" ? 150000 : A360.shipFee(subtotal, district, coupon.ok && coupon.freeShip);
  const total = subtotal - (coupon.ok ? coupon.amount : 0) + (fee || 0);
  const shop = lines[0].showroomId;
  return chrome(`
    <div class="steps"><span>Giỏ</span><span class="now">Thanh toán</span><span>Xác nhận</span></div>
    <h1>Thanh toán · ${mode === "ship" ? "Giao tận nơi" : "Lắp tại showroom"}</h1>
    <div class="grid-2">
      <form class="card" id="payForm" data-subtotal="${subtotal}" data-mode="${mode}" style="padding:16px">
        <label class="field">Họ tên<input name="name" required value="${esc(A360.session.get()?.name || "")}"></label>
        <label class="field">Số điện thoại<input name="phone" required pattern="0[0-9]{9}" value="${esc(A360.session.get()?.phone || "")}" placeholder="10 số"></label>
        <label class="field">Email<input name="email" type="email" placeholder="Để nhận biên nhận"></label>
        ${mode === "ship" ? `
          <label class="field">Khu vực<select name="district" data-act="district" required>
            <option value="">Chọn</option>
            ${["Quận 7", "Quận 1", "Thủ Đức", "Khác"].map((item) => `<option ${item === district ? "selected" : ""}>${item}</option>`).join("")}
          </select></label>
          <label class="field">Địa chỉ<input name="address" required placeholder="Số nhà, đường"></label>` : `
          <p><b>${esc(shopName(shop))}</b></p>
          <label class="field">Ngày<input type="date" name="date" required></label>
          <label class="field">Khung giờ<select name="time" required>${A360.slots.map((time) => `<option>${time}</option>`).join("")}</select></label>
          <label class="field">Hãng và dòng xe<input name="car" required placeholder="Ví dụ Toyota Camry 2022"></label>`}
        ${lines.some((line) => line.fitment === "consult") ? `<p class="note">Đơn có sản phẩm cần xác nhận độ vừa trước khi lắp.</p>${mode === "ship" ? `<label class="field">Xe<input name="car" required></label>` : ""}` : ""}
        <label class="field">Mã giảm giá<input name="coupon" value="${esc(code)}" placeholder="GIAM10, FREESHIP, HETHAN"></label>
        <p class="alert" id="couponAlert" ${coupon.ok ? "hidden" : ""}>${coupon.ok ? "" : esc(coupon.message)}</p>
        <fieldset style="border:0;padding:0">
          <legend><b>Thanh toán</b></legend>
          ${mode === "install" ? `<label class="choice"><input type="radio" name="payment" value="cash" checked> Tiền mặt tại showroom</label>` : ""}
          <label class="choice"><input type="radio" name="payment" value="transfer" ${mode === "ship" ? "checked" : ""}> Chuyển khoản</label>
          <label class="choice"><input type="radio" name="payment" value="gateway"> Cổng thanh toán</label>
        </fieldset>
        <label class="checks"><input type="checkbox" name="agree" required> Tôi đồng ý điều kiện mua hàng</label>
        <button class="btn btn-red" type="submit">Đặt hàng</button>
      </form>
      <aside class="card money" style="padding:16px">
        ${lines.map((line) => `<div><span>${esc(line.name)} × ${line.qty}</span><b>${A360.vnd(line.lineTotal)}</b></div>`).join("")}
        <div><span>Giảm giá</span><b id="discountVal">${coupon.ok ? "−" + A360.vnd(coupon.amount) : "0đ"}</b></div>
        <div><span>${mode === "install" ? "Phí lắp" : "Phí giao"}</span><b id="feeVal">${fee === null ? "Chọn khu vực" : A360.vnd(fee)}</b></div>
        <div class="total"><span>Tổng</span><span id="totalVal">${A360.vnd(Math.max(total, 0))}</span></div>
      </aside>
    </div>`, "catalog");
}

function confirmPage() {
  const order = A360.orders.list().find((item) => item.code === params.get("ma"));
  if (!order) return chrome(`<h1>Không thấy đơn</h1>`, "catalog");
  const bank = order.payment === "transfer" && !order.paid;
  const gate = params.get("cong") === "1" && order.payment === "gateway" && !order.paid;
  return chrome(`
    <div class="steps"><span>Giỏ</span><span>Thanh toán</span><span class="now">Xác nhận</span></div>
    <div class="card" style="padding:18px">
      <h1>Đơn ${esc(order.code)}</h1>
      <p class="tag ${order.paid || order.payment === "cash" ? "ok" : "warn"}">${esc(order.status)}${order.paid ? " · Đã thanh toán" : ""}</p>
      <p>${esc(order.name)} · ${esc(order.phone)}</p>
      ${order.mode === "ship" ? `<p>Giao tới ${esc(order.address)}</p>` : `<p>Lắp tại ${esc(shopName(order.showroomId))} · ${esc(order.date || "")} ${esc(order.time || "")}</p>`}
      <ul>${order.lines.map((line) => `<li>${esc(line.name)} × ${line.qty} — ${A360.vnd(line.unit * line.qty)}</li>`).join("")}</ul>
      <p class="total"><b>Tổng ${A360.vnd(order.total)}</b></p>
      ${bank ? `<div class="okbox"><b>Chuyển khoản</b><br>Ngân hàng Demo · 0123456789 · 360 AUTO DETAILING<br>Số tiền ${A360.vnd(order.total)}<br>Nội dung bắt buộc: ${esc(order.code)}<br>Đơn giữ hàng 24 giờ.</div>` : ""}
      ${gate ? `<div class="panel" style="margin-top:12px"><h2>Cổng thanh toán</h2><p>Số tiền ${A360.vnd(order.total)}. Bấm một lần. Bấm lại không tạo thêm phiếu thu.</p><button class="btn btn-blue" type="button" data-act="gate" data-result="ok" data-code="${esc(order.code)}">Thanh toán thành công</button> <button class="btn btn-line" type="button" data-act="gate" data-result="fail" data-code="${esc(order.code)}">Thất bại</button></div>` : ""}
      <p><a href="tra-cuu-don.html">Tra cứu đơn</a></p>
    </div>`, "catalog");
}

function servicesPage() {
  const current = A360.services.find((item) => item.id === params.get("dv")) || A360.services[0];
  const shops = A360.showrooms.filter((shop) => current.shops.includes(shop.id));
  return chrome(`
    <p class="crumb"><a href="index.html">Trang chủ</a> / Dịch vụ</p>
    <div class="grid-2">
      <div>
        <div class="grid-2" style="grid-template-columns:1fr 1fr">
          ${A360.services.map((item) => `<a class="card" style="padding:10px" href="dich-vu.html?dv=${item.id}"><img src="${item.image}" alt="" style="height:90px;width:100%;object-fit:cover;border-radius:10px"><strong>${esc(item.name)}</strong></a>`).join("")}
        </div>
      </div>
      <article class="card" style="padding:16px">
        <img src="${current.image}" alt="" style="height:180px;width:100%;object-fit:cover;border-radius:12px">
        <h1>${esc(current.name)}</h1>
        <p>${esc(current.summary)}</p>
        <p>Thời lượng khoảng ${current.minutes} phút. Giá ${A360.vnd(current.priceFrom)} – ${A360.vnd(current.priceTo)}.</p>
        <ol>${current.steps.map((step) => `<li>${esc(step)}</li>`).join("")}</ol>
        <h2>Đặt lịch</h2>
        <form id="bookForm">
          <input type="hidden" name="serviceId" value="${current.id}">
          <label class="field">Họ tên<input name="name" required></label>
          <label class="field">Số điện thoại<input name="phone" required pattern="0[0-9]{9}"></label>
          <label class="field">Showroom<select name="showroomId">${shops.map((shop) => `<option value="${shop.id}">${esc(shop.name)}</option>`).join("")}</select></label>
          <label class="field">Ngày<input type="date" name="date" required></label>
          <label class="field">Giờ<select name="time">${A360.slots.map((time) => `<option>${time}</option>`).join("")}</select></label>
          <label class="field">Dòng xe<input name="car" required></label>
          <button class="btn btn-red" type="submit">Gửi lịch hẹn</button>
        </form>
        <p class="note">Khung 10:00 tại Quận 7 của phủ ceramic đang hết chỗ, dùng để thử đường lỗi.</p>
      </article>
    </div>`, "services");
}

function searchPage() {
  const q = (params.get("q") || "").trim().toLowerCase();
  const fold = (text) => text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const query = fold(q);
  const foundP = A360.products.filter((item) => fold(item.name + item.variants.map((v) => v.sku).join(" ")).includes(query));
  const foundS = A360.services.filter((item) => fold(item.name).includes(query));
  return chrome(`
    <h1>Tìm kiếm</h1>
    <form id="searchForm"><label class="field">Từ khóa<input name="q" value="${esc(q)}" placeholder="man hinh, camera, ceramic"></label><button class="btn btn-blue" type="submit">Tìm</button></form>
    ${q && !foundP.length && !foundS.length ? `<p>Không thấy kết quả cho “${esc(q)}”.</p><a href="phu-kien.html">Xem danh mục</a>` : ""}
    <h2>Sản phẩm</h2><div class="grid-3">${foundP.map(card).join("")}</div>
    <h2>Dịch vụ</h2><ul>${foundS.map((item) => `<li><a href="dich-vu.html?dv=${item.id}">${esc(item.name)}</a></li>`).join("")}</ul>
  `, "catalog");
}

function accountPage() {
  const user = A360.session.get();
  if (!user) {
    return chrome(`<h1>Tài khoản</h1>
      <form class="card" id="loginForm" style="padding:16px;max-width:420px">
        <label class="field">Số điện thoại<input name="phone" required pattern="0[0-9]{9}"></label>
        <label class="field">Mã xác nhận<input name="code" required placeholder="Mã mẫu 123456"></label>
        <button class="btn btn-blue" type="submit">Đăng nhập</button>
        <p class="note">Bản UX: mã luôn là 123456. Số 0901234567 có đơn đã hoàn thành.</p>
      </form>`, "home");
  }
  const mine = A360.orders.list().filter((order) => order.phone.replace(/\D/g, "") === user.phone.replace(/\D/g, ""));
  const visits = A360.bookings.list().filter((item) => item.phone.replace(/\D/g, "") === user.phone.replace(/\D/g, ""));
  return chrome(`<h1>Xin chào ${esc(user.name)}</h1><p>${esc(user.phone)} <button type="button" data-act="logout">Thoát</button></p>
    <h2>Đơn hàng</h2>
    ${mine.map((order) => `<p><a href="xac-nhan.html?ma=${order.code}">${esc(order.code)}</a> · ${esc(order.status)} · ${A360.vnd(order.total)}</p>`).join("") || "<p>Chưa có đơn.</p>"}
    <h2>Lịch hẹn</h2>
    ${visits.map((item) => `<p>${esc(item.code)} · ${esc(item.serviceName)} · ${esc(item.time)} · ${esc(item.status)}</p>`).join("") || "<p>Chưa có lịch.</p>"}`, "home");
}

function lookupPage() {
  const code = params.get("ma") || "";
  const phone = params.get("phone") || "";
  const order = code && phone ? A360.orders.find(code, phone) : null;
  return chrome(`<h1>Tra cứu đơn</h1>
    <form class="card" id="lookupForm" style="padding:16px;max-width:460px">
      <label class="field">Mã đơn<input name="ma" value="${esc(code)}" required></label>
      <label class="field">Số điện thoại đặt hàng<input name="phone" value="${esc(phone)}" required></label>
      <button class="btn btn-blue" type="submit">Xem</button>
    </form>
    ${code && phone && !order ? `<p class="alert">Không khớp mã đơn và số điện thoại.</p>` : ""}
    ${order ? `<div class="card" style="padding:16px;margin-top:12px"><b>${esc(order.status)}</b><p>${esc(order.code)} · ${A360.vnd(order.total)}</p><p>Không hiện địa chỉ đầy đủ trên trang tra cứu công khai.</p></div>` : ""}`, "home");
}

function showroomPage() {
  return chrome(`<h1>Hệ thống showroom</h1><div class="grid-3">${A360.showrooms.map((shop) => `<article class="card" style="padding:16px"><h2>${esc(shop.name)}${shop.primary ? " · Chính" : ""}</h2><p>${esc(shop.address)}</p><p>${esc(shop.hours)}</p><a href="tel:${shop.phone.replace(/\s/g, "")}">${esc(shop.phone)}</a></article>`).join("")}</div>`, "shops");
}

function adminPage() {
  const tab = params.get("tab") || "tong";
  const role = params.get("role") || "quan-tri";
  const shopFilter = role === "tu-van" ? "q7" : "";
  const list = A360.orders.list().filter((order) => !shopFilter || order.showroomId === shopFilter || (shopFilter === "q7" && order.mode === "ship"));
  const visible = role === "tu-van" ? list.filter((order) => order.showroomId === "q7" || order.mode === "ship") : A360.orders.list();
  const thread = A360.chat.thread();
  const nav = [
    ["tong", "Tổng quan"],
    ["don", "Đơn hàng"],
    ["lich", "Lịch hẹn"],
    ["chat", "Hộp thư"],
    ["cms", "Trang chủ CMS"]
  ];
  let body = "";
  if (tab === "tong") {
    body = `<div class="kpis">
      <div class="card kpi"><span>Đơn</span><b>${visible.length}</b></div>
      <div class="card kpi"><span>Chờ xử lý</span><b>${visible.filter((order) => order.status.startsWith("Chờ")).length}</b></div>
      <div class="card kpi"><span>Lịch mới</span><b>${A360.bookings.list().length}</b></div>
      <div class="card kpi"><span>Chat</span><b>${thread.messages.filter((msg) => msg.author === "khách").length}</b></div>
    </div><p>Doanh thu trên báo cáo chỉ tính đơn Hoàn thành. Vai trò tư vấn Quận 7 không thấy đơn lắp của showroom khác.</p>`;
  }
  if (tab === "don") {
    body = `<table><tr><th>Mã</th><th>Khách</th><th>Showroom</th><th>Trạng thái</th><th></th></tr>
      ${visible.map((order) => `<tr><td>${esc(order.code)}</td><td>${esc(order.name)}<br>${esc(order.phone)}</td><td>${esc(order.mode === "ship" ? "Giao hàng" : shopName(order.showroomId))}</td><td>${esc(order.status)}</td><td>${order.status !== "Hoàn thành" && order.status !== "Đã hủy" ? `<button type="button" data-act="complete" data-code="${esc(order.code)}">Hoàn thành</button>` : ""}</td></tr>`).join("")}
    </table>`;
  }
  if (tab === "lich") {
    const items = A360.bookings.list();
    body = items.length ? `<table><tr><th>Mã</th><th>Dịch vụ</th><th>Showroom</th><th>Giờ</th><th>Trạng thái</th></tr>${items.map((item) => `<tr><td>${esc(item.code)}</td><td>${esc(item.serviceName)}</td><td>${esc(shopName(item.showroomId))}</td><td>${esc(item.time)}</td><td>${esc(item.status)}</td></tr>`).join("")}</table>` : "<p>Chưa có lịch từ website.</p>";
  }
  if (tab === "chat") {
    body = `<div class="card" style="padding:12px"><p>Trạng thái: ${esc(thread.status)} · ${esc(thread.phone || "Chưa có số")}</p>
      ${thread.messages.map((msg) => `<div class="msg ${esc(msg.author)}">${esc(msg.text)}</div>`).join("") || "<p>Chưa có tin.</p>"}
      <form id="staffReply"><input name="text" placeholder="Trả lời khách" required><button class="btn btn-blue" type="submit">Gửi</button></form>
      <button type="button" class="btn btn-line" data-act="draft-booking">Tạo lịch từ hội thoại</button></div>`;
  }
  if (tab === "cms") {
    body = `<div class="card" style="padding:16px"><h2>Khối trang chủ</h2><p>Bản nháp không hiện với khách. Xuất bản ở đây chỉ là trạng thái UX lưu trên trình duyệt.</p>
      ${["Banner", "Cam kết", "Dịch vụ", "Danh mục", "Khuyến mãi", "Giới thiệu", "Liên hệ"].map((name, index) => `<label class="checks"><input type="checkbox" checked data-act="block"> ${name}</label>`).join("")}
      <p class="note">Banner “Flash đã kết thúc” ở trạng thái hết hạn nên không xuất hiện trên trang chủ.</p></div>`;
  }
  return `<div class="page"><div class="wrap admin">
    <aside class="panel"><h2>Vận hành</h2>
      <label class="field">Vai trò<select data-act="role"><option value="quan-tri" ${role === "quan-tri" ? "selected" : ""}>Quản trị</option><option value="tu-van" ${role === "tu-van" ? "selected" : ""}>Tư vấn Quận 7</option></select></label>
      <nav>${nav.map(([id, label]) => `<button type="button" class="${tab === id ? "on" : ""}" data-act="tab-admin" data-tab="${id}">${label}</button>`).join("")}</nav>
      <p><a href="index.html">Về website</a></p>
    </aside>
    <section><h1>${esc(nav.find((item) => item[0] === tab)?.[1] || "")}</h1>${body}</section>
  </div></div><div class="toast" id="toast" role="status"></div>`;
}

const views = {
  catalog: catalogPage,
  product: productPage,
  cart: cartPage,
  checkout: checkoutPage,
  confirm: confirmPage,
  services: servicesPage,
  search: searchPage,
  account: accountPage,
  lookup: lookupPage,
  shops: showroomPage,
  admin: adminPage
};

function render() {
  const view = views[pageId] || catalogPage;
  if (pageId === "admin") document.getElementById("app").innerHTML = view();
  else paint(view());
}
render();

document.body.addEventListener("click", (event) => {
  const node = event.target.closest("[data-act]");
  if (!node) return;
  const act = node.dataset.act;
  if (act === "menu") document.getElementById("nav")?.classList.toggle("open");
  if (act === "open-chat") document.getElementById("chatBox").hidden = false;
  if (act === "close-chat") document.getElementById("chatBox").hidden = true;
  if (act === "variant") {
    const url = new URL(location.href);
    url.searchParams.set("v", node.dataset.v);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (act === "qty") {
    const el = document.getElementById("qty");
    el.textContent = String(Math.max(1, Math.min(20, Number(el.textContent) + Number(node.dataset.dir))));
  }
  if (act === "add") {
    const p = A360.product(node.dataset.slug);
    const variantId = params.get("v") || p.variants[0].id;
    const mode = document.querySelector("input[name=mode]:checked")?.value || "ship";
    const showroomId = document.querySelector("[data-act=shop]")?.value || "";
    const result = A360.cart.add({ slug: p.slug, variantId, qty: Number(document.getElementById("qty")?.textContent || 1), mode, showroomId });
    toast(result.message);
    if (result.ok) render();
  }
  if (act === "line-qty") {
    const lines = A360.cart.get();
    const line = lines.find((item) => item.key === node.dataset.key);
    if (line) A360.cart.setQty(line.key, line.qty + Number(node.dataset.dir));
    render();
  }
  if (act === "remove") {
    A360.cart.remove(node.dataset.key);
    render();
  }
  if (act === "cat") location.href = "phu-kien.html" + (node.value ? "?cat=" + node.value : "");
  if (act === "logout") { A360.session.logout(); render(); }
  if (act === "tab") {
    document.querySelectorAll(".tabs button").forEach((button) => button.classList.toggle("on", button === node));
    ["mo-ta", "thong-so", "danh-gia"].forEach((id) => { document.getElementById("tab-" + id).hidden = id !== node.dataset.tab; });
  }
  if (act === "gate") {
    const order = A360.orders.list().find((item) => item.code === node.dataset.code);
    if (node.dataset.result === "ok") {
      if (!order.paid) A360.orders.update(order.code, { paid: true, status: "Chờ xác nhận", gatewayRef: "PAY-" + order.code });
      location.href = "xac-nhan.html?ma=" + order.code;
    } else {
      toast("Thanh toán thất bại. Đơn vẫn chờ thanh toán.");
    }
  }
  if (act === "complete") {
    A360.orders.update(node.dataset.code, { status: "Hoàn thành", paid: true });
    render();
  }
  if (act === "tab-admin") {
    const url = new URL(location.href);
    url.searchParams.set("tab", node.dataset.tab);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (act === "draft-booking") {
    const thread = A360.chat.thread();
    if (!thread.phone) { toast("Hội thoại chưa có số điện thoại."); return; }
    location.href = "dich-vu.html?dv=ceramic";
  }
});

function refreshPay() {
  const form = document.getElementById("payForm");
  if (!form) return;
  const subtotal = Number(form.dataset.subtotal);
  const mode = form.dataset.mode;
  const district = form.district?.value || "";
  const coupon = A360.couponResult(form.coupon?.value || "", subtotal, mode);
  const alert = document.getElementById("couponAlert");
  if (alert) {
    alert.hidden = coupon.ok;
    alert.textContent = coupon.ok ? "" : coupon.message;
  }
  const fee = mode === "install" ? 150000 : A360.shipFee(subtotal, district, coupon.ok && coupon.freeShip);
  const discount = document.getElementById("discountVal");
  const feeNode = document.getElementById("feeVal");
  const total = document.getElementById("totalVal");
  if (discount) discount.textContent = coupon.ok && coupon.amount ? "−" + A360.vnd(coupon.amount) : "0đ";
  if (feeNode) feeNode.textContent = fee === null ? "Chọn khu vực" : A360.vnd(fee);
  if (total) total.textContent = A360.vnd(Math.max(subtotal - (coupon.ok ? coupon.amount : 0) + (fee || 0), 0));
}

document.body.addEventListener("input", (event) => {
  if (event.target?.name === "coupon") refreshPay();
});

document.body.addEventListener("change", (event) => {
  const node = event.target.closest("[data-act]");
  if (!node) return;
  if (node.dataset.act === "vehicle") {
    A360.vehicle.set(node.value);
    render();
  }
  if (node.dataset.act === "instock") {
    const url = new URL(location.href);
    if (node.checked) url.searchParams.set("stock", "1");
    else url.searchParams.delete("stock");
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  const url = new URL(location.href);
  if (node.dataset.act === "sort") {
    url.searchParams.set("sort", node.value);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (node.dataset.act === "mode") {
    url.searchParams.set("mode", node.value);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (node.dataset.act === "shop") {
    url.searchParams.set("shop", node.value);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (node.dataset.act === "role") {
    url.searchParams.set("role", node.value);
    location.href = url.pathname + "?" + url.searchParams.toString();
  }
  if (node.dataset.act === "district") refreshPay();
});

document.body.addEventListener("submit", (event) => {
  const form = event.target;
  if (form.id === "payForm") {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    const mode = params.get("mode") === "install" ? "install" : "ship";
    const lines = A360.cart.get().map(A360.enrich).filter((line) => line.mode === mode && !line.invalid);
    const subtotal = lines.reduce((sum, line) => sum + line.lineTotal, 0);
    const coupon = A360.couponResult(data.coupon, subtotal, mode);
    if (data.coupon && !coupon.ok) { toast(coupon.message); return; }
    const fee = mode === "install" ? 150000 : A360.shipFee(subtotal, data.district, coupon.freeShip);
    const order = A360.orders.create({
      name: data.name, phone: data.phone, email: data.email || "", mode,
      payment: data.payment, paid: false,
      status: data.payment === "cash" ? "Chờ xác nhận" : "Chờ thanh toán",
      showroomId: lines[0].showroomId, address: data.address ? data.address + ", " + data.district : "",
      date: data.date || "", time: data.time || "",
      subtotal, discount: coupon.ok ? coupon.amount : 0, fee: fee || 0,
      total: subtotal - (coupon.ok ? coupon.amount : 0) + (fee || 0),
      lines: lines.map((line) => ({ slug: line.slug, name: line.name, variantName: line.variantName, qty: line.qty, unit: line.unit }))
    });
    A360.cart.removeMany(lines.map((line) => line.key));
    const gate = data.payment === "gateway" ? "&cong=1" : "";
    location.href = "xac-nhan.html?ma=" + order.code + gate;
  }
  if (form.id === "bookForm") {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    if (A360.bookings.taken(data.showroomId, data.serviceId, data.time)) {
      toast("Khung giờ vừa hết chỗ. Chọn giờ khác.");
      return;
    }
    const service = A360.services.find((item) => item.id === data.serviceId);
    const booking = A360.bookings.create({ ...data, serviceName: service.name, status: "Chờ xác nhận" });
    form.reset();
    toast("Đã nhận lịch " + booking.code);
  }
  if (form.id === "searchForm") {
    event.preventDefault();
    const q = new FormData(form).get("q");
    location.href = "tim-kiem.html?q=" + encodeURIComponent(q);
  }
  if (form.id === "loginForm") {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (data.code !== "123456") { toast("Mã không đúng."); return; }
    A360.session.login(data.phone, data.phone === "0901234567" ? "Nguyễn An" : "Khách");
    render();
  }
  if (form.id === "lookupForm") {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    location.href = "tra-cuu-don.html?ma=" + encodeURIComponent(data.ma) + "&phone=" + encodeURIComponent(data.phone);
  }
  if (form.id === "chatForm") {
    event.preventDefault();
    const text = new FormData(form).get("text");
    A360.chat.push("khách", text);
    form.reset();
    const thread = A360.chat.thread();
    if (thread.messages.filter((msg) => msg.author === "khách").length === 1) {
      A360.chat.push("he-thong", "Bạn có thể để lại số điện thoại để showroom gọi lại.");
    }
    drawChat();
  }
  if (form.id === "staffReply") {
    event.preventDefault();
    A360.chat.push("tu-van", new FormData(form).get("text"));
    const thread = A360.chat.thread();
    thread.status = "Đang xử lý";
    A360.chat.save(thread);
    render();
  }
  if (form.id === "reviewForm") {
    event.preventDefault();
    toast("Đã gửi. Đánh giá ở trạng thái chờ duyệt, chưa tính vào điểm trung bình.");
    form.reset();
  }
});
