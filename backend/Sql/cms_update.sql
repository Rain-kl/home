use `home`;

SET NAMES utf8mb4;

-- ----------------------------
CREATE TABLE IF NOT EXISTS `cms_site_link`
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
SELECT *
FROM (
    SELECT 'Blog' AS icon, '博客' AS name, 'https://blog.imsyy.top/' AS link, 1 AS sort_order, 1 AS enabled_flag
    UNION ALL SELECT 'Cloud', '网盘', 'https://pan.imsyy.top/', 2, 1
    UNION ALL SELECT 'CompactDisc', '音乐', 'https://music.imsyy.top/', 3, 1
    UNION ALL SELECT 'Compass', '起始页', 'https://nav.imsyy.top/', 4, 1
    UNION ALL SELECT 'Book', '网址集', 'https://web.imsyy.top/', 5, 1
    UNION ALL SELECT 'Fire', '今日热榜', 'https://hot.imsyy.top/', 6, 1
    UNION ALL SELECT 'LaptopCode', '站点监测', 'https://status.imsyy.top/', 7, 1
) seed
WHERE NOT EXISTS (SELECT 1 FROM `cms_site_link`);
