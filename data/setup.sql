INSERT INTO carduser (userId, idNumber, userName, gender) VALUES (1364250, 'hzc0', 'hzc_user0', 0), (1364251, 'hzc1', 'hzc_user1', 0), (1364252, 'hzc2', 'hzc_user2', 0);
INSERT INTO cardinfo (cardNumber, cardstatus, userId, cardBalance) VALUES ('hzc_card0', 0, null, 0), ('hzc_card0_2', 0, null, 0), ('hzc_card1', 5010, 1364251, 0), ('hzc_card2', 5010, 1364252, 0), ('hzc_card3', 5010, 1364252, 500), ('hzc_card_black', 5011, null, 0), ('hzc_card_off', 5012, null, 0), ('hzc_card_unit', 5021, null, 0);
INSERT INTO consumptiondetails (cardNumber, cardBalance, createTime) VALUES ('hzc_card3', '50', '2019-06-22 18:08:28'), ('hzc_card3', '100', '2019-06-24 21:08:28');
INSERT INTO rechargedetails (cardNumber, cardBalance, createTime) VALUES ('hzc_card3', '50', '2019-06-25 18:08:28');
