// Minimal Othello (pure JS) — legal-move check, flips, pass, endgame, score
(function(){
  const BOARD_SIZE = 8;
  const dirs = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]];

  let board = [];
  let turn = "black"; // "black" or "white"
  const boardDiv = document.getElementById("board");
  const turnEl = document.getElementById("turn");
  const scoreEl = document.getElementById("score");
  const restartBtn = document.getElementById("restart");

  function init(){
    board = Array.from({length: BOARD_SIZE}, ()=>Array(BOARD_SIZE).fill(null));
    board[3][3] = "white";
    board[3][4] = "black";
    board[4][3] = "black";
    board[4][4] = "white";
    turn = "black";
    render();
  }

  function inBoard(r,c){ return r>=0 && r<BOARD_SIZE && c>=0 && c<BOARD_SIZE; }

  // return array of [r,c] that would be flipped for move (r,c) by color
  function getFlips(r,c,color){
    if (!inBoard(r,c) || board[r][c] !== null) return [];
    const opponent = color === "black" ? "white" : "black";
    const flips = [];
    for (const [dr,dc] of dirs){
      let rr = r + dr, cc = c + dc;
      const line = [];
      while (inBoard(rr,cc) && board[rr][cc] === opponent){
        line.push([rr,cc]);
        rr += dr; cc += dc;
      }
      if (line.length > 0 && inBoard(rr,cc) && board[rr][cc] === color){
        flips.push(...line);
      }
    }
    return flips;
  }

  function anyValid(color){
    for (let r=0;r<BOARD_SIZE;r++){
      for (let c=0;c<BOARD_SIZE;c++){
        if (getFlips(r,c,color).length>0) return true;
      }
    }
    return false;
  }

  function applyMove(r,c,color){
    const flips = getFlips(r,c,color);
    if (flips.length === 0) return false;
    board[r][c] = color;
    for (const [rr,cc] of flips) board[rr][cc] = color;
    return true;
  }

  function countScores(){
    let b=0,w=0;
    for (let r=0;r<BOARD_SIZE;r++){
      for (let c=0;c<BOARD_SIZE;c++){
        if (board[r][c] === "black") b++;
        if (board[r][c] === "white") w++;
      }
    }
    return {black:b, white:w};
  }

  function render(){
    // board
    boardDiv.innerHTML = "";
    for (let r=0;r<BOARD_SIZE;r++){
      for (let c=0;c<BOARD_SIZE;c++){
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.dataset.r = r; cell.dataset.c = c;
        // valid move highlight
        if (getFlips(r,c,turn).length > 0) cell.classList.add("valid");
        // stone
        if (board[r][c]){
          const s = document.createElement("div");
          s.className = "stone " + board[r][c];
          cell.appendChild(s);
        }
        cell.addEventListener("click", onCellClick);
        boardDiv.appendChild(cell);
      }
    }
    // turn and score
    turnEl.textContent = turn === "black" ? "黒" : "白";
    const sc = countScores();
    scoreEl.textContent = `黒:${sc.black} 白:${sc.white}`;

    // endgame check
    if (!anyValid("black") && !anyValid("white")){
      const winner = sc.black === sc.white ? "引き分け" : (sc.black > sc.white ? "黒の勝ち" : "白の勝ち");
      setTimeout(()=>{ alert("ゲーム終了 — " + winner + `（黒:${sc.black} 白:${sc.white}）`); }, 50);
    }
  }

  function onCellClick(e){
    const r = parseInt(e.currentTarget.dataset.r);
    const c = parseInt(e.currentTarget.dataset.c);

    if (applyMove(r,c,turn)){
      // move applied
      // next turn: if opponent has no moves, stay with current player (pass)
      const opponent = turn === "black" ? "white" : "black";
      if (anyValid(opponent)){
        turn = opponent;
      } else if (anyValid(turn)){
        // opponent has no moves, current keeps turn (pass)
        // turn remains same
        // optionally inform
        // (no alert to avoid noise)
      } else {
        // neither have moves: end will be caught by render()
      }
      render();
    } else {
      // invalid move: ignore or optionally flash
      // do nothing
    }
  }

  restartBtn.addEventListener("click", ()=>{
    init();
  });

  // start
  document.addEventListener("DOMContentLoaded", ()=> init());
})();
