DELETE FROM carduser WHERE userName in ('hzc_user0', 'hzc_user0_2', 'hzc_user1', 'hzc_user2', 'hzc_user_nx');
DELETE FROM carduser WHERE userId=10000000;
DELETE FROM cardinfo WHERE cardNumber in('1376525', 'abc', 'Abc#123', '', 'hzc_card0', 'hzc_card0_2', 'hzc_card1', 'hzc_card2', 'hzc_card3', 'hzc_card_black', 'hzc_card_off', 'hzc_card_unit', 'hzc_card_nx');
DELETE FROM consumptiondetails WHERE cardNumber='hzc_card3';
DELETE FROM rechargedetails WHERE cardNumber='hzc_card3';
