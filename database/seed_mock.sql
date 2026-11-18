SET NAMES utf8mb4;
USE jingcaixing;

INSERT INTO attractions
  (attraction_id, name, category, description, duration, opening_hours, latitude, longitude, image_path)
VALUES
  (1, '故宫博物院', '历史人文', '虚拟测试数据：明清皇家宫殿建筑群，适合安排半日游览。', 240, '08:30-17:00，周一闭馆', 39.9163456, 116.3971559, '/images/attractions/1.jpg'),
  (2, '天坛公园', '历史人文', '虚拟测试数据：以祈年殿为代表的明清祭祀建筑群。', 180, '06:00-22:00', 39.8822090, 116.4065450, '/images/attractions/2.jpg'),
  (3, '颐和园', '自然风光', '虚拟测试数据：以昆明湖和万寿山为核心的皇家园林。', 240, '06:30-20:00', 39.9998960, 116.2754910, '/images/attractions/3.jpg'),
  (4, '北海公园', '自然风光', '虚拟测试数据：拥有湖泊、白塔和古典园林景观的城市公园。', 150, '06:30-21:00', 39.9242680, 116.3893650, '/images/attractions/4.jpg'),
  (5, '簋街', '美食探店', '虚拟测试数据：聚集多种北京夜间餐饮选择的美食街区。', 120, '10:00-次日02:00', 39.9435000, 116.4237000, '/images/attractions/5.jpg'),
  (6, '雍和宫', '历史人文', '虚拟测试数据：北京著名藏传佛教寺院，建筑保存完整。', 120, '09:00-17:00', 39.9498680, 116.4173670, '/images/attractions/6.jpg'),
  (7, '香山公园', '自然风光', '虚拟测试数据：以山林景观和秋季红叶闻名的北京西郊公园。', 180, '06:00-19:30', 39.9953720, 116.1881240, '/images/attractions/7.jpg'),
  (8, '南锣鼓巷', '美食探店', '虚拟测试数据：融合胡同风貌、文创店铺与餐饮的步行街区。', 120, '全天开放', 39.9372290, 116.4037490, '/images/attractions/8.jpg'),
  (9, '八达岭长城', '历史人文', '虚拟测试数据：保存较完整的明长城段落，适合安排一日行程。', 300, '06:30-16:30', 40.3561730, 116.0146260, '/images/attractions/9.jpg'),
  (10, '奥林匹克森林公园', '自然风光', '虚拟测试数据：位于北京中轴线北端的大型城市森林公园。', 150, '06:00-21:00', 40.0214840, 116.3963720, '/images/attractions/10.jpg')
ON DUPLICATE KEY UPDATE
  name = VALUES(name), category = VALUES(category), description = VALUES(description),
  duration = VALUES(duration), opening_hours = VALUES(opening_hours),
  latitude = VALUES(latitude), longitude = VALUES(longitude), image_path = VALUES(image_path);
