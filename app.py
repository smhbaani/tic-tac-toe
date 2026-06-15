import streamlit as st
import math

st.set_page_config(
    page_title="Tic Tac Toe AI",
    page_icon="🎮",
    layout="centered"
)

st.markdown("""
<style>

.stApp{
    background-color:#FFFACD;
}

h1{
    color:#5F4A8B;
    text-align:center;
}

.status{
    text-align:center;
    color:#5F4A8B;
    font-size:22px;
    font-weight:bold;
    margin-bottom:20px;
}

div.stButton > button{
    width:120px !important;
    height:120px !important;
    background-color:#5F4A8B;
    color:#FFFACD;
    font-size:42px;
    font-weight:bold;
    border-radius:20px;
    border:none;
}

div.stButton > button:hover{
    background-color:#6e59a3;
    color:#FFFACD;
}

</style>
""", unsafe_allow_html=True)

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False

board = st.session_state.board

HUMAN = "X"
AI = "O"

winning_combos = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]


def check_winner(board, player):
    for combo in winning_combos:
        if all(board[i] == player for i in combo):
            return True
    return False


def is_draw(board):
    return "" not in board


def minimax(board, depth, maximizing):

    if check_winner(board, AI):
        return 10 - depth

    if check_winner(board, HUMAN):
        return depth - 10

    if is_draw(board):
        return 0

    if maximizing:
        best = -math.inf

        for i in range(9):
            if board[i] == "":
                board[i] = AI
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best = max(best, score)

        return best

    else:
        best = math.inf

        for i in range(9):
            if board[i] == "":
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best = min(best, score)

        return best


def ai_move():

    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = AI

            score = minimax(board, 0, False)

            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        board[move] = AI


st.title("🎮 Tic Tac Toe AI")

status = "Your Turn (X)"

if check_winner(board, HUMAN):
    status = "🎉 You Win!"
    st.session_state.game_over = True

elif check_winner(board, AI):
    status = "🤖 AI Wins!"
    st.session_state.game_over = True

elif is_draw(board):
    status = "🤝 Draw!"
    st.session_state.game_over = True

st.markdown(f'<div class="status">{status}</div>', unsafe_allow_html=True)

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        idx = row * 3 + col

        with cols[col]:

            if st.button(
                board[idx] if board[idx] else " ",
                key=f"cell_{idx}"
            ):

                if board[idx] == "" and not st.session_state.game_over:

                    board[idx] = HUMAN

                    if not check_winner(board, HUMAN) and not is_draw(board):
                        ai_move()

                    st.rerun()

if st.button("🔄 Restart Game"):

    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.rerun()