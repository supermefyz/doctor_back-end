/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80033
 Source Host           : localhost:3306
 Source Schema         : medical_database

 Target Server Type    : MySQL
 Target Server Version : 80033
 File Encoding         : 65001

 Date: 06/04/2025 16:56:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (3, 'admin', 'scrypt:32768:8:1$JxamJ8DRSGJL4Wta$74b98fce9262a29ec9490504d611b8d241136c0470a78ac5fd1badeffe6d19117bdc047127cf06fd444d7eea3a23090d18beb89f7022f844882e4e8d5f45396f');

-- ----------------------------
-- Table structure for doctor
-- ----------------------------
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE `doctor`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `department` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of doctor
-- ----------------------------
INSERT INTO `doctor` VALUES (1, '龙明智', '123456', '姜家园院区高级专家', 'scrypt:32768:8:1$NqsEKzP51Uw2OD6s$e64ccc0f6052084b044cc184d04e9811a16ab15e735ac296081afe5cf80c8ce2578a533ce0b21384af4148c118b488edeefa5075583bf51d9302b79648521c90', 0);
INSERT INTO `doctor` VALUES (2, '孙烈', '', '姜家园院区高级专家', 'scrypt:32768:8:1$hS91QxxEsd7SDQJQ$38cdf164270540945f6fc7f79dc8d89f5a92cc19140c8c4194445b32054affcffc2b3f372ae5938858b6ae52b9cafb2dc399e9d5a34fe714f228e5b89356d06a', 1);
INSERT INTO `doctor` VALUES (3, '杨富', NULL, '姜家园院区高级专家', '', 0);
INSERT INTO `doctor` VALUES (4, '洪梅', NULL, '姜家园院区高级专家', 'scrypt:32768:8:1$jTZh4TGGd30NPh9X$2aea2d207bdc267346c005bd74bb668fbcae5777815c160ca9d0e113529be18de3870e0c15d69d4c40298815a9cb279ce5431f177769d59648d18d2dad9c2f2e', 0);
INSERT INTO `doctor` VALUES (5, '谭晓', NULL, '姜家园院区高级专家', 'scrypt:32768:8:1$HKDqvNeh1Oz1E6tL$5dee87501aa71767b2a0d424066b8cb8bc2f0389e8a93af871f3251715be413d3ca3ab2b686f3824873bc133b746b4b871ceac15d59d327ffa9e13cc52ce901a', 0);
INSERT INTO `doctor` VALUES (6, '俞建', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (7, '杨季明', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (8, '章海燕', NULL, '姜家园院区专家门诊', 'scrypt:32768:8:1$J2LLwZ6vZEi3i5gY$2855bd5adb11683e117ceec878b897bcf6ff7542f30349fe1909e3d70a0dde51fd79c70c3bdc70f1112601856d51e67d555dfa07f1880f503cf2cc789389e702', 0);
INSERT INTO `doctor` VALUES (9, '朱舒舒', NULL, '姜家园院区专家门诊', 'scrypt:32768:8:1$OV9oxeYUPS8c6r43$a1eaff49e9eadbd5646277af82134fa843c94a2f04c4fdbf971f556a1d56251f9fb056532d6f8f7583c3ef422a6125c03d0be3532571a089c8a91b41b1f76611', 0);
INSERT INTO `doctor` VALUES (10, '邱敏', NULL, '姜家园院区专家门诊', 'scrypt:32768:8:1$kKDCs5kkVb1JXjKO$5acec2b09cc499e921d8635e3678df88fe4c4a3859dde3e7a56ff2c73db0685b8bf9a7ebdf7a0914da481a2440dede4a5c04b61bf2ace5d664852e2f0fe7d9f2', 0);
INSERT INTO `doctor` VALUES (11, '胡文志', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (12, '张博晴', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (13, '程宏勇', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (14, '李秀珍', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (15, '王迪斌', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (16, '郭守玉', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (17, '徐少华', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (18, '钱琦', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (19, '贾志强', NULL, '姜家园院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (20, '蒯琳', NULL, '姜家园院区专科门诊1', '', 0);
INSERT INTO `doctor` VALUES (21, '赵文雪', NULL, '姜家园院区专科门诊1', '', 0);
INSERT INTO `doctor` VALUES (22, '肖芳萍', NULL, '姜家园院区专科门诊2', '', 0);
INSERT INTO `doctor` VALUES (23, '戴牧', NULL, '姜家园院区专科门诊2', '', 0);
INSERT INTO `doctor` VALUES (24, '王磊', NULL, '姜家园院区专科门诊2', '', 0);
INSERT INTO `doctor` VALUES (25, '姜海', NULL, '迈皋桥院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (26, '周海波', NULL, '迈皋桥院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (27, '李积薇', NULL, '迈皋桥院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (28, '刘玉辉', NULL, '迈皋桥院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (29, '张宝美', NULL, '迈皋桥院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (30, '戴一鸣', NULL, '迈皋桥院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (31, '张敏', NULL, '迈皋桥院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (32, '赵文雪', NULL, '萨家湾院区专家门诊', '', 0);
INSERT INTO `doctor` VALUES (33, '蒯琳', NULL, '萨家湾院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (34, '贾志强', NULL, '萨家湾院区专科门诊', '', 0);
INSERT INTO `doctor` VALUES (35, '李庆国', NULL, '迈区心血管中心（外科）', '', 0);
INSERT INTO `doctor` VALUES (36, '邵峻', NULL, '迈区心血管中心（外科）', '', 0);
INSERT INTO `doctor` VALUES (37, '王波', NULL, '迈区心血管中心（外科）', '', 0);
INSERT INTO `doctor` VALUES (38, '於文达', NULL, '迈区心血管中心（外科）', '', 0);
INSERT INTO `doctor` VALUES (39, '张冲', NULL, '迈区心血管中心（外科）', '', 0);
INSERT INTO `doctor` VALUES (40, '耿直', NULL, '迈区心血管中心（外科）', '', 0);

-- ----------------------------
-- Table structure for medical_records
-- ----------------------------
DROP TABLE IF EXISTS `medical_records`;
CREATE TABLE `medical_records`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int(0) NOT NULL,
  `gender` enum('男','女','其他') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `height` int(0) NOT NULL,
  `weight` int(0) NOT NULL,
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `medical_history` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `diagnosis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `suggestion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `time` date NOT NULL,
  `recommendation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 97 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of medical_records
-- ----------------------------
INSERT INTO `medical_records` VALUES (84, '李思', 23, '男', 160, 66, '12345678910', '糖尿病', '患者李思，23岁男性，患有糖尿病10年，近期出现尿液咸味和血丝，伴有尿痛、尿急、尿频症状。患者未定期监测血糖，也未遵循医嘱进行药物治疗和饮食控制。结合病史和症状，初步诊断为糖尿病肾病或尿路感染，需进一步检查确认。', '诊断建议\n1. 立即进行尿常规、尿培养和肾功能检查\n2. 完善血糖监测和糖化血红蛋白检测\n3. 严格控制血糖，开始规范的糖尿病治疗\n4. 建议低盐低蛋白饮食\n5. 必要时进行肾脏超声检查\n6. 密切监测血压', '2025-04-03', '推荐科室和医生（根据排班表推荐）\n1. 姜家园院区专家门诊 * 杨季明（周二上午/周二下午）\n2. 迈皋桥院区专家门诊 * 杨季明（周二上午）\n3. 姜家园院区高级专家 * 龙明智（周一上午/周四上午）\n\n注：优先推荐杨季明医生，因其在糖尿病及其并发症诊治方面经验丰富。患者需尽快就诊，避免病情进一步恶化。');
INSERT INTO `medical_records` VALUES (85, '李思', 23, '女', 160, 66, '12345678910', '糖尿病', '患者李思，23岁女性，有10年糖尿病病史，当前主要症状为头痛伴随恶心、呕吐和视力模糊，视力模糊可能与糖尿病视网膜病变或其他糖尿病相关并发症有关。', '诊断建议\n1. 立即进行血糖监测和糖化血红蛋白检测，评估糖尿病控制情况\n2. 建议进行眼科专科检查，排除糖尿病视网膜病变\n3. 建议进行头颅CT或MRI检查，排除颅内病变\n4. 需要评估是否存在糖尿病酮症酸中毒等急性并发症\n5. 建议进行肾功能检查，评估糖尿病肾病情况', '2025-04-03', '推荐科室和医生（根据排班表推荐）\n1. 内分泌科：姜家园院区专家门诊*杨季明（周二上午/周一下午）\n2. 眼科：姜家园院区专科门诊1*蒯琳（周一上午/周五上午）或赵文雪（周二上午/周四上午）\n3. 神经内科：姜家园院区专家门诊*胡文志（周三上午）');
INSERT INTO `medical_records` VALUES (89, '李思', 23, '男', 160, 66, '12345678910', '都有', '根据患者提供的症状（胃痛、恶心），初步诊断为急性胃炎或消化不良。由于患者否认呕吐、腹泻等其他消化系统症状，且症状持续时间较短，暂时不考虑严重胃肠道疾病。', '诊断建议\n1. 建议进行血常规和腹部超声检查以排除其他潜在疾病\n2. 暂时可服用质子泵抑制剂（如奥美拉唑）缓解症状\n3. 建议清淡饮食，避免辛辣刺激性食物\n4. 如症状持续或加重，应及时复诊', '2025-04-03', '推荐科室和医生（根据排班表推荐），并给出理由\n推荐科室：姜家园院区专家门诊 * 消化内科\n推荐医生：杨季明（周二上午/周一下午）或章海燕（周一全天）\n理由：\n1. 患者主要症状为消化道不适，消化内科专家最适合处理此类问题\n2. 杨季明医生和章海燕医生都是消化内科专家，在胃部疾病诊治方面经验丰富\n3. 这两位医生的出诊时间最近（周二上午/周一全天），可以尽快就诊\n4. 姜家园院区交通便利，检查设备齐全');
INSERT INTO `medical_records` VALUES (94, '。。。', 64, '女', 66, 99, '949676494676679', '精神病', '患者目前主要症状为阳痿，并伴有心理压力和焦虑情绪。考虑到患者有精神病史，可能与精神类药物或心理因素有关。', '诊断建议\n1. 建议进行详细的病史采集，包括当前服用的精神类药物及其剂量。\n2. 评估患者的心理状态，尤其是焦虑和抑郁症状。\n3. 可能需要调整精神类药物的剂量或种类，以减少对性功能的影响。\n4. 建议进行性功能相关的检查，如激素水平检测等。', '2025-04-03', '推荐科室和医生（根据排班表推荐），并给出理由\n推荐科室：精神科或心理科\n推荐医生：姜家园院区专家门诊的杨季明（周二上午）或章海燕（周一上午/下午）\n理由：患者有精神病史且目前症状与心理因素相关，杨季明和章海燕是精神科专家，能够综合评估患者的心理状态和药物影响，提供专业的治疗方案。');
INSERT INTO `medical_records` VALUES (95, '郭思怡', 21, '女', 165, 50, '13569422280', '无', '', '', '2025-04-03', NULL);
INSERT INTO `medical_records` VALUES (96, '郭思怡', 21, '女', 165, 50, '13569422280', '无', '', '', '2025-04-03', NULL);
INSERT INTO `medical_records` VALUES (100, '李思', 23, '男', 160, 66, '12345678910', '无', '', '', '2025-04-05', NULL);
INSERT INTO `medical_records` VALUES (103, '李思', 23, '男', 160, 66, '12345678910', '无', '', '', '2025-04-05', NULL);
INSERT INTO `medical_records` VALUES (104, '李思', 23, '男', 160, 66, '12345678910', '无', '患者目前主要症状为头疼、恶心、呕吐、视觉模糊、对光线敏感以及眼前发黑，这些症状可能提示偏头痛、颅内压增高、视神经炎或其他神经系统疾病。需要进一步检查以明确病因。', '诊断建议\n1. 立即进行神经系统检查，包括眼底检查、视野检查和头颅影像学检查（如CT或MRI）\n2. 测量血压以排除高血压危象\n3. 进行眼科专科检查排除视神经病变\n4. 建议卧床休息，避免强光刺激\n5. 如症状加重或出现意识障碍应立即急诊就医', '2025-04-05', '推荐科室和医生（根据排班表推荐），并给出理由\n推荐科室：神经内科\n推荐医生：姜家园院区高级专家门诊的龙明智（周一上午或周四上午）或孙烈（周二上午）\n\n理由：\n1. 患者症状主要涉及神经系统和视觉系统，神经内科是最合适的首诊科室\n2. 龙明智和孙烈都是高级专家，在神经系统疾病诊治方面经验丰富\n3. 患者症状较重且复杂，需要高级专家进行系统评估\n4. 如排除神经系统问题后，可转诊至眼科专科门诊进一步检查');
INSERT INTO `medical_records` VALUES (105, '李思', 23, '男', 160, 66, '12345678910', '无', '根据患者描述\"所有地方\"疼痛的症状，可能涉及全身性疼痛综合征、纤维肌痛症、慢性疲劳综合征或心理因素导致的躯体化障碍等。由于症状描述过于模糊且缺乏具体细节，无法做出确切诊断。', '诊断建议\n1. 建议患者详细描述疼痛的性质(钝痛/刺痛/酸痛等)、程度、持续时间、加重或缓解因素\n2. 完善病史采集，包括：\n   * 疼痛起始时间和演变过程\n   * 伴随症状(发热、乏力、睡眠障碍等)\n   * 近期生活压力事件\n   * 既往就医情况和用药史\n3. 建议进行基础检查：\n   * 全血细胞计数\n   * 炎症指标(CRP、ESR)\n   * 甲状腺功能检查\n   * 维生素D水平检测\n4. 考虑心理评估量表筛查', '2025-04-06', '推荐科室和医生（根据排班表推荐），并给出理由\n推荐科室：神经内科或疼痛科\n推荐医生：\n1. 姜家园院区专家门诊 * 胡文志(周三上午)\n   * 理由：擅长神经系统疾病诊治，可排查中枢性疼痛\n2. 姜家园院区专科门诊1 * 蒯琳(周一全天/周三下午/周五全天)\n   * 理由：专科门诊可系统评估慢性疼痛\n3. 迈皋桥院区专家门诊 * 周海波(周三上午)\n   * 理由：经验丰富的神经内科专家\n\n优先建议：周三上午就诊胡文志医生，因其在神经系统症状鉴别方面具有丰富经验，且时间最近。若症状持续，可考虑蒯琳医生的慢性疼痛专科门诊。');

SET FOREIGN_KEY_CHECKS = 1;
