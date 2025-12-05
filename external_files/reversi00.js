// この JS ファイル名は任意です（reversi.js でなくても動きます）

const BOARD_SIZE = 8;
let board = [];
let currentTurn = "black";

const boardDiv = document.getElementById("board");
const turnSpan = document.getElementById("turn");

// 初期化
function initBoard() {
  board = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));

  board[3][3] = "white";
  board[3][4] = "black";
  board[4][3] = "black";
  board[4][4] = "white";

  renderBoard();
}

// 描画
function renderBoard() {
  boardDiv.innerHTML = "";
  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;

      const disc = board[r][c];
      if (disc) {
        const d = document.createElement("div");
        d.classList.add("disc", disc);
        cell.appendChild(d);
      }

      cell.addEventListener("click", onCellClick);
      boardDiv.appendChild(cell);
    }
  }

  turnSpan.textContent = currentTurn === "black" ? "黒" : "白";
}

// クリック時処理
function onCellClick(e) {
  const row = Number(e.currentTarget.dataset.row);
  const col = Number(e.currentTarget.dataset.col);

  const flips = getFlippableStones(row, col, currentTurn);
  if (flips.length === 0) return; // 置けない場所

  // 置く
  board[row][col] = currentTurn;

  // ひっくり返す
  for (const [r, c] of flips) {
    board[r][c] = currentTurn;
  }

  // ターン交代
  currentTurn = currentTurn === "black" ? "white" : "black";

  renderBoard();
}

// ひっくり返せる石を取得
function getFlippableStones(row, col, color) {
  if (board[row][col] !== null) return [];

  const opponent = color === "black" ? "white" : "black";
  const dirs = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1],          [0, 1],
    [1, -1], [1, 0],  [1, 1],
  ];

  let result = [];

  for (const [dr, dc] of dirs) {
    let r = row + dr;
    let c = col + dc;
    let line = [];

    while (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
      if (board[r][c] === opponent) {
        line.push([r, c]);
      } else if (board[r][c] === color) {
        if (line.length > 0) result = result.concat(line);
        break;
      } else {
        break;
      }
      r += dr;
      c += dc;
    }
  }

  return result;
}

initBoard();
