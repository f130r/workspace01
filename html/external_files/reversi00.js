type Cell = "black" | "white" | null;

const BOARD_SIZE = 8;
let board: Cell[][] = [];
let currentTurn: Cell = "black";

const boardDiv = document.getElementById("board") as HTMLDivElement;
const turnSpan = document.getElementById("turn") as HTMLSpanElement;

// ボード初期化
function initBoard() {
  board = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
  board[3][3] = "white";
  board[3][4] = "black";
  board[4][3] = "black";
  board[4][4] = "white";

  renderBoard();
}

// ボード描画
function renderBoard() {
  boardDiv.innerHTML = "";
  for (let r = 0; r < BOARD_SIZE; r++) {
    for (let c = 0; c < BOARD_SIZE; c++) {
      const cellDiv = document.createElement("div");
      cellDiv.classList.add("cell");
      cellDiv.dataset.row = r.toString();
      cellDiv.dataset.col = c.toString();

      if (board[r][c] === "black") {
        const disc = document.createElement("div");
        disc.classList.add("black");
        cellDiv.appendChild(disc);
      } else if (board[r][c] === "white") {
        const disc = document.createElement("div");
        disc.classList.add("white");
        cellDiv.appendChild(disc);
      }

      cellDiv.addEventListener("click", onCellClick);
      boardDiv.appendChild(cellDiv);
    }
  }
  turnSpan.textContent = currentTurn === "black" ? "黒" : "白";
}

// クリック時処理
function onCellClick(e: MouseEvent) {
  const target = e.currentTarget as HTMLDivElement;
  const row = parseInt(target.dataset.row!);
  const col = parseInt(target.dataset.col!);

  if (board[row][col] !== null) return; // すでに置かれている

  board[row][col] = currentTurn;

  // 簡易版：ひっくり返す処理は省略
  currentTurn = currentTurn === "black" ? "white" : "black";
  renderBoard();
}

// 初期化
initBoard();
