#!  /usr/bin/env python
#ecoding=utf-8
import pandas
import csv
import re
import numpy as np


zb_pairs="zbqc_ticker,zbusdt_ticker,zbbtc_ticker,btcqc_ticker,btcusdt_ticker,bccusdt_ticker,ubtcusdt_ticker,lt"+\
"cusdt_ticker,ethusdt_ticker,etcusdt_ticker,btsusdt_ticker,eosusdt_ticker,qtumusdt_ticker,hsrusdt_tic"+\
"ker,xrpusdt_ticker,bcdusdt_ticker,dashusdt_ticker,bccqc_ticker,ubtcqc_ticker,ltcqc_ticker,ethqc_tick"+\
"er,etcqc_ticker,btsqc_ticker,eosqc_ticker,qtumqc_ticker,hsrqc_ticker,xrpqc_ticker,bcdqc_ticker,dashq"+\
"c_ticker,bccbtc_ticker,ubtcbtc_ticker,ltcbtc_ticker,ethbtc_ticker,etcbtc_ticker,btsbtc_ticker,eosbtc"+\
"_ticker,qtumbtc_ticker,hsrbtc_ticker,xrpbtc_ticker,bcdbtc_ticker,dashbtc_ticker,sbtcusdt_ticker,sbtc"+\
"qc_ticker,sbtcbtc_ticker,inkusdt_ticker,inkqc_ticker,inkbtc_ticker,tvusdt_ticker,tvqc_ticker,tvbtc_t"+\
"icker,bcxusdt_ticker,bcxqc_ticker,bcxbtc_ticker,bthusdt_ticker,bthqc_ticker,bthbtc_ticker,lbtcusdt_t"+\
"icker,lbtcqc_ticker,lbtcbtc_ticker,chatusdt_ticker,chatqc_ticker,chatbtc_ticker,hlcusdt_ticker,hlcqc"+\
"_ticker,hlcbtc_ticker,bcwusdt_ticker,bcwqc_ticker,bcwbtc_ticker,btpusdt_ticker,btpqc_ticker,btpbtc_t"+\
"icker,bitcnyqc_ticker,topcusdt_ticker,topcqc_ticker,topcbtc_ticker,entusdt_ticker,entqc_ticker,entbt"+\
"c_ticker,batusdt_ticker,batqc_ticker,batbtc_ticker,1stusdt_ticker,1stqc_ticker,1stbtc_ticker,safeusd"+\
"t_ticker,safeqc_ticker,safebtc_ticker,qunusdt_ticker,qunqc_ticker,qunbtc_ticker,btnusdt_ticker,btnqc"+\
"_ticker,btnbtc_ticker,trueusdt_ticker,trueqc_ticker,truebtc_ticker,cdcusdt_ticker,cdcqc_ticker,cdcbt"+\
"c_ticker,ddmusdt_ticker,ddmqc_ticker,ddmbtc_ticker,bitebtc_ticker,hotcusdt_ticker,hotcqc_ticker,hotc"+\
"btc_ticker,usdtqc_ticker,xucqc_ticker,xucbtc_ticker,epcqc_ticker,epcbtc_ticker,bdsqc_ticker,bdsbtc_t"+\
"icker,gramqc_ticker,gramusdt_ticker,grambtc_ticker,dogeqc_ticker,dogeusdt_ticker,dogebtc_ticker"

zb_pairs2=["bcc_btc","bcc_qc","bcc_usdt","bcd_btc","bcd_qc","bcd_usdt","bcw_btc","bcw_qc","bcw_usdt","bcx_btc","bcx_qc","bcx_usdt","bitcny_qc","btc_qc","btc_usdt","bth_btc","bth_qc","bth_usdt","btp_btc","btp_qc","btp_usdt","bts_btc","bts_qc","bts_usdt","chat_btc","chat_qc","chat_usdt","dash_btc","dash_qc","dash_usdt","eos_btc","eos_qc","eos_usdt","etc_btc","etc_qc","etc_usdt","eth_btc","eth_qc","eth_usdt","hlc_btc","hlc_qc","hlc_usdt","hsr_btc","hsr_qc","hsr_usdt","ink_btc","ink_qc","ink_usdt","lbtc_btc","lbtc_qc","lbtc_usdt","ltc_btc","ltc_qc","ltc_usdt","qtum_btc","qtum_qc","qtum_usdt","sbtc_btc","sbtc_qc","sbtc_usdt","topc_usdt","tv_btc","tv_qc","tv_usdt","ubtc_btc","ubtc_qc","ubtc_usdt","xrp_btc","xrp_qc","xrp_usdt","zb_btc","zb_qc","zb_usdt"]



bitstamp_pairs="btcusd,btceur,eurusd,xrpusd,xrpeur,xrpbtc,ltcusd,ltceur,ltcbtc,ethusd,etheur,ethbtc,bchusd,bcheur,bchbtc"

gitio_pairs=["eth_btc","etc_btc","etc_eth","zec_btc","dash_btc","ltc_btc","bcc_btc","qtum_btc",
"qtum_eth","xrp_btc","zrx_btc","zrx_eth","dnt_eth","dpy_eth","oax_eth","lrc_eth",
"lrc_btc","pst_eth","tnt_eth","snt_eth","snt_btc","omg_eth","omg_btc","pay_eth",
"pay_btc","bat_eth","cvc_eth","storj_eth","storj_btc","eos_eth","eos_btc"]


#币种
coinstr="btc,ltc,eth,doge,ont,eos,btm,ae,iht,gem,trx,ocn,bcdn,ada,lrc,tsl,kick,neo,etc,xrp,gtc"
coinstr=coinstr+",usdt,qc"#zb新加
coinstr=coinstr+",usd,bch"#bitstamp新加

coins=coinstr.split(",")
zb_pairs=zb_pairs.split(",")
bitstamp_pairs=bitstamp_pairs.split(",")


giteio=["btc_usdt","bch_usdt","eth_usdt","etc_usdt","qtum_usdt","ltc_usdt","dash_usdt","zec_usdt","btm_usdt","eos_usdt","req_usdt","snt_usdt","omg_usdt","pay_usdt","cvc_usdt","zrx_usdt","tnt_usdt","xmr_usdt","xrp_usdt","doge_usdt","bat_usdt","pst_usdt","btg_usdt","dpy_usdt","lrc_usdt","storj_usdt","rdn_usdt","stx_usdt","knc_usdt","link_usdt","cdt_usdt","ae_usdt","ae_eth","ae_btc","cdt_eth","rdn_eth","stx_eth","knc_eth","link_eth","req_eth","rcn_eth","trx_eth","arn_eth","kick_eth","bnt_eth","ven_eth","mco_eth","fun_eth","data_eth","rlc_eth","zsc_eth","wings_eth","ctr_eth","mda_eth","rcn_usdt","trx_usdt","kick_usdt","ven_usdt","mco_usdt","fun_usdt","data_usdt","zsc_usdt","mda_usdt","xtz_usdt","gnt_usdt","gnt_eth","gem_usdt","gem_eth","rfr_usdt","rfr_eth","dadi_usdt","dadi_eth","abt_usdt","abt_eth","ledu_usdt","ledu_btc","ledu_eth","ost_usdt","ost_eth","xlm_usdt","xlm_eth","xlm_btc","mobi_usdt","mobi_eth","mobi_btc","ocn_usdt","ocn_eth","ocn_btc","zpt_usdt","zpt_eth","zpt_btc","cofi_usdt","cofi_eth","jnt_usdt","jnt_eth","jnt_btc","blz_usdt","blz_eth","gxs_usdt","gxs_btc","mtn_usdt","mtn_eth","ruff_usdt","ruff_eth","ruff_btc","tnc_usdt","tnc_eth","tnc_btc","zil_usdt","zil_eth","tio_usdt","tio_eth","bto_usdt","bto_eth","theta_usdt","theta_eth","ddd_usdt","ddd_eth","ddd_btc","mkr_usdt","mkr_eth","dai_usdt","smt_usdt","smt_eth","mdt_usdt","mdt_eth","mdt_btc","mana_usdt","mana_eth","lun_usdt","lun_eth","salt_usdt","salt_eth","fuel_usdt","fuel_eth","elf_usdt","elf_eth","drgn_usdt","drgn_eth","gtc_usdt","gtc_eth","gtc_btc","qlc_usdt","qlc_btc","qlc_eth","dbc_usdt","dbc_btc","dbc_eth","bnty_usdt","bnty_eth","lend_usdt","lend_eth","icx_usdt","icx_eth","btf_usdt","btf_btc","ada_usdt","ada_btc","lsk_usdt","lsk_btc","waves_usdt","waves_btc","bifi_usdt","bifi_btc","mds_eth","mds_usdt","dgd_usdt","dgd_eth","qash_usdt","qash_eth","qash_btc","powr_usdt","powr_eth","powr_btc","fil_usdt","bcd_usdt","bcd_btc","sbtc_usdt","sbtc_btc","god_usdt","god_btc","bcx_usdt","bcx_btc","hsr_usdt","hsr_btc","hsr_eth","qsp_usdt","qsp_eth","ink_btc","ink_usdt","ink_eth","ink_qtum","med_qtum","med_eth","med_usdt","bot_qtum","bot_usdt","bot_eth","qbt_qtum","qbt_eth","qbt_usdt","tsl_qtum","tsl_usdt","gnx_usdt","gnx_eth","neo_usdt","gas_usdt","neo_btc","gas_btc","iota_usdt","iota_btc","nas_usdt","nas_eth","nas_btc","eth_btc","etc_btc","etc_eth","zec_btc","dash_btc","ltc_btc","bch_btc","btg_btc","qtum_btc","qtum_eth","xrp_btc","doge_btc","xmr_btc","zrx_btc","zrx_eth","dnt_eth","dpy_eth","oax_eth","rep_eth","lrc_eth","lrc_btc","pst_eth","bcdn_eth","bcdn_usdt","tnt_eth","snt_eth","snt_btc","btm_eth","btm_btc","llt_eth","snet_eth","snet_usdt","llt_snet","omg_eth","omg_btc","pay_eth","pay_btc","bat_eth","bat_btc","cvc_eth","storj_eth","storj_btc","eos_eth","eos_btc","bts_usdt","bts_btc","tips_eth","xmc_usdt","xmc_btc","cs_eth","cs_usdt","man_eth","man_usdt","rem_eth","lym_eth","lym_usdt","instar_eth","ont_eth","ont_usdt","bft_eth","bft_usdt","iht_eth","iht_usdt","senc_eth","senc_usdt","tomo_eth","elec_eth","ship_eth","tfd_eth","hav_eth","hur_eth","lst_eth","swh_eth","swh_usdt","dock_usdt","dock_eth"]
# results=[]
# for pair in giteio:
#     rel_pair=pair.split("_")
#     results.append([rel_pair[0]+rel_pair[1],pair])

# results=[]
# for pair in zb_pairs:
#     rel_pair=pair.split("_")[0]
#     my_pair="";
#     for coin in coins:
#         coin=coin.lower();
#         regex1="^"+coin+"(\w{1,})"
#         regex2="(\w{1,})"+coin+"$"
#         ptn1=re.compile(regex1,re.S);
#         res1=re.findall(ptn1,rel_pair);
#         ptn2=re.compile(regex2,re.S);
#         res2=re.findall(ptn2,rel_pair);
#         if len(res1)>0 or len(res2)>0:
#             if len(res1)>0:
#                 my_pair=coin+"_"+res1[0]
#                 break
#             elif len(res2)>0:
#                 my_pair=res2[0]+"_"+coin
#                 break
#             continue;
#         else:
#             continue
#
#
#     results.append([rel_pair,my_pair])

results=[]
for pair in zb_pairs2:
    rel_pair=pair.split("_")
    results.append([rel_pair[0]+rel_pair[1],pair])

# results=[]
# for pair in bitstamp_pairs:
#     my_pair="";
#     for coin in coins:
#         coin=coin.lower();
#         regex1="^"+coin+"(\w{1,})"
#         regex2="(\w{1,})"+coin+"$"
#         ptn1=re.compile(regex1,re.S);
#         res1=re.findall(ptn1,pair);
#         ptn2=re.compile(regex2,re.S);
#         res2=re.findall(ptn2,pair);
#         if len(res1)>0 or len(res2)>0:
#             if len(res1)>0:
#                 my_pair=coin+"_"+res1[0]
#                 break
#             elif len(res2)>0:
#                 my_pair=res2[0]+"_"+coin
#                 break
#             continue;
#         else:
#             continue
#
#
#     results.append([pair,my_pair])

#save to excel
# data=pandas.DataFrame(results)
# writer=pandas.ExcelWriter('Result.xlsx')
# data.to_excel(writer)
# writer.save()
with open('Result.csv', 'w',encoding='utf_8_sig',newline='') as f:
    writer = csv.writer(f,dialect='excel')
    writer.writerows(results)
    # writer.writerows(np.reshape(gitio_pairs,(-1,1)))