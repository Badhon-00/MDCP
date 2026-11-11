import {queryChannelAnalytics} from "./analytics.js";
import {createThumbnail,downloadOwnedMedia} from "./media.js";

export const YOUTUBE_TOOL_SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    operation: {type:"string",enum:["search","video_stats","channel_overview","analytics","upload","playlist_add","thumbnail","download_owned"]},
    query: {type:"string",description:"Search phrase"},
    maxResults: {type:"integer",minimum:1,maximum:50},
    ids: {type:"array",items:{type:"string"},maxItems:50},
    channelId: {type:"string"},
    startDate: {type:"string",pattern:"^\\d{4}-\\d{2}-\\d{2}$"},
    endDate: {type:"string",pattern:"^\\d{4}-\\d{2}-\\d{2}$"},
    metrics: {type:"string"},
    dimensions: {type:"string"},
    filePath: {type:"string"},
    title: {type:"string"},
    description: {type:"string"},
    tags: {type:"array",items:{type:"string"},maxItems:500},
    privacyStatus: {type:"string",enum:["private","unlisted","public"]},
    playlistId: {type:"string"},
    videoId: {type:"string"},
    input: {type:"string"},
    text: {type:"string"},
    output: {type:"string"},
    url: {type:"string"},
    approved: {type:"boolean"},
    rightsAttested: {type:"boolean"}
  },
  required:["operation"]
};

const requireApproval = (args, action) => {
  if (args.approved !== true) throw new Error(`Explicit approval is required for ${action}. Set approved=true only after the user confirms.`);
};

export async function executeYouTubeOperation({client,fetchImpl=fetch}, args={}) {
  if (!client?.request) throw new Error("Configured YouTube client is required");
  switch(args.operation) {
    case "search": {
      if(!args.query?.trim()) throw new Error("query is required");
      const r=await client.request("search",{params:{part:"snippet",q:args.query,type:"video",maxResults:Math.min(50,Math.max(1,args.maxResults||10))},quotaCost:100});
      return r.items??[];
    }
    case "video_stats": {
      if(!Array.isArray(args.ids)||!args.ids.length) throw new Error("ids is required");
      const r=await client.request("videos",{params:{part:"snippet,statistics,contentDetails",id:args.ids.slice(0,50).join(",")},quotaCost:1});
      return r.items??[];
    }
    case "channel_overview": {
      const params={part:"snippet,statistics,contentDetails",...(args.channelId?{id:args.channelId}:{mine:true})};
      const r=await client.request("channels",{auth:!args.channelId,params,quotaCost:1});
      return r.items??[];
    }
    case "analytics": {
      const accessToken=await client.accessToken();
      return queryChannelAnalytics({accessToken,startDate:args.startDate,endDate:args.endDate,metrics:args.metrics,dimensions:args.dimensions,fetchImpl});
    }
    case "upload": {
      requireApproval(args,"video upload");
      if(!args.filePath||!args.title) throw new Error("filePath and title are required");
      return client.uploadVideo({filePath:args.filePath,title:args.title,description:args.description||"",tags:args.tags||[],privacyStatus:args.privacyStatus||"private"});
    }
    case "playlist_add": {
      requireApproval(args,"playlist mutation");
      if(!args.playlistId||!args.videoId) throw new Error("playlistId and videoId are required");
      return client.request("playlistItems",{method:"POST",auth:true,quotaCost:50,params:{part:"snippet"},body:{snippet:{playlistId:args.playlistId,resourceId:{kind:"youtube#video",videoId:args.videoId}}}});
    }
    case "thumbnail":
      return createThumbnail({input:args.input,text:args.text,output:args.output||"thumbnail.jpg"});
    case "download_owned":
      if(args.rightsAttested!==true) throw new Error("Confirm that you own or are licensed to download this media (rightsAttested=true).");
      return downloadOwnedMedia(args.url);
    default: throw new Error("Unsupported YouTube operation");
  }
}

export function createYouTubeTool(dependencies) {
  return {
    name:"youtube",
    description:"YouTube creator operations: search, channel/video metrics, authorized analytics, thumbnail, licensed media, upload and playlist. Use one operation per call; mutations require approval.",
    inputSchema:YOUTUBE_TOOL_SCHEMA,
    async handler(args) {
      const result=await executeYouTubeOperation(dependencies,args);
      return {content:[{type:"text",text:JSON.stringify(result)}],structuredContent:{result}};
    }
  };
}

// MCP SDK v2-compatible registration; also usable by thin host adapters.
export function registerYouTubeTool(server, dependencies) {
  const tool=createYouTubeTool(dependencies);
  if(typeof server?.registerTool!=="function") throw new Error("MCP server must expose registerTool(name, config, handler)");
  server.registerTool(tool.name,{description:tool.description,inputSchema:tool.inputSchema},tool.handler);
  return tool.name;
}
