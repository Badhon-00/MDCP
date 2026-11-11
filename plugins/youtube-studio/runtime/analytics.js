export async function queryChannelAnalytics({accessToken,startDate,endDate,metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",dimensions="day",filters,fetchImpl=fetch}) {
  if(!accessToken) throw new Error("OAuth accessToken required for private channel analytics");
  const valid=/^\d{4}-\d{2}-\d{2}$/;
  if(!valid.test(startDate||"")||!valid.test(endDate||"")||startDate>endDate) throw new Error("Dates must be YYYY-MM-DD and startDate <= endDate");
  const url=new URL("https://youtubeanalytics.googleapis.com/v2/reports");
  for(const [k,v] of Object.entries({ids:"channel==MINE",startDate,endDate,metrics,dimensions,filters})) if(v) url.searchParams.set(k,v);
  const r=await fetchImpl(url,{headers:{Authorization:`Bearer ${accessToken}`}});
  if(!r.ok) throw new Error(`Analytics API failed (${r.status}): ${await r.text()}`);
  return r.json();
}
