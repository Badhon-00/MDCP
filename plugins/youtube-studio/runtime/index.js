export {createYouTubeClient} from "./youtube-client.js";
export {queryChannelAnalytics} from "./analytics.js";
export {createThumbnail,downloadOwnedMedia} from "./media.js";
export {YOUTUBE_TOOL_SCHEMA,executeYouTubeOperation,createYouTubeTool,registerYouTubeTool} from "./agent-tool.js";

export async function searchVideos(client, query, maxResults=10) {
  if(!client?.request || !query?.trim()) throw new Error("client and search query are required");
  const result=await client.request("search",{params:{part:"snippet",q:query,type:"video",maxResults:Math.min(50,Math.max(1,Number(maxResults)||10))},quotaCost:100});
  return result.items??[];
}
export async function getVideoStats(client, ids) {
  if(!client?.request || !Array.isArray(ids) || ids.length===0) throw new Error("client and video IDs are required");
  const result=await client.request("videos",{params:{part:"snippet,statistics,contentDetails",id:ids.slice(0,50).join(",")},quotaCost:1});
  return result.items??[];
}
export async function addToPlaylist(client, playlistId, videoId) {
  if(!client?.request || !playlistId || !videoId) throw new Error("client, playlistId and videoId are required");
  return client.request("playlistItems",{method:"POST",auth:true,quotaCost:50,params:{part:"snippet"},body:{snippet:{playlistId,resourceId:{kind:"youtube#video",videoId}}}});
}
export async function uploadVideo(client, options) {
  if(!client?.uploadVideo) throw new Error("YouTube client is required");
  return client.uploadVideo(options);
}
