// src/pages/upload.jsx
import React, {useState, useEffect} from 'react';

const teams = ["teamA","teamB","teamC"];
const weeks = Array.from({length:16},(_,i)=>`week${i+1}`);

export default function UploadPage(){
  const params = typeof window !== 'undefined' ? new URLSearchParams(window.location.search) : new URLSearchParams();
  const [team, setTeam] = useState(params.get('team') || 'teamA');
  const [week, setWeek] = useState(params.get('week') || 'week1');
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState('');

  async function doUpload(e){
    e.preventDefault();
    if(!file){ setMsg("Select a file"); return; }
    const fd = new FormData();
    fd.append("team", team);
    fd.append("week", week);
    fd.append("file", file);
    try{
      const res = await fetch("http://127.0.0.1:9000/upload/", { method: "POST", body: fd });
      const j = await res.json();
      if(res.ok){
        setMsg("Saved: " + j.saved);
        setTimeout(()=>window.location.reload(), 1200);
      }else{
        setMsg("Error: " + (j.detail || JSON.stringify(j)));
      }
    }catch(err){
      setMsg("Failed: " + err.message);
    }
  }

  return (
    <div style={{padding: 24}}>
      <h1>Upload Documentation</h1>
      <form onSubmit={doUpload}>
        <label>Team:&nbsp;
          <select value={team} onChange={e=>setTeam(e.target.value)}>
            {teams.map(t=> <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        &nbsp;&nbsp;
        <label>Week:&nbsp;
          <select value={week} onChange={e=>setWeek(e.target.value)}>
            {weeks.map(w=> <option key={w} value={w}>{w}</option>)}
          </select>
        </label>
        <div style={{marginTop:10}}>
          <input type="file" onChange={e=>setFile(e.target.files[0])} />
        </div>
        <button type="submit" style={{marginTop:10}}>Upload</button>
      </form>
      <div style={{marginTop:10}}>{msg}</div>
    </div>
  );
}
