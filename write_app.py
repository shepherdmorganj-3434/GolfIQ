import os

app_code = r"""
import { useState, useEffect } from 'react'

const COURSES=['Augusta National','Pebble Beach Golf Links','Torrey Pines South','Pinehurst No. 2','TPC Sawgrass','Bethpage Black','Whistling Straits','Shinnecock Hills','Oakmont Country Club','Bandon Dunes','Pacific Dunes','Kiawah Island Ocean','Erin Hills','Chambers Bay','Riviera Country Club','Spyglass Hill','Medinah Country Club','Oakland Hills South','Merion Golf Club East','Winged Foot West']

const GAMES={
  stroke:{name:'Stroke Play',sub:'Solo · Standard',color:'#4cc834',bg:'#182e1c',cat:'Standard',tag:'Solo · Standard',pills:['18 holes','1-4 players','Classic'],rules:[{t:'Objective',txt:'Count every shot across all 18 holes. Lowest total score wins.'},{t:'Scoring',txt:'Write down stroke total per hole. Add up front 9, back 9, and grand total.'},{t:'Over/Under par',txt:'Compare your score to course par. Score of 84 on a par-72 = +12.'}],scoring:[{l:'Birdie',p:'-1',c:'pos'},{l:'Par',p:'E',c:'neu'},{l:'Bogey',p:'+1',c:'neg'}]},
  stableford:{name:'Stableford',sub:'Solo · Points',color:'#84cc16',bg:'#1a2a0a',cat:'Standard',tag:'Solo · Points',pills:['18 holes','Handicap','Points'],rules:[{t:'Objective',txt:'Score points per hole - highest points total wins.'},{t:'Points',txt:'Eagle=4pts, Birdie=3pts, Par=2pts, Bogey=1pt, Double+=0pts.'},{t:'Handicap',txt:'Strokes deducted based on handicap index.'}],scoring:[{l:'Eagle',p:'4 pts',c:'pos'},{l:'Birdie',p:'3 pts',c:'pos'},{l:'Par',p:'2 pts',c:'neu'},{l:'Bogey',p:'1 pt',c:'neu'},{l:'Double+',p:'0 pts',c:'neg'}]},
  matchplay:{name:'Match Play',sub:'1v1 · Hole-by-hole',color:'#f87171',bg:'#2a1010',cat:'Head-to-Head',tag:'1v1 · Hole-by-hole',pills:['1v1','Hole-by-hole','Strategic'],rules:[{t:'Objective',txt:'Win more individual holes than your opponent.'},{t:'Winning',txt:'Lower score = go 1 Up. Tie = halved. Game ends when lead exceeds holes left.'},{t:'Early finish',txt:'3&2 = you were 3 holes up with 2 to play.'}],scoring:[{l:'Win hole',p:'+1 Up',c:'pos'},{l:'Halve',p:'Square',c:'neu'},{l:'Lose hole',p:'1 Down',c:'neg'}]},
  bestball:{name:'Best Ball',sub:'Team · 2v2',color:'#4cc834',bg:'#182e1c',cat:'Team',tag:'Team · 2v2',pills:['2v2','Best score counts','Match or stroke'],rules:[{t:'Setup',txt:'2 teams of 2. Each player plays their own ball the whole round.'},{t:'Team score',txt:'On each hole, lowest score from either teammate counts for the team.'},{t:'Winning',txt:'Play match play or stroke play total.'}],scoring:[{l:'Team A lower',p:'A wins',c:'pos'},{l:'Tied',p:'Halved',c:'neu'},{l:'Team B lower',p:'B wins',c:'neg'}]},
  bestball22:{name:'2v2 Best Ball',sub:'Team · Weekend classic',color:'#2dd4bf',bg:'#0c2025',cat:'Team',tag:'Team · 4 Players',pills:['4 players','2 teams','Optional skins'],rules:[{t:'Classic setup',txt:'4 players, 2 teams. Everyone plays their ball, lowest from each team wins the hole.'},{t:'Optional twist',txt:'Add a skins pot per hole. Ties carry the skin to the next hole.'},{t:'Handicap',txt:'Net scores can level the playing field.'}],scoring:[{l:'Win hole',p:'+1',c:'pos'},{l:'Tie',p:'0',c:'neu'},{l:'Lose hole',p:'-1',c:'neg'}]},
  rydercup:{name:'Ryder Cup',sub:'Team · Full Competition',color:'#f5a623',bg:'#22180a',cat:'Team',tag:'Team · Full Competition',pills:['Team event','Multi-format','Points'],rules:[{t:'Structure',txt:'Two teams across 3 formats: Foursomes, Fourball, Singles.'},{t:'Foursomes',txt:'2v2 - teammates alternate hitting the same ball.'},{t:'Fourball',txt:'2v2 - everyone plays their ball. Best score per team wins.'},{t:'Singles',txt:'1v1 match play. Each player vs one from the other team.'}],scoring:[{l:'Win match',p:'1 point',c:'pos'},{l:'Tie',p:'1/2 each',c:'neu'},{l:'Lose',p:'0 points',c:'neg'}]},
  wolf:{name:'Wolf',sub:'Side Game · 4 Players',color:'#a78bfa',bg:'#1a1330',cat:'Side Games',tag:'Side Game · 4 Players',pills:['4 players','Rotating captain','Strategy'],rules:[{t:'The Wolf',txt:'Rotating Wolf tees first, then picks a partner after each drive or goes solo.'},{t:'No going back',txt:'Once you pass on a player, you cannot go back to them.'},{t:'Lone Wolf early',txt:'Go solo before all drives = +3 if you win, -3 if you lose.'},{t:'Lone Wolf auto',txt:'Passed on everyone = forced solo. +2 win / -2 lose.'}],scoring:[{l:'Lone Wolf wins',p:'+3',c:'pos'},{l:'Lone Wolf loses',p:'-3',c:'neg'},{l:'Partner win',p:'+1',c:'pos'}]},
  skins:{name:'Skins',sub:'Side Game · Any Players',color:'#f97316',bg:'#271508',cat:'Side Games',tag:'Side Game · Any Players',pills:['2-6 players','Per hole','Carries over'],rules:[{t:'How it works',txt:'Each hole has a value. Lowest score wins the skin.'},{t:'Ties carry over',txt:'If players tie, the skin rolls to the next hole.'},{t:'Payout',txt:'Count total skins at end. Each skin = a set value.'}],scoring:[{l:'Win hole',p:'Win skin',c:'pos'},{l:'Tie',p:'Carries',c:'neu'},{l:'Lose',p:'No skin',c:'neg'}]},
  nassau:{name:'Nassau',sub:'Side Game · 3 Bets',color:'#60a5fa',bg:'#0e1e30',cat:'Side Games',tag:'Side Game · 3 Bets',pills:['3 bets','Front Back Total','Any format'],rules:[{t:'Three bets',txt:'Front 9, Back 9, and Overall 18 - three separate competitions.'},{t:'Why it works',txt:'Lose the front badly? Still alive on back and overall.'},{t:'Presses',txt:'Optional: if down 2+ holes, press to open a new bet.'}],scoring:[{l:'Win front 9',p:'+1 bet',c:'pos'},{l:'Win back 9',p:'+1 bet',c:'pos'},{l:'Win overall',p:'+1 bet',c:'pos'}]},
  bbb:{name:'Bingo Bango Bongo',sub:'Side Game · Mixed Levels',color:'#f472b6',bg:'#2a1020',cat:'Side Games',tag:'Side Game · Any Group',pills:['3 pts/hole','Skill-leveling','Any size'],rules:[{t:'3 points per hole',txt:'Bingo=first on green. Bango=closest to pin. Bongo=first in hole.'},{t:'Why it works',txt:'High handicappers can win too - getting on green first does not require low scores.'},{t:'Order',txt:'Furthest from hole plays first - keeps points fair.'}],scoring:[{l:'Bingo',p:'1 pt',c:'pos'},{l:'Bango',p:'1 pt',c:'pos'},{l:'Bongo',p:'1 pt',c:'pos'}]},
}

const CATS=[{label:'Standard',games:['stroke','stableford']},{label:'Head-to-Head',games:['matchplay']},{label:'Team Formats',games:['bestball','bestball22','rydercup']},{label:'Side Games',games:['wolf','skins','nassau','bbb']}]
const GAME_CONFIGS={stroke:{teams:null,min:1,max:4},stableford:{teams:null,min:1,max:4},matchplay:{teams:['Player A','Player B']},bestball:{teams:['Team A','Team B'],perTeam:2},bestball22:{teams:['Team A','Team B'],perTeam:2},rydercup:{teams:['Team A','Team B'],perTeam:4},wolf:{teams:null,exact:4},skins:{teams:null,min:2,max:6},nassau:{teams:null,min:2,max:4},bbb:{teams:null,min:2,max:6}}
const PARS=[5,4,3,4,5,4,4,3,4,4,4,5,3,5,4,3,4,5]
const YARDS=[570,350,104,323,188,516,97,428,481,436,390,202,391,575,397,112,376,543]
const HCP=[11,7,17,9,15,3,13,5,1,4,12,8,16,2,14,18,6,10]
const ROUNDS=[
  {course:'Pebble Beach GL',format:'Stroke Play',date:'Mar 30, 2026',winner:'JD',winnerScore:'84 (+12)',winColor:'#4cc834',winBg:'#0f2218',players:[{name:'JD',scores:[5,4,4,3,5,5,4,3,4,5,4,5,4,4,5,3,5,4]},{name:'Mike',scores:[5,5,5,4,5,6,4,4,5,5,5,5,4,5,5,4,5,4]},{name:'Chris',scores:[6,5,5,4,5,6,5,4,5,6,5,5,5,5,5,4,5,4]}],pars:[5,4,3,4,5,4,4,3,4,4,4,5,3,5,4,3,4,5],type:'stroke'},
  {course:'Augusta National',format:'Stableford',date:'Mar 22, 2026',winner:'JD',winnerScore:'38 pts',winColor:'#4cc834',winBg:'#0f2218',players:[{name:'JD',scores:[3,4,3,4,4,3,3,4,3,3,4,3,3,4,4,3,4,4],pts:[2,2,3,2,2,3,2,2,3,2,2,3,2,2,2,3,2,3]},{name:'Dan',scores:[4,5,4,4,5,4,4,4,4,4,4,4,4,4,5,4,4,4],pts:[2,1,2,2,1,2,2,2,2,2,2,2,2,2,1,2,2,1]}],pars:[4,5,3,3,4,3,4,5,4,4,4,3,5,4,5,3,4,4],type:'stableford'},
  {course:'Torrey Pines South',format:'Match Play',date:'Mar 15, 2026',winner:'JD',winnerScore:'3&2',winColor:'#4cc834',winBg:'#0f2218',players:[{name:'JD',scores:[4,5,4,3,4,4,4,3,5,4,4,5,3,4,4,3,'-','-']},{name:'Alex',scores:[5,5,5,4,4,5,4,4,5,4,5,5,4,5,4,4,'-','-']}],pars:[4,4,3,5,4,4,3,4,5,4,4,5,3,5,4,3,4,4],matchResult:['W','H','W','W','H','W','H','W','L','H','W','H','W','W','H','3&2','-','-'],type:'match'},
]

const s = {
  app:{fontFamily:"'Barlow',sans-serif",width:'390px',margin:'0 auto',background:'#0e1923',minHeight:'100vh',position:'relative',overflow:'hidden'},
  screen:{display:'flex',flexDirection:'column',minHeight:'100vh',paddingBottom:'80px'},
  nav:{position:'fixed',bottom:0,left:'50%',transform:'translateX(-50%)',width:'390px',background:'#0b1520',borderTop:'1px solid #1e2f3d',display:'flex',justifyContent:'space-around',padding:'10px 0 14px',zIndex:50},
  navItem:{display:'flex',flexDirection:'column',alignItems:'center',gap:'3px',cursor:'pointer',padding:'2px 10px'},
  navLabel:{fontSize:'9px',fontWeight:700,letterSpacing:'.6px',textTransform:'uppercase'},
  logo:{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'28px',fontWeight:800,lineHeight:1},
  hdr:{padding:'28px 24px 20px',display:'flex',alignItems:'center',justifyContent:'space-between'},
  avatar:{width:'36px',height:'36px',borderRadius:'50%',background:'#1e3a28',border:'2px solid #4cc834',display:'flex',alignItems:'center',justifyContent:'center',fontSize:'13px',fontWeight:700,color:'#4cc834',cursor:'pointer'},
  hero:{margin:'0 16px 22px',background:'#173827',borderRadius:'20px',border:'1px solid #2a5038',padding:'22px 20px',position:'relative',overflow:'hidden'},
  heroLabel:{fontSize:'11px',fontWeight:600,letterSpacing:'1.5px',color:'#4cc834',textTransform:'uppercase',marginBottom:'6px'},
  heroTitle:{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'26px',fontWeight:800,color:'#fff',marginBottom:'4px',lineHeight:1.1},
  heroSub:{fontSize:'13px',color:'#6b9a7a',marginBottom:'18px'},
  btnWhite:{display:'inline-flex',alignItems:'center',gap:'6px',background:'#fff',color:'#0a1f10',fontFamily:"'Barlow',sans-serif",fontSize:'14px',fontWeight:700,padding:'10px 20px',borderRadius:'10px',border:'none',cursor:'pointer'},
  secHdr:{padding:'0 20px',marginBottom:'12px',display:'flex',alignItems:'center',justifyContent:'space-between'},
  secTitle:{fontSize:'11px',fontWeight:700,letterSpacing:'1.5px',color:'#4a6b5a',textTransform:'uppercase'},
  secLink:{fontSize:'12px',fontWeight:600,color:'#2a5038',cursor:'pointer'},
  roundCard:{background:'#131f2b',border:'1px solid #1e3040',borderRadius:'14px',padding:'14px 16px',marginBottom:'10px',cursor:'pointer'},
  roundTop:{display:'flex',alignItems:'flex-start',justifyContent:'space-between',marginBottom:'8px'},
  roundCourse:{fontSize:'14px',fontWeight:700,color:'#dce9e1'},
  roundMeta:{fontSize:'11px',color:'#3a5a50',marginTop:'2px'},
  scoreNum:{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'26px',fontWeight:800,color:'#fff',lineHeight:1,textAlign:'right'},
  roundBottom:{borderTop:'1px solid #1a2e3d',paddingTop:'8px',display:'flex',alignItems:'center',justifyContent:'space-between'},
  winnerText:{fontSize:'12px',fontWeight:700,color:'#f5a623'},
  playersText:{fontSize:'11px',color:'#3a5a50'},
  fmtCard:{display:'flex',alignItems:'center',gap:'12px',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'14px',padding:'13px 14px',marginBottom:'8px',cursor:'pointer'},
  fmtIcon:{width:'40px',height:'40px',borderRadius:'11px',display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0},
  fmtName:{fontSize:'15px',fontWeight:700,color:'#c8dce8'},
  fmtSub:{fontSize:'12px',color:'#2e5040',marginTop:'2px'},
  backBtn:{width:'32px',height:'32px',borderRadius:'10px',background:'#131f2b',border:'1px solid #1e3040',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',flexShrink:0},
  detailHdr:{padding:'20px 20px 14px',display:'flex',alignItems:'center',gap:'12px'},
  catLabel:{fontSize:'10px',fontWeight:700,letterSpacing:'1.8px',textTransform:'uppercase',color:'#1e3a30',margin:'16px 0 8px 2px'},
  fieldRow:{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'10px',marginBottom:'16px'},
  fieldLabel:{fontSize:'11px',fontWeight:700,letterSpacing:'1.2px',textTransform:'uppercase',color:'#2e5040',marginBottom:'6px'},
  fieldInput:{width:'100%',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'12px',padding:'12px 14px',fontFamily:"'Barlow',sans-serif",fontSize:'15px',fontWeight:600,color:'#c8dce8',outline:'none'},
  gameOpt:{display:'flex',alignItems:'center',gap:'12px',background:'#111f2c',border:'1.5px solid #1a2e3d',borderRadius:'13px',padding:'11px 14px',cursor:'pointer',marginBottom:'7px'},
  btnMain:{width:'100%',background:'#fff',border:'none',borderRadius:'12px',padding:'14px',fontFamily:"'Barlow Condensed',sans-serif",fontSize:'18px',fontWeight:800,color:'#0a1f10',cursor:'pointer'},
  playerRow:{display:'flex',alignItems:'center',gap:'8px',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'12px',padding:'9px 12px',marginBottom:'7px'},
  playerInput:{flex:1,minWidth:0,background:'transparent',border:'none',outline:'none',fontFamily:"'Barlow',sans-serif",fontSize:'15px',fontWeight:600,color:'#c8dce8'},
  hcpInput:{width:'34px',background:'#0d1820',border:'1px solid #1a2e3d',borderRadius:'7px',padding:'4px',fontFamily:"'Barlow Condensed',sans-serif",fontSize:'14px',fontWeight:700,color:'#4a7a8a',textAlign:'center',outline:'none'},
  countBtn:{width:'44px',height:'44px',background:'#131f2b',border:'none',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',flexShrink:0},
  countDisplay:{flex:1,textAlign:'center',fontFamily:"'Barlow Condensed',sans-serif",fontSize:'28px',fontWeight:800,color:'#fff',lineHeight:1,minWidth:'60px',padding:'8px 0'},
}

const NavBar = ({active, onNav}) => (
  <div style={s.nav}>
    {[['home','Home','M3 10L10 3l7 7v7H13v-4H7v4H3v-7z'],['formats','Formats','M3 3h6v6H3zM11 3h6v6h-6zM3 11h6v6H3zM11 11h6v6h-6z'],['rounds','Rounds','M3 4h14a2 2 0 012 2v10a2 2 0 01-2 2H3a2 2 0 01-2-2V6a2 2 0 012-2zM7 4V2M13 4V2M1 8h18'],['stats','Stats','M10 2v16M2 10h16'],['profile','Profile','M10 7a3 3 0 100-6 3 3 0 000 6zM4 17a6 6 0 0112 0']].map(([id,label,path])=>(
      <div key={id} style={s.navItem} onClick={()=>onNav(id)}>
        <svg width="19" height="19" viewBox="0 0 20 20" fill="none">
          <path d={path} stroke={active===id?'#4cc834':'#3a5248'} strokeWidth="1.5" strokeLinejoin="round" strokeLinecap="round"/>
        </svg>
        <span style={{...s.navLabel,color:active===id?'#4cc834':'#3a5248'}}>{label}</span>
      </div>
    ))}
  </div>
)

function HomeScreen({onNav, onNewRound, onViewCard}) {
  return (
    <div style={s.screen}>
      <div style={s.hdr}>
        <div style={s.logo}><span style={{color:'#fff'}}>Hole</span><span style={{color:'#4cc834'}}>IQ</span></div>
        <div style={s.avatar}>JD</div>
      </div>
      <div style={s.hero}>
        <div style={s.heroLabel}>Ready to play?</div>
        <div style={s.heroTitle}>Start a New Round</div>
        <div style={s.heroSub}>Select a format and get started</div>
        <button style={s.btnWhite} onClick={onNewRound}>New Round ↗</button>
      </div>
      <div style={s.secHdr}>
        <div style={s.secTitle}>Recent rounds</div>
        <div style={s.secLink} onClick={()=>onNav('rounds')}>View all →</div>
      </div>
      <div style={{padding:'0 16px'}}>
        {ROUNDS.map((r,i)=>(
          <div key={i} style={s.roundCard} onClick={()=>onViewCard(i)}>
            <div style={s.roundTop}>
              <div><div style={s.roundCourse}>{r.course}</div><div style={s.roundMeta}>{r.format} · {r.date.split(',')[0]}</div></div>
              <div><div style={s.scoreNum}>{r.winnerScore.split(' ')[0]}</div><div style={{fontSize:'11px',fontWeight:600,textAlign:'right',color:r.type==='match'?'#4cc834':'#f97316'}}>{r.type==='match'?'Win':r.winnerScore.split('(')[1]?.replace(')','')}</div></div>
            </div>
            <div style={s.roundBottom}>
              <div style={{display:'flex',alignItems:'center',gap:'6px'}}>
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M6.5 1l1 3h3.2L8.1 5.8l1 3-2.6-1.9-2.6 1.9 1-3L2.3 4h3.2z" stroke="#f5a623" strokeWidth="1.1" strokeLinejoin="round"/></svg>
                <span style={s.winnerText}>{r.winner} Won</span>
                <span style={s.playersText}>{r.players.slice(1).map(p=>p.name).join(' · ')}</span>
              </div>
              <span style={{fontSize:'11px',color:'#2a4535',fontWeight:600}}>View →</span>
            </div>
          </div>
        ))}
      </div>
      <NavBar active="home" onNav={onNav}/>
    </div>
  )
}

function FormatsScreen({onNav, onSelectFormat}) {
  return (
    <div style={s.screen}>
      <div style={{padding:'22px 20px 6px'}}>
        <h2 style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'28px',fontWeight:800,color:'#fff'}}>Game Formats</h2>
        <p style={{fontSize:'13px',color:'#3a5a50',marginTop:'4px'}}>Tap any format to learn how it works</p>
      </div>
      {CATS.map(cat=>(
        <div key={cat.label} style={{padding:'0 16px'}}>
          <div style={s.catLabel}>{cat.label}</div>
          {cat.games.map(id=>{const g=GAMES[id];return(
            <div key={id} style={s.fmtCard} onClick={()=>onSelectFormat(id)}>
              <div style={{...s.fmtIcon,background:g.bg}}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="6" stroke={g.color} strokeWidth="1.4"/><path d="M10 7v3l2 1.5" stroke={g.color} strokeWidth="1.4" strokeLinecap="round"/></svg>
              </div>
              <div><div style={s.fmtName}>{g.name}</div><div style={s.fmtSub}>{g.sub}</div></div>
              <div style={{marginLeft:'auto',color:'#1e3830',fontSize:'18px'}}>›</div>
            </div>
          )})}
        </div>
      ))}
      <NavBar active="formats" onNav={onNav}/>
    </div>
  )
}

function DetailScreen({gameId, onBack, onPlay}) {
  const g=GAMES[gameId]
  if(!g) return null
  return (
    <div style={s.screen}>
      <div style={s.detailHdr}>
        <div style={s.backBtn} onClick={onBack}><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 11L5 7l4-4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg></div>
        <span style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'20px',fontWeight:800,color:'#fff'}}>{g.name}</span>
      </div>
      <div style={{flex:1,overflowY:'auto',paddingBottom:'80px'}}>
        <div style={{margin:'0 16px 16px',borderRadius:'18px',padding:'20px',background:g.bg,border:`1px solid ${g.color}22`}}>
          <div style={{fontSize:'10px',fontWeight:700,letterSpacing:'1.5px',textTransform:'uppercase',color:g.color,marginBottom:'8px'}}>{g.tag.toUpperCase()}</div>
          <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'30px',fontWeight:800,color:'#fff',marginBottom:'10px'}}>{g.name}</div>
          <div style={{display:'flex',gap:'6px',flexWrap:'wrap'}}>
            {g.pills.map(p=><span key={p} style={{fontSize:'10px',fontWeight:700,padding:'4px 10px',borderRadius:'7px',background:`${g.color}18`,color:g.color}}>{p}</span>)}
          </div>
        </div>
        <div style={{padding:'0 16px'}}>
          <div style={{fontSize:'10px',fontWeight:700,letterSpacing:'1.5px',textTransform:'uppercase',color:'#2e4a3a',marginBottom:'10px'}}>How it works</div>
          {g.rules.map((r,i)=>(
            <div key={i} style={{display:'flex',alignItems:'flex-start',gap:'10px',marginBottom:'10px'}}>
              <div style={{width:'22px',height:'22px',borderRadius:'50%',background:g.bg,color:g.color,display:'flex',alignItems:'center',justifyContent:'center',fontSize:'11px',fontWeight:800,flexShrink:0}}>{i+1}</div>
              <div style={{fontSize:'13px',color:'#7a9a8a',lineHeight:1.5}}><strong style={{color:'#c8dce8'}}>{r.t}:</strong> {r.txt}</div>
            </div>
          ))}
          <div style={{fontSize:'10px',fontWeight:700,letterSpacing:'1.5px',textTransform:'uppercase',color:'#2e4a3a',margin:'16px 0 10px'}}>Scoring</div>
          {g.scoring.map((s2,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'9px 12px',borderRadius:'10px',marginBottom:'6px',background:'#111f2c'}}>
              <span style={{fontSize:'13px',color:'#7a9a8a',fontWeight:600}}>{s2.l}</span>
              <span style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'20px',fontWeight:800,color:s2.c==='pos'?'#4cc834':s2.c==='neg'?'#f87171':'#60a5fa'}}>{s2.p}</span>
            </div>
          ))}
        </div>
      </div>
      <div style={{position:'fixed',bottom:0,left:'50%',transform:'translateX(-50%)',width:'390px',padding:'12px 16px 18px',background:'#0e1923',borderTop:'1px solid #1a2a3a',zIndex:20}}>
        <button style={s.btnMain} onClick={onPlay}>Play this format →</button>
      </div>
    </div>
  )
}

function NewRoundScreen({onBack, onConfirm}) {
  const [date,setDate]=useState(new Date().toISOString().split('T')[0])
  const [time,setTime]=useState(()=>{const d=new Date();return String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')})
  const [course,setCourse]=useState('')
  const [courseQ,setCourseQ]=useState('')
  const [showCourses,setShowCourses]=useState(false)
  const [selGame,setSelGame]=useState(null)
  const [pendingGame,setPendingGame]=useState(null)
  const canContinue=course&&selGame

  const filtered=COURSES.filter(c=>c.toLowerCase().includes(courseQ.toLowerCase())).slice(0,8)

  return (
    <div style={s.screen}>
      <div style={{padding:'22px 20px 14px',display:'flex',alignItems:'center',gap:'12px'}}>
        <div style={s.backBtn} onClick={onBack}><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 11L5 7l4-4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg></div>
        <span style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'22px',fontWeight:800,color:'#fff'}}>New Round</span>
        <div style={{display:'flex',gap:'6px',marginLeft:'auto'}}>
          <div style={{width:'18px',height:'6px',borderRadius:'3px',background:'#4cc834'}}></div>
          <div style={{width:'6px',height:'6px',borderRadius:'50%',background:'#1a2e3d'}}></div>
        </div>
      </div>
      <div style={{flex:1,padding:'0 16px',overflowY:'auto'}}>
        <div style={s.fieldRow}>
          <div><div style={s.fieldLabel}>Date</div><input type="date" style={s.fieldInput} value={date} onChange={e=>setDate(e.target.value)}/></div>
          <div><div style={s.fieldLabel}>Tee Time</div><input type="time" style={s.fieldInput} value={time} onChange={e=>setTime(e.target.value)}/></div>
        </div>
        <div style={{marginBottom:'16px'}}>
          <div style={s.fieldLabel}>Course</div>
          <div style={{position:'relative'}}>
            <input style={s.fieldInput} placeholder="Search for a course..." value={courseQ} onChange={e=>{setCourseQ(e.target.value);setCourse('')}} onFocus={()=>setShowCourses(true)} onBlur={()=>setTimeout(()=>setShowCourses(false),200)}/>
            {showCourses&&courseQ&&(
              <div style={{position:'absolute',top:'calc(100% + 4px)',left:0,right:0,background:'#111f2c',border:'1px solid #1a3040',borderRadius:'12px',zIndex:10,maxHeight:'180px',overflowY:'auto'}}>
                {filtered.map(c=>(
                  <div key={c} style={{padding:'11px 14px',fontSize:'14px',fontWeight:600,color:'#c8dce8',cursor:'pointer',borderBottom:'1px solid #0f1d28'}} onMouseDown={()=>{setCourse(c);setCourseQ(c);setShowCourses(false)}}>{c}</div>
                ))}
              </div>
            )}
          </div>
        </div>
        <div style={s.fieldLabel}>Game Format</div>
        {CATS.map(cat=>(
          <div key={cat.label}>
            <div style={{fontSize:'9px',fontWeight:700,letterSpacing:'1.5px',textTransform:'uppercase',color:'#1e3830',margin:'10px 0 6px',paddingLeft:'2px'}}>{cat.label}</div>
            {cat.games.map(id=>{const g=GAMES[id];return(
              <div key={id} style={{...s.gameOpt,borderColor:selGame===id?'#4cc834':'#1a2e3d',background:selGame===id?'#0f2218':'#111f2c'}} onClick={()=>setPendingGame(id)}>
                <div style={{width:'34px',height:'34px',borderRadius:'9px',background:g.bg,display:'flex',alignItems:'center',justifyContent:'center'}}>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="5" stroke={g.color} strokeWidth="1.4"/></svg>
                </div>
                <div><div style={{fontSize:'14px',fontWeight:700,color:'#c8dce8'}}>{g.name}</div><div style={{fontSize:'11px',color:'#3a6050'}}>{g.tag}</div></div>
                {selGame===id&&<div style={{marginLeft:'auto',width:'18px',height:'18px',borderRadius:'50%',background:'#4cc834',display:'flex',alignItems:'center',justifyContent:'center'}}><svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 5l2.5 2.5 3.5-4" stroke="#0a1f10" strokeWidth="1.5" strokeLinecap="round"/></svg></div>}
              </div>
            )})}
          </div>
        ))}
      </div>
      {pendingGame&&(
        <div style={{position:'absolute',top:0,left:0,right:0,bottom:0,background:'rgba(5,10,16,.82)',zIndex:100,borderRadius:'24px'}} onClick={e=>{if(e.target===e.currentTarget)setPendingGame(null)}}>
          <div style={{background:'#111f2c',border:'1px solid #1e3040',borderRadius:'0 0 20px 20px',animation:'none'}}>
            <div style={{padding:'20px 20px 0',display:'flex',alignItems:'center',gap:'14px'}}>
              <div style={{width:'46px',height:'46px',borderRadius:'13px',background:GAMES[pendingGame].bg,display:'flex',alignItems:'center',justifyContent:'center'}}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none"><circle cx="11" cy="11" r="7" stroke={GAMES[pendingGame].color} strokeWidth="1.5"/></svg>
              </div>
              <div>
                <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'26px',fontWeight:800,color:'#fff'}}>{GAMES[pendingGame].name}</div>
                <div style={{fontSize:'13px',color:GAMES[pendingGame].color,fontWeight:600}}>{GAMES[pendingGame].tag}</div>
              </div>
            </div>
            <div style={{height:'1px',background:'#1a2e3d',margin:'16px 20px'}}></div>
            <div style={{fontSize:'15px',fontWeight:600,color:'#8ab4c4',padding:'0 20px 18px'}}>Are you sure you want to play this format?</div>
            <div style={{display:'flex',gap:'10px',padding:'0 16px 20px'}}>
              <button style={{flex:1,background:'#fff',border:'1.5px solid #fff',borderRadius:'12px',padding:'13px',fontFamily:"'Barlow Condensed',sans-serif",fontSize:'17px',fontWeight:800,color:'#0a1f10',cursor:'pointer'}} onClick={()=>setPendingGame(null)}>No</button>
              <button style={{flex:2,background:'#fff',border:'1.5px solid #fff',borderRadius:'12px',padding:'13px',fontFamily:"'Barlow Condensed',sans-serif",fontSize:'17px',fontWeight:800,color:'#0a1f10',cursor:'pointer'}} onClick={()=>{setSelGame(pendingGame);setPendingGame(null);if(course)onConfirm({date,time,course,gameId:pendingGame})}}>Yes, set it up</button>
            </div>
          </div>
        </div>
      )}
      <div style={{position:'absolute',bottom:0,left:0,right:0,padding:'12px 16px 18px',background:'#0e1923',borderTop:'1px solid #1a2a3a',zIndex:20}}>
        <button style={{...s.btnMain,background:canContinue?'#fff':'#1a3822',color:canContinue?'#0a1f10':'#2a5030',cursor:canContinue?'pointer':'not-allowed'}} disabled={!canContinue} onClick={()=>{if(canContinue)onConfirm({date,time,course,gameId:selGame})}}>Continue →</button>
      </div>
    </div>
  )
}

function PlayersScreen({roundInfo, onBack, onStart}) {
  const g=GAMES[roundInfo.gameId]
  const cfg=GAME_CONFIGS[roundInfo.gameId]
  const d=new Date(roundInfo.date+'T'+roundInfo.time)
  const ds=d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})
  const ts=d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'})

  const renderRows=(avClass,count,prefix)=>Array.from({length:count},(_,i)=>(
    <div key={i} style={s.playerRow}>
      <div style={{width:'30px',height:'30px',borderRadius:'50%',display:'flex',alignItems:'center',justifyContent:'center',fontSize:'11px',fontWeight:700,background:avClass==='av-a'?'#1a3822':avClass==='av-b'?'#2a1a0c':'#1a1535',color:avClass==='av-a'?'#4cc834':avClass==='av-b'?'#f97316':'#a78bfa',flexShrink:0}}>{prefix}{i+1}</div>
      <input style={s.playerInput} placeholder="Player name"/>
      <div style={{display:'flex',flexDirection:'column',alignItems:'center',gap:'2px',flexShrink:0}}>
        <div style={{fontSize:'9px',fontWeight:700,letterSpacing:'.8px',textTransform:'uppercase',color:'#1e3830'}}>HCP</div>
        <input style={s.hcpInput} type="number" min="0" max="54" placeholder="–"/>
      </div>
    </div>
  ))

  return (
    <div style={s.screen}>
      <div style={{padding:'22px 20px 14px',display:'flex',alignItems:'center',gap:'12px'}}>
        <div style={s.backBtn} onClick={onBack}><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 11L5 7l4-4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg></div>
        <span style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'22px',fontWeight:800,color:'#fff'}}>Game Profile</span>
        <div style={{display:'flex',gap:'6px',marginLeft:'auto'}}>
          <div style={{width:'6px',height:'6px',borderRadius:'50%',background:'#2a5038'}}></div>
          <div style={{width:'18px',height:'6px',borderRadius:'3px',background:'#4cc834'}}></div>
        </div>
      </div>
      <div style={{margin:'0 16px 16px',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'16px',padding:'14px 16px',display:'flex',alignItems:'center',gap:'12px'}}>
        <div style={{width:'38px',height:'38px',borderRadius:'10px',background:g.bg,display:'flex',alignItems:'center',justifyContent:'center'}}>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="6" stroke={g.color} strokeWidth="1.4"/></svg>
        </div>
        <div><div style={{fontSize:'15px',fontWeight:700,color:'#c8dce8'}}>{g.name} · {roundInfo.course}</div><div style={{fontSize:'12px',color:'#3a6050',marginTop:'2px'}}>{ds} · {ts}</div></div>
      </div>
      <div style={{padding:'0 16px',flex:1}}>
        {cfg.teams&&cfg.perTeam ? cfg.teams.map((t,ti)=>(
          <div key={t} style={{marginBottom:'18px'}}>
            <div style={{fontSize:'12px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:ti===0?'#4cc834':'#f97316',marginBottom:'8px'}}>{t}</div>
            {renderRows(ti===0?'av-a':'av-b',cfg.perTeam,String.fromCharCode(65+ti))}
          </div>
        )) : cfg.teams ? cfg.teams.map((t,ti)=>(
          <div key={t} style={{marginBottom:'18px'}}>
            <div style={{fontSize:'12px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:ti===0?'#4cc834':'#f97316',marginBottom:'8px'}}>{t}</div>
            {renderRows(ti===0?'av-a':'av-b',1,String.fromCharCode(65+ti))}
          </div>
        )) : (
          <div style={{marginBottom:'18px'}}>
            <div style={{display:'flex',justifyContent:'space-between',marginBottom:'8px'}}>
              <div style={{fontSize:'12px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:'#60a5fa'}}>Players</div>
              <div style={{fontSize:'11px',color:'#1e3830'}}>{cfg.exact?`Exactly ${cfg.exact} required`:`${cfg.min}-${cfg.max} players`}</div>
            </div>
            {renderRows('av-s',cfg.exact||cfg.min,'P')}
          </div>
        )}
      </div>
      <div style={{position:'absolute',bottom:0,left:0,right:0,padding:'12px 16px 18px',background:'#0e1923',borderTop:'1px solid #1a2a3a',zIndex:20}}>
        <button style={s.btnMain} onClick={onStart}>Start Round 🏌️</button>
      </div>
    </div>
  )
}

function ScorecardScreen({course, onEnd}) {
  const [hole,setHole]=useState(0)
  const [scores,setScores]=useState(Array.from({length:4},()=>new Array(18).fill(0)))
  const [tab,setTab]=useState('score')
  const players=[{name:'JD',av:'av-1',init:'JD'},{name:'Mike',av:'av-2',init:'MK'},{name:'Chris',av:'av-3',init:'CR'},{name:'Dan',av:'av-4',init:'DN'}]
  const avColors={av1:{bg:'#1a3822',color:'#4cc834'},'av-1':{bg:'#1a3822',color:'#4cc834'},'av-2':{bg:'#2a1a0c',color:'#f97316'},'av-3':{bg:'#1a1535',color:'#a78bfa'},'av-4':{bg:'#0e1e30',color:'#60a5fa'}}

  const changeScore=(pi,d)=>{const ns=[...scores];ns[pi]=[...ns[pi]];const par=PARS[hole];ns[pi][hole]=Math.max(1,Math.min(12,(ns[pi][hole]||par)+d));setScores(ns);}
  const getTotal=(pi)=>scores[pi].reduce((a,b)=>a+b,0)
  const parThru=PARS.slice(0,scores[0].filter(x=>x>0).length).reduce((a,b)=>a+b,0)
  const relStr=(t)=>{if(!t)return{txt:'E',color:'#6b9a7a'};const d=t-parThru;if(d===0)return{txt:'E',color:'#6b9a7a'};if(d>0)return{txt:'+'+d,color:'#f97316'};return{txt:''+d,color:'#4cc834'};}
  const badgeInfo=(score,par)=>{if(!score)return null;const d=score-par;if(d<=-2)return{txt:'Eagle',bg:'#f5a623',color:'#1a0a00'};if(d===-1)return{txt:'Birdie',bg:'#4cc834',color:'#0a1f10'};if(d===0)return{txt:'Par',bg:'#1a2e3d',color:'#4a7a8a'};if(d===1)return{txt:'Bogey',bg:'#2a1a0c',color:'#f97316'};return{txt:'Double',bg:'#2a1010',color:'#f87171'};}

  return (
    <div style={{display:'flex',flexDirection:'column',minHeight:'100vh'}}>
      <div style={{background:'#0b1520',borderBottom:'1px solid #1a2e3d',padding:'18px 18px 14px'}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'10px'}}>
          <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'18px',fontWeight:800,color:'#fff'}}>{course||'Pebble Beach GL'}</div>
          <button style={{background:'#fff',border:'none',borderRadius:'8px',padding:'6px 12px',fontSize:'12px',fontWeight:700,color:'#0a1f10',cursor:'pointer'}} onClick={onEnd}>End Round</button>
        </div>
        <div style={{display:'flex',alignItems:'center'}}>
          <div style={{width:'34px',height:'34px',borderRadius:'9px',background:'#131f2b',border:'1px solid #1a2e3d',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',flexShrink:0}} onClick={()=>setHole(Math.max(0,hole-1))}>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 11L5 7l4-4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg>
          </div>
          <div style={{flex:1,display:'flex',alignItems:'center',justifyContent:'center',gap:'3px',padding:'0 8px',overflow:'hidden'}}>
            {Array.from({length:18},(_,i)=><div key={i} style={{height:'5px',borderRadius:'3px',background:i===hole?'#4cc834':i<hole?'#2a5038':'#1a2e3d',width:i===hole?'22px':'16px',flexShrink:0,transition:'all .2s'}}></div>)}
          </div>
          <div style={{width:'34px',height:'34px',borderRadius:'9px',background:'#131f2b',border:'1px solid #1a2e3d',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',flexShrink:0}} onClick={()=>setHole(Math.min(17,hole+1))}>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M5 3l4 4-4 4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg>
          </div>
        </div>
      </div>
      <div style={{padding:'18px 18px 0',background:'#0e1923'}}>
        <div style={{display:'flex',justifyContent:'space-between',marginBottom:'14px'}}>
          <div><div style={{fontSize:'10px',fontWeight:700,letterSpacing:'1.5px',textTransform:'uppercase',color:'#2e5040',marginBottom:'2px'}}>Hole</div><div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'64px',fontWeight:800,color:'#fff',lineHeight:1}}>{hole+1}</div></div>
          <div style={{display:'flex',flexDirection:'column',alignItems:'flex-end',gap:'6px',marginTop:'4px'}}>
            {[['Par',PARS[hole],true],['Yards',YARDS[hole],false],['HCP',HCP[hole],false]].map(([l,v,accent])=>(
              <div key={l} style={{background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'10px',padding:'6px 12px',textAlign:'center',minWidth:'58px'}}>
                <div style={{fontSize:'9px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:'#2e4a3a',marginBottom:'2px'}}>{l}</div>
                <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'18px',fontWeight:800,color:accent?'#4cc834':'#c8dce8'}}>{v}</div>
              </div>
            ))}
          </div>
        </div>
        <div style={{display:'flex',background:'#0b1520',borderBottom:'1px solid #1a2e3d'}}>
          {['score','board'].map(t=><div key={t} style={{flex:1,padding:'10px',textAlign:'center',fontSize:'11px',fontWeight:700,letterSpacing:'.8px',textTransform:'uppercase',cursor:'pointer',color:tab===t?'#4cc834':'#2e5040',borderBottom:tab===t?'2px solid #4cc834':'2px solid transparent'}} onClick={()=>setTab(t)}>{t==='score'?'Scoring':'Leaderboard'}</div>)}
        </div>
      </div>
      <div style={{flex:1,overflowY:'auto',paddingBottom:'80px'}}>
        {tab==='score'?players.map((p,i)=>{const sc=scores[i][hole]||0;const total=getTotal(i);const rel=relStr(total);const badge=badgeInfo(sc,PARS[hole]);const av=avColors[p.av]||{bg:'#1a3822',color:'#4cc834'};return(
          <div key={i} style={{background:'#111f2c',border:`1.5px solid ${sc>0?'#4cc834':'#1a2e3d'}`,borderRadius:'16px',padding:'12px 14px',margin:'10px 14px 0'}}>
            <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'10px'}}>
              <div style={{display:'flex',alignItems:'center',gap:'10px'}}>
                <div style={{width:'32px',height:'32px',borderRadius:'50%',background:av.bg,color:av.color,display:'flex',alignItems:'center',justifyContent:'center',fontSize:'12px',fontWeight:700}}>{p.init}</div>
                <div style={{fontSize:'14px',fontWeight:700,color:'#c8dce8'}}>{p.name}{badge&&<span style={{fontSize:'12px',fontWeight:700,padding:'2px 8px',borderRadius:'6px',marginLeft:'6px',background:badge.bg,color:badge.color}}>{badge.txt}</span>}</div>
              </div>
              <div style={{textAlign:'right'}}>
                <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'18px',fontWeight:800,color:'#fff'}}>{total||'–'}</div>
                <div style={{fontSize:'11px',fontWeight:700,color:rel.color}}>{total?rel.txt:''}</div>
              </div>
            </div>
            <div style={{display:'flex',background:'#0d1820',borderRadius:'12px',overflow:'hidden'}}>
              <button style={s.countBtn} onClick={()=>changeScore(i,-1)}><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 8h8" stroke="#4a7a8a" strokeWidth="2" strokeLinecap="round"/></svg></button>
              <div style={s.countDisplay}>{sc||'–'}</div>
              <button style={s.countBtn} onClick={()=>changeScore(i,1)}><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 4v8M4 8h8" stroke="#4a7a8a" strokeWidth="2" strokeLinecap="round"/></svg></button>
            </div>
          </div>
        )): players.map((p,i)=>{const total=getTotal(i);const rel=relStr(total);const av=avColors[p.av]||{bg:'#1a3822',color:'#4cc834'};return(
          <div key={i} style={{display:'flex',alignItems:'center',gap:'10px',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'12px',padding:'12px 14px',margin:'10px 14px 0'}}>
            <div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'20px',fontWeight:800,color:'#2a4050',width:'24px'}}>{i+1}</div>
            <div style={{width:'32px',height:'32px',borderRadius:'50%',background:av.bg,color:av.color,display:'flex',alignItems:'center',justifyContent:'center',fontSize:'12px',fontWeight:700}}>{p.init}</div>
            <div style={{flex:1}}><div style={{fontSize:'14px',fontWeight:700,color:'#c8dce8'}}>{p.name}</div></div>
            <div style={{textAlign:'right'}}><div style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'22px',fontWeight:800,color:'#fff'}}>{total||'–'}</div><div style={{fontSize:'11px',fontWeight:700,color:rel.color}}>{total?rel.txt:''}</div></div>
          </div>
        )}
      }
      </div>
      <div style={{position:'fixed',bottom:0,left:'50%',transform:'translateX(-50%)',width:'390px',padding:'12px 14px 16px',background:'#0b1520',borderTop:'1px solid #1a2e3d',zIndex:20}}>
        <button style={{...s.btnMain,background:hole===17?'#f5a623':'#fff',display:'flex',alignItems:'center',justifyContent:'center',gap:'8px'}} onClick={()=>hole<17?setHole(hole+1):onEnd()}>
          <span>{hole===17?'Finish Round':'Save & Next Hole'}</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M5 3l6 5-6 5" stroke="#0a1f10" strokeWidth="1.8" strokeLinecap="round"/></svg>
        </button>
      </div>
    </div>
  )
}

function ScorecardViewScreen({roundIdx, onBack}) {
  const r=ROUNDS[roundIdx]
  if(!r) return null
  const front=[0,1,2,3,4,5,6,7,8],back=[9,10,11,12,13,14,15,16,17]
  const sc=(score,par,type)=>{if(score==='-')return<span style={{color:'#2a4050'}}>–</span>;const sv=parseInt(score),d=sv-parseInt(par);if(type==='match')return<span style={{color:'#8ab4c4'}}>{score}</span>;if(d<=-2)return<span style={{background:'#f5a623',color:'#1a0a00',borderRadius:'50%',width:'22px',height:'22px',display:'inline-flex',alignItems:'center',justifyContent:'center',fontSize:'11px',fontWeight:800}}>{score}</span>;if(d===-1)return<span style={{background:'#4cc834',color:'#0a1f10',borderRadius:'50%',width:'22px',height:'22px',display:'inline-flex',alignItems:'center',justifyContent:'center',fontSize:'11px',fontWeight:800}}>{score}</span>;if(d===0)return<span style={{color:'#8ab4c4'}}>{score}</span>;if(d===1)return<span style={{color:'#f97316'}}>{score}</span>;return<span style={{color:'#f87171'}}>{score}</span>;}
  const mc=(res)=>{if(!res||res==='-')return<span style={{color:'#1e3040'}}>–</span>;if(res==='W')return<span style={{color:'#4cc834',fontWeight:800}}>W</span>;if(res==='L')return<span style={{color:'#f87171',fontWeight:800}}>L</span>;if(res==='H')return<span style={{color:'#4a7a8a'}}>H</span>;return<span style={{color:'#f5a623',fontWeight:800}}>{res}</span>;}

  return (
    <div style={s.screen}>
      <div style={{padding:'20px 20px 14px',display:'flex',alignItems:'center',gap:'12px'}}>
        <div style={s.backBtn} onClick={onBack}><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M9 11L5 7l4-4" stroke="#4a7a8a" strokeWidth="1.5" strokeLinecap="round"/></svg></div>
        <span style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'20px',fontWeight:800,color:'#fff'}}>{r.course}</span>
      </div>
      <div style={{margin:'0 16px 16px',background:'#111f2c',border:'1px solid #1a2e3d',borderRadius:'16px',padding:'14px 16px'}}>
        <div style={{fontSize:'16px',fontWeight:700,color:'#dce9e1',marginBottom:'6px'}}>{r.course}</div>
        <div style={{display:'flex',gap:'8px',flexWrap:'wrap'}}>
          <span style={{fontSize:'10px',fontWeight:700,letterSpacing:'.8px',textTransform:'uppercase',padding:'3px 8px',borderRadius:'6px',background:'#1a2e3d',color:'#4a7a8a'}}>{r.format}</span>
          <span style={{fontSize:'12px',color:'#3a5a50'}}>{r.date}</span>
        </div>
      </div>
      <div style={{margin:'0 16px 16px',borderRadius:'14px',padding:'12px 16px',display:'flex',alignItems:'center',gap:'10px',background:r.winBg,border:`1px solid ${r.winColor}33`}}>
        <div style={{width:'36px',height:'36px',borderRadius:'50%',background:`${r.winColor}22`,border:`2px solid ${r.winColor}`,display:'flex',alignItems:'center',justifyContent:'center'}}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1.5l1.2 3.7H13l-3.1 2.3 1.2 3.7L8 9l-3.1 2.2 1.2-3.7L3 5.2h3.8z" stroke={r.winColor} strokeWidth="1.2" strokeLinejoin="round"/></svg>
        </div>
        <div>
          <div style={{fontSize:'16px',fontWeight:800,color:'#fff'}}>{r.winner} Won · {r.winnerScore}</div>
          <div style={{fontSize:'11px',color:r.winColor,fontWeight:600}}>Winner</div>
        </div>
      </div>
      <div style={{padding:'0 16px',overflowX:'auto',flex:1}}>
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:'12px'}}>
          <thead><tr>
            <th style={{fontSize:'9px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:'#2a4050',padding:'6px 4px',textAlign:'left'}}>Hole</th>
            <th style={{fontSize:'9px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:'#2a4050',padding:'6px 4px',textAlign:'center'}}>Par</th>
            {r.players.map(p=><th key={p.name} style={{fontSize:'9px',fontWeight:700,color:'#2a4050',padding:'6px 4px',textAlign:'center'}}>{p.name}</th>)}
            {r.type==='stableford'&&<th style={{fontSize:'9px',color:'#2a4050',padding:'6px 4px',textAlign:'center'}}>Pts</th>}
            {r.type==='match'&&<th style={{fontSize:'9px',color:'#2a4050',padding:'6px 4px',textAlign:'center'}}>Res</th>}
          </tr></thead>
          <tbody>
            {[front,back].map((holes,si)=>[
              <tr key={'hdr'+si} style={{background:'#0d1820'}}><td colSpan={3+r.players.length+(r.type!=='stroke'?1:0)} style={{fontSize:'10px',fontWeight:700,letterSpacing:'1px',textTransform:'uppercase',color:'#2a4050',padding:'6px 4px'}}>{si===0?'Front 9':'Back 9'}</td></tr>,
              ...holes.map(i=>(
                <tr key={i}><td style={{color:'#2a4050',fontSize:'11px',padding:'5px 4px'}}>{i+1}</td><td style={{color:'#3a6050',padding:'5px 4px',textAlign:'center'}}>{r.pars[i]}</td>{r.players.map(p=><td key={p.name} style={{padding:'5px 4px',textAlign:'center'}}>{sc(p.scores[i],r.pars[i],r.type)}</td>)}{r.type==='stableford'&&<td style={{color:'#4cc834',fontWeight:700,padding:'5px 4px',textAlign:'center'}}>{r.players[0].pts[i]}</td>}{r.type==='match'&&<td style={{padding:'5px 4px',textAlign:'center'}}>{mc(r.matchResult[i])}</td>}</tr>
              )),
              <tr key={'tot'+si} style={{background:'#0d1820'}}><td style={{fontWeight:800,color:'#c8dce8',padding:'6px 4px'}}>{si===0?'Out':'In'}</td><td style={{color:'#3a6050',padding:'6px 4px',textAlign:'center'}}>{holes.reduce((a,i)=>a+r.pars[i],0)}</td>{r.players.map(p=><td key={p.name} style={{color:'#fff',fontWeight:800,padding:'6px 4px',textAlign:'center'}}>{holes.reduce((a,i)=>a+(parseInt(p.scores[i])||0),0)}</td>)}{r.type==='stableford'&&<td style={{color:'#4cc834',fontWeight:800,padding:'6px 4px',textAlign:'center'}}>{holes.reduce((a,i)=>a+r.players[0].pts[i],0)}</td>}{r.type==='match'&&<td></td>}</tr>
            ])}
            <tr style={{background:'#0d1820',borderTop:'1px solid #1a2e3d'}}>
              <td style={{color:'#fff',fontWeight:800,padding:'6px 4px'}}>Total</td>
              <td style={{color:'#3a6050',padding:'6px 4px',textAlign:'center'}}>{r.pars.reduce((a,b)=>a+b,0)}</td>
              {r.players.map(p=><td key={p.name} style={{color:'#4cc834',fontSize:'15px',fontWeight:800,padding:'6px 4px',textAlign:'center'}}>{r.type==='match'?'–':p.scores.reduce((a,s)=>a+(parseInt(s)||0),0)}</td>)}
              {r.type==='stableford'&&<td style={{color:'#4cc834',fontSize:'15px',fontWeight:800,padding:'6px 4px',textAlign:'center'}}>{r.players[0].pts.reduce((a,b)=>a+b,0)}</td>}
              {r.type==='match'&&<td style={{color:'#4cc834',fontWeight:800,padding:'6px 4px',textAlign:'center'}}>3&2</td>}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function App() {
  const [screen,setScreen]=useState('home')
  const [selectedFormat,setSelectedFormat]=useState(null)
  const [roundInfo,setRoundInfo]=useState(null)
  const [viewCardIdx,setViewCardIdx]=useState(null)
  const [navActive,setNavActive]=useState('home')

  useEffect(()=>{
    const link=document.createElement('link')
    link.href='https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&family=Barlow+Condensed:wght@600;700;800&display=swap'
    link.rel='stylesheet'
    document.head.appendChild(link)
  },[])

  const nav=(id)=>{setNavActive(id);if(id==='home')setScreen('home');else if(id==='formats')setScreen('formats');else if(id==='rounds')setScreen('rounds');}

  return (
    <div style={{background:'#1a2a36',minHeight:'100vh',display:'flex',justifyContent:'center',padding:'0'}}>
      <div style={{width:'390px',background:'#0e1923',minHeight:'100vh',position:'relative',overflow:'hidden'}}>
        {screen==='home'&&<HomeScreen onNav={nav} onNewRound={()=>setScreen('newround')} onViewCard={(i)=>{setViewCardIdx(i);setScreen('viewcard');}}/>}
        {screen==='formats'&&<FormatsScreen onNav={nav} onSelectFormat={(id)=>{setSelectedFormat(id);setScreen('detail');}}/>}
        {screen==='detail'&&<DetailScreen gameId={selectedFormat} onBack={()=>setScreen('formats')} onPlay={()=>setScreen('newround')}/>}
        {screen==='newround'&&<NewRoundScreen onBack={()=>setScreen('home')} onConfirm={(info)=>{setRoundInfo(info);setScreen('players');}}/>}
        {screen==='players'&&roundInfo&&<PlayersScreen roundInfo={roundInfo} onBack={()=>setScreen('newround')} onStart={()=>setScreen('scorecard')}/>}
        {screen==='scorecard'&&<ScorecardScreen course={roundInfo?.course} onEnd={()=>setScreen('home')}/>}
        {screen==='viewcard'&&viewCardIdx!==null&&<ScorecardViewScreen roundIdx={viewCardIdx} onBack={()=>setScreen('home')}/>}
        {screen==='rounds'&&(
          <div style={{...s.screen}}>
            <div style={s.hdr}><div style={s.logo}><span style={{color:'#fff'}}>Hole</span><span style={{color:'#4cc834'}}>IQ</span></div></div>
            <div style={{padding:'0 20px 16px'}}><h2 style={{fontFamily:"'Barlow Condensed',sans-serif",fontSize:'28px',fontWeight:800,color:'#fff'}}>All Rounds</h2></div>
            <div style={{padding:'0 16px'}}>
              {ROUNDS.map((r,i)=>(
                <div key={i} style={s.roundCard} onClick={()=>{setViewCardIdx(i);setScreen('viewcard');}}>
                  <div style={s.roundTop}><div><div style={s.roundCourse}>{r.course}</div><div style={s.roundMeta}>{r.format} · {r.date}</div></div><div><div style={s.scoreNum}>{r.winnerScore.split(' ')[0]}</div></div></div>
                  <div style={s.roundBottom}><div style={{display:'flex',alignItems:'center',gap:'6px'}}><span style={s.winnerText}>{r.winner} Won</span></div><span style={{fontSize:'11px',color:'#2a4535',fontWeight:600}}>View →</span></div>
                </div>
              ))}
            </div>
            <NavBar active="rounds" onNav={nav}/>
          </div>
        )}
      </div>
    </div>
  )
}
""".strip()

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'App.jsx')
with open(output_path, 'w') as f:
    f.write(app_code)

print(f"Successfully wrote {len(app_code.splitlines())} lines to {output_path}")
