
import requests

def get_cetus_bounties():
    try:
        ws=requests.get("https://api.warframestat.us/pc/worldstate").json()
        node=ws.get("OstronCetusNode", {})
        jobs=[]
        for job in node.get("jobs", []):
            entry={
                "type":job.get("type","Unknown"),
                "levels":f"{job.get('minEnemyLevel')} - {job.get('maxEnemyLevel')}",
                "stages":job.get("stages",[]),
                "rewards":[]
            }
            rewards=job.get("rewardTable",{})
            for s,items in rewards.items():
                for it in items:
                    entry["rewards"].append(it.get("itemName","Unknown"))
            jobs.append(entry)
        return jobs
    except:
        return []
