CREATE database if NOT EXISTS `home` default character set utf8mb4 collate utf8mb4_unicode_ci;
use `home`;

SET NAMES utf8mb4;

-- ----------------------------
-- Table structure for cms_site_link
-- ----------------------------
DROP TABLE IF EXISTS `cms_site_link`;
CREATE TABLE `cms_site_link`
(
    `id`           BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `icon`         VARCHAR(64)  DEFAULT NULL COMMENT '图标名称',
    `name`         VARCHAR(64)  DEFAULT NULL COMMENT '站点名称',
    `link`         VARCHAR(500) DEFAULT NULL COMMENT '站点链接',
    `sort_order`   INT          DEFAULT 0 COMMENT '排序',
    `enabled_flag` TINYINT(4)   DEFAULT 1 COMMENT '是否启用',
    `create_time`  DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time`  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

    PRIMARY KEY (`id`),
    KEY `idx_sort_order` (`sort_order`),
    KEY `idx_enabled_flag` (`enabled_flag`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='首页导航站点表';

INSERT INTO `cms_site_link`
(`icon`, `name`, `link`, `sort_order`, `enabled_flag`)
VALUES
    ('Blog', '博客', 'https://blog.imsyy.top/', 1, 1),
    ('Cloud', '网盘', 'https://pan.imsyy.top/', 2, 1),
    ('CompactDisc', '音乐', 'https://music.imsyy.top/', 3, 1),
    ('Compass', '起始页', 'https://nav.imsyy.top/', 4, 1),
    ('Book', '网址集', 'https://web.imsyy.top/', 5, 1),
    ('Fire', '今日热榜', 'https://hot.imsyy.top/', 6, 1),
    ('LaptopCode', '站点监测', 'https://status.imsyy.top/', 7, 1);
