use `home`;

SET NAMES utf8mb4;

-- ----------------------------

INSERT IGNORE INTO oms_parameter
(param_code, param_name, kind_code, param_value, param_desc, enabled_flag)
VALUES (1001, 'default', 'default', 'default', 'default', 1);

INSERT INTO oms_user
(user_id, username, password, nickname, email, phone, created_user, status)
VALUES
('admin', 'admin', '123456', '管理员', 'admin@admin.com', '', 'system', 1);