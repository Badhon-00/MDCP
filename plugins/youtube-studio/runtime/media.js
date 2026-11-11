import {spawn} from "node:child_process";
import {mkdir,writeFile,rm} from "node:fs/promises";
import path from "node:path";
function run(command,args){return new Promise((resolve,reject)=>{const child=spawn(command,args,{shell:false,stdio:["ignore","pipe","pipe"]});let err="";child.stderr.setEncoding("utf8");child.stderr.on("data",s=>{err+=s.slice(-10000)});child.on("error",reject);child.on("close",code=>code===0?resolve():reject(new Error(`${command} exited ${code}: ${err}`)));});}
export async function createThumbnail({input,text,output="thumbnail.jpg",ffmpegPath="ffmpeg"}) {
  if(!input||!text?.trim()) throw new Error("input and overlay text required");
  await mkdir(path.dirname(path.resolve(output)),{recursive:true});
  const textFile=`${output}.overlay.txt`; await writeFile(textFile,text.slice(0,90),{mode:0o600});
  try {await run(ffmpegPath,["-y","-i",input,"-vf",`scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,drawtext=textfile='${textFile.replace(/\\/g,"/")}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=h-text_h-80:box=1:boxcolor=black@0.55:boxborderw=18`,"-frames:v","1",output]);}
  finally {await rm(textFile,{force:true});}
  return output;
}
export async function downloadOwnedMedia(url,{outputDir="media",ytDlpPath="yt-dlp"}={}) {
  const u=new URL(url),host=u.hostname.toLowerCase();
  if(u.protocol!=="https:"||!(host==="youtube.com"||host.endsWith(".youtube.com")||host==="youtu.be"||host==="www.youtube-nocookie.com")) throw new Error("Only HTTPS YouTube URLs accepted");
  await mkdir(outputDir,{recursive:true});
  const template=path.join(outputDir,"%(id)s.%(ext)s");
  await run(ytDlpPath,["--no-playlist","--no-progress","--restrict-filenames","-o",template,"--print","after_move:filepath",url]);
  return {outputDir,template,note:"Download and reuse only media you own or are licensed to use."};
}
