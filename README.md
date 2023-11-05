# YokuhannRibuArea
#上反角対応リブ書きプログラムについての取り扱い

#プランク端について（生データでは、ずれがある）
　修正手順
　1.PlankUのスプライン補間を1つ前の状態にする
　2.RibCap_Uのスプライン補完の最前縁を直線でつなぐ
　ただし、プランク厚みの出力値がプログラム設定値よりも小さくでる
#後縁材の辺について
　設定値を実際のリブよりも大きく設定する必要性がある
後縁材の最前縁の辺の長さの設定値はあくまでも翼型出力に対するものであって、リブに対するものではない

#前縁材の出力について
　基本的には、use_lをプログラム設定値として出力すれば可能
　一部の翼型に対して、エラーが起こることが確認されている
　エラーが出た場合には、
　　PlankPs_U　を　print()関数を用いてターミナルへ表示
　　use_lsのif文のスコープ内でPlankPs＿Uへ再度データ加工したものをPlankPs＿Uへ再度割り当て（最初の数点を除く）
　 use_la ブロック内で最後に。palnkpsuを加工前データに再度割り当てを行う

<データ処理例>
加工前
[vector(296.6761556221747, 4.17233936809196), vector(289.4872266396978, 3.665738366043222), vector(282.35121952900806, 3.1581287873727697), vector(275.26987977486573, 2.6523885568842145), vector(268.24426902932356, 2.148350780856416), vector(261.2760213843865, 1.6452917845000377), vector(254.3672118101302, 1.1425665962868892), vector(247.5201775072675, 0.6412287430823325), vector(240.73644294142355, 0.1436216788026199), vector(2.8000000000000003, 0.0), vector(3.011967021563573, 1.0937655053306126), vector(3.317676264206333, 2.9145781362978895), vector(3.738476787930445, 5.197784360871181), vector(4.248304896568959, 7.445076456533703), vector(4.837234568624714, 9.055044091544758), vector(5.580797178278644, 10.712418541430967), vector(6.449621539053343, 12.459411862721375), vector(7.400721908658877, 14.11318614494653), vector(8.489757888724235, 15.66020773656323), vector(9.771925501218144, 17.397845190648344), vector(11.17931580261017, 19.29924443379305), vector(12.672179309018563, 21.238244901679757), vector(14.243818730229965, 23.102248373786722), vector(15.960466271692844, 24.889555223547514), vector(17.846417138935063, 26.802430496345295), vector(19.844572061996033, 28.7765402659183), vector(21.942649325944572, 30.761929296684606), vector(24.138882067093565, 32.70946291015828), vector(26.471809778876732, 34.61409116120548), vector(28.95357417890238, 36.583407993016664), vector(31.54978556034494, 38.5937043799848), vector(34.250900930556995, 40.61384998478757), vector(37.053518901946006, 42.61329479097554), vector(39.97527550788813, 44.57101042391767), vector(43.03428321523375, 46.53871016192605), vector(46.21415767701406, 48.54051346646764), vector(49.499552725133526, 50.550378407996675), vector(52.88836946936908, 52.54850794730506), vector(56.38338765046398, 54.515244927898195), vector(60.00224129439769, 56.45515409266676), vector(63.74329278333529, 58.41582426445639), vector(67.58907245663414, 60.38105724523673), vector(71.53644844581854, 62.33535246116452), vector(75.5844405129482, 64.26270070960194), vector(79.74424718905605, 66.15398244131437), vector(84.01970679169334, 68.04322152496968), vector(88.39867110332646, 69.93058422920522), vector(92.87566306166677, 71.80267404036617), vector(97.44923404931144, 73.6468372369936), vector(102.12598758814816, 75.45292451872832), vector(106.91011709136187, 77.24203780855824), vector(111.79341306355272, 79.02090619932868), vector(116.76999248980354, 80.77837753734451), vector(121.8384965178994, 82.5043003687399), vector(127.00379943620574, 84.19050929660631), vector(132.26806701796585, 85.85414438922487), vector(137.62422884484795, 87.49845217275572), vector(143.06772949280085, 89.11397516273138), vector(148.5977001663208, 90.69187534638453), vector(154.21849363856893, 92.22723372644506), vector(159.92974579182606, 93.73686014191719), vector(165.72469877984096, 95.21788311066187), vector(171.60056310482602, 96.66272503837128), vector(177.557928801978, 98.06426447112946), vector(183.59939900116507, 99.42553592491682), vector(189.72170030982264, 100.75759103028605), vector(195.9194751805637, 102.05383769343105), vector(202.19139578528845, 103.30795773109173), vector(208.53947679682926, 104.51583565308755), vector(214.96283207344376, 105.68829817941956), vector(221.45648802695217, 106.82352560263426), vector(228.0179505356322, 107.91601184582633), vector(234.64770298114786, 108.96064323397619), vector(241.34571588581096, 109.96267317754071), vector(248.10840034524662, 110.92451233163081), vector(254.9326341009505, 111.8416634723334), vector(261.81783530828426, 112.70987840391255), vector(268.7639468478718, 113.53068840283753), vector(275.76826496627507, 114.30806775210787), vector(282.82753530948406, 115.0384258552802), vector(289.9406919593884, 115.71831918845824), vector(297.1072891236256, 116.34803683359426), vector(304.3249087778342, 116.93095393647197), vector(311.5904789061216, 117.46401006996129), vector(318.9027533021198, 117.94413150840565), vector(326.2610362482355, 118.37143168073312), vector(333.6630601420532, 118.74879632231715), vector(341.10600103271514, 119.07406309512326), vector(348.5885373577198, 119.34506029960869), vector(356.1095125985049, 119.56261430481864), vector(363.6665013584387, 119.72841742351541), vector(371.2569153004708, 119.84041471540218), vector(378.87940026259, 119.89659668802021), vector(386.53253192418305, 119.89791449812816), vector(394.2139838273642, 119.84504124331923), vector(401.921507354957, 119.73674535574702), vector(409.65357504628315, 119.57194832899678), vector(417.4084168190952, 119.35166655354585), vector(425.18375543370985, 119.07580678836315), vector(432.97753549845976, 118.74358295056538), vector(440.7879541417382, 118.35432123989322), vector(448.6132281236495, 117.90808865839759), vector(456.45144313170175, 117.40522327659177), vector(464.30047535249713, 116.84611445389763), vector(472.1580184651762, 116.23027046220108), vector(480.0222554861899, 115.55616978122819), vector(487.89155661138057, 114.82414983585416), vector(495.7635791151767, 114.03470539947065), vector(503.63611805678914, 113.18615000674896), vector(511.50763009663876, 112.27759353548427), vector(519.3764173962775, 111.30977363020168), vector(527.2403889420357, 110.28347103556716), vector(535.097470639524, 109.19882490017395), vector(542.9457283952275, 108.0560397247885), vector(550.7833632990242, 106.85545273985599), vector(558.6087783857375, 105.598221167417), vector(566.4197673534417, 104.28691895401226), vector(574.2138817584721, 102.92146723663174), vector(581.9896327775406, 101.5014986856271), vector(589.74568829093, 100.0294738629822), vector(597.479539697315, 98.50885272074581), vector(605.1885710864432, 96.93908839264446)]
加工後
[vector(2.8000000000000003, 0.0), vector(3.011967021563573, 1.0937655053306126), vector(3.317676264206333, 2.9145781362978895), vector(3.738476787930445, 5.197784360871181), vector(4.248304896568959, 7.445076456533703), vector(4.837234568624714, 9.055044091544758), vector(5.580797178278644, 10.712418541430967), vector(6.449621539053343, 12.459411862721375), vector(7.400721908658877, 14.11318614494653), vector(8.489757888724235, 15.66020773656323), vector(9.771925501218144, 17.397845190648344), vector(11.17931580261017, 19.29924443379305), vector(12.672179309018563, 21.238244901679757), vector(14.243818730229965, 23.102248373786722), vector(15.960466271692844, 24.889555223547514), vector(17.846417138935063, 26.802430496345295), vector(19.844572061996033, 28.7765402659183), vector(21.942649325944572, 30.761929296684606), vector(24.138882067093565, 32.70946291015828), vector(26.471809778876732, 34.61409116120548), vector(28.95357417890238, 36.583407993016664), vector(31.54978556034494, 38.5937043799848), vector(34.250900930556995, 40.61384998478757), vector(37.053518901946006, 42.61329479097554), vector(39.97527550788813, 44.57101042391767), vector(43.03428321523375, 46.53871016192605), vector(46.21415767701406, 48.54051346646764), vector(49.499552725133526, 50.550378407996675), vector(52.88836946936908, 52.54850794730506), vector(56.38338765046398, 54.515244927898195), vector(60.00224129439769, 56.45515409266676), vector(63.74329278333529, 58.41582426445639), vector(67.58907245663414, 60.38105724523673), vector(71.53644844581854, 62.33535246116452), vector(75.5844405129482, 64.26270070960194), vector(79.74424718905605, 66.15398244131437), vector(84.01970679169334, 68.04322152496968), vector(88.39867110332646, 69.93058422920522), vector(92.87566306166677, 71.80267404036617), vector(97.44923404931144, 73.6468372369936), vector(102.12598758814816, 75.45292451872832), vector(106.91011709136187, 77.24203780855824), vector(111.79341306355272, 79.02090619932868), vector(116.76999248980354, 80.77837753734451), vector(121.8384965178994, 82.5043003687399), vector(127.00379943620574, 84.19050929660631), vector(132.26806701796585, 85.85414438922487), vector(137.62422884484795, 87.49845217275572), vector(143.06772949280085, 89.11397516273138), vector(148.5977001663208, 90.69187534638453), vector(154.21849363856893, 92.22723372644506), vector(159.92974579182606, 93.73686014191719), vector(165.72469877984096, 95.21788311066187), vector(171.60056310482602, 96.66272503837128), vector(177.557928801978, 98.06426447112946), vector(183.59939900116507, 99.42553592491682), vector(189.72170030982264, 100.75759103028605), vector(195.9194751805637, 102.05383769343105), vector(202.19139578528845, 103.30795773109173), vector(208.53947679682926, 104.51583565308755), vector(214.96283207344376, 105.68829817941956), vector(221.45648802695217, 106.82352560263426), vector(228.0179505356322, 107.91601184582633), vector(234.64770298114786, 108.96064323397619), vector(241.34571588581096, 109.96267317754071), vector(248.10840034524662, 110.92451233163081), vector(254.9326341009505, 111.8416634723334), vector(261.81783530828426, 112.70987840391255), vector(268.7639468478718, 113.53068840283753), vector(275.76826496627507, 114.30806775210787), vector(282.82753530948406, 115.0384258552802), vector(289.9406919593884, 115.71831918845824), vector(297.1072891236256, 116.34803683359426), vector(304.3249087778342, 116.93095393647197), vector(311.5904789061216, 117.46401006996129), vector(318.9027533021198, 117.94413150840565), vector(326.2610362482355, 118.37143168073312), vector(333.6630601420532, 118.74879632231715), vector(341.10600103271514, 119.07406309512326), vector(348.5885373577198, 119.34506029960869), vector(356.1095125985049, 119.56261430481864), vector(363.6665013584387, 119.72841742351541), vector(371.2569153004708, 119.84041471540218), vector(378.87940026259, 119.89659668802021), vector(386.53253192418305, 119.89791449812816), vector(394.2139838273642, 119.84504124331923), vector(401.921507354957, 119.73674535574702), vector(409.65357504628315, 119.57194832899678), vector(417.4084168190952, 119.35166655354585), vector(425.18375543370985, 119.07580678836315), vector(432.97753549845976, 118.74358295056538), vector(440.7879541417382, 118.35432123989322), vector(448.6132281236495, 117.90808865839759), vector(456.45144313170175, 117.40522327659177), vector(464.30047535249713, 116.84611445389763), vector(472.1580184651762, 116.23027046220108), vector(480.0222554861899, 115.55616978122819), vector(487.89155661138057, 114.82414983585416), vector(495.7635791151767, 114.03470539947065), vector(503.63611805678914, 113.18615000674896), vector(511.50763009663876, 112.27759353548427), vector(519.3764173962775, 111.30977363020168), vector(527.2403889420357, 110.28347103556716), vector(535.097470639524, 109.19882490017395), vector(542.9457283952275, 108.0560397247885), vector(550.7833632990242, 106.85545273985599), vector(558.6087783857375, 105.598221167417), vector(566.4197673534417, 104.28691895401226), vector(574.2138817584721, 102.92146723663174), vector(581.9896327775406, 101.5014986856271), vector(589.74568829093, 100.0294738629822), vector(597.479539697315, 98.50885272074581), vector(605.1885710864432, 96.93908839264446)]

後縁材の最前縁の辺の長さの設定値はあくまでも翼型出力に対するものであって、リブに対するものではない
　

#エラー対処
x must be strictly increasing sequence
対処１
前縁材出力に問題がある可能性あり
よって、use_l == Falseで設定を行う
対処２
bunnkatusuuの部分を小さくする




