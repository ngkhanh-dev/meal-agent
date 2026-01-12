import re
from datetime import datetime

def get_menus(from_date_str: str, to_date_str: str, is_special: int = 0):
    print(f"--- Truy suất toàn bộ thực đơn từ {from_date_str} đến {to_date_str} ---")
    
    # Dữ liệu raw của bạn
    raw_data = """
    Thời gian: 2025-08-01 00:00:00 - Danh sách món ăn: Cá trắm khúc sốt,Chả mỡ rim tiêu,Qủa su + cà rốt xào,Rau muống luộc,Canh sấu,Lạc,Dứa
    Thời gian: 2025-07-31 00:00:00 - Danh sách món ăn: Thịt kho dừa,Trứng cuộn hành,Cà bung đậu,Cải ngọt luộc,Canh moi rau mùng tơi +cà pháo,Lạc,Mía
    Thời gian: 2025-07-30 00:00:00 - Danh sách món ăn: Tôm rang hành,Đậu nhồi thịt,Bí bao tử xào,Cải chíp luộc,Canh cải thịt,Lạc,Chuối
    Thời gian: 2025-07-29 00:00:00 - Danh sách món ăn: Cá rô chiên giòn,Thịt kho củ cải,Bắp cải xào,Rau dền luộc,Canh rau ngót,Lạc,Ổi
    Thời gian: 2025-07-28 00:00:00 - Danh sách món ăn: Gà rán kho gừng,Thịt viên sốt,Rau muống xào,Qủa đỗ luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-07-25 00:00:00 - Danh sách món ăn: Gà ta nấu lá giang,Nem rán,Nộm dưa giá,Rau cải xào,Canh bí thịt,Lạc,Mía
    Thời gian: 2025-07-23 00:00:00 - Danh sách món ăn: Cá cam kho,Thịt quay mềm,Dưa cải sen,Bắp cải xào,Canh rau ngót thịt,Lạc,Vải
    Thời gian: 2025-07-24 00:00:00 - Danh sách món ăn: Vịt om sấu,Thịt rim tiêu,Măng xé xào,Cải ngồng luộc,Canh bầu thịt,Lạc,Mận
    Thời gian: 2025-07-22 00:00:00 - Danh sách món ăn: Tôm rang hành,Đậu kho thịt,Gía đỗ xào,Cải ngọt luộc,Canh cải  thịt,Lạc,Ổi
    Thời gian: 2025-07-21 00:00:00 - Danh sách món ăn: Thịt kho trứng cút,Cá rô chiên giòn,Bí bao tử xào,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-07-18 00:00:00 - Danh sách món ăn: Vịt om măng,Chả cốm,Đậu rán + rau sống,Bún,Canh thịt chua,Lạc,Dứa
    Thời gian: 2025-07-17 00:00:00 - Danh sách món ăn: Thịt kho tàu,Chả lá lốt,Mướp giá xào,Bắp cải luộc,Canh dầm cà,Lạc,Mía
    Thời gian: 2025-07-16 00:00:00 - Danh sách món ăn: Cá trôi kho xổi,Thịt rim tiêu,Dưa cải sen,Cải ngọt xào,Canh bí xanh thịt,Lạc,Thanh long
    Thời gian: 2025-07-15 00:00:00 - Danh sách món ăn: Gà ta nấu xáo,Đậu kho thịt,Củ cải xào thì là,Ngồng cải luộc,Canh rau ngót thịt,Lạc,Chè đỗ đen
    Thời gian: 2025-07-14 00:00:00 - Danh sách món ăn: Tôm rang lá chanh,Thịt kho củ cải,Bí đỏ xào,Rau muống xào,Canh me,Lạc,Dưa hấu
    Thời gian: 2025-07-10 00:00:00 - Danh sách món ăn: Ngan om sấu,Chả mỡ rim tiêu,Qủa lặc lè xào,Cải ngồng luộc,Canh rau dền bt,Lạc,Thanh long
    Thời gian: 2025-07-11 00:00:00 - Danh sách món ăn: Cá basa kho tộ,Thịt ram sả ớt,Quả đỗ xào,Muống luộc,Canh sấu,Lạc,Chuối
    Thời gian: 2025-07-09 00:00:00 - Danh sách món ăn: Đùi gà chiên mắm,Trứng đúc thịt,Mướp giá xào,Bắp cải luộc,Canh rau ngót thịt,Lạc,Dưa hấu
    Thời gian: 2025-07-08 00:00:00 - Danh sách món ăn: Cá quả kho chuối,Thịt xào măng xé,Cà tím om,Cải ngọt luộc,Canh cải thịt,Lạc,Nhãn
    Thời gian: 2025-07-07 00:00:00 - Danh sách món ăn: Thịt kho trúng cút,Tim bò xào cần tây,Đậu phụ sốt cà chua,Muống luộc,Canh sấu,Lạc,Mía
    Thời gian: 2025-07-04 11:05:03 - Danh sách món ăn: Thịt miếng + băm nướng,Nem cuốn,Nộm dưa giá,Bún + rau sống,Canh thịt chua,Lạc,Mận
    Thời gian: 2025-07-03 00:00:00 - Danh sách món ăn: Cá trắm sốt,Chả mỡ rim tiêu,Quả su xào,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-06-30 00:00:00 - Danh sách món ăn: Thị viên sốt,Gà rán,Quả đỗ xào,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-07-01 00:00:00 - Danh sách món ăn: Thịt kho dừa,Trứng cuộn hành,Cà bung đậu,Cải ngọt luộc,Canh moi rau rền,Lạc,Ổi
    Thời gian: 2025-06-27 00:00:00 - Danh sách món ăn: Gà kho gừng,Đậu nhồi thịt,Ngồng cải luộc,Bắp cải xào,Canh rau dền,Lạc,Mía
    Thời gian: 2025-06-26 00:00:00 - Danh sách món ăn: Thịt kho trứng cút,Chân giò xào xả ớt,Quả lặc lè luộc,Rau muống luộc,Canh sấu,Lạc,Chuối
    Thời gian: 2025-06-25 00:00:00 - Danh sách món ăn: Cá chép kho,Thịt rim tiêu,Quả su xào thịt,Rau rền luộc,Canh cải thịt,Lạc,Mận
    Thời gian: 2025-06-24 00:00:00 - Danh sách món ăn: Đùi gà nấu răm,Trứng đúc thịt,Quả đỗ luộc,Cải ngọt xào,Rau ngót nấu thịt,Lạc,Ổi
    Thời gian: 2025-06-23 00:00:00 - Danh sách món ăn: Thịt kho củ cải,Cá rô chiên giòn,Giá đỗ xào,Bắp cải luộc,Canh dầm cà chua,Lạc,Dưa hấu
    Thời gian: 2025-06-20 00:00:00 - Danh sách món ăn: Thịt nướng,Thịt viên nướng,Nem rán,Bún rau sống,Canh thịt chua,Lạc,Mận
    Thời gian: 2025-06-19 00:00:00 - Danh sách món ăn: Thịt quay mềm,Cá ba sa kho,Dưa cải sen,Rau muống xào tỏi,Canh sấu,Lạc,Chuối
    Thời gian: 2025-06-17 00:00:00 - Danh sách món ăn: Bò kho dưa,Trứng đúc thịt,Quả đỗ luộc,Cải bắp xào,Canh rau ngót thịt,Lạc,Mía
    Thời gian: 2025-06-18 00:00:00 - Danh sách món ăn: Thịt kho dừa,Đùi gà xào,Khoai tây xào,Cải ngồng luộc,Canh tép mùng tơi,Lạc,Ổi
    Thời gian: 2025-06-16 00:00:00 - Danh sách món ăn: Thịt kho tàu,Cá chép om măng,Bí đỏ xào tỏi,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-06-13 00:00:00 - Danh sách món ăn: Cá trấu sốt,Thăn lợn xào,Quả su xào,Cải ngồng luộc,Canh tép mùng tơi,Lạc,Dưa hấu
    Thời gian: 2025-06-12 00:00:00 - Danh sách món ăn: Thịt rim tiêu,Đùi gà rán,Bí xanh xào,Bắp cải luộc,Rau ngót nấu thịt,Lạc,Mía
    Thời gian: 2025-06-11 00:00:00 - Danh sách món ăn: Cá ba sa kho tiêu,Thịt ram sả,Dưa cải,Củ cải xào,Canh cải thịt,Lạc,Chuối tây
    Thời gian: 2025-06-10 00:00:00 - Danh sách món ăn: Thịt kho tàu,Trứng đúc thịt,Cà bung đậu,Cải ngọt luộc,Canh rau dền,Lạc,ổi
    Thời gian: 2025-06-09 00:00:00 - Danh sách món ăn: Đùi gà kho xả,Đậu sốt thịt,Quả đỗ luộc,Rau muống xào tỏi,Canh sấu,Lạc,Mận
    Thời gian: 2025-07-03 00:00:00 - Danh sách món ăn: Tôm rang hành,Đậu sốt thịt,Bí bao tử xào,Cải chíp luộc,Canh cải thịt,Lạc,Chuối
    Thời gian: 2025-07-02 00:00:00 - Danh sách món ăn: Cá cam kho,Thịt luộc,Dưa cải sen,Bắp cải xào,Canh rau ngót,Lạc,Mía
    Thời gian: 2025-06-06 10:27:05 - Danh sách món ăn: Vịt om sấu,Nem rán,Đậu rán,Bún,rau sống,Lạc,Dứa
    Thời gian: 2025-06-05 10:25:54 - Danh sách món ăn: Đùi gà kho xả,Thịt rim tiêu,Khoai tây xào,Cải ngồng luộc,Canh bầu thịt,Lạc,Ổi
    Thời gian: 2025-06-04 10:24:37 - Danh sách món ăn: Thịt quay mềm,Trứng đúc thịt,Mướp giá xào,Rau dền luộc,Canh cải thịt,Lạc,Chuối tây
    Thời gian: 2025-06-03 10:22:36 - Danh sách món ăn: Cá diếc kho tương,Chân giò xào xả ớt,Cải ngọt xào,Bắp cải luộc,Canh tép mùng tơi,Lạc,Mận
    Thời gian: 2025-05-30 00:00:00 - Danh sách món ăn: Ngan om khoai sọ,Thịt kho chả mỡ,Cải mèo xào,Bắp cải luộc,Canh thịt rau cải,Lạc,Mận hậu
    Thời gian: 2025-05-29 00:00:00 - Danh sách món ăn: Cá quả kho chuối,Chân giò xào xả ớt,Bí đỏ xào tỏi,Ngồng cải luộc,Rau ngót nấu thịt,Lạc,Dứa chín
    Thời gian: 2025-05-28 00:00:00 - Danh sách món ăn: Thịt kho củ cải,Tôm rang hành,Đậu sốt cà,Rau muống xào tỏi,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-05-27 00:00:00 - Danh sách món ăn: Cá cam kho tộ,Trứng đúc thịt,Chuối đậu om,Cải ngọt luộc,Canh bí đỏ thịt,Lạc,Chuối tây
    Thời gian: 2025-05-26 00:00:00 - Danh sách món ăn: Thịt kho trứng cút,Chả lá lốt,Rau lang xào tỏi,Dưa bắp cải,Canh thịt chua sấu,Lạc,Ổi
    Thời gian: 2025-05-23 00:00:00 - Danh sách món ăn: Ngan om khoai sọ,Thịt kho chả mỡ,Cải mèo xào,Bắp cải luộc,Canh thịt rau cải,Lạc,Mận hậu
    Thời gian: 2025-05-22 00:00:00 - Danh sách món ăn: Cá quả kho chuối,Chân giò xào xả ớt,Bí đỏ xào tỏi,Ngồng cải luộc,Rau ngót nấu thịt,Lạc,Dứa chín
    Thời gian: 2025-05-21 00:00:00 - Danh sách món ăn: Thịt kho củ cải,Tôm rang hành,Đậu sốt cà,Rau muống xào tỏi,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-05-20 00:00:00 - Danh sách món ăn: Cá cam kho tộ,Trứng đúc thịt,Chuối đậu om,Cải ngọt luộc,Canh bí đỏ thịt,Lạc,Chuối tây
    Thời gian: 2025-05-19 00:00:00 - Danh sách món ăn: Thịt kho trứng cút,Chả lá lốt,Rau lang xào tỏi,Dưa bắp cải,Canh thịt chua sấu,Lạc,Ổi
    Thời gian: 2025-05-16 00:00:00 - Danh sách món ăn: Thịt kho tàu,Gà xào sả ớt,Bí xanh xào,Rau muống luộc,Canh sấu,Lạc,Chuối tây
    Thời gian: 2025-05-15 00:00:00 - Danh sách món ăn: Tôm rang hành,Đậu nhồi thịt,Khoai tây xào,Bắp cải luộc,Canh rau dền bt,Lạc,Dứa chín
    Thời gian: 2025-05-14 00:00:00 - Danh sách món ăn: Bò kho gừng,Trứng đúc thịt,Qủa bí đỏ xào tỏi,Cải ngồng luộc,Canh cải thịt,Lạc,Mía
    Thời gian: 2025-05-13 00:00:00 - Danh sách món ăn: Thịt kho củ cải,Cá trắm kho xổi,Măng giá xào,Cải ngọt luộc,Canh tép mùng tơi,Lạc,Ổi
    Thời gian: 2025-05-12 00:00:00 - Danh sách món ăn: Gà rang gừng,Thịt quay mềm,Dưa cải sen xào,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-04-29 03:47:23 - Danh sách món ăn: Thịt kho trứng cút,Gà xào sả ớt,Đậu phụ sốt,Rau muống luộc,Canh sấu,Lạc,Ổi
    Thời gian: 2025-04-28 03:44:30 - Danh sách món ăn: Cá basa kho tộ,Thịt rang hành,Bắp cải xào,Quả đỗ luộc,Canh ngao rau cải,Lạc,Dưa hấu
    Thời gian: 2025-04-26 11:14:24 - Danh sách món ăn: Thịt nấu giả cầy,Chả cốm,Đậu rán,Bún - rau sống,Canh thịt chua,Dứa
    Thời gian: 2025-04-25 00:00:00 - Danh sách món ăn: Bò kho gừng,Nem rán,Nộm dưa giá,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-04-24 00:00:00 - Danh sách món ăn: Cá trắm kho,Thịt kho tàu,Su hào xào mùi,Cải chíp luộc,Canh khoai tây,Lạc,Ổi
    Thời gian: 2025-04-23 00:00:00 - Danh sách món ăn: Gà nấu xáo,Thịt rang hành,Cà tím om đậu,Cải bắp luộc,Canh thịt chua rau ngổ,Lạc,Chuối tiêu
    Thời gian: 2025-04-22 00:00:00 - Danh sách món ăn: Thịt kho trứng gà,Cá rô phi chiên,Đậu phụ tẩm hành,Cải ngọt luộc,Canh cải thịt,Lạc,Mía
    Thời gian: 2025-04-21 00:00:00 - Danh sách món ăn: Ngan kho gừng,Đậu nhồi thịt,Qủa Đỗ xào tỏi,Cải ngồng luộc,Canh moi mùng tơi,Giò,Dứa chín
    Thời gian: 2025-04-18 00:00:00 - Danh sách món ăn: Đùi gà chiên mắm,Giò chả rim tiêu,Cải ngồng xào tỏi,Dưa cải sen,Canh thịt chua,Lạc,Ổi
    Thời gian: 2025-04-16 00:00:00 - Danh sách món ăn: Thịt kho tàu,Chân giò xào xả ớt,Bí bao tử xào,Cải ngọt luộc,Canh rau dền bt,Lạc,Chuối
    Thời gian: 2025-04-17 00:00:00 - Danh sách món ăn: Cá quả kho tiêu,Trứng cuộn hành,Cà tím om đậu,Rau lang luộc,Canh bí thịt,Lạc,Dứa chín
    Thời gian: 2025-04-15 00:00:00 - Danh sách món ăn: Cá hồng om măng,Thịt rim tiêu,Khoai tây xào,Cải chíp luộc,Canh ngao mùng tơi,Trứng,Mía
    Thời gian: 2025-04-14 00:00:00 - Danh sách món ăn: Thịt kho dừa,Chả lá lốt,Bắp cải xào,Rau muống luộc,Canh sấu,Lạc,Dưa hấu
    Thời gian: 2025-04-07 05:28:28 - Danh sách món ăn: Gà kho gừng,Thịt luộc,Dưa bắp cải,Cải ngọt xào tỏi,Canh cải nước thịt,Lạc,Dưa hấu
    Thời gian: 2025-04-08 05:27:34 - Danh sách món ăn: Cá trắm kho,Giò chả rim tiêu,Đậu phụ sốt cà chua,Rau muống luộc,Canh sấu,Lạc,Ổi
    Thời gian: 2025-04-09 10:00:27 - Danh sách món ăn: Thịt kho củ cải,Tôm rang hành,Măng xào,Cải chíp luộc,Canh mùng tơi bt,Lạc,Chuối
    Thời gian: 2025-04-10 09:59:40 - Danh sách món ăn: Cá rô chiên giòn,Thịt kho trứng cút,Qủa đỗ xào,Bắp cải luộc,Canh cải cúc,Lạc,Mía
    Thời gian: 2025-04-11 09:51:54 - Danh sách món ăn: Thịt ram sả,Trứng đúc thịt,Su Su xào tỏi,Cải mèo luộc,Canh bí đỏ,Lạc,Củ đậu
    Thời gian: 2025-02-19 09:58:52 - Danh sách món ăn: Bò kho gừng,Giò chả rim tiêu,Bí bao tử xào,Cải ngồng luộc,Canh rau dền bt,Lạc,Cam
    Thời gian: 2025-02-18 09:57:13 - Danh sách món ăn: Cá cam kho tiêu,Thịt kho trứng cút,Dưa bắp cải,Qủa đỗ xào,Canh thịt chua,Lạc,Ổi
    Thời gian: 2024-12-02 03:48:43 - Danh sách món ăn: Gà kho xả,Thăn lợn xào,Đậu phụ sốt cà,Rau muống luộc,Canh cải thịt,Lạc,Dưa hấu
    Thời gian: 2024-05-27 00:00:00 - Danh sách món ăn: Đùi gà kho xả,Thịt rang hành,Qủa su xào tỏi,Bắp cải luộc,Canh dầm cà,Lạc,Dưa hấu
    Thời gian: 2024-05-24 00:00:00 - Danh sách món ăn: Thịt chiên lá móc mật,Giò chả kho,Đậu rán,Rau muống xào,Canh sấu,Lạc,Ôỉ
    Thời gian: 2024-05-22 00:00:00 - Danh sách món ăn: Cá rô lọc chiên,Thịt kho tàu,Qủa su xào,Bắp cải luộc,Canh dầm cà,Lạc,Dứa
    Thời gian: 2024-05-23 00:00:00 - Danh sách món ăn: Nạc vai rim,Thịt thăn xào tc,Chuối đậu om,Cải ngọt luộc,Canh tép mùng tơi,Lạc,Chuối
    Thời gian: 2024-05-21 00:00:00 - Danh sách món ăn: Gà chiên giòn,Thịt kho đậu,Bí xanh xào,Cải chíp luộc,Canh rau dền bt,Lạc,Dưa hấu
    Thời gian: 2024-05-20 00:00:00 - Danh sách món ăn: Nạc vai rim tiêu,Trứng kho,Qủa đỗ xào,Rau muống luộc,Canh sấu,Lạc,Mía
    Thời gian: 2024-05-17 00:00:00 - Danh sách món ăn: Thịt rang cháy cạnh,Nem rán,Dưa góp,Bún,Canh riêu cua,Lạc,Dưá chín
    Thời gian: 2024-05-16 00:00:00 - Danh sách món ăn: Thịt kho trứng cút,Cá nục chiên,Bí bao tử xào,Cải ngồng luộc,Canh rau ngót thịt,Lạc,Mía
    Thời gian: 2024-05-15 00:00:00 - Danh sách món ăn: Gà kho gừng,Đậu trắng sốt thịt,Củ cải xào,Rau muống luộc,Canh sấu,Lạc,Chuối
    Thời gian: 2024-05-14 00:00:00 - Danh sách món ăn: Cá trôi kho sổi,Thịt quay mềm,Cà tím om đậu,Cải ngọt luộc,Canh thịt chua,Lạc,Ôỉ
    Thời gian: 2024-05-13 00:00:00 - Danh sách món ăn: Thịt kho dừa,Trứng đúc thịt,Củ quả xào tỏi,Canh cải gừng,Bắp cải luộc,Lạc,Dưa hấu
    Thời gian: 2024-05-10 11:01:35 - Danh sách món ăn: Thịt chưng mắm tép,Đậu nhồi thịt,Khoai tây xào,Canh rau dền bt,Lạc,Chuối tiêu,Cải ngồng luộc
    Thời gian: 2024-12-06 03:48:43 - Danh sách món ăn: Gà chiên mắm (ko cho gừng),Thịt kho dừa,Khoai tây xào,Bắp cải luộc,Canh dầm cà,Lạc,Ôỉ
    Thời gian: 2024-12-05 03:48:43 - Danh sách món ăn: Cá trắm sốt,Thịt chân giò xào xả ớt,Chuối om đậu,Cải mèo luộc,Canh rau dền bt,Lạc,Dưa hấu
    Thời gian: 2024-12-04 03:48:43 - Danh sách món ăn: Thịt kho tàu,Trứng đúc thịt,Su hào xào mùi ta,Cải ngọt luộc,Canh bí đỏ thịt,Lạc,Chuối
    Thời gian: 2024-12-03 03:48:43 - Danh sách món ăn: Cá diếc kho tương,Giò chả rim tiêu  ,Dưa bắp cải,Su su xào,Canh ngao mùng tơi,Lạc,Đu đủ chín
    """ # ... (Bạn dán đầy đủ data vào đây)

    try:
        # Chuẩn hóa ngày bắt đầu và kết thúc về dạng date (Y-M-D)
        # replace("Z", "+00:00") để xử lý định dạng ISO từ LLM/Client gửi lên
        start_date = datetime.fromisoformat(from_date_str.replace("Z", "+00:00")).date()
        end_date = datetime.fromisoformat(to_date_str.replace("Z", "+00:00")).date()
    except Exception as e:
        print(f"Lỗi định dạng ngày: {e}")
        return []

    all_matched_menus = []
    
    # Regex lấy phần Ngày (YYYY-MM-DD) và Danh sách món
    pattern = r"Thời gian:\s*([\d-]+)\s+[\d:]+\s*-\s*Danh sách món ăn:\s*(.+)"
    matches = re.findall(pattern, raw_data)
    
    for date_part, items_str in matches:
        try:
            current_date = datetime.strptime(date_part, "%Y-%m-%d").date()
            
            # KIỂM TRA KHOẢNG NGÀY
            if start_date <= current_date <= end_date:
                items = [item.strip() for item in items_str.split(",") if item.strip()]
                
                # Xác định tính chất đặc biệt của món ăn
                special_keywords = ['bún', 'ngan', 'vịt', 'nem rán', 'giả cầy', 'phở', 'cháo', 'nướng']
                is_this_special = any(kw in items_str.lower() for kw in special_keywords)
                is_special_val = 1 if is_this_special else 0

                # Lọc theo tham số is_special nếu cần
                # Nếu bạn muốn lấy "TẤT CẢ" dòng trong ngày đó bất kể loại món, hãy bỏ điều kiện if này.
                # Ở đây tôi giữ lại lọc theo ý bạn: Nếu truyền is_special thì chỉ lấy loại đó.
                if is_special == is_special_val:
                    all_matched_menus.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "items": items,
                        "is_special": is_special_val
                    })
        except:
            continue

    # Sắp xếp theo thứ tự thời gian tăng dần
    all_matched_menus.sort(key=lambda x: x['date'])
    
    return all_matched_menus

# --- TEST ---
# Lấy toàn bộ thực đơn trong tháng 7 năm 2025
# result = get_menus("2025-07-01T00:00:00Z", "2025-07-31T23:59:59Z", is_special=0)
# print(f"Tìm thấy {len(result)} dòng thực đơn cơm thường.")