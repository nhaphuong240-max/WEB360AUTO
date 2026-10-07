# Đặc tả yêu cầu phần mềm

**Sản phẩm:** Website 360 Auto Detailing  
**Phiên bản tài liệu:** 2.0  
**Đối tượng đọc:** chủ đầu tư, vận hành showroom, đội phát triển, đội kiểm thử  
**Trạng thái:** bản để thống nhất phạm vi trước khi thiết kế chi tiết và lập dự toán

Tài liệu này thay bản mô tả tổng quan trước đó. Mỗi yêu cầu có mã để truy vết khi nghiệm thu. Giao diện trang chủ bám mockup `index.html`. Phần giỏ hàng, thanh toán, CMS và chat là phạm vi sản phẩm, không chỉ là giao diện minh họa.

---

## 1. Mục đích

360 Auto Detailing bán phụ kiện xe hơi và nhận lịch chăm sóc xe tại nhiều showroom. Website phải làm được bốn việc trên cùng một nền:

1. Trình bày thương hiệu và chuyển khách từ trang chủ sang mua hàng hoặc đặt lịch.
2. Bán phụ kiện có kiểm tra độ vừa xe, tồn kho theo showroom, giao hàng hoặc lắp tại chỗ.
3. Để nhân viên showroom tự sửa nội dung, giá, khuyến mãi và lịch mà không nhờ kỹ thuật.
4. Gom hỏi đáp từ web, Zalo và Messenger vào một hộp thư, gắn được với đơn và lịch hẹn.

Chỉ số vận hành dùng để nghiệm thu sau khi chạy thật ba tháng:

| Chỉ số | Mức cần đạt |
| --- | --- |
| Khách tự hoàn tất đặt hàng phụ kiện không cần gọi tổng đài | Từ 70% số đơn online |
| Lịch hẹn tạo từ web có đủ showroom, dịch vụ và khung giờ | 100% lịch mới |
| Thời gian nhân viên sửa banner trang chủ và thấy trên web | Dưới 5 phút sau khi xuất bản |
| Tin nhắn trong giờ làm việc được trả lời lần đầu | Dưới 5 phút với 90% hội thoại |
| Đơn đã thanh toán bị trừ kho hai lần | 0 |

## 2. Thuật ngữ

| Thuật ngữ | Nghĩa trong tài liệu |
| --- | --- |
| Phụ kiện | Hàng hóa có mã, giá, tồn kho, có thể giao hoặc lắp |
| Dịch vụ | Hạng mục detailing tính theo công và vật tư, đặt bằng lịch hẹn |
| Biến thể | Một cách bán của phụ kiện: màu, kích thước hoặc phiên bản, có SKU và tồn riêng |
| Độ vừa xe | Quy tắc phụ kiện lắp được lên hãng, dòng, đời hoặc phiên bản xe nào |
| Showroom | Điểm bán và làm dịch vụ, có địa chỉ, giờ mở cửa, tồn kho và lịch thợ |
| Nhận tại chỗ | Khách mua phụ kiện và lắp hoặc nhận tại một showroom |
| Giữ hàng mềm | Tạm giữ tồn trong lúc khách đang thanh toán, tự nhả nếu quá hạn |
| Chiến dịch | Chương trình giảm giá có thời hạn, áp lên một tập sản phẩm |
| CMS | Khu soạn và xuất bản nội dung trang |
| Hội thoại | Một chuỗi tin với một khách trên một kênh |
| Giá niêm yết | Giá khách thấy, đã gồm VAT |
| Đơn nháp | Đơn nhân viên tạo từ chat hoặc tại quầy, chưa chốt thanh toán |

## 3. Phạm vi

### 3.1 Nằm trong phạm vi

- Website tiếng Việt, dùng được trên điện thoại và máy tính.
- Trang chủ đúng cấu trúc mockup, nội dung lấy từ CMS.
- Danh mục phụ kiện, trang sản phẩm, tìm kiếm, lọc theo xe.
- Giỏ hàng, mã giảm giá, thanh toán, theo dõi đơn, yêu cầu đổi trả.
- Đặt lịch dịch vụ theo sức chứa showroom.
- Tài khoản khách, sổ địa chỉ, danh sách xe.
- CMS trang, trang chủ, dịch vụ, bài viết, showroom, media, SEO.
- Chat trên web, nút Zalo, nút Messenger, hộp thư nhân viên.
- Tồn kho nhiều showroom, phân quyền nhân viên theo showroom.
- Hóa đơn điện tử ở mức xuất dữ liệu cho phần mềm hóa đơn. Website không phát hành hóa đơn cơ quan thuế.

### 3.2 Ngoài phạm vi

- Ứng dụng cài trên điện thoại.
- Đăng bán lên sàn thương mại điện tử.
- Phần mềm kế toán, chấm công, tính lương thợ.
- Chẩn đoán lỗi xe từ xa, báo giá sơn tính từng tấm theo phần mềm thẩm định.
- Sàn trung gian để garage bên ngoài nhận việc.

### 3.3 Giả định

- Giá bán thống nhất toàn quốc. Khác nhau giữa showroom chỉ ở tồn kho và lịch lắp, không ở giá.
- Một phụ kiện có thể vừa bán giao hàng vừa bán lắp tại chỗ, hoặc chỉ một trong hai hình thức. Cấu hình trên sản phẩm.
- Biển số xe là tùy chọn. Khách không bắt buộc cung cấp để mua hàng.
- Zalo Official Account và Facebook Page do chủ đầu tư sở hữu và cấp quyền kết nối.

## 4. Vai trò

### 4.1 Khách

- **Khách vãng lai** xem trang, tìm hàng, thêm giỏ, đặt lịch, chat. Giỏ lưu trên trình duyệt 30 ngày.
- **Khách thành viên** làm thêm các việc của vãng lai, cộng hồ sơ, địa chỉ, xe, lịch sử đơn, lịch hẹn và đánh giá.

Đăng nhập không bắt buộc để mua hoặc đặt lịch.

### 4.2 Nhân viên

| Vai trò | Thấy dữ liệu | Được làm |
| --- | --- | --- |
| Biên tập | Toàn bộ nội dung | Sửa nháp, xem trước. Xuất bản nếu được cấp thêm quyền xuất bản |
| Tư vấn | Đơn, lịch, chat, khách của showroom được gán | Xác nhận đơn và lịch, trả lời chat, tạo đơn nháp. Không sửa giá gốc, không sửa tồn |
| Thủ kho | Tồn và phiếu kho của showroom được gán | Nhập, xuất, điều chuyển, xác nhận đã giao cho đơn vị vận chuyển |
| Quản lý showroom | Mọi dữ liệu vận hành của showroom mình | Việc của tư vấn và thủ kho, cộng xem báo cáo showroom, không sửa cấu hình thanh toán |
| Quản trị hệ thống | Toàn hệ thống | Mọi quyền, gồm tài khoản, cổng thanh toán, kênh chat, xóa và khôi phục |

Một người có thể có nhiều vai trò. Dữ liệu showroom luôn bị cắt theo showroom được gán, trừ quản trị hệ thống. Mọi thao tác ghi dữ liệu trong khu quản trị đều lưu nhật ký: ai, lúc nào, đối tượng, giá trị trước và sau.

Khách không có đường vào khu quản trị. Nhân viên không dùng chung tài khoản.

## 5. Bản đồ trang

Đường dẫn công khai dùng tiếng Việt không dấu.

| Trang | Đường dẫn |
| --- | --- |
| Trang chủ | `/` |
| Giới thiệu | `/gioi-thieu` |
| Dịch vụ | `/dich-vu` và `/dich-vu/{slug}` |
| Danh mục | `/phu-kien` và `/phu-kien/{slug}` |
| Sản phẩm | `/san-pham/{slug}` |
| Khuyến mãi | `/khuyen-mai` |
| Tin tức | `/tin-tuc` và `/tin-tuc/{slug}` |
| Showroom | `/showroom` và `/showroom/{slug}` |
| Liên hệ | `/lien-he` |
| Tìm kiếm | `/tim-kiem?q=` |
| Giỏ hàng | `/gio-hang` |
| Thanh toán | `/thanh-toan` |
| Cảm ơn | `/don-hang/{ma}/xac-nhan` |
| Tra cứu đơn | `/tra-cuu-don` |
| Tài khoản | `/tai-khoan/...` |
| Chính sách | `/chinh-sach/{slug}` |

Khu quản trị nằm tại `/quan-tri`, tách phiên đăng nhập với website.

Trang chủ là một trang dài. Thứ tự khối mặc định, quản trị được sắp lại:

1. Header
2. Banner
3. Bốn cam kết
4. Dịch vụ
5. Danh mục phụ kiện
6. Khuyến mãi
7. Giới thiệu
8. Liên hệ
9. Chân trang
10. Cụm nút nổi

## 6. Quy tắc dùng chung

**BR-GIA-01.** Mọi giá khách thấy là giá đã gồm VAT. Trong quản trị, mỗi sản phẩm lưu giá trước VAT và thuế suất. Website tự tính giá sau VAT để hiển thị và để đối soát.

**BR-GIA-02.** Thứ tự tính tiền một đơn:

1. Đơn giá biến thể.
2. Nếu sản phẩm đang trong chiến dịch còn hiệu lực, lấy giá chiến dịch thay đơn giá.
3. Nhân số lượng.
4. Trừ giảm giá theo dòng nếu có.
5. Trừ mã giảm giá cấp đơn.
6. Cộng phí giao hàng hoặc phí lắp, tùy hình thức nhận.
7. Ra tổng thanh toán.

Không áp dụng hai chiến dịch lên cùng một dòng. Nếu sản phẩm nằm trong nhiều chiến dịch còn hạn, dùng chiến dịch cho giá thấp hơn.

**BR-KHO-01.** Thêm vào giỏ không trừ kho.

**BR-KHO-02.** Khi khách sang bước thanh toán, hệ thống giữ mềm từng biến thể trong 15 phút. Hết 15 phút mà chưa tạo đơn thì nhả giữ. Trong lúc giữ, khách khác không mua vượt quá tồn khả dụng. Tồn khả dụng = tồn thực trừ số đang giữ mềm trừ số đã gắn với đơn chưa xuất kho.

**BR-KHO-03.** Đơn tạo thành công chuyển số giữ mềm thành giữ cứng theo đơn. Hủy đơn trước khi xuất kho thì nhả giữ cứng. Xuất kho hoặc hoàn tất lắp thì trừ tồn thực.

**BR-KHO-04.** Giao hàng trừ tồn kho giao hàng trung tâm. Lắp hoặc nhận tại showroom trừ tồn đúng showroom khách chọn. Không được lấy tồn showroom này để hứa lắp tại showroom khác.

**BR-XE-01.** Cây xe gồm hãng, dòng, đời, phiên bản. Phụ kiện khai báo một trong ba mức: lắp được mọi xe, lắp theo danh sách phiên bản, hoặc cần tư vấn. Mức cần tư vấn vẫn cho đặt, nhưng trang sản phẩm và đơn phải hiện câu “Cần xác nhận độ vừa trước khi lắp”.

**BR-XE-02.** Khách đã chọn xe trên website thì bộ lọc và huy hiệu “Vừa xe của bạn” dùng đúng xe đó cho đến khi khách đổi xe hoặc xóa lựa chọn.

**BR-MA-01.** Một đơn dùng tối đa một mã giảm giá. Mã kiểm tra đồng thời: còn hạn, còn lượt, đơn đạt giá trị tối thiểu, sản phẩm trong đơn thuộc phạm vi mã, khách thuộc nhóm được dùng nếu mã giới hạn nhóm. Sai thì báo một lý do, theo thứ tự vừa nêu, không báo chung “mã không hợp lệ”.

**BR-TT-01.** Tổng tiền gửi sang cổng thanh toán phải bằng tổng đơn tại thời điểm tạo giao dịch. Lệch số tiền khi cổng trả về thì không đánh dấu đã thanh toán, đơn vào hàng đợi đối soát và báo quản trị.

**BR-TT-02.** Thông báo thanh toán từ cổng xử lý theo mã giao dịch. Nhận trùng một mã đã thành công thì bỏ qua, không tạo thêm phiếu thu.

## 7. Trang chủ

Nội dung từng khối đọc từ CMS. Bố cục, kiểu chữ và màu theo mockup. Tắt một khối thì khối đó biến mất và các khối còn lại khít lên, không để khoảng trống.

### FR-HOME-01 Header

Header dính khi cuộn. Gồm logo, menu, tìm kiếm, nút Đặt lịch, icon giỏ.

- Logo về `/`.
- Menu tối đa hai cấp. Cấp hai mở khi rê trên máy tính và khi chạm trên điện thoại.
- Số trên giỏ là tổng số lượng món, không phải số dòng. Giỏ trống thì không hiện số.
- Bấm icon giỏ mở ngăn giỏ. Ngăn có tối đa năm dòng gần nhất, tổng tạm tính, nút xem giỏ và nút thanh toán. Không sửa số lượng trong ngăn. Sửa số lượng chỉ ở trang giỏ.
- Dưới 1024px, menu vào nút hamburger. Nút tìm kiếm, đặt lịch và giỏ vẫn hiện. Menu mở phủ hết chiều ngang header, đóng khi chọn một mục hoặc bấm ra ngoài.

**Nghiệm thu:** sửa nhãn menu trong CMS, xuất bản, tải lại trang chủ thấy nhãn mới. Thêm một món, số giỏ tăng đúng số lượng đã chọn.

### FR-HOME-02 Banner

Một banner có ảnh nền hoặc video không tiếng, nhãn nhỏ, tiêu đề, mô tả, tối đa hai nút. Mỗi nút có chữ và đường dẫn nội bộ hoặc ngoài.

- Nhiều banner xếp thành slide, chuyển mỗi 6 giây, có chấm chọn, dừng khi rê chuột hoặc khi người dùng chạm.
- Banner có ngày giờ bắt đầu và kết thúc theo múi giờ Việt Nam. Ngoài khoảng đó không xuất hiện.
- Không có banner nào đang hiệu lực thì ẩn cả khối, không hiện ảnh vỡ.
- Video không tự phát tiếng. Trên điện thoại, nếu video lỗi, hiện ảnh dự phòng của chính banner đó.

**Nghiệm thu:** tạo hai banner, một đã hết hạn. Trang chủ chỉ chạy banner còn hạn.

### FR-HOME-03 Khối cam kết

Đúng bốn vị trí dưới banner như mockup: bảo hành, giao hàng, showroom, hỗ trợ. Mỗi thẻ có icon chọn từ thư viện, tiêu đề tối đa 40 ký tự, mô tả tối đa 80 ký tự. Sắp xếp được. Trên điện thoại xếp một cột và không bị nút nổi che mất chữ. Nút nổi nằm phía trên nội dung nhưng chừa mép phải cho thẻ, hoặc thu nhỏ và không đè chữ.

### FR-HOME-04 Dịch vụ nổi bật

Tiêu đề và dòng phụ sửa được. Danh sách dịch vụ do CMS chọn và sắp xếp. Mỗi thẻ có ảnh, tên, mô tả ngắn, nút Xem chi tiết tới `/dich-vu/{slug}`.

Trang dịch vụ gồm nội dung dài, các bước thực hiện, thời lượng, khoảng giá, ảnh, câu hỏi thường gặp, showroom có làm dịch vụ này, và nút Đặt lịch. Nút đó mở form với dịch vụ đã chọn, khách không phải chọn lại.

Dịch vụ ẩn trong CMS biến khỏi trang chủ và khỏi danh sách, nhưng đường dẫn cũ trả về trang 404 có liên kết về danh sách dịch vụ.

### FR-HOME-05 Danh mục phụ kiện

Mỗi danh mục có ảnh, tên, nhãn tùy chọn. Nhãn chỉ nhận các giá trị Hot, Mới, hoặc một phần trăm giảm. Phần trăm không gõ tay: nếu bật “lấy mức giảm cao nhất trong danh mục” thì hệ thống tính từ chiến dịch đang chạy của sản phẩm thuộc danh mục. Bấm thẻ mở `/phu-kien/{slug}`.

### FR-HOME-06 Khuyến mãi trên trang chủ

Khối lấy tối đa một sản phẩm đánh dấu nổi bật và tối đa ba sản phẩm tiếp theo trong các chiến dịch đang chạy, còn tồn khả dụng lớn hơn không, đang ở trạng thái đang bán.

Mỗi thẻ hiện ảnh, phần trăm giảm đã tính, tên, giá bán, giá gốc gạch ngang, nút thêm giỏ. Hết hàng thì thay nút bằng chữ Hết hàng và không gọi được thao tác thêm giỏ.

Thêm giỏ từ đây dùng biến thể mặc định. Nếu sản phẩm có nhiều biến thể bắt buộc chọn, nút không thêm ngay mà đưa khách tới trang sản phẩm và tô nhóm biến thể chưa chọn.

### FR-HOME-07 Giới thiệu

Khối hai cột như mockup: chữ trên nền xanh, ảnh bên phải. Có tiêu đề, đoạn mô tả, danh sách tối đa sáu ý, đúng ba chỉ số. Mỗi chỉ số có số và đơn vị chữ. Ảnh có chú thích. Trên điện thoại, chữ nằm trên ảnh.

### FR-HOME-08 Liên hệ trên trang chủ

Hiện showroom được đánh dấu là showroom chính: số điện thoại bấm gọi, email, địa chỉ, giờ mở cửa theo đúng ngày trong tuần, ảnh, bản đồ đúng tọa độ, nút Đặt lịch hẹn.

Giờ mở cửa khai báo từng thứ. Ngày đóng cửa thì ghi “Đóng cửa”, không hiện giờ của ngày thường.

### FR-HOME-09 Chân trang và nút nổi

Chân trang có cột giới thiệu, cột liên kết, icon mạng xã hội, dòng bản quyền, hotline. Liên kết hỏng trong menu không được xuất bản: CMS báo liên kết chưa chọn đích.

Nút nổi gồm Messenger, Zalo, gọi, và lên đầu trang. Nút lên đầu trang chỉ hiện khi đã cuộn quá 500px. Cả cụm không che nút thanh toán ở cuối màn hình điện thoại: khi thanh điều hướng dưới cùng của trình duyệt hiện, cụm nút nằm phía trên vùng đó.

## 8. Tìm kiếm

### FR-SEARCH-01 Gợi ý

Sau khi khách ngừng gõ 300 mili giây và chuỗi dài từ hai ký tự, hiện tối đa tám gợi ý: sản phẩm, dịch vụ, bài viết. Mỗi gợi ý có loại và tên. Phím mũi tên chọn, Enter mở đúng trang. Esc đóng ô.

### FR-SEARCH-02 Trang kết quả

`/tim-kiem` có tab Tất cả, Sản phẩm, Dịch vụ, Bài viết. Tab Tất cả hiện mỗi loại tối đa bốn mục và đường xem hết. Không có kết quả thì nêu rõ từ đã tìm, gợi ý bốn danh mục bán chạy và nút mở chat.

Tìm không phân biệt hoa thường và dấu. “man hinh” ra “màn hình”. Tìm theo tên và SKU. Không tìm trong mô tả dài ở bước gợi ý. Trang kết quả có tìm trong mô tả.

## 9. Danh mục và sản phẩm

### FR-CAT-01 Trang danh mục

Có breadcrumb, bộ lọc, cách sắp xếp, lưới sản phẩm.

Bộ lọc:

- Danh mục con nếu có
- Hãng xe, dòng xe, đời xe
- Thương hiệu phụ kiện
- Khoảng giá
- Còn hàng
- Showroom còn hàng để lắp

Các ô trong một nhóm là hoặc. Các nhóm khác nhau là và. Đổi lọc thì địa chỉ trên trình duyệt đổi theo, sao chép liên kết cho người khác thấy cùng kết quả.

Sắp xếp: mới nhất, bán chạy trong 30 ngày, giá tăng, giá giảm, giảm sâu nhất. Mặc định là bán chạy, nếu chưa đủ dữ liệu bán thì mới nhất.

Mỗi trang 24 sản phẩm. Có phân trang, không tải vô hạn, để khách và bộ máy tìm kiếm tới được trang sau.

### FR-PDP-01 Trang sản phẩm

Hiển thị thư viện ảnh, tên, SKU biến thể đang chọn, thương hiệu, trạng thái kho, giá, giá gốc, phần trăm giảm, biến thể, số lượng, cách nhận hàng, mô tả, thông số, xe tương thích, bảo hành, sản phẩm mua cùng, đánh giá.

Quy tắc biến thể:

- Nhóm biến thể nào đánh dấu bắt buộc thì chưa chọn không thêm được giỏ. Thông báo chỉ đúng nhóm còn thiếu.
- Đổi biến thể đổi ảnh, SKU, giá và tồn.
- Biến thể hết hàng vẫn hiện nhưng không chọn được, có gạch chéo.

Cách nhận hàng:

- **Giao tận nơi** chỉ hiện nếu sản phẩm cho phép giao và kho giao hàng còn tồn khả dụng.
- **Lắp hoặc nhận tại showroom** chỉ hiện nếu sản phẩm cho phép và còn ít nhất một showroom có tồn. Danh sách showroom chỉ gồm showroom còn tồn của biến thể đó. Mỗi dòng showroom ghi số lượng còn và quận, huyện.

Nếu cả hai cách đều không khả dụng, nút thêm giỏ tắt và hiện “Tạm hết hàng”.

### FR-PDP-02 Đánh giá

Chỉ tài khoản đã có đơn hoàn thành chứa đúng biến thể, và chưa đánh giá biến thể đó trên đơn đó, mới gửi đánh giá. Đánh giá có số sao từ 1 đến 5, nội dung từ 20 đến 1000 ký tự, tối đa bốn ảnh. Đánh giá mới ở trạng thái chờ duyệt. Công khai sau khi biên tập hoặc quản lý showroom duyệt. Từ chối phải có lý do nội bộ.

Điểm trung bình trên thẻ sản phẩm chỉ tính đánh giá đã duyệt.

### FR-PDP-03 Sản phẩm ngừng bán

Trạng thái ngừng bán: trang vẫn mở nếu đã từng có đường dẫn, hiện “Ngừng kinh doanh”, không thêm giỏ, không xuất hiện trong danh mục và tìm kiếm. Sản phẩm nháp không có đường dẫn công khai.

## 10. Giỏ hàng và thanh toán

### FR-CART-01 Thêm, sửa, xóa

- Thêm một biến thể đã có trong giỏ thì cộng số lượng, không tạo dòng mới.
- Số lượng mỗi dòng từ 1 đến tồn khả dụng của cách nhận hàng đang chọn, tối đa 20.
- Đổi cách nhận hàng của một dòng có thể làm số lượng bị cắt xuống tồn của cách mới. Hệ thống báo rõ đã điều chỉnh số lượng.
- Xóa dòng có hộp xác nhận trên trang giỏ.
- Giỏ vãng lai sống 30 ngày kể từ lần sửa cuối. Giỏ thành viên sống đến khi khách xóa hoặc đặt hàng.
- Đăng nhập: gộp giỏ trình duyệt vào giỏ tài khoản. Trùng biến thể thì cộng. Vượt tồn thì giữ mức tồn khả dụng và báo dòng nào bị giảm.

### FR-CART-02 Trang giỏ

Mỗi dòng: ảnh, tên, biến thể, cách nhận hàng, showroom nếu có, đơn giá, số lượng, thành tiền, nút xóa. Cuối trang là bảng tiền theo BR-GIA-02, ô mã giảm giá và nút thanh toán.

Dòng không còn bán hoặc hết tồn được đánh dấu và loại khỏi tổng tiền. Nút thanh toán tắt cho đến khi khách xóa các dòng đó hoặc giảm số lượng về mức còn bán.

### FR-CART-03 Mã giảm giá

Ô nhập trên trang giỏ và trên trang thanh toán. Áp dụng thành công thì hiện số tiền được trừ và cho gỡ mã. Thất bại thì giữ nguyên giỏ và nêu lý do theo BR-MA-01.

Mã miễn phí giao hàng không có tác dụng với đơn lắp tại showroom. Khi đó báo “Mã chỉ áp dụng cho đơn giao hàng”.

### FR-CHK-01 Điều kiện vào thanh toán

Giỏ có ít nhất một dòng còn bán. Khách đã chọn cách nhận hàng cho mọi dòng. Không cho trộn trong cùng một đơn hai kiểu: vừa giao tận nơi vừa lắp tại showroom. Nếu khách thêm hai kiểu, trang giỏ yêu cầu tách: chọn một kiểu để thanh toán lần này, dòng kia ở lại giỏ.

### FR-CHK-02 Form thanh toán

Trường bắt buộc chung: họ tên, điện thoại Việt Nam 10 số, email.

Nếu giao hàng: tỉnh, quận, phường, địa chỉ cụ thể, ghi chú tùy chọn. Phí giao hàng tính lại khi đủ địa chỉ tỉnh và quận. Chưa có phí thì không cho đặt.

Nếu lắp hoặc nhận tại showroom: showroom, ngày, khung giờ còn chỗ. Khung giờ lấy từ lịch showroom đó. Dịch vụ lắp mặc định gắn với nhóm sản phẩm, thời lượng cộng dồn theo số lượng và có trần do quản trị đặt cho một lịch hẹn.

Xe: hãng, dòng, đời là bắt buộc nếu trong đơn có sản phẩm mức “cần tư vấn” hoặc khách chọn lắp tại chỗ. Biển số tùy chọn.

Phương thức thanh toán hiện theo cấu hình:

- Tiền mặt khi nhận hoặc khi làm tại showroom
- Chuyển khoản
- Cổng trực tuyến

Đơn toàn bộ nhận tại showroom mới được chọn tiền mặt tại showroom. Đơn giao hàng không hiện lựa chọn này.

Trước nút đặt hàng có ô đồng ý điều khoản mua hàng. Chưa chọn thì không gửi.

### FR-CHK-03 Tạo đơn

Bấm đặt hàng:

1. Kiểm tra lại giá, mã, tồn và khung giờ trên máy chủ. Không tin số liệu trình duyệt gửi lên.
2. Nếu giữ mềm đã hết hạn, thử giữ lại. Không đủ hàng thì trả về giỏ kèm dòng lỗi, không tạo đơn.
3. Tạo đơn trạng thái Chờ thanh toán hoặc Chờ xác nhận tùy phương thức.
4. Tiền mặt và chuyển khoản: trạng thái Chờ xác nhận với tiền mặt, Chờ thanh toán với chuyển khoản.
5. Cổng trực tuyến: tạo giao dịch, chuyển khách sang cổng, đơn ở Chờ thanh toán.
6. Gửi trang cảm ơn sau khi đơn tồn tại. Với cổng trực tuyến, trang cảm ơn chỉ hiện sau khi khách được cổng trả về, kể cả khi thanh toán chưa xong. Trang nói rõ đã thanh toán hay đang chờ.

Mã đơn dạng `DH` cộng năm cộng sáu chữ số, duy nhất.

### FR-CHK-04 Chuyển khoản

Trang cảm ơn và email hiện: ngân hàng, số tài khoản, chủ tài khoản, số tiền, nội dung bắt buộc là mã đơn. Nhân viên kế toán đối soát đánh dấu đã thu khi tiền vào. Hệ thống không tự coi là đã trả chỉ vì khách bấm “tôi đã chuyển”.

Quá 24 giờ chưa đánh dấu đã thu, đơn vẫn giữ hàng cứng đến giờ đó rồi nhả kho và chuyển sang Đã hủy nếu quản trị bật hủy tự động. Mặc định có bật.

### FR-CHK-05 Cổng thanh toán

Hỗ trợ một cổng ở giai đoạn thanh toán trực tuyến, cấu hình được VNPay hoặc MoMo. Cổng trả kết quả theo cả đường khách quay lại và đường thông báo máy chủ.

- Thành công, đúng số tiền, đúng mã giao dịch: đơn sang Đã thanh toán, rồi Chờ xác nhận để showroom xử lý.
- Khách hủy trên cổng: đơn ở Chờ thanh toán, khách mở lại trang đơn và thanh toán tiếp được trong hạn giữ hàng.
- Thất bại hoặc sai số tiền: không thu, đưa vào hàng đợi đối soát, hiện cho quản trị.

### FR-ORD-01 Vòng đời đơn

| Trạng thái | Ai chuyển tiếp | Ý nghĩa |
| --- | --- | --- |
| Chờ thanh toán | Hệ thống, khi thu tiền thành công | Chưa có tiền với cách phải trả trước |
| Chờ xác nhận | Tư vấn | Đã có cơ sở xử lý, chưa soạn hàng |
| Đang chuẩn bị | Thủ kho | Đã giữ hàng để soạn hoặc để lắp |
| Đang giao | Thủ kho | Đã bàn giao vận chuyển, có mã vận đơn |
| Chờ khách đến | Tư vấn | Đơn nhận hoặc lắp tại showroom, đã đến hẹn |
| Hoàn thành | Tư vấn hoặc thủ kho | Khách đã nhận hoặc đã lắp xong |
| Đã hủy | Khách hoặc tư vấn | Dừng đơn, nhả kho nếu chưa xuất |
| Đang đổi trả | Tư vấn | Có yêu cầu đổi trả đang xử lý |

Khách tự hủy chỉ khi đơn đang Chờ thanh toán hoặc Chờ xác nhận. Tư vấn hủy được trước khi trạng thái là Đang giao hoặc Hoàn thành. Hủy bắt buộc chọn lý do trong danh mục lý do.

Không nhảy cóc trạng thái. Muốn từ Hoàn thành về trước thì không được. Sai sót sau hoàn thành xử lý bằng đơn đổi trả, không sửa trạng thái cũ.

### FR-ORD-02 Theo dõi và đổi trả

Tra cứu công khai bằng mã đơn và số điện thoại đặt hàng. Khớp thì thấy trạng thái, các mốc thời gian và mã vận đơn nếu có. Không thấy địa chỉ đầy đủ của người khác khi chỉ đoán mã đơn.

Thành viên thấy đủ địa chỉ trong tài khoản của mình.

Yêu cầu đổi trả: đơn Hoàn thành, còn trong số ngày đổi trả của từng sản phẩm. Khách chọn dòng, số lượng, lý do, ảnh. Tạo phiếu ở trạng thái Chờ duyệt. Quản lý showroom duyệt thì phiếu sang Chờ hàng về hoặc Đã hoàn tiền tùy cách xử lý đã chọn: đổi mới, trả hàng hoàn tiền, hoặc từ chối. Từ chối có lý do khách đọc được.

Hoàn tiền qua cổng thì ghi nhận số tiền và mã hoàn. Hoàn tiền chuyển khoản thì nhân viên nhập biên lai. Website không tự chuyển khoản ra ngân hàng khách.

## 11. Đặt lịch dịch vụ

### FR-BK-01 Form

Dùng một form cho header, trang dịch vụ, trang liên hệ và chat. Trường:

- Họ tên, điện thoại
- Dịch vụ
- Showroom còn làm dịch vụ đó
- Ngày
- Khung giờ còn chỗ
- Hãng xe, dòng xe
- Ghi chú, tùy chọn

Dịch vụ đã biết từ trang nguồn thì điền sẵn và cho đổi.

### FR-BK-02 Sức chứa

Mỗi showroom khai báo lịch làm việc, thời lượng một khung, số chỗ trong một khung, và ngày nghỉ ngoại lệ. Chỗ đã chiếm gồm lịch ở trạng thái Chờ xác nhận và Đã xác nhận. Lịch hủy hoặc khách không đến thì nhả chỗ.

Khách chỉ thấy khung còn ít nhất một chỗ. Hai khách gửi cùng một khung cuối cùng: người được máy chủ ghi nhận trước giữ chỗ, người sau nhận lỗi “Khung giờ vừa hết chỗ” và danh sách khung còn lại. Không tạo hai lịch đè lên một chỗ.

### FR-BK-03 Xử lý lịch

Trạng thái: Chờ xác nhận, Đã xác nhận, Đang làm, Hoàn thành, Khách không đến, Đã hủy.

Tư vấn của đúng showroom xác nhận hoặc từ chối. Từ chối có lý do. Khi xác nhận, hệ thống gửi tin cho khách với mã lịch, giờ, địa chỉ showroom.

Khách hủy trên web khi lịch còn Chờ xác nhận, hoặc Đã xác nhận nhưng còn cách giờ hẹn ít nhất số giờ cấu hình. Mặc định 4 giờ. Quá hạn thì trên web chỉ hiện hướng dẫn gọi showroom.

Nhắc lịch một lần, mặc định 2 giờ trước giờ hẹn, nếu lịch đang Đã xác nhận.

### FR-BK-04 Gắn với đơn lắp đặt

Đơn lắp tại showroom tạo một lịch loại “lắp phụ kiện”, gắn mã đơn. Hủy đơn thì hủy lịch lắp nếu chưa sang Đang làm. Hủy lịch lắp không tự hủy đơn đã thanh toán. Trường hợp đó tư vấn phải xử lý hoàn tiền theo phiếu đổi trả.

## 12. Tài khoản khách

### FR-ACC-01 Đăng ký và đăng nhập

Đăng ký bằng số điện thoại. Gửi mã 6 số, hiệu lực 5 phút, tối đa năm lần gửi một số trong 1 giờ, tối đa năm lần nhập sai rồi khóa 15 phút.

Sau khi đúng mã, khách đặt mật khẩu từ 8 ký tự, có chữ và số. Đăng nhập bằng số điện thoại và mật khẩu. Quên mật khẩu dùng lại mã điện thoại.

Email là tùy chọn lúc đăng ký, dùng để nhận biên nhận. Nếu có email thì phải đúng định dạng và chưa gắn tài khoản khác.

### FR-ACC-02 Hồ sơ

Khách sửa tên, email, mật khẩu. Đổi số điện thoại phải xác nhận mã số mới. Xóa tài khoản: khách gửi yêu cầu, hệ thống ẩn dữ liệu đăng nhập sau 7 ngày, giữ đơn hàng và hóa đơn theo thời hạn lưu của mục 16. Trong 7 ngày khách đăng nhập lại thì hủy được yêu cầu xóa.

Sổ địa chỉ tối đa 10 địa chỉ, một địa chỉ mặc định. Garage tối đa 10 xe.

## 13. CMS

### FR-CMS-01 Trang tĩnh

Biên tập viên tạo trang với tiêu đề, đường dẫn, nội dung, ảnh chia sẻ, tiêu đề SEO, mô tả SEO, trạng thái. Trạng thái: nháp, chờ xuất bản, đã xuất bản, lưu trữ.

Soạn thảo có đoạn văn, tiêu đề, danh sách, ảnh, video, nút, bảng, bản đồ. Dán từ Word phải sạch định dạng lạ, không kéo theo font ngoài.

Xem trước dùng đúng giao diện website, có dải chữ “Bản xem trước” mà khách công khai không thấy. Xuất bản ghi phiên bản. Khôi phục một phiên bản cũ tạo thành một lần xuất bản mới, không xóa lịch sử.

Đường dẫn đổi thì đường dẫn cũ tự chuyển trong 180 ngày.

### FR-CMS-02 Trang chủ

Màn hình riêng liệt kê khối. Mỗi khối bật, tắt, sắp xếp, sửa nội dung. Xem trước cả trang trước khi xuất bản. Xuất bản trang chủ là một thao tác, không bắt xuất bản từng sản phẩm nằm trong khối. Sản phẩm ngừng bán tự biến khỏi khối khuyến mãi dù trang chủ chưa xuất bản lại.

### FR-CMS-03 Dịch vụ, bài viết, showroom

Dịch vụ có các trường ở FR-HOME-04 cộng khoảng giá từ, khoảng giá đến, thời lượng phút, danh sách showroom thực hiện.

Bài viết có chuyên mục, ảnh đại diện, ngày đăng, trạng thái, bài liên quan chọn tay. Hẹn giờ đăng được.

Showroom có tên, slug, địa chỉ đủ cấp, tọa độ, điện thoại, email, giờ từng ngày, ngày nghỉ, ảnh, mô tả, cờ showroom chính. Chỉ một showroom chính. Chọn showroom chính mới thì showroom chính cũ mất cờ.

### FR-CMS-04 Media

Tải jpg, png, webp, tối đa 5 MB mỗi ảnh. Video mp4 tối đa 30 MB. Bắt buộc text thay thế với ảnh dùng trên trang. Xóa tệp đang được nội dung đã xuất bản tham chiếu thì bị chặn và liệt kê chỗ đang dùng.

### FR-CMS-05 SEO

Mỗi trang công khai có title và meta description. Để trống thì hệ thống ghép từ tên trang và tên thương hiệu, đồng thời cảnh báo trong danh sách SEO thiếu. Sitemap chỉ chứa đường dẫn đã xuất bản. Trang nháp có thẻ không cho lập chỉ mục.

Trang 404 có ô tìm kiếm và liên kết về trang chủ, danh mục, liên hệ.

### FR-CMS-06 Menu

Menu header và footer sửa tách nhau. Mỗi mục có nhãn và một đích: trang, danh mục, đường dẫn. Mục không có đích thì không cho lưu. Kéo thả để sắp xếp trong phạm vi hai cấp.

## 14. Khuyến mãi

### FR-PROMO-01 Chiến dịch giá

Chiến dịch có tên, thời gian bắt đầu và kết thúc, danh sách sản phẩm hoặc danh mục, kiểu giảm theo số tiền hoặc phần trăm, trần giảm nếu là phần trăm, nhãn hiển thị. Không cho thời gian chồng lên một chiến dịch khác trên cùng sản phẩm nếu cả hai cùng kiểu giá bán. Hệ thống chỉ ra sản phẩm bị trùng lúc lưu.

Giá sau giảm không được nhỏ hơn hoặc bằng 0.

### FR-PROMO-02 Mã giảm giá

Mã có chuỗi duy nhất không phân biệt hoa thường, kiểu giảm, giá trị, đơn tối thiểu, số lượt toàn hệ thống, số lượt mỗi khách, thời hạn, phạm vi sản phẩm, nhóm khách nếu cần. Tắt mã thì mã ngừng áp dụng ngay, đơn đã đặt không tính lại.

Báo cáo mã gồm số lần dùng, tổng tiền giảm, đơn đã dùng.

## 15. Chat

### FR-CHAT-01 Kênh nhanh

Nút Zalo, Messenger và gọi đọc cấu hình: liên kết Zalo, liên kết Messenger, số điện thoại. Đổi cấu hình có hiệu lực ngay, không cần xuất bản trang chủ. Số điện thoại hiển thị có dấu cách cho người đọc, đường gọi dùng dạng số liền.

Nếu một kênh để trống, ẩn nút kênh đó.

### FR-CHAT-02 Widget trên website

Khách mở ô chat, gửi chữ và ảnh. Ảnh tối đa 5 MB, định dạng jpg, png, webp. Chưa đăng nhập vẫn nhắn được. Phiên khách vãng lai giữ trên trình duyệt 30 ngày.

Lần đầu trong một hội thoại, ô chat hỏi tên và số điện thoại sau tin nhắn đầu tiên, không chặn tin đầu. Khách bỏ qua vẫn nhắn tiếp. Khi có số điện thoại, hệ thống gắn hội thoại với khách đã có cùng số, hoặc tạo khách tiềm năng.

Đã đăng nhập thì gắn sẵn tài khoản, không hỏi lại tên.

Ngoài giờ làm việc của showroom chính, tin tự động gửi trong 3 giây: giờ mở cửa và lời mời để lại số. Tin tự động không tính là lần trả lời của nhân viên.

### FR-CHAT-03 Hộp thư

Một danh sách hội thoại lọc theo kênh, showroom, trạng thái, nhân viên phụ trách, chưa trả lời. Trạng thái: Mới, Đang xử lý, Chờ khách, Đã xong.

Mỗi hội thoại hiện kênh, tên, số điện thoại, showroom, người phụ trách, 20 tin gần nhất và tải tin cũ hơn. Tin nội bộ giữa nhân viên có nền khác và không bao giờ gửi ra kênh khách.

Từ hội thoại, tư vấn tạo lịch hẹn hoặc đơn nháp. Form mở với tên và số điện thoại điền sẵn. Đơn nháp và lịch lưu mã hội thoại.

Chuyển hội thoại cho nhân viên khác cùng showroom hoặc cho showroom khác. Người nhận thấy hội thoại ở đầu danh sách trạng thái Mới.

### FR-CHAT-04 Phân phối và hạn trả lời

Hội thoại web mới gán theo vòng cho tư vấn đang bật trạng thái Sẵn sàng của showroom chính. Không ai sẵn sàng thì hội thoại ở hàng chưa gán và báo quản lý showroom.

Trong giờ làm việc, hội thoại chưa có tin nhân viên sau 5 phút thì đánh dấu quá hạn trên hộp thư. Đây là mốc vận hành, không chặn khách nhắn tiếp.

Câu trả lời mẫu do quản lý soạn, tư vấn chèn vào ô trả lời rồi vẫn sửa trước khi gửi.

### FR-CHAT-05 Zalo và Messenger

Giai đoạn có hộp thư gom kênh: tin khách gửi vào Zalo OA và Facebook Page xuất hiện trong cùng hộp thư, trả lời từ hộp thư gửi ngược ra đúng kênh. Mất kết nối kênh thì hội thoại đó khóa ô trả lời và hiện lỗi “Kênh đang ngắt”, không làm mất lịch sử.

Tin nhắn lưu tại hệ thống 360. Không gửi nội dung chat cho dịch vụ huấn luyện mô hình.

## 16. Kho và showroom

### FR-INV-01 Tồn

Mỗi biến thể có một dòng tồn cho kho giao hàng trung tâm và một dòng cho mỗi showroom. Số liệu: tồn thực, đang giữ, khả dụng. Khả dụng không nhập tay. Nhân viên chỉ sửa tồn thực thông qua phiếu.

Phiếu nhập, phiếu xuất hủy, phiếu điều chuyển giữa hai điểm. Điều chuyển trừ điểm đi khi xuất và cộng điểm đến khi điểm đến xác nhận đã nhận. Không cộng ngay lúc tạo phiếu.

### FR-INV-02 Ngưỡng hết hàng

Mỗi biến thể có ngưỡng cảnh báo riêng, mặc định 3. Khả dụng xuống bằng hoặc dưới ngưỡng thì hiện trong danh sách sắp hết của thủ kho và quản lý showroom. Không gửi cho khách.

### FR-INV-03 Bán tại quầy

Tư vấn tạo đơn nháp, chọn showroom của mình, thêm sản phẩm, chọn thanh toán tiền mặt hoặc chuyển khoản, rồi chốt. Đơn này đi cùng vòng đời với đơn web. Đơn tại quầy không cần email. Bắt buộc có số điện thoại.

## 17. Thông báo

| Sự kiện | Kênh khách | Kênh nội bộ |
| --- | --- | --- |
| Tạo đơn | Email nếu có. Trang cảm ơn luôn có | Quản lý và tư vấn showroom liên quan |
| Đã thanh toán | Email | Kế toán và showroom |
| Đổi trạng thái đơn sang đang giao, chờ khách đến, hoàn thành, đã hủy | Email | Showroom |
| Tạo lịch, xác nhận, nhắc, hủy | SMS hoặc Zalo giao dịch, cộng email nếu có | Tư vấn showroom |
| Tin chat mới | Trong widget hoặc kênh gốc | Người được gán |
| Tồn chạm ngưỡng | Không gửi | Thủ kho showroom đó |

Khách có một công tắc nhận tin khuyến mãi, mặc định tắt. Tin về đơn, lịch và mã xác nhận không phụ thuộc công tắc này.

Nội dung mẫu sửa trong CMS thư: có biến mã đơn, tên khách, tổng tiền, giờ hẹn, địa chỉ showroom. Thiếu biến bắt buộc thì không cho lưu mẫu.

## 18. Báo cáo

Quản trị và quản lý showroom xem, xuất được tệp bảng tính:

- Doanh thu theo ngày, theo showroom, theo nguồn đơn web hoặc tại quầy. Doanh thu tính trên đơn Hoàn thành, theo ngày hoàn thành.
- Số đơn theo trạng thái.
- Sản phẩm bán theo số lượng và doanh thu, trong khoảng ngày tùy chọn.
- Tỷ lệ lịch hoàn thành, khách không đến, hủy.
- Thời gian trả lời chat lần đầu, số hội thoại quá hạn.
- Hiệu quả mã giảm giá.

Quản lý showroom chỉ xuất dữ liệu showroom mình. Số liệu trên báo cáo khớp danh sách đơn khi cùng bộ lọc. Báo cáo không sửa được.

## 19. Yêu cầu phi chức năng

**Hiệu năng.** Trang chủ trên kết nối 4G phổ thông hiện được chữ banner và khối đầu trong 3 giây với trang đã xuất bản. Tìm gợi ý trả về trong 1 giây ở tải bình thường. Thời điểm ghi đơn và trừ giữ hàng xử lý tuần tự để không bán vượt tồn.

**Sẵn sàng.** Mục tiêu vận hành 99,5% tính theo tháng, không tính cửa sổ bảo trì đã báo trước. Bảo trì làm ngoài giờ mở cửa showroom. Sao lưu dữ liệu mỗi ngày, giữ 30 bản. Khôi phục được dữ liệu về một bản trong 30 ngày. Mất dữ liệu tối đa chấp nhận là 24 giờ giao dịch.

**Nhật ký.** Giữ nhật ký quản trị 12 tháng. Nhật ký không cho nhân viên sửa hoặc xóa. Quản trị được xem và xuất.

**Trình duyệt.** Bản phát hành hiện tại của Chrome, Safari, Edge, và Firefox. Safari trên iPhone và Chrome trên Android thuộc hai phiên bản lớn gần nhất.

**Ngôn ngữ và định dạng.** Giao diện tiếng Việt có dấu. Tiền `1.890.000đ`. Ngày `20/10/2026`. Giờ 24 giờ, múi giờ Việt Nam.

## 20. Bảo mật và dữ liệu cá nhân

- Mật khẩu lưu đã băm. Không gửi mật khẩu trong email.
- Khu quản trị có thể bật mã bước hai cho từng tài khoản nhân viên.
- Phân quyền kiểm tra tại máy chủ cho mọi thao tác sửa.
- Ảnh đánh giá và ảnh chat chỉ tải lên kho đã quét loại tệp. Không chạy tệp khách tải lên.
- Số thẻ không đi qua máy chủ website. Chỉ lưu mã giao dịch cổng thanh toán.
- Trang chính sách nêu dữ liệu thu thập: họ tên, điện thoại, email, địa chỉ, thông tin xe, nội dung chat, nhật ký truy cập phục vụ đơn hàng.
- Khách yêu cầu xuất dữ liệu của mình hoặc xóa tài khoản trong mục tài khoản. Đơn hàng, phiếu thu và hóa đơn giữ 10 năm để phục vụ nghĩa vụ lưu chứng từ, sau đó xóa hoặc ẩn thông tin nhận diện theo chính sách pháp lý chủ đầu tư xác nhận với kế toán.
- Cookie phân tích chỉ chạy sau khi khách đồng ý trên thanh cookie. Cookie giỏ hàng và đăng nhập là cookie cần để site chạy, nêu rõ trong chính sách, không chờ đồng ý phân tích.
- Kết nối quản trị và trang thanh toán dùng HTTPS.

## 21. Tích hợp

| Hệ thống | Dữ liệu đi | Dữ liệu về | Khi lỗi |
| --- | --- | --- | --- |
| Cổng thanh toán | Mã đơn, số tiền, nội dung | Kết quả, mã giao dịch | Giữ đơn chờ thanh toán, đưa vào đối soát |
| Đơn vị vận chuyển | Địa chỉ, cân nặng, tiền thu hộ nếu có | Phí, mã vận đơn, trạng thái giao | Cho nhập tay phí và mã vận đơn |
| SMS hoặc Zalo thông báo | Mẫu tin, số điện thoại | Trạng thái gửi | Ghi thất bại, không chặn việc tạo đơn hoặc lịch |
| Zalo OA, Facebook Page | Tin trả lời | Tin khách | Khóa ô trả lời kênh đó, giữ lịch sử |
| Bản đồ | Tọa độ showroom | Bản đồ nhúng | Hiện địa chỉ chữ nếu bản đồ không tải |

Cân nặng phục vụ phí giao hàng khai báo trên biến thể, đơn vị gram. Thiếu cân nặng thì dùng mức mặc định của danh mục và hiện cảnh báo cho thủ kho.

## 22. Dữ liệu chính

Không phải thiết kế bảng vật lý. Đây là các nhóm thông tin bắt buộc phải lưu được.

**Sản phẩm.** Tên, slug, trạng thái, thương hiệu, danh mục, mô tả, thông số, cách nhận hàng cho phép, bảo hành theo tháng, ngưỡng hết hàng, ảnh, biến thể.

**Biến thể.** SKU duy nhất, giá trước VAT, thuế suất, thuộc tính, cân nặng, ảnh, trạng thái.

**Tương thích xe.** Sản phẩm gắn với mức mọi xe, danh sách phiên bản, hoặc cần tư vấn.

**Tồn.** Biến thể, địa điểm, tồn thực. Số giữ tính từ các phiếu giữ còn hiệu lực.

**Đơn.** Mã, khách, nguồn web hoặc quầy, trạng thái, cách nhận, showroom hoặc địa chỉ, tiền hàng, giảm giá, phí, tổng, phương thức thanh toán, mã hội thoại nếu có.

**Dòng đơn.** Biến thể, số lượng, đơn giá tại lúc đặt, thành tiền. Đổi giá sau này không sửa dòng đơn cũ.

**Thanh toán.** Đơn, số tiền, phương thức, trạng thái, mã giao dịch, người đối soát nếu thu tay.

**Lịch hẹn.** Mã, khách, showroom, dịch vụ hoặc đơn lắp, bắt đầu, kết thúc, trạng thái, số chỗ chiếm.

**Nội dung.** Trang, phiên bản, khối trang chủ, menu, media, chiến dịch, mã giảm giá.

**Chat.** Hội thoại, kênh, khách, người phụ trách, tin, hướng đi vào hoặc ra, cờ tin nội bộ.

**Khách.** Số điện thoại duy nhất, tên, email, địa chỉ, xe, cờ nhận tin khuyến mãi, trạng thái tài khoản.

## 23. Nghiệm thu theo tình huống

Các tình huống dưới đây là điều kiện ký nhận phạm vi. Kiểm thử đi hết bước, gồm cả đường lỗi.

1. Khách mới vào trang chủ, thấy đủ khối mockup, banner hết hạn không xuất hiện, bấm Mua ngay tới đúng liên kết CMS.
2. Khách chọn xe, mở danh mục, chỉ thấy huy hiệu vừa xe trên phụ kiện tương thích, vẫn thấy phụ kiện cần tư vấn kèm câu cảnh báo.
3. Thêm biến thể hết tồn thì bị chặn. Thêm biến thể còn hàng thì số giỏ tăng đúng.
4. Hai trình duyệt cùng mua chiếc cuối: một đơn thành công, đơn kia báo hết hàng, tồn thực không âm.
5. Mã giảm giá hết hạn, chưa đủ đơn tối thiểu, và mã hợp lệ cho ba thông báo khác nhau.
6. Đơn giao hàng không chọn được tiền mặt tại showroom. Đơn lắp tại chỗ không chọn được giao hàng trong cùng đơn.
7. Thanh toán cổng thành công thì đơn đã thanh toán đúng một lần dù thông báo cổng gửi tới hai lần.
8. Thanh toán lệch số tiền thì đơn không sang đã thanh toán và có trong hàng đối soát.
9. Khách hủy đơn đang chờ xác nhận thì tồn khả dụng tăng lại.
10. Hai khách đặt cùng khung giờ cuối: một lịch được tạo, người kia thấy hết chỗ.
11. Biên tập viên xem trước banner nháp, khách công khai không thấy. Sau xuất bản thì thấy trong 5 phút.
12. Xóa ảnh đang dùng trên trang đã xuất bản thì bị chặn.
13. Tư vấn showroom A không mở được đơn của showroom B.
14. Khách nhắn chat ngoài giờ, nhận tin tự động, để số điện thoại, tư vấn hôm sau thấy hội thoại và tạo được lịch với số đó.
15. Đánh giá từ tài khoản chưa mua sản phẩm thì bị từ chối. Đánh giá hợp lệ ở trạng thái chờ duyệt, chưa làm đổi điểm trung bình.
16. Trên màn hình rộng 390px, menu mở hết chiều ngang, đặt được lịch, thêm được giỏ, chữ ở khối cam kết không bị nút nổi che.

## 24. Phân kỳ bàn giao

**Giai đoạn 1, đủ để mở bán.** Trang chủ và các trang công khai, danh mục, sản phẩm, lọc xe, giỏ, đặt hàng tiền mặt và chuyển khoản, tồn một kho giao hàng và tồn theo showroom, đặt lịch, CMS trang chủ, dịch vụ, sản phẩm, showroom, menu, nút gọi, Zalo, Messenger dạng liên kết. Nghiệm thu tình huống 1 đến 6, 9 đến 13, 16.

**Giai đoạn 2.** Tài khoản khách, cổng thanh toán và đối soát, mã giảm giá, đánh giá, bài viết, widget chat và hộp thư web, đổi trả, báo cáo doanh thu và lịch. Nghiệm thu tình huống 7, 8, 14, 15.

**Giai đoạn 3.** Gom Zalo OA và Messenger vào hộp thư, nhắc lịch tự động, điều chuyển kho giữa showroom, xuất dữ liệu cho hóa đơn điện tử.

Mỗi giai đoạn có bản xem thử trên môi trường riêng trước khi lên môi trường khách dùng. Dữ liệu thật không dùng để thử thanh toán.

## 25. Việc chủ đầu tư cần cung cấp

Trước giai đoạn 1 cần có: bộ nhận diện, ảnh showroom và dịch vụ, danh sách showroom kèm giờ mở cửa, bảng giá dịch vụ, danh mục phụ kiện và tồn khởi tạo, tài khoản nhận chuyển khoản, số hotline, liên kết Zalo và Facebook, nội dung các trang chính sách. Cổng thanh toán và hợp đồng vận chuyển cần trước giai đoạn 2.
