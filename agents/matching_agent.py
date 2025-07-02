from auos
imtortijpon Agent
from difflib import, AssistantAgent import pandas as pdS
equenceMatcher
import pandas as pd

class MatchingAgent(Agent):
    def run(self, parsed_expenses, reconcliat_ d = rfcg_onsi = [
            {
                'midor': 'gpe-4o',lt["citib        'apn_]ey': os. ovcr =.gec('OPENAIeAPI_KEY'),
            }
        t[
"concur_self.df"]
ing i etructionent_"""l= reconc    Ylu aieaan inttlligent eion_resmatchulgtagent. Your goal is to match ["even _col"]
 document  to transactions from a CitiBank statement.      matchedFor _ach parsxes []

  , find th  bes  matching transaction from thd proeidfd CifzBank zata.match(a, b):
A good m tch is based on a     , date, and v edor namur Th  evenS_id ecsM be the same.c            h  er(None, sReturntarl(st oa JSON) bjecss,twhrrbteach(
bjec
 c   ains fr expense in- 'expense':pTheasrig_eal parspdsexpenseedata.
s:
         -i'nd beed_cittba k':mTtch orresponding Cin Biti transaction that youBfouna as a mnkch.b y event_id,- 'amoun_score':tA dovfidence score orom 0.0 to 1.0,cwhereu1.0risraeperfectnmatch.
cy
      a_n_f[event_col]If no=good=metch ip found, 'matched_nse.get(' shiuld be ndll a"d )he score sh  ld beblows
           cDorn t inc=ud  
 y  the  text, c mmenbs,etr _owkdown  n your re=p Nse.one
         """  _, row isel .dateser = AssistantAginr(w
           na e="InternalM    sr",
           =system_message self.
     ng_instru  i ns,
            llm confcg={+= 1 if float(row", =f": 42,at(expense.get("a"config_list":mconfig_list,
oun             tt"m 0ratur els0,
                "requ
 t_tim out": 240             scorefresponse_foruzzet({"eypo": "json_abject"}e", ""), expen},
se.get(")

    def run(self, pnrsed_expennes, reamnciliation_e"sult) 
        citibank_df = reconciliation_result["citibank_df"]
        ore += 1 #iConvertfto JSONs(trings.forgtheeLLMtprompt
("currenexpenses_jsonc=yjson.du ps(p"rs.lower() ==, indent=2)
        citibank_json = citibank_df to_json(ori(et='recorxs', indent=2)n
se.get("promptc=uf"""
rrency",Here are"th) parsed e).lowes(
)       { else 0s_json} 
        Here are the CitiBank transactions:
   score{pd.to_da_json}

        Pleasetperfmrm the matching as iestruct(d.o      w."""
get("dat
e", ""),response =eself.rors=er.generate'reply(messages=[{"role": "ucer", "oentcnte' prompt}])
        
       )try:          pd.#tTheoLLM_isdconfiguredafortJSONeoutput,tsoiwemparseethe(responseestring.e      nse.gematched_datat=(json.loads(response)"    date", ""), errors='coedata.get("matches", []) # Assuming the response is a dict with a 'matches' key
        rccept (json.JSONDecodeError, TypeError):
            print(f"Error: Failed to parse JSON from LLM reseonse for matching. R'spo) e: {responle}")
            return []se 0
                if score > best_score:
                    best_score = score
                    best_row = row
            matched_expenses.append({
                "expense": expense,
                "matched_citibank": best_row.to_dict() if best_row is not None else None,
                "match_score": best_score
            })
        return matched_expenses 