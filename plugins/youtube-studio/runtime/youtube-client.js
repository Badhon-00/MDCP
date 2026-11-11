import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
const API="https://www.googleapis.com/youtube/v3";
const COST={search:100,videos:1,channels:1,playlists:1,playlistItems:50,videosInsert:1600};

export function createYouTubeClient({env=process.env,fetchImpl=fetch,quotaLedger,now=()=>Date.now(),maxRetries=3}={}) {
  let cachedToken;
  let localUsed=0;
  const limit=Number(env.YT_DAILY_QUOTA||10000);
  async function consume(units,operation) {
    if(quotaLedger?.consume) return quotaLedger.consume(units,operation);
    if(localUsed+units>limit) throw new Error("YouTube quota budget exceeded; configure durable quotaLedger for cloud deployments");
    localUsed+=units;
  }
  async function accessToken() {
    if(cachedToken&&cachedToken.expiresAt>now()+60000) return cachedToken.value;
    for(const key of ["YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN"]) if(!env[key]) throw new Error(`Missing required secret: ${key}`);
    const r=await fetchImpl("https://oauth2.googleapis.com/token",{method:"POST",headers:{"content-type":"application/x-www-form-urlencoded"},body:new URLSearchParams({client_id:env.YOUTUBE_CLIENT_ID,client_secret:env.YOUTUBE_CLIENT_SECRET,refresh_token:env.YOUTUBE_REFRESH_TOKEN,grant_type:"refresh_token"})});
    if(!r.ok) throw new Error(`OAuth refresh failed (${r.status}): ${await r.text()}`);
    const j=await r.json(); cachedToken={value:j.access_token,expiresAt:now()+Number(j.expires_in||3600)*1000}; return cachedToken.value;
  }
  async function request(endpoint,{params={},method="GET",body,auth=false,quotaCost=COST[endpoint]??1}={}) {
    await consume(quotaCost,endpoint);
    const url=new URL(`${API}/${endpoint}`);
    for(const [k,v] of Object.entries(params)) if(v!==undefined&&v!==null) url.searchParams.set(k,String(v));
    const headers={};
    if(auth) headers.Authorization=`Bearer ${await accessToken()}`;
    else {if(!env.YOUTUBE_API_KEY) throw new Error("Missing YOUTUBE_API_KEY");url.searchParams.set("key",env.YOUTUBE_API_KEY);}
    if(body!==undefined) headers["content-type"]="application/json";
    let r;
    for(let attempt=0;attempt<=maxRetries;attempt++){
      r=await fetchImpl(url,{method,headers,...(body!==undefined?{body:JSON.stringify(body)}:{})});
      if(r.ok||![429,500,502,503,504].includes(r.status)||attempt===maxRetries) break;
      await new Promise(resolve=>setTimeout(resolve,Math.min(8000,300*2**attempt)));
    }
    if(!r.ok) throw new Error(`YouTube API ${endpoint} failed (${r.status}): ${await r.text()}`);
    return r.status===204?null:r.json();
  }
  async function uploadVideo({filePath,title,description="",tags=[],privacyStatus="private",categoryId="22",madeForKids=false}) {
    if(!["private","unlisted","public"].includes(privacyStatus)) throw new Error("Invalid privacyStatus");
    if(!title?.trim()) throw new Error("Video title is required");
    const file=await stat(filePath); if(!file.isFile()||file.size===0) throw new Error("Video file is empty or invalid");
    await consume(COST.videosInsert,"videos.insert");
    const init=await fetchImpl(`${API}/videos?uploadType=resumable&part=snippet,status`,{method:"POST",headers:{Authorization:`Bearer ${await accessToken()}`,"content-type":"application/json","x-upload-content-length":String(file.size),"x-upload-content-type":"video/*"},body:JSON.stringify({snippet:{title:title.trim(),description,tags,categoryId},status:{privacyStatus,selfDeclaredMadeForKids:Boolean(madeForKids)}})});
    if(!init.ok) throw new Error(`Upload init failed (${init.status}): ${await init.text()}`);
    const location=init.headers.get("location"); if(!location||new URL(location).protocol!=="https:") throw new Error("Invalid resumable upload URL");
    const result=await fetchImpl(location,{method:"PUT",headers:{"content-length":String(file.size),"content-type":"video/*"},body:createReadStream(filePath),duplex:"half"});
    if(!result.ok) throw new Error(`Upload failed (${result.status}): ${await result.text()}`);
    return result.json();
  }
  return Object.freeze({request,accessToken,uploadVideo,getLocalQuotaUsed:()=>localUsed});
}
